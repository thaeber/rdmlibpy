from pathlib import Path
from typing import Any, Optional

from omegaconf import OmegaConf

from .base import ProcessBase
from .registry import register
from .workflow import Workflow


class ScalarSource(ProcessBase):
    name: str = 'scalar.source'
    version: str = '1'
    value: Any = None

    def run(self, value: Any = None):
        if value is not None:
            return value
        else:
            return self.value


class IncludeMetadataFile(ProcessBase):
    name: str = 'include.metadata.file'
    version: str = '1'

    def run(self, source: str | Path, key: str | None = None):
        source = Path(source)
        conf = OmegaConf.load(source)
        OmegaConf.resolve(conf)

        if key is not None:
            conf = OmegaConf.select(conf, key)
            # conf = cast(DictConfig, conf)
        return Workflow.create(conf).run()


register(ScalarSource())
register(IncludeMetadataFile())
