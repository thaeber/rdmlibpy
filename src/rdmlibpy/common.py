from typing import Any

from .base import ProcessBase
from .registry import register


class ScalarSource(ProcessBase):
    name: str = 'scalar.source'
    version: str = '1'
    value: Any = None

    def run(self, value: Any = None):
        if value is not None:
            return value
        else:
            return self.value


register(ScalarSource())
