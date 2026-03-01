"""
src/prompt_engine/base.py
Responsabilidade: bloco base compartilhado por todos os prompts.

Técnicas aplicadas:
  - Persona Prompting: define o modelo como especialista em Pedagogia
  - Context Setting: injeta os dados reais do aluno no prompt
"""

from src.students import formatar_perfil_para_prompt


def construir_base(aluno: dict, topico: str) -> str:
    """
    Monta o bloco inicial comum a todos os prompts.

    Este bloco estabelece:
      - A persona do modelo (especialista em Pedagogia)
      - O contexto completo do aluno (idade, nível, estilo, interesses)
      - O tópico a ser ensinado
      - Diretrizes gerais de linguagem e didática
    """
    return f"""Você é um especialista em Educação, Pedagogia e Design Instrucional,
com vasta experiência em adaptar conteúdos educacionais para diferentes
idades, níveis de conhecimento e estilos de aprendizado.

Seu objetivo é gerar materiais educacionais personalizados, claros,
precisos e pedagogicamente eficazes.

{formatar_perfil_para_prompt(aluno)}

TÓPICO A SER ENSINADO:
{topico}

DIRETRIZES GERAIS:
- Use linguagem adequada à idade e ao nível do aluno
- Adapte exemplos ao estilo de aprendizado e aos interesses do aluno
- Seja claro, didático e progressivo
- Não assuma conhecimento prévio além do informado
- Evite jargões desnecessários para o nível do aluno"""