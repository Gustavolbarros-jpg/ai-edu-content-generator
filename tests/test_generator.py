"""
tests/test_generator.py
Testes de integração para src/generator.py
Usa mock da API — não faz chamadas reais ao Gemini.
"""

import pytest
from unittest.mock import MagicMock, patch
from src.cache import limpar
from src.generator import gerar, comparar


CONTEUDO_FAKE_V1 = {
    "tipo": "explicacao_conceitual",
    "versao_prompt": "v1",
    "titulo": "Teste v1",
    "conteudo": "Explicação básica de teste."
}

CONTEUDO_FAKE_V2 = {
    "tipo": "explicacao_conceitual",
    "versao_prompt": "v2",
    "titulo": "Teste v2",
    "conceitos_chave": ["conceito 1"],
    "analogia_utilizada": "analogia de teste",
    "conteudo": "Explicação avançada de teste."
}


@pytest.fixture(autouse=True)
def limpa_cache():
    limpar()
    yield
    limpar()


@pytest.fixture
def mock_api(monkeypatch):
    """Mock da API Gemini — retorna JSON fake sem chamar a API."""
    import json
    resposta_mock = MagicMock()
    resposta_mock.text = json.dumps(CONTEUDO_FAKE_V1)

    client_mock = MagicMock()
    client_mock.models.generate_content.return_value = resposta_mock

    monkeypatch.setattr("src.generator._client", client_mock)
    return client_mock


def test_gerar_retorna_dict(mock_api):
    resultado = gerar("aluno_01", "fotossíntese", "explicacao_conceitual", "v1")
    assert isinstance(resultado, dict)


def test_gerar_conteudo_correto(mock_api):
    resultado = gerar("aluno_01", "fotossíntese", "explicacao_conceitual", "v1")
    assert resultado["tipo"] == "explicacao_conceitual"
    assert resultado["versao_prompt"] == "v1"


def test_gerar_usa_cache_na_segunda_chamada(mock_api):
    gerar("aluno_01", "fotossíntese", "explicacao_conceitual", "v1")
    gerar("aluno_01", "fotossíntese", "explicacao_conceitual", "v1")
    # API deve ter sido chamada só uma vez
    assert mock_api.models.generate_content.call_count == 1


def test_gerar_aluno_inexistente(mock_api):
    with pytest.raises(ValueError, match="não encontrado"):
        gerar("aluno_99", "fotossíntese", "explicacao_conceitual", "v1")


def test_gerar_tipo_invalido(mock_api):
    with pytest.raises(ValueError):
        gerar("aluno_01", "fotossíntese", "tipo_invalido", "v1")


def test_gerar_versao_invalida(mock_api):
    with pytest.raises(ValueError):
        gerar("aluno_01", "fotossíntese", "explicacao_conceitual", "v99")


def test_comparar_retorna_v1_e_v2(mock_api):
    import json
    # Alterna entre v1 e v2 nas chamadas
    respostas = [json.dumps(CONTEUDO_FAKE_V1), json.dumps(CONTEUDO_FAKE_V2)]
    mock_api.models.generate_content.side_effect = [
        MagicMock(text=r) for r in respostas
    ]
    resultado = comparar("aluno_01", "fotossíntese", "explicacao_conceitual")
    assert "v1" in resultado["comparacao"]
    assert "v2" in resultado["comparacao"]