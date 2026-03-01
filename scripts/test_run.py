from src.generator import gerar
import json


tipos = [
    "explicacao_conceitual",
    "exemplos_praticos", 
    "perguntas_reflexao",
    "resumo_visual"
]

for tipo in tipos:
    print(f"\n{'='*50}")
    print(f"GERANDO: {tipo}")
    print("="*50)
    resultado = gerar(
        aluno_id="aluno_05",
        topico="fotossíntese",
        tipo=tipo,
        versao="v2"
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2))