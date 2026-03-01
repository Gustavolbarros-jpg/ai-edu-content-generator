"""
src/prompt_engine/__init__.py
Porta de entrada do módulo prompt_engine.

Expõe apenas a função `montar` e as constantes públicas.
O restante da estrutura interna (base, v1, v2) é detalhe de implementação.
"""

from src.prompt_engine import v1, v2

TIPOS = ["explicacao_conceitual", "exemplos_praticos", "perguntas_reflexao", "resumo_visual"]
VERSOES = ["v1", "v2"]

_TABELA = {
    ("explicacao_conceitual", "v1"): v1.explicacao,
    ("explicacao_conceitual", "v2"): v2.explicacao,
    ("exemplos_praticos",     "v1"): v1.exemplos,
    ("exemplos_praticos",     "v2"): v2.exemplos,
    ("perguntas_reflexao",    "v1"): v1.perguntas,
    ("perguntas_reflexao",    "v2"): v2.perguntas,
    ("resumo_visual",         "v1"): v1.resumo_visual,
    ("resumo_visual",         "v2"): v2.resumo_visual,
}


def montar(aluno: dict, topico: str, tipo: str, versao: str = "v2") -> str:
    """
    Monta e retorna o prompt completo pronto para enviar à API.

    Args:
        aluno: perfil do aluno (de data/students.json)
        topico: assunto a ser ensinado
        tipo: um dos valores em TIPOS
        versao: "v1" (base) ou "v2" (otimizado)

    Returns:
        string com o prompt completo

    Raises:
        ValueError: se tipo ou versao forem inválidos
    """
    if tipo not in TIPOS:
        raise ValueError(f"Tipo inválido: '{tipo}'. Use um de: {TIPOS}")
    if versao not in VERSOES:
        raise ValueError(f"Versão inválida: '{versao}'. Use 'v1' ou 'v2'.")

    return _TABELA[(tipo, versao)](aluno, topico)