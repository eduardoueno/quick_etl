from typing import List
from pydantic import BaseModel, StrictStr

from quicketl.src.common.dtos.contracts.column import Column


class Contract(BaseModel):

    id: StrictStr
    data_atualizacao: StrictStr
    data_criacao: StrictStr


class TimeTravelContract(Contract):
    defasagem: StrictStr
    intervalo_tempo: StrictStr
    colunas_particao_data: List[Column]
