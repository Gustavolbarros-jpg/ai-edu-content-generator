import json
import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import gerar

ALUNOS = ["aluno_01", "aluno_02", "aluno_03", "aluno_04", "aluno_05"]
TIPOS = ["explicacao_conceitual", "exemplos_praticos", "perguntas_reflexao", "resumo_visual"]
VERSOES = ["v1", "v2"]
TOPICO = "fotossíntese"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE_DIR, "samples"), exist_ok=True)
caminho = os.path.join(BASE_DIR, "samples", "all_results.json")

# Carrega resultados anteriores se existirem
if os.path.exists(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        resultados = json.load(f)
    print(f"Retomando — {len(resultados)} resultados já existem")
else:
    resultados = []

# Cria set de combinações já feitas para não repetir
feitos = {
    (r["aluno_id"], r["tipo"], r["versao"])
    for r in resultados
    if r["status"] == "ok"
}

for aluno_id in ALUNOS:
    for tipo in TIPOS:
        for versao in VERSOES:
            if (aluno_id, tipo, versao) in feitos:
                print(f"[SKIP] {aluno_id} · {tipo} · {versao} — já gerado")
                continue

            print(f"\n[GERANDO] {aluno_id} · {tipo} · {versao}")
            try:
                conteudo = gerar(
                    aluno_id=aluno_id,
                    topico=TOPICO,
                    tipo=tipo,
                    versao=versao
                )
                resultados.append({
                    "aluno_id": aluno_id,
                    "topico": TOPICO,
                    "tipo": tipo,
                    "versao": versao,
                    "status": "ok",
                    "conteudo": conteudo
                })
            except Exception as e:
                print(f"[ERRO] {e}")
                resultados.append({
                    "aluno_id": aluno_id,
                    "topico": TOPICO,
                    "tipo": tipo,
                    "versao": versao,
                    "status": "erro",
                    "erro": str(e)
                })

            # Salva após cada geração
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Concluído! {len(resultados)} gerações salvas em {caminho}")