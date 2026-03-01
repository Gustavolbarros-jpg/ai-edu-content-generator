"""
app.py
Interface web Flask para a plataforma educacional.
"""

import logging
from flask import Flask, render_template, request, jsonify
from src.generator import gerar, comparar
from src.students import carregar_perfis
from src.history import listar
from src.cache import info

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def _tratar_erro(e: Exception) -> tuple:
    msg = str(e)
    logger.error(f"Erro na requisição: {msg}")

    if "429" in msg:
        return "Limite de requisições atingido. Aguarde alguns segundos e tente novamente.", 429
    if "404" in msg and "model" in msg.lower():
        return "Modelo não encontrado. Verifique o GEMINI_MODEL no arquivo .env", 404
    if "GEMINI_API_KEY" in msg:
        return "Chave da API não configurada. Verifique o arquivo .env", 401
    if "não encontrado" in msg:
        return str(e), 404
    return f"Erro interno: {msg}", 500


@app.route("/")
def index():
    perfis = carregar_perfis()
    logger.info(f"Interface carregada — {len(perfis)} alunos disponíveis")
    return render_template("index.html", perfis=perfis)


@app.route("/gerar", methods=["POST"])
def gerar_conteudo():
    dados = request.json
    aluno_id = dados.get("aluno_id")
    topico = dados.get("topico", "").strip()
    tipo = dados.get("tipo")
    versao = dados.get("versao", "v2")

    if not topico:
        return jsonify({"status": "erro", "mensagem": "Tópico não pode ser vazio."}), 400

    logger.info(f"Gerando: {aluno_id} · {tipo} · {versao} · tópico={topico}")

    try:
        resultado = gerar(aluno_id=aluno_id, topico=topico, tipo=tipo, versao=versao)
        logger.info(f"Gerado com sucesso: {aluno_id} · {tipo} · {versao}")
        return jsonify({"status": "ok", "conteudo": resultado})
    except Exception as e:
        mensagem, status = _tratar_erro(e)
        return jsonify({"status": "erro", "mensagem": mensagem}), status


@app.route("/comparar", methods=["POST"])
def comparar_versoes():
    dados = request.json
    aluno_id = dados.get("aluno_id")
    topico = dados.get("topico", "").strip()
    tipo = dados.get("tipo")

    if not topico:
        return jsonify({"status": "erro", "mensagem": "Tópico não pode ser vazio."}), 400

    logger.info(f"Comparando v1 vs v2: {aluno_id} · {tipo} · tópico={topico}")

    try:
        resultado = comparar(aluno_id=aluno_id, topico=topico, tipo=tipo)
        logger.info(f"Comparação concluída: {aluno_id} · {tipo}")
        return jsonify({"status": "ok", "comparacao": resultado["comparacao"]})
    except Exception as e:
        mensagem, status = _tratar_erro(e)
        return jsonify({"status": "erro", "mensagem": mensagem}), status


@app.route("/historico")
def historico():
    aluno_id = request.args.get("aluno_id")
    tipo = request.args.get("tipo")
    registros = listar(aluno_id=aluno_id, tipo=tipo)
    logger.info(f"Histórico consultado — {len(registros)} registros")
    return jsonify(registros)


@app.route("/cache")
def cache_info():
    dados = info()
    return jsonify(dados)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "erro", "mensagem": "Rota não encontrada."}), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Erro interno: {e}")
    return jsonify({"status": "erro", "mensagem": "Erro interno do servidor."}), 500


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", debug=True)