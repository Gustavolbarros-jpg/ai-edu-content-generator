"""
cli.py
Interface de linha de comando para a plataforma educacional.
"""

import json
import os
from src.generator import gerar, comparar
from src.students import carregar_perfis
from src.cache import limpar, info
from src.history import listar

def menu_principal():
    print("\n" + "="*50)
    print("  PLATAFORMA DE CONTEÚDO EDUCACIONAL")
    print("="*50)
    print("1. Gerar conteúdo para um aluno")
    print("2. Comparar v1 vs v2")
    print("3. Ver histórico")
    print("4. Info do cache")
    print("5. Limpar cache")
    print("0. Sair")
    return input("\nEscolha: ").strip()

def selecionar_aluno():
    perfis = carregar_perfis()
    print("\n--- ALUNOS ---")
    for i, p in enumerate(perfis, 1):
        print(f"  {i}. {p['nome']} ({p['idade']} anos, {p['nivel_conhecimento']})")
    idx = int(input("\nEscolha (1-5): ").strip()) - 1
    return perfis[idx]["id"]

def selecionar_tipo():
    tipos = [
        "explicacao_conceitual",
        "exemplos_praticos",
        "perguntas_reflexao",
        "resumo_visual"
    ]
    print("\n--- TIPO DE CONTEÚDO ---")
    for i, t in enumerate(tipos, 1):
        print(f"  {i}. {t}")
    idx = int(input("\nEscolha (1-4): ").strip()) - 1
    return tipos[idx]

def selecionar_versao():
    print("\n--- VERSÃO DO PROMPT ---")
    print("  1. v1 (básico)")
    print("  2. v2 (otimizado)")
    escolha = input("\nEscolha (1-2): ").strip()
    return "v1" if escolha == "1" else "v2"

def main():
    while True:
        opcao = menu_principal()

        if opcao == "0":
            print("\nAté logo!")
            break

        elif opcao == "1":
            try:
                aluno_id = selecionar_aluno()
                topico = input("\nTópico: ").strip()
                tipo = selecionar_tipo()
                versao = selecionar_versao()

                print(f"\n[GERANDO] {tipo} · {versao} · {aluno_id}...")
                resultado = gerar(aluno_id, topico, tipo, versao)
                print("\n" + json.dumps(resultado, ensure_ascii=False, indent=2))

            except Exception as e:
                print(f"\n[ERRO] {e}")

        elif opcao == "2":
            try:
                aluno_id = selecionar_aluno()
                topico = input("\nTópico: ").strip()
                tipo = selecionar_tipo()

                print(f"\n[COMPARANDO] {tipo} · {aluno_id}...")
                resultado = comparar(aluno_id, topico, tipo)
                print("\n=== V1 ===")
                print(json.dumps(resultado["comparacao"]["v1"], ensure_ascii=False, indent=2))
                print("\n=== V2 ===")
                print(json.dumps(resultado["comparacao"]["v2"], ensure_ascii=False, indent=2))

            except Exception as e:
                print(f"\n[ERRO] {e}")

        elif opcao == "3":
            historico = listar()
            if not historico:
                print("\nNenhuma geração registrada.")
            else:
                print(f"\n{len(historico)} geração(ões):")
                for h in historico[-5:]:
                    print(f"  {h['id']} | {h['aluno_id']} | {h['tipo']} | {h['versao_prompt']} | {h['gerado_em'][:19]}")

        elif opcao == "4":
            print(f"\n{info()}")

        elif opcao == "5":
            limpar()

if __name__ == "__main__":
    main()