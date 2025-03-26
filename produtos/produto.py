from pydantic import BaseModel, field_validator
from typing import Optional

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    estoque: int

    @field_validator('id')
    def validar_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('O id do produto não pode ser negativo ou zero.')
        return v

    @field_validator('nome')
    def validar_nome(cls, v):
        if not v.strip():
            raise ValueError('O nome do produto não pode ser vazio.')
        if len(v) > 100:
            raise ValueError('O nome do produto não pode exceder 100 caracteres.')
        return v

    @field_validator('preco')
    def validar_preco(cls, v):
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero.')
        return v

    @field_validator('estoque')
    def validar_estoque(cls, v):
        if v < 0:
            raise ValueError('O estoque não pode ser negativo.')
        return v