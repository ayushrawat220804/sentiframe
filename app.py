import os
import re
from typing import Optional, List, Dict
import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
from sentiframe import YouTubeScraper
from sentiframe.base_scraper import BaseScraper
import pandas as pd
from youtube_api import YouTubeAPI

# Load environment variables
load_dotenv()

def extract_video_id(url: str) -> Optional[str]:
    """Extract the video ID from a YouTube URL."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([^"&?/\s]{11})',  # Standard YouTube URLs
        r'(?:embed/)([^"&?/\s]{11})',              # Embedded URLs
        r'(?:shorts/)([^"&?/\s]{11})'              # Shorts URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_comments(video_id: str, max_results: int = 100):
    """Fetch comments for a given YouTube video ID."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        st.error('YouTube API key not found. Please check your .env file.')
        return []

    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        # Get video details first
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not video_response['items']:
            st.error('Video not found or is not accessible.')
            return []
            
        video_title = video_response['items'][0]['snippet']['title']
        
        # Get video comments
        comments = []
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            textFormat='plainText',
            order='time'
        )
        
        while request and len(comments) < max_results:
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            
            # Check if there are more comments
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=max_results,
                    textFormat='plainText',
                    order='time',
                    pageToken=response['nextPageToken']
                )
            else:
                break
                
        return video_title, comments
        
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')
        return None, []

def main():
    # Set page title and description
    st.set_page_config(page_title="YouTube Comment Analyzer", page_icon="🎥")
    
    # Add header with styling
    st.markdown("""
    # 🎥 YouTube Comment Analyzer
    Analyze comments from any YouTube video! Just paste the video URL below.
    """)
    
    # Initialize YouTube API
    try:
        api = YouTubeAPI()
    except ValueError as e:
        st.error("❌ " + str(e))
        st.info("Please add your YouTube API key to the .env file")
        return
    
    # Create two columns for input
    col1, col2 = st.columns([3, 1])
    
    # URL input in the first (wider) column
    with col1:
        url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    
    # Number of comments selector in the second (narrower) column
    with col2:
        max_comments = st.number_input("Max Comments", min_value=10, max_value=500, value=100, step=10)
    
    # Add a fetch button
    if st.button("📥 Fetch Comments", type="primary"):
        if not url:
            st.warning("⚠️ Please enter a YouTube video URL")
            return
            
        try:
            # Show loading spinner while fetching
            with st.spinner("Fetching video data..."):
                result = api.analyze_video(url, max_comments=max_comments)
                
                # Display video information
                st.markdown("### 📺 Video Information")
                
                # Create two columns for video info
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    st.markdown(f"**Title:** {result['metadata']['title']}")
                    st.markdown(f"**Channel:** {result['metadata']['channel']}")
                    
                with info_col2:
                    st.markdown(f"**Views:** {int(result['metadata']['view_count']):,}")
                    st.markdown(f"**Likes:** {int(result['metadata']['like_count']):,}")
                
                # Display comments section
                st.markdown(f"### 💬 Comments ({len(result['comments'])})")
                
                # Create a DataFrame for better display
                comments_data = []
                for comment in result['comments']:
                    comments_data.append({
                        'Author': comment['author'],
                        'Comment': comment['text'],
                        'Likes': comment['likes'],
                        'Date': comment['published_at'][:10]  # Just the date part
                    })
                
                if comments_data:
                    df = pd.DataFrame(comments_data)
                    
                    # Add filters
                    col1, col2 = st.columns(2)
                    with col1:
                        selected_author = st.selectbox(
                            "Filter by Author",
                            options=["All Authors"] + list(df['Author'].unique())
                        )
                    with col2:
                        sort_by = st.selectbox(
                            "Sort by",
                            options=["Likes ↓", "Date ↓", "Date ↑"]
                        )
                    
                    # Apply filters and sorting
                    if selected_author != "All Authors":
                        df = df[df['Author'] == selected_author]
                        
                    if sort_by == "Likes ↓":
                        df = df.sort_values('Likes', ascending=False)
                    elif sort_by == "Date ↓":
                        df = df.sort_values('Date', ascending=False)
                    elif sort_by == "Date ↑":
                        df = df.sort_values('Date', ascending=True)
                    
                    # Display comments in expandable containers
                    for _, row in df.iterrows():
                        with st.expander(f"💬 {row['Author']} - {row['Date']} (👍 {row['Likes']})"):
                            st.markdown(row['Comment'])
                else:
                    st.info("No comments found for this video")
                        
        except ValueError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            if "quota" in str(e).lower():
                st.info("ℹ️ This might be due to YouTube API quota limits. Please try again later.")

if __name__ == "__main__":
    main()

scraper = YouTubeScraper()
result = scraper.analyze_video("https://youtube.com/watch?v=...")

# Access video information
print(f"Title: {result['metadata']['title']}")
print(f"Views: {result['metadata']['view_count']}")

# Access comments
for comment in result['comments']:
    print(f"Author: {comment['author']}")
    print(f"Text: {comment['text']}")

def load_api_key():
    # Implementation of load_api_key function
    pass

def format_timestamp():
    # Implementation of format_timestamp function
    pass

class MyCustomScraper(BaseScraper):
    def extract_id(self, url):
        # Your implementation
        pass
    # ... other required methods 

# Initialize the API
api = YouTubeAPI()

# Analyze a video
result = api.analyze_video("https://www.youtube.com/watch?v=...")

# Get just the metadata
metadata = api.get_video_metadata(video_id)

# Get just the comments
comments = api.get_video_comments(video_id, max_results=100) 