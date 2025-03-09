from __future__ import annotations

import abc
from typing import Any, Dict, Optional

import pydantic


class ProcessBase(pydantic.BaseModel, abc.ABC):
    name: str
    version: str

    def updated(self, **config):
        _config = self.model_dump(exclude_defaults=True)
        _config.update(config)
        return self.model_validate(_config)

    @abc.abstractmethod
    def run(self, source, **params) -> Any:
        pass

    def _run_with_node(self, node: ProcessNode, **kwargs):
        # resolve parameters;
        # each parameter, which itself represents an executable node, is
        # evaluated before the process of the current node instance is executed.
        # params = node.get_params()

        if node.parent is not None:
            # run parent process
            source = node.parent.run(**kwargs)

            # run process & return result
            params = node.get_params()
            return self.run(source, **params)
        else:
            params = node.get_params()
            params.update(**kwargs)
            return self.run(**params)

    def preprocess(self):
        return None

    @property
    def fullname(self):
        return f'{self.name}@v{self.version}'


class ProcessNode(pydantic.BaseModel):
    runner: ProcessBase
    parent: Optional[ProcessNode] = None
    params: Dict[str, ProcessParam] = {}

    @pydantic.field_validator('params', mode='before')
    @classmethod
    def validate_node_params(cls, params: dict) -> Dict[str, ProcessParam]:
        result: Dict[str, ProcessParam] = {}
        for key, value in params.items():
            if not isinstance(value, ProcessParam):
                result[key] = PlainProcessParam(value=value)
            else:
                result[key] = value
        return result

    def run(self, **kwargs):
        return self.runner._run_with_node(self, **kwargs)

    def get_param(self, key: str, default=None):
        if default is None:
            return self.params[key].get_value()
        else:
            if key in self.params:
                return self.params[key].get_value()
            else:
                return default

    def get_params(self):
        # resolve parameters;
        # Each parameter, which itself represents an executable node, is
        # evaluated before the process of the current node instance is executed.
        return {key: item.get_value() for key, item in self.params.items()}


class ProcessParam(pydantic.BaseModel, abc.ABC):
    @abc.abstractmethod
    def get_value(self):
        raise NotImplementedError()


class PlainProcessParam(ProcessParam):
    value: Any

    def get_value(self):
        return self.value


class RunnableProcessParam(ProcessParam):
    node: ProcessNode

    def get_value(self):
        return self.node.run()
