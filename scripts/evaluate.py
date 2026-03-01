"""
scripts/evaluate.py
Roda o LLM-as-a-Judge para todos os tipos de conteúdo de um aluno.
Compara v1 vs v2 e salva o resultado em samples/evaluation.json
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import avaliar
from src.generator import gerar
from src.students import buscar_aluno_por_id

ALUNO_ID = "aluno_01"
TOPICO = "fotossíntese"
TIPOS = [
    "explicacao_conceitual",
    "exemplos_praticos",
    "perguntas_reflexao",
    "resumo_visual"
]

def main():
    aluno = buscar_aluno_por_id(ALUNO_ID)
    resultados = []

    for tipo in TIPOS:
        print(f"\nAvaliando: {tipo}...")
        try:
            v1 = gerar(ALUNO_ID, TOPICO, tipo, "v1")
            v2 = gerar(ALUNO_ID, TOPICO, tipo, "v2")
            avaliacao = avaliar(aluno, tipo, v1, v2)
            resultados.append({
                "aluno_id": ALUNO_ID,
                "topico": TOPICO,
                "tipo": tipo,
                "avaliacao": avaliacao
            })
            print(f"  v1: {avaliacao['v1']['media']} | v2: {avaliacao['v2']['media']} | vencedor: {avaliacao['vencedor']}")
        except Exception as e:
            print(f"  ERRO: {e}")

    os.makedirs("samples", exist_ok=True)
    with open("samples/evaluation.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"\nResultados salvos em samples/evaluation.json")

if __name__ == "__main__":
    main()