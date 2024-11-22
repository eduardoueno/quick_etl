from typing import List, Optional
from pydantic import StrictStr
from quicketl.src.common.dtos.contracts.column import (
    CategoricColumn,
    Column,
    DateColumn,
)
from quicketl.src.common.dtos.contracts.contract import Contract


class Output(Contract):

    defasagem: StrictStr
    intervalo_tempo: StrictStr
    colunas: List[Column]
    colunas_particao_data: List[DateColumn]
    colunas_particao_categorica: Optional[List[CategoricColumn]]
