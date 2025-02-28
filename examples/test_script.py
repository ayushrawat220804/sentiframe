from sentiframe import YouTubeScraper

def main():
    # Initialize the scraper
    scraper = YouTubeScraper()
    
    # Example YouTube video URL
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        # Analyze the video
        result = scraper.analyze_video(video_url, max_comments=50)
        
        # Print video metadata
        print("\nVideo Metadata:")
        print(f"Title: {result['metadata']['title']}")
        print(f"Channel: {result['metadata']['channel']}")
        print(f"Views: {result['metadata']['view_count']}")
        print(f"Likes: {result['metadata']['like_count']}")
        print(f"Total Comments: {result['metadata']['comment_count']}")
        
        # Print comments
        print(f"\nFetched Comments ({len(result['comments'])}):")
        for i, comment in enumerate(result['comments'], 1):
            print(f"\n{i}. Author: {comment['author']}")
            print(f"   Likes: {comment['likes']}")
            print(f"   Text: {comment['text']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 