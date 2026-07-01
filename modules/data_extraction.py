from typing import Optional,
from modules.logger import get_logger
import requests
import base64

logger = get_logger("data-extraction")

def get_image_from_url(url):
    
    if not url:
            raise ValueError ("URL is empty or none")
    
    try:
    
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response
         
    except requests.RequestException as e:
        logger.error(f"Failed to fetch image: {e}")
        raise

def encode_image(image_paths:Optional[list[str]] = None,
                                urls:Optional[list[str]] = None):
    
    try:
        images = []
        image = None
    
        if url:
            for url in urls:
                image = get_image_from_url(url).content
                images.append(image)
        
        if image_paths:
            for image_path in image_paths:
                with open(image_path, "rb") as f:
                    image = f.read()
                    images.append(image)
            
        if not images:
            raise ValueError("Provide at least one image path or URL.")
        
        # encode raw bytes into bytes object and again decode bytes object into python string
        encoded_image = [
            base64.b64encode(img).decode("utf-8")
            for img in images
        ]
        
        return encoded_image
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Multi-image encoding failed: : {e}")
        raise
        
 