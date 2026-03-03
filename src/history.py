"""
src/history.py
Responsabilidade: persistir o histórico de gerações com timestamp.
Cada geração é salva independente do cache — o cache evita chamadas à API,
o histórico registra tudo que foi gerado para análise posterior.
"""

import json
import os
from datetime import datetime

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


def _carregar() -> list:
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
            # suporta tanto lista direta quanto {"historico": [...]}
            if isinstance(dados, list):
                return dados
            return dados.get("historico", [])
        except json.JSONDecodeError:
            return []


def _salvar(dados):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def registrar(aluno_id: str, topico: str, tipo: str, versao: str, conteudo: dict, do_cache: bool = False):
    """Adiciona uma entrada ao histórico."""
    historico = _carregar()
    historico.append({
        "id": f"GEN_{len(historico) + 1:04d}",
        "gerado_em": datetime.now().isoformat(),
        "aluno_id": aluno_id,
        "topico": topico,
        "tipo": tipo,
        "versao_prompt": versao,
        "do_cache": do_cache,
        "conteudo": conteudo,
    })
    _salvar(historico)


def listar(aluno_id: str = None, tipo: str = None) -> list:
    """Lista o histórico com filtros opcionais."""
    historico = _carregar()
    if aluno_id:
        historico = [h for h in historico if h["aluno_id"] == aluno_id]
    if tipo:
        historico = [h for h in historico if h["tipo"] == tipo]
    return historico


def limpar():
    _salvar([])
    print("[HISTÓRICO] Limpo.")