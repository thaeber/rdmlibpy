from pathlib import Path
from typing import Any, ClassVar

from rdmlibpy.base import ProcessBase, ProcessNode
from rdmlibpy.process import Cache, Loader, Writer, DelegatedSource


class TestProcessBase:
    def test_get_config(self):
        class TestProcess(ProcessBase):
            name: str = 'test'
            version: str = '1'
            test_param: str = 'test'
            test_number: int = 1

            def run(self, source: str, **params: Any) -> Any:
                return source

        process = TestProcess(test_param='test')
        config = process.get_config()

        assert config == {'test_param': 'test', 'test_number': 1}
        assert process.name == 'test'
        assert process.version == '1'
