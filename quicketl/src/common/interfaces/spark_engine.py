from abc import ABC
from typing import List


class SparkEngine(ABC):

    def read_table(self):
        pass

    def write_table(self):
        pass

    def show_partitions(self) -> List[str]:

        return [
            "ano=2024/mes=1/dia=1",
            "ano=2024/mes=2/dia=1",
            "ano=2024/mes=3/dia=1",
            "ano=2024/mes=4/dia=1",
        ]
