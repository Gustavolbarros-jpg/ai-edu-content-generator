"""
src/schemas.py
Validação de schema dos outputs da API usando Pydantic.
"""

from pydantic import BaseModel, field_validator
from typing import Optional


class ExplicacaoConceitual(BaseModel):
    tipo: str
    versao_prompt: str
    titulo: str
    conteudo: str
    conceitos_chave: Optional[list] = None
    analogia_utilizada: Optional[str] = None
    nivel_adequado: Optional[bool] = None

    @field_validator("tipo")
    def tipo_deve_ser_correto(cls, v):
        assert v == "explicacao_conceitual", "tipo inválido"
        return v


class ExemploItem(BaseModel):
    titulo: str
    descricao: str
    nivel: Optional[str] = None
    conexao_com_aluno: Optional[str] = None


class ExemplosPraticos(BaseModel):
    tipo: str
    versao_prompt: str
    exemplos: list[ExemploItem]
    estilo_aplicado: Optional[str] = None

    @field_validator("tipo")
    def tipo_deve_ser_correto(cls, v):
        assert v == "exemplos_praticos", "tipo inválido"
        return v


class PerguntaItem(BaseModel):
    pergunta: str
    numero: Optional[int] = None
    nivel_cognitivo: Optional[str] = None
    objetivo_pedagogico: Optional[str] = None


class PerguntasReflexao(BaseModel):
    tipo: str
    versao_prompt: str
    perguntas: list

    @field_validator("tipo")
    def tipo_deve_ser_correto(cls, v):
        assert v == "perguntas_reflexao", "tipo inválido"
        return v


class ResumoVisual(BaseModel):
    tipo: str
    versao_prompt: str
    mapa_ascii: str
    descricao: Optional[str] = None
    legenda: Optional[str] = None
    dica_de_uso: Optional[str] = None
    estilo_aplicado: Optional[str] = None

    @field_validator("tipo")
    def tipo_deve_ser_correto(cls, v):
        assert v == "resumo_visual", "tipo inválido"
        return v


SCHEMAS = {
    "explicacao_conceitual": ExplicacaoConceitual,
    "exemplos_praticos": ExemplosPraticos,
    "perguntas_reflexao": PerguntasReflexao,
    "resumo_visual": ResumoVisual,
}


def validar(tipo: str, conteudo: dict) -> dict:
    """Valida o conteúdo contra o schema do tipo. Retorna o dict validado."""
    schema = SCHEMAS.get(tipo)
    if not schema:
        raise ValueError(f"Schema não encontrado para tipo: {tipo}")
    validado = schema(**conteudo)
    return validado.model_dump(exclude_none=False)