from typing import List
from pydantic import BaseModel, Field


class DesenhoItem(BaseModel):
    numero_figura: str = Field(..., description="Número da figura (ex: '1', '2')")
    descricao_breve: str = Field(..., description="Breve descrição da figura")


class RelatorioDescritivoPI(BaseModel):
    titulo: str = Field(..., description="Título da invenção")
    campo_da_invencao: str = Field(..., description="Campo técnico da invenção")
    estado_da_tecnica: str = Field(..., description="Estado da técnica / fundamentos da invenção")
    problema_e_vantagens: str = Field(..., description="Problema técnico resolvido e vantagens")
    desenhos: List[DesenhoItem] = Field(
        default_factory=list, description="Lista de figuras/desenhos"
    )
    paragrafos_descricao: List[str] = Field(
        default_factory=list, description="Parágrafos com a descrição detalhada"
    )
    exemplos_concretizacao: str = Field(
        ..., description="Exemplos de concretização da invenção"
    )
