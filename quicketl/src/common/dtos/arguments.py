import os

from typing import Optional
from pydantic import BaseModel, Field, StrictStr

from quicketl.src.common.constants import InternalMode


class Args(BaseModel):

    PATH: Optional[StrictStr] = Field(default=None)
    BUCKET_NAME: Optional[StrictStr] = Field(default=None)
    JOB_NAME: Optional[StrictStr] = Field(default=None)
    INTERNAL_MODE: InternalMode
