from typing import Optional
from modules.logger import get_logger
import requests
import base64
from PIL import Image
import io

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

def encode_images(image_paths:Optional[list[str]] = None,
                                urls:Optional[list[str]] = None):
    
    try:
        images = []
        image = None
    
        if urls:
            for url in urls:
                image = Image.open(io.BytesIO(get_image_from_url(url).content)).convert("RGB")
                images.append(image)
        
        if image_paths:
            for image_path in image_paths:
                image = Image.open(image_path).convert("RGB")
                images.append(image)
            
        if not images:
            raise ValueError("Provide at least one image path or URL.")
        
        return images
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Multi-image encoding failed: : {e}")
        raise
    
def encode_image(image_path:Optional[str] = None,
                                url:Optional[str] = None):
    
    try:
        
        image = None
    
        if url:
            image = Image.open(io.BytesIO(get_image_from_url(url).content)).convert("RGB")
            
        if image_path: 
            image = Image.open(image_path).convert("RGB")
                
        if not image:
            raise ValueError("Provide at least one image path or URL.")
        
        return image
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Single-image encoding failed: : {e}")
        raise
        
 