from flask import Flask, Response, request, jsonify, make_response
import pytorch_lightning as pl
from flask_cors import CORS
import uuid

# def ProcessingImage(img) -> any:
#     image = Image.open(img).convert("RGB")

#     processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

#     model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

#     pixel_values = processor(image, return_tensors="pt").pixel_values

#     task_prompt = "<s_cord-v2>"

#     decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model.to(device)

#     pixel_values = processor(image, return_tensors="pt").pixel_values

#     outputs = model.generate(
#         pixel_values.to(device),
#         decoder_input_ids=decoder_input_ids.to(device),
#         max_length=model.decoder.config.max_position_embeddings,
#         pad_token_id=processor.tokenizer.pad_token_id,
#         eos_token_id=processor.tokenizer.eos_token_id,
#         use_cache=True,
#         bad_words_ids=[[processor.tokenizer.unk_token_id]],
#         return_dict_in_generate=True,
#     )

#     sequence = processor.batch_decode(outputs.sequences)[0]
#     sequence = sequence.replace(processor.tokenizer.eos_token,"").replace(processor.tokenizer.pad_token,"")
#     sequence = re.sub(r"<.*?>","",sequence, count=1).strip()

#     result = processor.token2json(sequence)
#     return result


app = Flask(__name__)
CORS(app)


@app.route("/parser", methods=["POST"])
def DocumentParse() -> Response:
    files = request.files.getlist("files")
    data = []
    for file in files:
       img = file.stream
       i = ProcessingImage(img)
       i["id"] = uuid.uuid4()
       data.append(i)
    result = {"message": "Files received", "files": [file.filename for file in files], "data": data}
    return make_response(jsonify(result), 200)


@app.route("/")
def index():
  return "Hello, World!"


app.run(debug=True, port=3001, host='0.0.0.0')  

