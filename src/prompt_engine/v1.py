"""
src/prompt_engine/v1.py
Responsabilidade: prompts v1 — versão base para comparação.

Técnicas aplicadas nesta versão:
  - Persona Prompting (via bloco base)
  - Context Setting básico (via bloco base)
  - Output Formatting simples

Limitações intencionais (para evidenciar melhoria na v2):
  - Sem chain-of-thought → resposta tende a ser genérica
  - Analogia livre → modelo escolhe sem critério pedagógico
  - Sem níveis cognitivos (Bloom) → perguntas podem ser rasas
  - Sem adaptação VARK → exemplos não consideram estilo de aprendizado
  - Formato de saída mínimo → menos campos para análise comparativa
"""

from src.prompt_engine.base import construir_base


def explicacao(aluno: dict, topico: str) -> str:
    return f"""{construir_base(aluno, topico)}

TAREFA:
Escreva uma explicação conceitual sobre o tópico acima para este aluno.

INSTRUÇÕES:
- Adapte a linguagem para {aluno['idade']} anos e nível {aluno['nivel_conhecimento']}
- Use pelo menos uma analogia para facilitar a compreensão
- Cubra os conceitos principais do tópico

FORMATO DE SAÍDA (JSON puro, sem markdown):
{{
  "tipo": "explicacao_conceitual",
  "versao_prompt": "v1",
  "titulo": "título atrativo para o aluno",
  "conteudo": "explicação completa aqui"
}}"""


def exemplos(aluno: dict, topico: str) -> str:
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie exatamente 3 exemplos práticos sobre o tópico para este aluno.

INSTRUÇÕES:
- Cada exemplo deve ter título e descrição
- Use situações concretas e fáceis de visualizar
- Adapte para a idade de {aluno['idade']} anos

FORMATO DE SAÍDA (JSON puro, sem markdown):
{{
  "tipo": "exemplos_praticos",
  "versao_prompt": "v1",
  "exemplos": [
    {{"titulo": "...", "descricao": "..."}},
    {{"titulo": "...", "descricao": "..."}},
    {{"titulo": "...", "descricao": "..."}}
  ]
}}"""


def perguntas(aluno: dict, topico: str) -> str:
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie exatamente 4 perguntas de reflexão sobre o tópico para este aluno.

INSTRUÇÕES:
- As perguntas devem ser abertas (não respondíveis com sim/não)
- Devem estimular o pensamento, não apenas memorização
- Linguagem adequada para {aluno['idade']} anos e nível {aluno['nivel_conhecimento']}
- Ordene da mais simples para a mais desafiadora

FORMATO DE SAÍDA (JSON puro, sem markdown):
{{
  "tipo": "perguntas_reflexao",
  "versao_prompt": "v1",
  "perguntas": ["...", "...", "...", "..."]
}}"""


def resumo_visual(aluno: dict, topico: str) -> str:
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie um resumo visual em formato de mapa mental ASCII sobre o tópico.

INSTRUÇÕES:
- Mostre os conceitos principais e seus detalhes
- Use hierarquia visual clara com indentação
- Inclua entradas, processo e saídas do fenômeno
- Use os caracteres: │ ├ └ ─

FORMATO DE SAÍDA (JSON puro, sem markdown):
{{
  "tipo": "resumo_visual",
  "versao_prompt": "v1",
  "mapa_ascii": "mapa mental completo aqui",
  "descricao": "breve explicação do mapa"
}}"""