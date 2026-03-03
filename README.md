#  AI Edu Content Generator

Uma plataforma educacional inteligente que gera conteúdo altamente personalizado para alunos, adaptando-se às suas idades, níveis de conhecimento e estilos de aprendizado (VARK).

Este projeto é a minha submissão para o **Desafio Técnico – Estágio em IA e Engenharia de Prompt**. 

🌐**[Acesse a Aplicação em Produção (Railway) Aqui!](https://ai-edu-content-generator-production.up.railway.app/)**
🎥
---

##  O Desafio
O objetivo foi criar um sistema capaz de receber o perfil de um aluno e um tópico, e usar a API de uma LLM para gerar quatro tipos de conteúdos distintos (Explicação, Exemplos, Perguntas e Mapa Mental ASCII) estruturados rigorosamente em JSON.

##  Principais Funcionalidades e Destaques Técnicos

Para garantir uma entrega de excelência, além de cumprir os requisitos obrigatórios, implementei recursos de nível de produção:

* **Engenharia de Prompt Avançada (V1 vs V2):** O sistema permite comparar lado a lado um prompt base (V1) com um prompt otimizado (V2). A V2 utiliza *Persona Prompting*, *Chain-of-Thought*, *Taxonomia de Bloom* e *Adaptação VARK*. (Veja os detalhes em `PROMPT_ENGINEERING_NOTES.md`).
* **Structured Outputs Nativos:** Em vez de depender de expressões regulares (Regex) para extrair os JSONs da resposta em texto da IA, o projeto foi atualizado para utilizar o `response_mime_type="application/json"` da SDK moderna do Google Gemini, garantindo 100% de estabilidade na resposta estruturada.
* **Estratégia de Resiliência e FinOps (Warm Cache):** Para contornar os rígidos limites de requisição (Rate Limit 429) da API gratuita do Gemini durante a avaliação, implementei um sistema de cache baseado em Hash MD5. As requisições idênticas são servidas instantaneamente a partir do disco, economizando tokens e latência. (A aplicação em produção já possui um *Warm Cache* de alguns cenários, como o do aluno *Lucas Mendes*, para testes rápidos).
* **Arquitetura MVC:** Código Python rigorosamente modularizado (`src/`), separando a lógica de negócio, as chamadas à API, os perfis dos alunos e a interface.
* **Validação de Contratos (Pydantic):** Os schemas de resposta são garantidos por modelos Pydantic, garantindo que o front-end nunca quebre com variáveis ausentes.
* **Self-Healing:** O sistema de manipulação de arquivos foi desenhado para criar suas próprias estruturas de diretórios automaticamente caso não existam.

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
git clone [https://github.com/Gustavolbarros-jpg/ai-edu-content-generator.git](https://github.com/Gustavolbarros-jpg/ai-edu-content-generator.git)
cd ai-edu-content-generator
Crie um ambiente virtual e instale as dependências:

Bash

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure a Chave da API:
Crie um arquivo .env na raiz do projeto baseado no .env.example e insira sua chave do Google Gemini:

Snippet de código

GEMINI_API_KEY="sua_chave_aqui"
Inicie o servidor:

Bash

python app.py
Acesse http://localhost:5000 no seu navegador.

 Como Testar (Golden Path)
Para testar a aplicação na URL de produção sem esbarrar nos limites da API gratuita do Gemini, recomendo utilizar os cenários que deixei pré-processados no Cache.

Selecione Lucas Mendes > Fotossíntese > Resumo Visual > Clique em Comparar.

A diferença entre o prompt básico (v1) e o prompt otimizado para o estilo de aprendizado visual (v2) ficará evidente.

***

### Passo a passo para fechar tudo:

1. **Substitua** todo o texto do seu `README.md` atual pelo template que mandei acima.
2. **Atualize os Links:** Não se esqueça de trocar `COLOQUE_SEU_LINK_DO_RAILWAY_AQUI` pela URL real do seu deploy e de colocar o link do seu vídeo (Loom ou YouTube).
3. Salve, faça o *commit* na branch `develop` (ex: `docs: atualiza README com destaques do projeto e instrucoes de uso`), dê o *merge* para a `main` e suba (push).
4. Relaxe e mande a submissão para a vaga. O seu projeto está nível Sênior em organização!