

import json
import os

# Caminho absoluto para o arquivo de perfis
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "students.json")


def carregar_perfis() -> list[dict]:
    #Carrega todos os perfis de alunos do arquivo JSON.
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados["students"]


def buscar_aluno_por_id(aluno_id: str) -> dict | None:
    #Retorna o perfil de um aluno específico pelo ID.
    perfis = carregar_perfis()
    for aluno in perfis:
        if aluno["id"] == aluno_id:
            return aluno
    return None


def listar_alunos() -> list[dict]:
    #Retorna lista resumida de alunos (id, nome, nível) para exibição em menu.
    perfis = carregar_perfis()
    return [
        {
            "id": a["id"],
            "nome": a["nome"],
            "idade": a["idade"],
            "nivel": a["nivel_conhecimento"],
            "estilo": a["estilo_aprendizado"],
        }
        for a in perfis
    ]


def formatar_perfil_para_prompt(aluno: dict) -> str:
    # Formata os dados do aluno em texto estruturado para ser injetado nos prompts.
    #Esta string será usada diretamente no context setting dos prompts.
    
    return f"""
PERFIL DO ALUNO:
- Nome: {aluno['nome']}
- Idade: {aluno['idade']} anos
- Série/Nível escolar: {aluno['serie']}
- Nível de conhecimento: {aluno['nivel_conhecimento']}
- Estilo de aprendizado preferido: {aluno['estilo_aprendizado']}
- Interesses pessoais: {', '.join(aluno['interesses'])}
- Dificuldades conhecidas: {', '.join(aluno['dificuldades'])}
- Observações pedagógicas: {aluno['observacoes']}
""".strip()


if __name__ == "__main__":
    # Teste rápido do módulo
    print("=== Perfis Disponíveis ===")
    for aluno in listar_alunos():
        print(f"  [{aluno['id']}] {aluno['nome']} | {aluno['idade']} anos | {aluno['nivel']} | {aluno['estilo']}")

    print("\n=== Exemplo de Perfil Formatado para Prompt ===")
    aluno = buscar_aluno_por_id("aluno_01")
    print(formatar_perfil_para_prompt(aluno))