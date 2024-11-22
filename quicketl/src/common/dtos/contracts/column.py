from typing import Optional
from pydantic import BaseModel, StrictStr

from quicketl.src.common.constants import SparkType


class Column(BaseModel):
    nome: StrictStr
    descricao: Optional[StrictStr]
    tipo: Optional[SparkType]
    formato: Optional[StrictStr]


class CategoricColumn(BaseModel):
    nome: StrictStr
    descricao: Optional[StrictStr]
    tipo: Optional[SparkType]
    formato: Optional[StrictStr]
    filtro: StrictStr


class DateColumn(BaseModel):
    nome: StrictStr
    descricao: Optional[StrictStr]
    tipo: Optional[SparkType]
    formato: StrictStr
