# ocr_df = pytesseract.image_to_data(img)
# processor = AutoProcessor.from_pretrained("nielsr/layoutlmv3-finetuned-funsd", apply_ocr=True)
# model = AutoModelForTokenClassification.from_pretrained("nielsr/layoutlmv3-finetuned-funsd")

# feature_extractor = LayoutLMv3ImageProcessor(apply_ocr=True, ocr_lang="eng")
# model = LayoutLMv3ForSequenceClassification.from_pretrained("nielsr/layoutlmv3-finetuned-funsd")
# tokenizer  = LayoutLMv3TokenizerFast.from_pretrained("microsoft/layoutlmv3-base")

# processor = LayoutLMv3Processor(feature_extractor, tokenizer)

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model.to(device)



# encoding = processor(
#      img, max_length=512, padding="max_length", truncation=True, return_tensors="pt"
# )
# print(model)

# with torch.no_grad():
#     outputs = model(**encoding)

# # 6. Process the output
# predictions = outputs.logits.argmax(-1).squeeze().tolist()
# token_boxes = encoding.bbox.squeeze().tolist()

# # Map predictions to tokens and their positions
# words = processor.tokenizer.convert_ids_to_tokens(encoding.input_ids.squeeze().tolist())
# results = []
# for word, box, prediction in zip(words, token_boxes, predictions):
#     if word != processor.tokenizer.pad_token:
#         results.append({
#             "word": word,
#             "box": box,
#             "prediction": model.config.id2label[prediction]
#         })

# # Print results
# def clean_word(word):
#     return word.replace("Ġ", "")

# # # When processing results:
# # for item in results:
# #     item['word'] = clean_word(item['word'])
# #     print(f"Word: {item['word']}, Box: {item['box']}, Prediction: {item['prediction']}")

# features = feature_extractor(img)
# words = features["words"][0]
# bounding_boxes = features["boxes"][0]

# width_scale = img.width / 1000
# height_scale = img.height / 1000

# draw = ImageDraw.Draw(img)

# for bbox in bounding_boxes:
#     draw.rectangle(
#         [bbox[0] * width_scale, bbox[1] * height_scale, bbox[2] * width_scale, bbox[3] * height_scale], outline="blue", width=2
#     )

# img.show()
# feature_extractor = LayoutLMv3ImageProcessor(apply_ocr=True, ocr_lang="eng")
# model = LayoutLMv3ForSequenceClassification.from_pretrained("microsoft/layoutlmv3-base")
# tokenizer  = LayoutLMv3TokenizerFast.from_pretrained("microsoft/layoutlmv3-base")

# processor = LayoutLMv3Processor(feature_extractor, tokenizer)



# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model.to(device)



# encoding = processor(
#     img, max_length=512, padding="max_length", truncation=True, return_tensors="pt", return_offsets_mapping=True
# )

# print(encoding.keys())


# features = feature_extractor(img)
# words = features["words"][0]
# bounding_boxes = features["boxes"][0]



# offset_mapping = encoding.pop('offset_mapping')
# is_subword = np.array(offset_mapping.squeeze().tolist())[:,0] != 0



# width_scale = img.width / 1000
# height_scale = img.height / 1000




# draw = ImageDraw.Draw(img)

# for bbox in bounding_boxes:
#     draw.rectangle(
#         [bbox[0] * width_scale, bbox[1] * height_scale, bbox[2] * width_scale, bbox[3] * height_scale], outline="blue", width=2
#     )




# encoding = tokenizer(text=words, boxes=bounding_boxes, max_length=512, padding="max_length", truncation=True, return_tensors="pt")




# tokens = tokenizer.convert_ids_to_tokens(
#     encoding["input_ids"][0],
#     skip_special_tokens=True
# )

# encoding = processor(
#     img, boxes=bounding_boxes, truncation=True, return_tensors="pt", text=words
# )


# output = model(**encoding)



# logits = output.logits
# predictions = logits.argmax(-1).squeeze().tolist()
# token_boxes = encoding.bbox.squeeze().tolist()
# width, height = img.size
# print(predictions)

# # true_predictions = [model.config.id2label[pred] for pred, label in zip(predictions, labels) if label != - 100]
# # true_labels = [model.config.id2label[label] for prediction, label in zip(predictions, labels) if label != -100]
# # true_boxes = [unnormalize_box(box, width, height) for box, label in zip(token_boxes, labels) if label != -100]


# def iob_to_label(label):
#     label = label
#     if not label:
#       return 'other'
#     return label

# draw = ImageDraw.Draw(img)
# font = ImageFont.load_default()
# label2color = {'invoice_no':'blue', 'date':'green', 'amount':'orange'}


# for prediction, box in zip(true_predictions, true_boxes):
#     predicted_label = iob_to_label(prediction).lower()
#     draw.rectangle(box, outline=label2color[predicted_label])
#     draw.text((box[0] + 10, box[1] - 10), text=predicted_label, fill=label2color[predicted_label], font=font)

# img.show()
# app = Flask(__name__)


# app.run(debug=True, port=3001)


# @app.route("/DocumentParse", methods=["POST"])
# def DocumentParse():
#     data = request.json
#     result = {"message": "Data received", "data": data}
#     return jsonify(result), 200
