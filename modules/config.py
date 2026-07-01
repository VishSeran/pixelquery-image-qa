from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

VISION_MODEL = 'HuggingFaceTB/SmolVLM2-2.2B-Instruct'


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

vision_model = AutoModelForImageTextToText.from_pretrained(
    VISION_MODEL,
    torch_dtype = torch.bfloat16
).to(device)

vision_processor = AutoProcessor.from_pretrained(VISION_MODEL)




