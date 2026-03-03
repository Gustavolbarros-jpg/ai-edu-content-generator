# Prompt Engineering Notes

## Contexto e Origem

Este projeto nasceu da evolução de um pipeline de geração de conteúdo com IA que desenvolvi anteriormente. O pipeline original estabeleceu padrões de padronização e consistência — outputs em JSON estruturado, separação de blocos de contexto reutilizáveis, cache por hash — que foram adaptados e aprimorados aqui para o domínio educacional.

A adaptação exigiu incorporar camadas específicas de pedagogia: Taxonomia de Bloom para estruturar progressão cognitiva, adaptação VARK por estilo de aprendizado, e persona de educador experiente. Essas adições transformaram um pipeline genérico em um sistema especializado em personalização de conteúdo educacional.

O resultado é uma arquitetura onde as boas práticas de engenharia de prompt do pipeline original se combinam com técnicas pedagógicas para gerar conteúdo genuinamente adaptado a cada aluno.


## Visão Geral

O sistema implementa duas versões de prompt para cada tipo de conteúdo:

- **v1** — prompt base, direto ao ponto, sem técnicas avançadas. Serve como baseline para comparação.
- **v2** — prompt otimizado com múltiplas técnicas avançadas combinadas.

A diferença de qualidade entre v1 e v2 é intencional e demonstrável nos outputs gerados em `samples/`.

---

## Técnicas Implementadas

### 1. Persona Prompting

**Onde:** `src/prompt_engine/base.py` — bloco base injetado em todos os prompts v2.

**Implementação:**
```
Você é um especialista em Educação e Pedagogia com 15 anos de experiência
ensinando para alunos do ensino fundamental e médio...
```

**Por que funciona:** O modelo adota o frame mental de um educador experiente, calibrando automaticamente linguagem, exemplos e profundidade para o contexto pedagógico. Sem essa instrução, o modelo tende a gerar conteúdo genérico enciclopédico.

---

### 2. Context Setting

**Onde:** `src/prompt_engine/base.py` — função `formatar_perfil_para_prompt()`.

**Implementação:**
```
PERFIL DO ALUNO:
- Nome: Lucas Mendes
- Idade: 10 anos
- Nível de conhecimento: iniciante
- Estilo de aprendizado: visual
- Interesses: videogames, futebol, desenho
- Dificuldades: abstração, textos longos
```

**Por que funciona:** Fornece contexto específico e não ambíguo. O modelo não precisa inferir o público-alvo — ele recebe o perfil completo. Isso elimina respostas genéricas e força personalização real. O efeito é visível: o mesmo tópico (fotossíntese) gera analogias completamente diferentes para Lucas (videogame) vs Pedro (robótica).

---

### 3. Chain-of-Thought

**Onde:** `src/prompt_engine/v2.py` — prompt de explicação conceitual.

**Implementação:**
```
Antes de escrever a explicação, pense passo a passo:
1. Qual é o conceito central e seus pré-requisitos?
2. Quais analogias do universo do aluno se encaixam?
3. Qual nível de vocabulário é adequado para esta idade?
4. Como estruturar para máxima retenção?
5. Qual exemplo concreto ancora a explicação?
Agora escreva a explicação com base nesse raciocínio.
```

**Por que funciona:** Força o modelo a planejar antes de executar. Sem CoT, o modelo começa a escrever imediatamente e frequentemente perde coerência pedagógica no meio da explicação. Com CoT, a estrutura e progressão são mais sólidas.

**Diferença mensurável:** Outputs v2 têm progressão do simples ao complexo mais consistente. Outputs v1 às vezes misturam níveis de abstração.

---

### 4. Taxonomia de Bloom

**Onde:** `src/prompt_engine/v2.py` — prompt de perguntas de reflexão.

**Implementação:**
```
Gere 4 perguntas em níveis crescentes da Taxonomia de Bloom:
1. Compreensão — o aluno consegue explicar o conceito?
2. Aplicação — consegue usar o conhecimento em situação nova?
3. Análise — consegue comparar e diferenciar?
4. Síntese — consegue criar algo novo com o conhecimento?
```

**Por que funciona:** Garante que as perguntas não fiquem todas no nível superficial de memorização. A maioria dos geradores de perguntas sem essa instrução produz perguntas equivalentes ao nível 1-2 de Bloom. Com a instrução explícita, o modelo distribui os níveis cognitivos corretamente.

**Resultado visível nos samples:** As perguntas do aluno_03 (Pedro, 17 anos, avançado) chegam ao nível de síntese com propostas de projetos de engenharia.

---

### 5. Adaptação VARK

**Onde:** `src/prompt_engine/v2.py` — prompts de exemplos práticos e resumo visual.

**Implementação:**
```
O aluno tem estilo de aprendizado: VISUAL
Adapte o conteúdo para este estilo:
- Visual: use diagramas ASCII, metáforas visuais, descrições de imagens
- Auditivo: use ritmo, narrativa, analogias sonoras
- Leitura-escrita: use listas estruturadas, definições precisas, vocabulário técnico
- Cinestésico: use ações físicas, projetos práticos, experimentos
```

**Por que funciona:** O modelo por padrão gera conteúdo textual neutro. A instrução VARK força uma mudança de modalidade real. Comparando os resumos visuais: Lucas (visual) recebe mapa ASCII com símbolos e dicas de desenho; Ana (leitura-escrita) recebe estrutura hierárquica com definições precisas.

---

### 6. Output Formatting e Structured Outputs (JSON Mode)

**Onde:** Todos os prompts v1 e v2, e na chamada da API em `src/generator.py`.

**Implementação:**
No prompt:
```text
Responda EXCLUSIVAMENTE em JSON válido com esta estrutura exata:
{
  "tipo": "explicacao_conceitual",
  "versao_prompt": "v1",
  "titulo": "...",
  "conteudo": "..."
}
Não inclua texto fora do JSON. Não use blocos markdown.
Na API: Configuração response_mime_type="application/json" utilizando a SDK moderna do Google GenAI.

Por que funciona: Sem output formatting, o modelo envolve o JSON em texto explicativo e blocos markdown, quebrando o parse. A evolução nesta arquitetura foi combinar a instrução rigorosa no prompt com a camada de API (Native JSON Mode), forçando o modelo a respeitar a estrutura nativamente na origem. Uma camada final de validação via Pydantic assegura o contrato dos dados.


---

## Comparação v1 vs v2

| Aspecto | v1 | v2 |
|---|---|---|
| Persona | Não | Sim — educador com 15 anos |
| Perfil do aluno | Não | Sim — nome, idade, estilo, interesses |
| Chain-of-Thought | Não | Sim — 5 passos de raciocínio |
| Taxonomia de Bloom | Não | Sim — 4 níveis explícitos |
| Adaptação VARK | Não | Sim — por estilo de aprendizado |
| Campos no JSON | 3-4 | 6-8 |
| Objetivo pedagógico declarado | Não | Sim — por pergunta/exemplo |

---


```markdown
### 7. Avaliação Automatizada (LLM-as-a-Judge)

**Onde:** `src/evaluator.py` e script de testes `scripts/evaluate.py`.

**Implementação:**
Foi desenvolvido um prompt avaliador ("Juiz") que recebe o perfil do aluno, o tópico e as gerações (v1 e v2) de forma anônima (A e B). O juiz é instruído a:
1. Avaliar clareza, adequação à idade e uso de analogias.
2. Identificar qual versão atendeu melhor ao estilo de aprendizado do aluno.
3. Declarar um vencedor justificado.

**Por que funciona:** Avaliar a qualidade da geração de texto em larga escala é um desafio. O padrão *LLM-as-a-Judge* remove o viés humano e cria um pipeline de avaliação autônomo. Os resultados (disponíveis em `samples/evaluation.json`) comprovam analiticamente e de forma escalável que as técnicas de Engenharia de Prompt aplicadas na V2 geram um conteúdo superior.

## Decisões de Design

**Por que JSON estruturado?**
Permite que a interface consuma os outputs de forma programática. Campos semânticos como `conceitos_chave`, `analogia_utilizada` e `objetivo_pedagogico` tornam a qualidade do prompt auditável — o avaliador pode ver o raciocínio do modelo, não apenas o resultado final.

**Por que manter o v1?**
O v1 existe como baseline de comparação. Sem ele, é impossível demonstrar o valor das técnicas avançadas. A diferença de qualidade só é visível quando os dois são apresentados lado a lado.

**Por que Gemini 2.5 Flash?**
Melhor custo-benefício para o free tier. O modelo é suficientemente capaz para as técnicas implementadas. O Gemini 2.5 Pro gerava outputs mais ricos mas esgotava a cota diária rapidamente.


