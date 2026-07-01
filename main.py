from typing import Optional

import gradio as gr

from modules.data_extraction import encode_image
from modules.logger import get_logger
from modules.model_config import get_response_from_model

logger = get_logger("main")

def image_caption_process(image_path:Optional[str],image_url:Optional[str], user_query):
    
    try:
        image = encode_image(image_path, image_url)
        response = get_response_from_model(image, user_query)
        
        return response
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"main function error: : {e}")
        raise 

def gradio_interface():
    
    
    image_input = gr.Image(label="Drag and drop the image or url",sources="upload",type="filepath")
    input_url = gr.Textbox(label="Type the image url", placeholder="Image url")
    user_query = gr.Textbox(label="User query", placeholder="Input your question here")
    text_output = gr.Textbox(label="Image caption")
    
    interface = gr.Interface(
        fn=image_caption_process,
        inputs=[image_input, input_url,user_query],
        outputs=[text_output],
        title="Image Captioning AI",
        description="This application is use to generate a caption for images"
    )
    
    interface.launch()
    
if __name__ == "__main__":
    gradio_interface()