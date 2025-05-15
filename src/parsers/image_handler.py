from src.utils.request_helpers import download_image

class ImageHandler:
    def __init__(self, file_utils):
        self.file_utils = file_utils
    
    def process_images_in_element(self, element, assets_folder):
        """Process all images within an HTML element and replace with markdown"""
        for img in element.find_all('img'):
            img_src = img.get('src', '')
            if not img_src:
                continue
                
            # Make sure it's a full URL
            if not img_src.startswith(('http://', 'https://')):
                img_src = f"https://www.examtopics.com{img_src}"
            
            # Download image and get local path
            local_path = download_image(img_src, assets_folder)
            
            # Convert to relative path
            relative_path = self.file_utils.get_relative_path(local_path)
            
            img_alt = img.get('alt', 'image')
            # Replace the img tag with markdown image syntax using relative path
            img.replace_with(f"![{img_alt}]({relative_path})")
    
    def get_image_markdown(self, img, assets_folder):
        """Generate markdown for an image element"""
        img_src = img.get('src', '')
        if not img_src:
            return None
            
        # Make sure it's a full URL
        if not img_src.startswith(('http://', 'https://')):
            img_src = f"https://www.examtopics.com{img_src}"
        
        # Download image and get local path
        local_path = download_image(img_src, assets_folder)
        
        # Convert to relative path
        relative_path = self.file_utils.get_relative_path(local_path)
        
        img_alt = img.get('alt', 'image')
        return f"![{img_alt}]({relative_path})"
