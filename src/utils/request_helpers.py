import requests
import os
import requests
from urllib.parse import urlparse

def fetch(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def download_image(image_url, save_folder='assets'):
    """
    Download an image from a URL and save it to the specified folder.
    
    Args:
        image_url (str): URL of the image to download
        save_folder (str): Folder where the image will be saved
            
    Returns:
        str: Local path to the saved image, or original URL if download failed
    """

    # Ensure the save folder exists
    os.makedirs(save_folder, exist_ok=True)
    
    try:
        # Extract image filename from URL
        parsed_url = urlparse(image_url)
        image_filename = os.path.basename(parsed_url.path)
        
        # Full path to save the image
        save_path = os.path.join(save_folder, image_filename)
        
        # Download the image with certificate verification disabled
        response = requests.get(image_url, stream=True, verify=False)
        response.raise_for_status()
        
        # Save the image to disk
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Return the local path to use in markdown
        return save_path
    except Exception as e:
        print(f"Failed to download image from {image_url}: {e}")
        # Return original URL if download fails
        return image_url