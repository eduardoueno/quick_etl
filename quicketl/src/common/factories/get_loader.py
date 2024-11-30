import os
from quicketl.src.common.constants import ContractType, InternalMode
from quicketl.src.common.context import QuickContext
from quicketl.src.common.loaders.local_loader import LocalLoader
from quicketl.src.common.utils import get_src_path


def get_loader(ctx: QuickContext, contract_type: ContractType):

    internal_mode = ctx.args.INTERNAL_MODE

    if internal_mode == InternalMode.TEST_1:
        paths = {
            ContractType.CONFIG: os.path.join(
                get_src_path(), "mocks", "test_1", "config"
            ),
            ContractType.PROCESSING: os.path.join(
                get_src_path(), "mocks", "test_1", "processing"
            ),
            ContractType.INPUT: os.path.join(
                get_src_path(), "mocks", "test_1", "input"
            ),
            ContractType.OUTPUT: os.path.join(
                get_src_path(), "mocks", "test_1", "output"
            ),
        }

        return LocalLoader(file_path=paths[contract_type])

    raise
