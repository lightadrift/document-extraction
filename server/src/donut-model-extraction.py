from flask import Flask, request, jsonify
import torch
#from transformers import LayoutLMv3ForSequenceClassification, LayoutLMv3Tokenizer, LayoutLMv3ImageProcessor, LayoutLMv3Processor, LayoutLMv3TokenizerFast, AutoProcessor, AutoModelForTokenClassification, AutoModelForSequenceClassification
from PIL import Image, ImageDraw, ImageFont
import pytorch_lightning as pl
import numpy as np
import pytesseract
import re
from transformers import DonutProcessor, VisionEncoderDecoderModel,  AutoModel, AutoTokenizer


image = Image.open('wholesale-store2.png').convert("RGB")


processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

pixel_values = processor(image, return_tensors="pt").pixel_values

task_prompt = "<s_cord-v2>"

decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

pixel_values = processor(image, return_tensors="pt").pixel_values

outputs = model.generate(
    pixel_values.to(device),
    decoder_input_ids=decoder_input_ids.to(device),
    max_length=model.decoder.config.max_position_embeddings,
    pad_token_id=processor.tokenizer.pad_token_id,
    eos_token_id=processor.tokenizer.eos_token_id,
    use_cache=True,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

sequence = processor.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(processor.tokenizer.eos_token,"").replace(processor.tokenizer.pad_token,"")
sequence = re.sub(r"<.*?>","",sequence, count=1).strip()


result = processor.token2json(sequence)


print(result)