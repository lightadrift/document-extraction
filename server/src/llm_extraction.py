from functools import wraps
import logging
import re
from transformers import AutoModel, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer, DonutProcessor, VisionEncoderDecoderModel
from typing import Any, Dict, Optional
from PIL import Image
import torch
from llama_cpp import Llama
from helpers.functions import image_to_base64_data_uri
import os
# isso aqui server pra definir o diretório em que o huggingface salva seus modelos. Por padrão vai ser no disco C; Ele tem que ser definido antes do imports de AutoModel e Auto Tokenizer aparentemente
os.environ["HF_HOME"] = "A:\\HuggingFace\\cache"


# não implementei o handling de error completo. Por equanto um placeholder desse dois tipos de erros

class ModelInitializationError(Exception):
    """Custom exception for model initialization errors."""
    pass


class DocumentParsingError(Exception):
    """Custom exception for document parsing errors."""
    pass

# não usei esse decorador ainda
def check_model_initialization(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.model is None or self.tokenizer is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")
        return func(self, *args, **kwargs)
    return wrapper

# um sigleton básico pra que não seja criado uma nova instancia de um modelo a cada request
# o problema aqui é que há um cold start na primeira requesição pro servidor, mas pra resolver isso, talvez cada modelo tenha seu contanier já inicializado quando o servidor inicia


class ParserManager:
    _instance = None
    _parsers = {}

    def __new__(cls):
        """
            checka se já há uma instância do ParserManager criada
        """
        if cls._instance is None:
            cls._instance = super(ParserManager, cls).__new__(cls)
        return cls._instance

    def get_parser(self, model_name: str) -> 'Parser':
        """
        Metodo para verificar se há alguma instância do modelo especificado já criado. Se não, é criado um novo
        """
        if model_name not in self._parsers:
            self._parsers[model_name] = Parser(model_name)
        return self._parsers[model_name]

    @property
    def available_models(self):
        return list(Parser.AVAILABLE_MODELS.keys())


class Parser:

    AVAILABLE_MODELS = {
        "minicpm": {
            "model": "openbmb/MiniCPM-V-2_6",
            "tokenizer": "openbmb/MiniCPM-V-2_6"
        },
        "minicpm-gguf": {
            "model_path": "A:\\Projetos\\ProjectOffer\\server\\models\\models--openbmb--MiniCPM-V-2_6-gguf\\snapshots\\69b9eaaebde4d5e2fafa1adb6a4169c349244cf6\\ggml-model-Q4_K_M.gguf",
        },
        "donut": {
            "model": "naver-clova-ix/donut-base-finetuned-cord-v2",
            "tokenizer": "naver-clova-ix/donut-base-finetuned-cord-v2"
        },
        "udop": {
            "model": "microsoft/udop-large",
            "tokenizer": "microsoft/udop-large"
        },
    }

    def __init__(self, model_name: str = "minicpm"):

        self.logger = logging.getLogger(__name__)

        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not available. Choose from: {
                             list(self.AVAILABLE_MODELS.keys())}")

        self.model_name = model_name
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.parse_methods = {
            "minicpm": self.parse_document_minicpm,
            "minicpm-gguf": self.parse_document_minicpm_gguf,
            "donut": self.parse_document_donut,
            "udop": self.parse_document_udop,
        }

        try:
            self.__initialize_model()
        except Exception as e:
            self.logger.error(f"Falha em inicializar o modelo: {str(e)}")
            raise ModelInitializationError(
                "Falha em inicializar o modelo") from e

    def __initialize_model(self):
        """
         inicializa o modelo definido
        """
        # não é o código mais sofisticado, mas funciona. como a versõa gguf não funciona com o AutoModel (talvez tenha, mas não cheguei a pesquisar muito sobre), ele usa o llma cpp pra inferencia
        try:
            model_config = self.AVAILABLE_MODELS[self.model_name]

            if self.model_name == "minicpm-gguf":
                self.model = Llama(
                    model_path=model_config["model_path"],
                    # chat_handler=Llava15ChatHandler,

                    n_ctx=26000, # eu ainda não conseguir fazer um metodo efetivo de passar uma imagem pro llm cpp. A única forma foi por base64, mas a quantidade de contexto fica muito alta.
                    n_threads=12,

                )
                self.tokenizer = None
            elif self.model_name == "donut":
                self.model = VisionEncoderDecoderModel.from_pretrained(
                    "naver-clova-ix/donut-base-finetuned-cord-v2")
                self.processor = DonutProcessor.from_pretrained(
                    "naver-clova-ix/donut-base-finetuned-cord-v2")
                pass
            else:
                self.model = AutoModel.from_pretrained(
                    model_config["model"],
                    trust_remote_code=True
                )
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_config["tokenizer"],
                    trust_remote_code=True
                )
                self.model.to("cpu")
                self.model.eval()

        except Exception as e:
            self.logger.error(f"Error em inicializar o modelo: {str(e)}")
            raise ModelInitializationError(
                f"Error em inicializar o modelo: {str(e)}") from e

    def parse_document(self, image: Image.Image):
        """
          metodo para extração de dados dos documentos
        """
        if self.model is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")

        parse_method = self.parse_methods.get(self.model_name)
        if parse_method is None:
            raise ValueError(f"No parse method defined for model: {
                             self.model_name}")
        return parse_method(image)

    def parse_document_donut(self, image):
        if self.model is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")
            
        image = Image.open(image).convert('RGB')
        # código abaixo é feito pelo nielsr https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Donut/CORD/Fine_tune_Donut_on_a_custom_dataset_(CORD)_with_PyTorch_Lightning.ipynb
        pixel_values = self.processor(image, return_tensors="pt").pixel_values

        task_prompt = "<s_cord-v2>"

        decoder_input_ids = self.processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)

        pixel_values = self.processor(image, return_tensors="pt").pixel_values

        outputs = self.model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=self.model.decoder.config.max_position_embeddings,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        sequence = self.processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(
            self.processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()

        result = self.processor.token2json(sequence)
        return result

    def parse_document_udop(self):
        if self.model is None or self.tokenizer is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")
        pass

    def parse_document_minicpm_gguf(self,  image: Image.Image):
        if self.model is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")
        base64_image_uri = image_to_base64_data_uri(image)
        question = """
        In this document, extract the important information such as the invoice number (if present), item IDs, item names, item prices, total, and subtotal. Format the information in a JSON file format like this:
        {
            "id": <id_of_invoice>,
            "date": <date_of_document>,
            "company": <company_name>,
            "phone": <company_phone_number>,
            "address": <company_address>,
            "items": [{
                "id": <id_of_item>,
                "name": <name_of_product>,
                "price": <price_of_product>
            }],
            "total": <total_price>,
            "subtotal": <subtotal_price>,
            "tax": <tax>,
            "payment": {
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

        messages = [
            {
                "role": "user",
                "content": f"{question}"
            },
            {"role": "user", "content": image}
        ]
        try:
            response = self.model.create_chat_completion(
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
            )
            print("aqui")
            print(response, "test")
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise DocumentParsingError(
                f"Error parsing document: {str(e)}") from e

    def parse_document_minicpm(self, image: Image.Image) -> Dict[str, Any]:
        if self.model is None or self.tokenizer is None:
            raise ModelInitializationError(
                "Modelo ou tokernizer não inicializado")

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
            raise DocumentParsingError(
                f"Error parsing document: {str(e)}") from e
