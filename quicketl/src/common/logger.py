import logging
from typing import Any, Optional


class Logger:

    def __init__(self, name: Optional[str] = "logger"):
        self.logger = logging.getLogger(name)

    def info(self, msg: Any):
        self.logger.info(msg)
        

