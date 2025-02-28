import os
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Clean up build directories."""
    dirs_to_clean = ['build', 'dist', 'sentiframe.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

def build_package():
    """Build the package."""
    print("\nBuilding package...")
    subprocess.run(['python', '-m', 'build'], check=True)
    print("Package built successfully!")

def upload_to_pypi(test=True):
    """Upload the package to PyPI."""
    command = ['twine', 'upload']
    if test:
        command.extend(['--repository', 'testpypi'])
    command.append('dist/*')
    
    print(f"\nUploading to {'Test ' if test else ''}PyPI...")
    subprocess.run(command, check=True)
    print("Upload completed!")

def main():
    # Ensure we're in the correct directory
    if not os.path.exists('setup.py'):
        raise FileNotFoundError("setup.py not found! Run this script from the project root.")
    
    try:
        # Clean previous builds
        clean_build_dirs()
        
        # Build the package
        build_package()
        
        # Upload to Test PyPI first
        print("\nUploading to Test PyPI first...")
        upload_to_pypi(test=True)
        
        # Ask for confirmation before uploading to real PyPI
        response = input("\nDo you want to upload to real PyPI? (y/N): ")
        if response.lower() == 'y':
            upload_to_pypi(test=False)
            print("\n🎉 Package published successfully!")
            print("\nYou can now install it with:")
            print("pip install sentiframe")
        else:
            print("\nSkipping upload to real PyPI")
            print("\nYou can test your package with:")
            print("pip install --index-url https://test.pypi.org/simple/ sentiframe")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed build and twine: pip install build twine")
        print("2. Created a PyPI account: https://pypi.org/account/register/")
        print("3. Set up your .pypirc file with your API tokens")
        
if __name__ == "__main__":
    main() 