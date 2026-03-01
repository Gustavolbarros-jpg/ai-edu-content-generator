"""
src/evaluator.py
Responsabilidade: avaliar a qualidade dos outputs gerados usando
o próprio Gemini como juiz (LLM-as-a-Judge).

Critérios de avaliação:
  - adequacao_linguagem: vocabulário adequado para idade/nível
  - clareza_pedagogica: clareza e progressão didática
  - personalizacao: uso dos interesses e estilo do aluno
  - riqueza_conteudo: profundidade e completude da resposta
"""

import os
import json
import logging
from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY não encontrada.")
        _client = genai.Client(api_key=api_key)
    return _client


def _montar_prompt_juiz(aluno: dict, tipo: str, conteudo_v1: dict, conteudo_v2: dict) -> str:
    return f"""Você é um especialista em avaliação de qualidade de conteúdo educacional.

Avalie os dois conteúdos abaixo gerados para o seguinte aluno:
- Nome: {aluno['nome']}
- Idade: {aluno['idade']} anos
- Nível: {aluno['nivel_conhecimento']}
- Estilo de aprendizado: {aluno['estilo_aprendizado']}
- Interesses: {', '.join(aluno['interesses'])}

Tipo de conteúdo: {tipo}

=== CONTEÚDO V1 ===
{json.dumps(conteudo_v1, ensure_ascii=False, indent=2)}

=== CONTEÚDO V2 ===
{json.dumps(conteudo_v2, ensure_ascii=False, indent=2)}

Avalie cada conteúdo nos critérios abaixo com nota de 1 a 5:
- adequacao_linguagem: vocabulário e tom adequados para a idade e nível
- clareza_pedagogica: clareza, progressão e estrutura didática
- personalizacao: uso real dos interesses e estilo do aluno
- riqueza_conteudo: profundidade, completude e campos semânticos

Responda EXCLUSIVAMENTE em JSON puro, sem markdown:
{{
  "v1": {{
    "adequacao_linguagem": <1-5>,
    "clareza_pedagogica": <1-5>,
    "personalizacao": <1-5>,
    "riqueza_conteudo": <1-5>,
    "media": <media das 4 notas>,
    "justificativa": "resumo em 1-2 frases"
  }},
  "v2": {{
    "adequacao_linguagem": <1-5>,
    "clareza_pedagogica": <1-5>,
    "personalizacao": <1-5>,
    "riqueza_conteudo": <1-5>,
    "media": <media das 4 notas>,
    "justificativa": "resumo em 1-2 frases"
  }},
  "vencedor": "v1 ou v2",
  "ganho_percentual": <quanto o vencedor superou em %>
}}"""


def avaliar(aluno: dict, tipo: str, conteudo_v1: dict, conteudo_v2: dict) -> dict:
    """Avalia v1 vs v2 usando o Gemini como juiz."""
    prompt = _montar_prompt_juiz(aluno, tipo, conteudo_v1, conteudo_v2)
    modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    client = _get_client()

    logger.info(f"[JUDGE] Avaliando {tipo} com LLM-as-a-Judge...")
    resposta = client.models.generate_content(model=modelo, contents=prompt)

    import re
    texto = resposta.text
    texto_limpo = re.sub(r"```(?:json)?\s*", "", texto).replace("```", "").strip()

    try:
        return json.loads(texto_limpo)
    except json.JSONDecodeError:
        match = re.search(r'(\{[\s\S]*\})', texto_limpo)
        if match:
            return json.loads(match.group(1))
        raise ValueError(f"Juiz retornou JSON inválido: {texto[:300]}")