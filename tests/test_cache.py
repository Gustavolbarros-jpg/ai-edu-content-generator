"""
tests/test_cache.py
Testes unitários para src/cache.py
"""

import pytest
import json
import os
from unittest.mock import patch
from src.cache import buscar, salvar, limpar, info


ALUNO_ID = "test_aluno"
TOPICO = "teste"
TIPO = "explicacao_conceitual"
VERSAO = "v1"
CONTEUDO_FAKE = {"tipo": "explicacao_conceitual", "versao_prompt": "v1", "titulo": "Teste", "conteudo": "conteúdo de teste"}


@pytest.fixture(autouse=True)
def limpa_cache_antes_e_depois():
    """Garante cache limpo antes e depois de cada teste."""
    limpar()
    yield
    limpar()


def test_buscar_retorna_none_quando_vazio():
    resultado = buscar(ALUNO_ID, TOPICO, TIPO, VERSAO)
    assert resultado is None


def test_salvar_e_buscar():
    salvar(ALUNO_ID, TOPICO, TIPO, VERSAO, CONTEUDO_FAKE)
    resultado = buscar(ALUNO_ID, TOPICO, TIPO, VERSAO)
    assert resultado is not None
    assert resultado["conteudo"] == CONTEUDO_FAKE


def test_cache_diferencia_versoes():
    conteudo_v1 = {"versao": "v1", "conteudo": "texto v1"}
    conteudo_v2 = {"versao": "v2", "conteudo": "texto v2"}
    salvar(ALUNO_ID, TOPICO, TIPO, "v1", conteudo_v1)
    salvar(ALUNO_ID, TOPICO, TIPO, "v2", conteudo_v2)
    assert buscar(ALUNO_ID, TOPICO, TIPO, "v1")["conteudo"] == conteudo_v1
    assert buscar(ALUNO_ID, TOPICO, TIPO, "v2")["conteudo"] == conteudo_v2


def test_cache_diferencia_alunos():
    conteudo_a1 = {"aluno": "01"}
    conteudo_a2 = {"aluno": "02"}
    salvar("aluno_01", TOPICO, TIPO, VERSAO, conteudo_a1)
    salvar("aluno_02", TOPICO, TIPO, VERSAO, conteudo_a2)
    assert buscar("aluno_01", TOPICO, TIPO, VERSAO)["conteudo"] == conteudo_a1
    assert buscar("aluno_02", TOPICO, TIPO, VERSAO)["conteudo"] == conteudo_a2


def test_limpar_remove_entradas():
    salvar(ALUNO_ID, TOPICO, TIPO, VERSAO, CONTEUDO_FAKE)
    limpar()
    assert buscar(ALUNO_ID, TOPICO, TIPO, VERSAO) is None


def test_info_retorna_contagem():
    assert info()["total_entradas"] == 0
    salvar(ALUNO_ID, TOPICO, TIPO, VERSAO, CONTEUDO_FAKE)
    assert info()["total_entradas"] == 1