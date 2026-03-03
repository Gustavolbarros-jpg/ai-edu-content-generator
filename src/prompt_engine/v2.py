"""
src/prompt_engine/v2.py
Responsabilidade: prompts v2 — versão otimizada com técnicas avançadas.

Técnicas aplicadas nesta versão:
  - Chain-of-Thought: raciocínio passo a passo antes da resposta (explicacao)
  - Context Setting profundo: interesses e estilo VARK injetados (exemplos)
  - Taxonomia de Bloom: níveis cognitivos crescentes (perguntas)
  - Structured Prompting: hierarquia explícita de 3 níveis (resumo_visual)
  - Output Formatting rígido: campos semânticos extras em todos os tipos
"""

from src.prompt_engine.base import construir_base


def explicacao(aluno: dict, topico: str) -> str:
    """
    Técnica principal: Chain-of-Thought

    Força o modelo a planejar 5 passos antes de escrever.
    Resultado esperado vs v1: progressão didática mais coerente,
    analogias conectadas aos interesses reais do aluno, vocabulário
    calibrado para a idade.
    """
    interesses = ", ".join(aluno.get("interesses", []))
    return f"""{construir_base(aluno, topico)}

TAREFA:
Gere uma explicação conceitual sobre o tópico acima para este aluno específico.

ANTES DE ESCREVER, raciocine internamente seguindo estas etapas:
  Passo 1 — Identifique os 2 ou 3 conceitos fundamentais do tópico
  Passo 2 — Considere o nível "{aluno['nivel_conhecimento']}" e a idade de {aluno['idade']} anos: que conhecimentos prévios ele já tem?
  Passo 3 — Escolha uma analogia com algo que o aluno conhece (interesses: {interesses})
  Passo 4 — Planeje a progressão: do mais simples ao mais complexo
  Passo 5 — Agora escreva a explicação seguindo esse plano

REGRAS OBRIGATÓRIAS:
- A explicação deve ter introdução, desenvolvimento e conclusão
- Use a analogia escolhida no Passo 3
- Não use termos técnicos sem explicá-los antes
- Adapte o vocabulário para {aluno['idade']} anos

FORMATO DE SAÍDA OBRIGATÓRIO (JSON puro, sem markdown):
{{
  "tipo": "explicacao_conceitual",
  "versao_prompt": "v2",
  "titulo": "título curto e atrativo para o aluno",
  "conceitos_chave": ["conceito 1", "conceito 2"],
  "analogia_utilizada": "descreva brevemente a analogia escolhida",
  "conteudo": "explicação completa aqui",
  "nivel_adequado": true
}}"""


def exemplos(aluno: dict, topico: str) -> str:
    """
    Técnica principal: Context Setting profundo + Output Formatting

    Injeta interesses e estilo VARK para exemplos hiper-personalizados.
    Resultado esperado vs v1: exemplos concretos ligados à realidade do
    aluno, com progressão de complexidade e raciocínio auditável via
    campo conexao_com_aluno.
    """
    interesses = ", ".join(aluno.get("interesses", []))
    estilo = aluno.get("estilo_aprendizado", "visual")
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie exatamente 3 exemplos práticos sobre o tópico, personalizados para este aluno.

CRITÉRIOS PARA CADA EXEMPLO:
  Exemplo 1 (básico): conectado diretamente a um dos interesses do aluno ({interesses})
  Exemplo 2 (intermediário): situação do cotidiano de um estudante de {aluno['idade']} anos
  Exemplo 3 (aplicado): mostra onde este conceito aparece no mundo real

ADAPTE ao estilo de aprendizado "{estilo}":
  visual        → inclua descrição de como isso "parece" ou pode ser desenhado
  auditivo      → use ritmo, narrativa, sons ou histórias
  leitura-escrita → use comparações e definições precisas
  cinestésico   → descreva uma ação ou experimento que o aluno pode fazer

FORMATO DE SAÍDA OBRIGATÓRIO (JSON puro, sem markdown):
{{
  "tipo": "exemplos_praticos",
  "versao_prompt": "v2",
  "estilo_aplicado": "{estilo}",
  "exemplos": [
    {{
      "nivel": "basico",
      "titulo": "...",
      "descricao": "...",
      "conexao_com_aluno": "explique por que este exemplo foi escolhido para este aluno"
    }},
    {{
      "nivel": "intermediario",
      "titulo": "...",
      "descricao": "...",
      "conexao_com_aluno": "..."
    }},
    {{
      "nivel": "aplicado",
      "titulo": "...",
      "descricao": "...",
      "conexao_com_aluno": "..."
    }}
  ]
}}"""


def perguntas(aluno: dict, topico: str) -> str:
    """
    Técnica principal: Output Formatting + Taxonomia de Bloom implícita

    4 perguntas com níveis cognitivos crescentes e objetivo pedagógico
    declarado. Resultado esperado vs v1: perguntas com propósito claro,
    abertas, que estimulam pensamento crítico real.
    """
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie exatamente 4 perguntas de reflexão sobre o tópico, com dificuldade crescente.

ESTRUTURA OBRIGATÓRIA DAS PERGUNTAS:
  Pergunta 1 (compreensão): verifica se o aluno entendeu o conceito básico
  Pergunta 2 (aplicação): pede para o aluno usar o conceito em uma situação
  Pergunta 3 (análise): pede para o aluno comparar, diferenciar ou explicar por quê
  Pergunta 4 (síntese): pede para o aluno criar, imaginar ou propor algo novo

REGRAS:
- Linguagem adequada para {aluno['idade']} anos e nível {aluno['nivel_conhecimento']}
- Perguntas abertas — não podem ser respondidas com "sim" ou "não"
- Cada pergunta deve instigar curiosidade, não apenas memorização

FORMATO DE SAÍDA OBRIGATÓRIO (JSON puro, sem markdown):
{{
  "tipo": "perguntas_reflexao",
  "versao_prompt": "v2",
  "perguntas": [
    {{
      "numero": 1,
      "nivel_cognitivo": "compreensão",
      "pergunta": "...",
      "objetivo_pedagogico": "o que esta pergunta pretende desenvolver no aluno"
    }},
    {{
      "numero": 2,
      "nivel_cognitivo": "aplicação",
      "pergunta": "...",
      "objetivo_pedagogico": "..."
    }},
    {{
      "numero": 3,
      "nivel_cognitivo": "análise",
      "pergunta": "...",
      "objetivo_pedagogico": "..."
    }},
    {{
      "numero": 4,
      "nivel_cognitivo": "síntese",
      "pergunta": "...",
      "objetivo_pedagogico": "..."
    }}
  ]
}}"""


def resumo_visual(aluno: dict, topico: str) -> str:
    """
    Técnica principal: Structured Prompting com hierarquia explícita

    Define 3 níveis obrigatórios no mapa e adapta o conteúdo dos nós
    ao estilo VARK do aluno. Resultado esperado vs v1: mapa navegável
    com hierarquia clara, legenda pedagógica e dica de uso.
    """
    estilo = aluno.get("estilo_aprendizado", "visual")
    return f"""{construir_base(aluno, topico)}

TAREFA:
Crie um resumo visual completo do tópico em formato de mapa mental ASCII.

ESTRUTURA OBRIGATÓRIA DO MAPA:
  Nível 0 (centro): o tópico principal
  Nível 1 (ramos): os 3 ou 4 conceitos principais do tópico
  Nível 2 (sub-ramos): 2 detalhes ou exemplos para cada conceito do Nível 1
  Nível 3 (folhas, opcional): conexões ou curiosidades relevantes

ADAPTE ao estilo "{estilo}":
  visual        → use símbolos e estrutura clara com espaçamento generoso
  auditivo      → adicione palavras-chave sonoras ou rítmicas nos nós
  leitura-escrita → inclua definições curtas junto aos nós
  cinestésico   → inclua verbos de ação nos nós ("fazer", "testar", "observar")

REGRAS DO ASCII:
- Use os caracteres: │ ├ └ ─ ┬
- Cada nó deve caber em uma linha
- Indentação indica hierarquia


FORMATO DE SAÍDA OBRIGATÓRIO (JSON puro, sem markdown):
{{
  "tipo": "resumo_visual",
  "versao_prompt": "v2",
  "estilo_aplicado": "{estilo}",
  "descricao": "breve parágrafo descrevendo o que este mapa mental aborda",
  "mapa_ascii": "cole aqui o mapa mental completo",
  "legenda": "explique as relações principais representadas no mapa",
  "dica_de_uso": "como o aluno pode usar este mapa para estudar"
}}"""