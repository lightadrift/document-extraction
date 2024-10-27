
from datasets import load_dataset
import torch
from PIL import Image
from transformers import UdopProcessor,  UdopForConditionalGeneration
from torch.utils.data import Dataset, DataLoader
from typing import Any, List
import json
import random
import bitsandbytes as bnb

dataset = load_dataset("naver-clova-ix/cord-v2")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
processor = UdopProcessor.from_pretrained("microsoft/udop-large")
model = UdopForConditionalGeneration.from_pretrained("microsoft/udop-large")


added_tokens = []

class CustomDataset(Dataset):
  def __init__(self, dataset, processor, split="train", sort_json_key: bool = True):
    self.dataset = dataset[split]
    self.processor = processor

    self.gt_token_sequences = []

    for ground_truth in self.dataset["ground_truth"]:
        ground_truth = json.loads(ground_truth)
        if "gt_parses" in ground_truth:
            assert isinstance(ground_truth["gt_parses"], list)
            gt_jsons = ground_truth["gt_parses"]
        else:
            assert "gt_parse" in ground_truth and isinstance(ground_truth["gt_parse"], dict)
            gt_jsons = [ground_truth["gt_parse"]]

        self.gt_token_sequences.append(
            [
                self.json2token(
                    gt_json,
                    update_special_tokens_for_json_key=split == "train",
                    sort_json_key=sort_json_key,
                )
                for gt_json in gt_jsons
            ]
        )

  def json2token(self, obj: Any, update_special_tokens_for_json_key: bool = True, sort_json_key: bool = True):
      """
      Convert an ordered JSON object into a token sequence
      """
      if type(obj) == dict:
          if len(obj) == 1 and "text_sequence" in obj:
              return obj["text_sequence"]
          else:
              output = ""
              if sort_json_key:
                  keys = sorted(obj.keys(), reverse=True)
              else:
                  keys = obj.keys()
              for k in keys:
                  if update_special_tokens_for_json_key:
                      self.add_tokens([fr"", fr""])
                  output += (
                      fr""
                      + self.json2token(obj[k], update_special_tokens_for_json_key, sort_json_key)
                      + fr""
                  )
              return output
      elif type(obj) == list:
          return r"".join(
              [self.json2token(item, update_special_tokens_for_json_key, sort_json_key) for item in obj]
          )
      else:
          obj = str(obj)
          if f"<{obj}/>" in added_tokens:
              obj = f"<{obj}/>"
          return obj

  def add_tokens(self, list_of_tokens: List[str]):
        """
        Add special tokens to tokenizer and resize the token embeddings of the decoder
        """
        newly_added_num = processor.tokenizer.add_tokens(list_of_tokens)
        if newly_added_num > 0:
            model.resize_token_embeddings(len(processor.tokenizer))
            added_tokens.extend(list_of_tokens)

  def __len__(self):
    return len(self.dataset)

  def __getitem__(self, idx):
    # get item of the dataset
    sample = self.dataset[idx]
    image = sample["image"]

    # prepare inputs for the UDOP encoder
    # the processor automatically applies OCR on the image
    # we'll set the max_length to 100 here for demo purposes as we're running on a T4 GPU in Colab
    encoding = self.processor(images=image, truncation=True, padding="max_length", max_length=200, return_tensors="pt")

    # remove the batch dimension which the processor adds by default
    encoding = {k:v.squeeze() for k,v in encoding.items()}

    # add labels for the UDOP decoder
    # again one can increase the max_length here, we'll use 128 due to memory constraints
    target_sequence = random.choice(self.gt_token_sequences[idx])  # can be more than one, e.g., DocVQA Task 1
    encoding["labels"] = self.processor.tokenizer(text_target=target_sequence,
                                                  padding="max_length", max_length=128, truncation=True,
                                                  return_tensors="pt").input_ids.squeeze()

    return encoding
  

train_dataset = CustomDataset(dataset, processor, sort_json_key=False)

train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True)



#training
optimizer = bnb.optim.Adam8bit(model.parameters(), lr=5e-5)

model.to(device)

model.train()

for epoch in range(1000):  # loop over the dataset multiple times
    for batch in train_dataloader:
        # get the inputs;
        batch = {k:v.to(device) for k,v in batch.items()}
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        bbox = batch["bbox"]
        pixel_values = batch["pixel_values"]
        labels = batch["labels"]

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            bbox=bbox,
            pixel_values=pixel_values,
            labels=labels,
        )
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        print("Loss:", loss.item())


model.save_pretrained("fine-tuned-model")
processor.save_pretrained("fine-tuned-model")

