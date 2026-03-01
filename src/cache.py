"""
src/cache.py
Responsabilidade: persistir e recuperar respostas da API para evitar
chamadas desnecessárias. Usa um único arquivo JSON indexado por hash.
"""

import json
import hashlib
import os
from datetime import datetime

CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "cache", "responses.json")


def _chave(aluno_id: str, topico: str, tipo: str, versao: str) -> str:
    raw = f"{aluno_id}|{topico}|{tipo}|{versao}"
    return hashlib.md5(raw.encode()).hexdigest()


def _carregar() -> dict:
    if not os.path.exists(CACHE_PATH):
        return {}
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar(dados: dict):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def buscar(aluno_id: str, topico: str, tipo: str, versao: str) -> dict | None:
    chave = _chave(aluno_id, topico, tipo, versao)
    entrada = _carregar().get(chave)
    if entrada:
        print(f"[CACHE HIT] {tipo} · {versao} · aluno={aluno_id} · tópico={topico}")
    return entrada


def salvar(aluno_id: str, topico: str, tipo: str, versao: str, conteudo: dict):
    dados = _carregar()
    chave = _chave(aluno_id, topico, tipo, versao)
    dados[chave] = {
        "aluno_id": aluno_id,
        "topico": topico,
        "tipo": tipo,
        "versao": versao,
        "cached_em": datetime.now().isoformat(),
        "conteudo": conteudo,
    }
    _salvar(dados)
    print(f"[CACHE SAVE] {tipo} · {versao}")


def limpar() -> int:
    _salvar({})
    print("[CACHE] Limpo.")
    return 0


def info() -> dict:
    dados = _carregar()
    return {"total_entradas": len(dados), "arquivo": CACHE_PATH}