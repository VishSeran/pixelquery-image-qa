from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

from modules.logger import get_logger

logger = get_logger("model-config")
VISION_MODEL = 'HuggingFaceTB/SmolVLM2-2.2B-Instruct'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

vision_model = AutoModelForImageTextToText.from_pretrained(
    VISION_MODEL,
    torch_dtype = torch.bfloat16
).to(device)

vision_processor = AutoProcessor.from_pretrained(VISION_MODEL)


def get_response_from_model(image, user_query):
    
    try:
        
        if not image:
            raise ValueError("Image inputs must not be empty")
        
        if not user_query:
            raise ValueError("User query must not be empty")
        
        system_message = "You are a helpful assistant. Answer the following user query in 1 or 2 sentences: "

        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": system_message + user_query
                    },
                    {
                        "type": "image",
                        "url": image
                    }
                ]
            }
        ]
        
        logger.info("Message has crafted")
        
        inputs = vision_processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            
        ).to(device, dtype=torch.bfloat16)
        
        logger.info("model input has crafted")
        
        generated_ids = vision_model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=200
        )
        
        if not generated_ids:
            logger.info("Response is fetched")
            
        generated_text = vision_processor.batch_decode(
            generated_ids,
            skip_specials_tokens = True
        )
        
        logger.info("Response is retrieved")
        return generated_text[0]
    
    except ValueError as e:
        logger.error(f"Value error: {e}")
        raise
    
    except Exception as e:
        logger.error(f"user query fetch error: : {e}")
        raise 
    





