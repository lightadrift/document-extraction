from transformers import AutoModel, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer
import torch
from PIL import Image
import os
from typing import Any, Dict, Optional

class ModelInitializationError(Exception):
    """Custom exception for model initialization errors."""
    pass

class DocumentParsingError(Exception):
    """Custom exception for document parsing errors."""
    pass

class Parser:
    def __init__(self):
        os.environ["HF_HOME"] = "A:\\HuggingFace\\cache"
        self.model = None
        self.tokenizer = None
        try:
            self.initialize_model()
        except Exception as e:
            self.logger.error(f"Failed to initialize model: {str(e)}")
            raise ModelInitializationError("Failed to initialize model") from e
    def initialize_model(self):
        try:
            self.model = AutoModel.from_pretrained('openbmb/MiniCPM-V-2_6', trust_remote_code=True)
            self.tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-2_6', trust_remote_code=True)
            self.model.to("cpu")
            self.model.eval()
        except Exception as e:
            self.logger.error(f"Error initializing model: {str(e)}")
            raise ModelInitializationError(f"Error initializing model: {str(e)}") from e

    def parse_document(self, image: Image.Image) -> Dict[str, Any]:
        if self.model is None or self.tokenizer is None:
            raise ModelInitializationError("Model or tokenizer not initialized")

        question = """
        In this document, extract the important information such as the invoice number (if present), item IDs, item names, item prices, total, and subtotal. If information about the key is not availible, make the value None. Format the information in a JSON file format like this:

        {
            "id": <id_of_invoice>, // if present
            "date": <date_of_document>,
            "company": <company_name>,
            "phone": <company_phone_number>,
            "address": <company_address>,
            "items": [{
                "id": <id_of_item>, // ID of the product if available
                "name": <name_of_product>,
                "price": <price_of_product>
            }],
            "total": <total_price>,
            "subtotal": <subtotal_price>,
            "tax": <tax>,
            "payment": { // if information about the payer is available
                "name": <name_of_the_payer>,
                "company": <payer_bank>,
                "email": <payer_email>,
                "address": <payer_address>,
                "phone": <payer_phone_number>,
                "account_number": <payer_account_number>,
                "due_date": <payment_due_date>
            }
        }
        """

        msgs = [{'role': 'user', 'content': [image, question]}]

        try:
            res = self.model.chat(
                image=None,
                msgs=msgs,
                tokenizer=self.tokenizer
            )
            return res
        except Exception as e:
            self.logger.error(f"Error parsing document: {str(e)}")
            raise DocumentParsingError(f"Error parsing document: {str(e)}") from e





def initialize_model():
    model = AutoModel.from_pretrained(
        'openbmb/MiniCPM-V-2_6', trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(
        'openbmb/MiniCPM-V-2_6', trust_remote_code=True)
    model.to("cpu")
    model.eval()
    return model, tokenizer



def DocumentExtraction(image):
    # model = model.to('cuda:0')


    question = """
    In this document, extract the important information such as the invoice number (if present), item IDs, item names, item prices, total, and subtotal. Format the information in a JSON file format like this:

    {
        "id": <id_of_invoice>, // if present
        "date": <date_of_document>,
        "company": <company_name>,
        "phone": <company_phone_number>,
        "address": <company_address>,
        "items": [{
            "id": <id_of_item>, // ID of the product if available
            "name": <name_of_product>,
            "price": <price_of_product>
        }],
        "total": <total_price>,
        "subtotal": <subtotal_price>,
        "tax": <tax>,
        "payment": { // if information about the payer is available
            "name": <name_of_the_payer>,
            "company": <payer_bank>,
            "email": <payer_email>,
            "address": <payer_address>,
            "phone": <payer_phone_number>,
            "account_number": <payer_account_number>,
            "due_date": <payment_due_date>
        }
    }


    """

    image = Image.open("./src/test.jpeg").convert("RGB")


    msgs = [{'role': 'user', 'content': [image, question]}]

    res = model.chat(
        image=None,
        msgs=msgs,
        tokenizer=tokenizer
    )


    print(res)
