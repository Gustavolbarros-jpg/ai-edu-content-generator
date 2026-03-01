import json
import os
from src.generator import gerar

ALUNOS = ["aluno_01", "aluno_02", "aluno_03", "aluno_04", "aluno_05"]
TIPOS = ["explicacao_conceitual", "exemplos_praticos", "perguntas_reflexao", "resumo_visual"]
VERSOES = ["v1", "v2"]
TOPICO = "fotossíntese"

resultados = []

for aluno_id in ALUNOS:
    for tipo in TIPOS:
        for versao in VERSOES:
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

# Salva tudo em samples/
os.makedirs("samples", exist_ok=True)
caminho = "samples/all_results.json"
with open(caminho, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Concluído! {len(resultados)} gerações salvas em {caminho}")