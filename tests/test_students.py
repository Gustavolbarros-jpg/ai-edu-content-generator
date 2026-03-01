"""
tests/test_students.py
Testes unitários para src/students.py
"""

import pytest
from src.students import carregar_perfis, buscar_aluno_por_id, formatar_perfil_para_prompt


def test_carregar_perfis_retorna_lista():
    perfis = carregar_perfis()
    assert isinstance(perfis, list)
    assert len(perfis) > 0


def test_carregar_perfis_tem_5_alunos():
    perfis = carregar_perfis()
    assert len(perfis) == 5


def test_perfil_tem_campos_obrigatorios():
    perfis = carregar_perfis()
    campos = ["id", "nome", "idade", "nivel_conhecimento", "estilo_aprendizado", "interesses"]
    for perfil in perfis:
        for campo in campos:
            assert campo in perfil, f"Campo '{campo}' ausente no perfil {perfil.get('id')}"


def test_buscar_aluno_existente():
    aluno = buscar_aluno_por_id("aluno_01")
    assert aluno is not None
    assert aluno["id"] == "aluno_01"


def test_buscar_aluno_inexistente():
    aluno = buscar_aluno_por_id("aluno_99")
    assert aluno is None


def test_formatar_perfil_retorna_string():
    aluno = buscar_aluno_por_id("aluno_01")
    resultado = formatar_perfil_para_prompt(aluno)
    assert isinstance(resultado, str)
    assert len(resultado) > 0


def test_formatar_perfil_contem_nome():
    aluno = buscar_aluno_por_id("aluno_01")
    resultado = formatar_perfil_para_prompt(aluno)
    assert aluno["nome"] in resultado