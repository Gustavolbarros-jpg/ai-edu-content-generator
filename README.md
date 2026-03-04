#  AI Edu Content Generator

Uma plataforma educacional inteligente que gera conteúdo altamente personalizado para alunos, adaptando-se às suas idades, níveis de conhecimento e estilos de aprendizado (VARK).

Este projeto é a minha submissão para o **Desafio Técnico – Estágio em IA e Engenharia de Prompt**. 

 **[Acesse a Aplicação em Produção (Railway) Aqui!](https://ai-edu-content-generator-production.up.railway.app/)**

---

##  O Desafio
O objetivo foi criar um sistema capaz de receber o perfil de um aluno e um tópico, e usar a API de uma LLM para gerar quatro tipos de conteúdos distintos (Explicação, Exemplos, Perguntas e Mapa Mental ASCII) estruturados rigorosamente em JSON.

##  Principais Funcionalidades e Destaques Técnicos

Para garantir uma entrega de excelência, além de cumprir os requisitos obrigatórios, implementei recursos de nível de produção:

* **Engenharia de Prompt Avançada (V1 vs V2):** O sistema permite comparar lado a lado um prompt base (V1) com um prompt otimizado (V2). A V2 utiliza *Persona Prompting*, *Chain-of-Thought*, *Taxonomia de Bloom* e *Adaptação VARK*. (Veja os detalhes em `PROMPT_ENGINEERING_NOTES.md`).
* **Structured Outputs Nativos:** Em vez de depender de expressões regulares (Regex) para extrair os JSONs da resposta em texto da IA, o projeto foi atualizado para utilizar o `response_mime_type="application/json"` da SDK moderna do Google Gemini, garantindo 100% de estabilidade na resposta estruturada.
* **Estratégia de Resiliência e FinOps (Warm Cache):** Para contornar os rígidos limites de requisição (Rate Limit 429) da API gratuita do Gemini durante a avaliação, implementei um sistema de cache baseado em Hash MD5. A aplicação já possui um *Warm Cache* pré-aquecido com **40 gerações** (5 alunos × 4 tipos × 2 versões), permitindo demonstração instantânea sem consumir cota da API.
* **LLM-as-a-Judge:** Pipeline de avaliação autônoma onde a própria IA avalia a qualidade dos outputs V1 vs V2 com critérios pedagógicos. Resultado: V2 vence em 3 de 4 tipos de conteúdo.
* **Retry Automático com Backoff:** O sistema tenta novamente até 3 vezes em caso de falha de JSON ou schema. Em caso de Rate Limit (429), retorna uma mensagem amigável ao usuário sem travar o servidor.
* **Arquitetura Modular:** Código Python rigorosamente modularizado (`src/`), separando a lógica de negócio, as chamadas à API, os perfis dos alunos e a interface.
* **Validação de Contratos (Pydantic):** Os schemas de resposta são garantidos por modelos Pydantic, garantindo que o front-end nunca quebre com variáveis ausentes.
* **Self-Healing:** O sistema cria automaticamente suas próprias estruturas de diretórios e arquivos caso não existam.
* **26 Testes Automatizados:** Cobertura completa com pytest, incluindo testes de retry, cache isolado com `tmp_path` e LLM-as-a-Judge mockado.

---

## 💻 Tecnologias Utilizadas

* **Backend:** Python 3.11, Flask
* **Inteligência Artificial:** Google GenAI SDK (Gemini 2.5 Flash)
* **Validação:** Pydantic
* **Infraestrutura:** Docker, Railway (Deploy CI/CD)
* **Testes:** Pytest

---

##  Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/Gustavolbarros-jpg/ai-edu-content-generator.git
cd ai-edu-content-generator
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure a Chave da API:
```bash
cp .env.example .env
# Edite o .env e insira sua chave do Google Gemini
```

4. Inicie o servidor:
```bash
python app.py
```

5. Acesse http://localhost:5000 no seu navegador.

---

##  Como Testar (Golden Path)

A aplicação possui um *Warm Cache* pré-aquecido com **40 gerações** (5 alunos × 4 tipos × 2 versões). Todos os cenários retornam instantaneamente sem consumir cota da API.

Selecione qualquer aluno > Fotossíntese > qualquer tipo > Clique em **Comparar**.

A diferença entre o prompt básico (V1) e o prompt otimizado (V2) ficará evidente nos badges e na qualidade do conteúdo gerado.

---

##  Avaliação Automatizada (LLM-as-a-Judge)

Para provar de forma analítica e sem viés humano a superioridade da Engenharia de Prompt da V2 sobre a V1, este projeto inclui um pipeline de avaliação autônoma. A própria IA atua como um "Juiz Cego" avaliando critérios pedagógicos (adequação de linguagem, clareza pedagógica, personalização e riqueza de conteúdo).

**Resultado:** V2 vence em 3 de 4 tipos de conteúdo, com destaque para `perguntas_reflexao` (V1: 3.75 | V2: 5.0).

Para rodar o avaliador:
```bash
python scripts/evaluate.py
```

Os resultados ficam salvos em `samples/evaluation.json`.

---

##  Rodar os Testes
```bash
python3 -m pytest tests/ -v
# 26 passed
```