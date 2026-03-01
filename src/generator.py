"""
src/generator.py
Responsabilidade: chamar a API Gemini e orquestrar o pipeline completo
de geração — cache → prompt → API → histórico → retorno.
"""

import json
import os
import re

from google import genai
from dotenv import load_dotenv

from src import cache, history
from src import prompt_engine
from src.students import buscar_aluno_por_id

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY não encontrada. Verifique seu arquivo .env")
        _client = genai.Client(api_key=api_key)
    return _client

def _extrair_json(texto: str) -> dict:
    # Remove blocos markdown
    texto_limpo = re.sub(r"```(?:json)?\s*", "", texto).replace("```", "").strip()
    # Remove apenas caracteres de controle invisíveis (não toca em \n estrutural)
    texto_limpo = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto_limpo)
    try:
        return json.loads(texto_limpo)
    except json.JSONDecodeError:
        # Tenta encontrar o bloco JSON e fazer parse linha a linha
        match = re.search(r'(\{[\s\S]*\})', texto_limpo)
        if match:
            bloco = match.group(1)
            # Escapa \n dentro de valores string
            bloco = re.sub(r'("(?:[^"\\]|\\.)*")', 
                          lambda m: m.group(0).replace('\n', '\\n'), 
                          bloco)
            try:
                return json.loads(bloco)
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Resposta da API não é JSON válido.\n\nResposta:\n{texto[:500]}")

def gerar(aluno_id: str, topico: str, tipo: str, versao: str = "v2") -> dict:
    """
    Pipeline completo de geração de conteúdo educacional.

    Fluxo:
      1. Valida parâmetros
      2. Verifica cache (evita chamada à API se já gerado antes)
      3. Monta o prompt via prompt_engine
      4. Chama a API Gemini
      5. Parseia o JSON da resposta
      6. Salva no cache e no histórico
      7. Retorna o conteúdo gerado
    """
    # 1. Validar aluno
    aluno = buscar_aluno_por_id(aluno_id)
    if not aluno:
        raise ValueError(f"Aluno '{aluno_id}' não encontrado.")

    # 2. Verificar cache
    cached = cache.buscar(aluno_id, topico, tipo, versao)
    if cached:
        history.registrar(aluno_id, topico, tipo, versao, cached["conteudo"], do_cache=True)
        return cached["conteudo"]

    # 3. Montar prompt
    prompt = prompt_engine.montar(aluno, topico, tipo, versao)

    # 4. Chamar API
    modelo_nome = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"[API] Gerando {tipo} · {versao} · modelo={modelo_nome}...")

    client = _get_client()
    resposta = client.models.generate_content(
        model=modelo_nome,
        contents=prompt
    )
    texto_resposta = resposta.text

    # 5. Parsear JSON
    conteudo = _extrair_json(texto_resposta)

    # 6. Persistir
    cache.salvar(aluno_id, topico, tipo, versao, conteudo)
    history.registrar(aluno_id, topico, tipo, versao, conteudo, do_cache=False)

    return conteudo


def comparar(aluno_id: str, topico: str, tipo: str) -> dict:
    """
    Gera o mesmo conteúdo com v1 e v2 e retorna os dois para comparação.
    Útil para demonstrar a diferença de qualidade entre versões de prompt.
    """
    print(f"\n{'='*50}")
    print(f"COMPARANDO VERSÕES: {tipo} · aluno={aluno_id} · tópico={topico}")
    print("="*50)

    resultado_v1 = gerar(aluno_id, topico, tipo, "v1")
    resultado_v2 = gerar(aluno_id, topico, tipo, "v2")

    return {
        "aluno_id": aluno_id,
        "topico": topico,
        "tipo": tipo,
        "comparacao": {
            "v1": resultado_v1,
            "v2": resultado_v2,
        }
    }