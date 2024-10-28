from flask import Flask, Response, request, jsonify, make_response
import pytorch_lightning as pl
from flask_cors import CORS
from llm_extraction import ParserManager



app = Flask(__name__)
CORS(app)

parser_manager = ParserManager()


# endpoint pra a extração dos documentos
@app.route("/parser", methods=["POST"])
def DocumentParse() -> Response:

    # busca nos headers da requisição por qual model iremos usar. se nenhum, o padrão é minicpm
    model_name = request.headers.get('X-Model-Name', 'minicpm')
 
    print(model_name)
    if not model_name:
        return make_response(jsonify({
            "error": "Nome do modelo não especificado no corpo da requisição"
        }), 400)

    if model_name not in parser_manager.available_models:
        return make_response(jsonify({
            "error": f"Modelo {model_name} não disponivel. Escolha um dos: {parser_manager.available_models}"
        }), 400)

    files = request.files.getlist("files")
    if not files:
        return make_response(jsonify({
            "error": "Nenhum arquivo fornecido"
        }), 400)

    try:
      
        parser = parser_manager.get_parser(model_name)
        data = []

        for file in files:
            img = file.stream
            res =parser.parse_document(img)
            data.append(res)
            

        result = {
            "message": "Arquivos recebidos",
            "model": model_name,
            "files": [file.filename for file in files],
            "data": data
        }
        return make_response(jsonify(result), 200)

    except Exception as e:
        return make_response(jsonify({
            "error": str(e)
        }), 500)


@app.route("/")
def index():
    return "Hello, World!"


app.run(debug=True, port=3001, host='0.0.0.0')
