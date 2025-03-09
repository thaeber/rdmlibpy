from __future__ import annotations

from collections import deque
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, cast

from . import base
from .registry import get_runner
from .metadata import MetadataNode, Metadata

PlainProcessDescriptorType = str | base.ProcessBase
PlainProcessWithParamsDescriptorType = Tuple[PlainProcessDescriptorType, Dict[str, Any]]
ProcessDescriptorType = (
    Mapping[str, Any]
    | MetadataNode
    | PlainProcessWithParamsDescriptorType
    | PlainProcessDescriptorType
)
WorkflowDescriptorType = ProcessDescriptorType | Sequence['WorkflowDescriptorType']


def run(workflow: WorkflowDescriptorType):
    return Workflow.create(workflow).run()


class Workflow:
    def __init__(self, process: base.ProcessNode):
        self.process = process

    def run(self, **kwargs):
        return self.process.run(**kwargs)

    @staticmethod
    def create(descriptor: WorkflowDescriptorType):
        if isinstance(descriptor, MetadataNode):
            descriptor = cast(dict, Metadata.to_container(descriptor))
        return Workflow(Workflow._create(None, descriptor))

    @staticmethod
    def _create(
        parent: Optional[base.ProcessNode], descriptor: WorkflowDescriptorType
    ) -> base.ProcessNode:
        match descriptor:
            case base.ProcessBase() as process:
                return base.ProcessNode(parent=parent, runner=process)
            case str() as process_name:
                process = get_runner(process_name)
                return base.ProcessNode(parent=parent, runner=process)
            case (base.ProcessBase() as process, dict() as params):
                return base.ProcessNode(
                    parent=parent,
                    runner=process,
                    params=Workflow._create_params(**params),
                )
            case (str() as process_name, dict() as params):
                process = get_runner(process_name)
                return base.ProcessNode(
                    parent=parent,
                    runner=process,
                    params=Workflow._create_params(**params),
                )
            case {**mapping}:
                return Workflow._create_process_from_mapping(parent, mapping)
            case [*sequence]:
                return Workflow._create_sequence(parent, sequence)
            case _:
                raise ValueError(
                    'The workflow descriptor must be either a mapping,'
                    ' a process instance, process name (with version)'
                    + ' or a sequence of these.'
                )

    @staticmethod
    def _create_params(**kwargs) -> Dict[str, base.ProcessParam]:
        params = {}
        for key, value in kwargs.items():
            if key.startswith('$'):
                # value itself is a process
                params[key[1:]] = base.RunnableProcessParam(
                    node=Workflow.create(value).process
                )
            else:
                params[key] = base.PlainProcessParam(value=value)
        return params

    @staticmethod
    def _create_process_from_mapping(
        parent: Optional[base.ProcessNode], process: Mapping[str, Any]
    ) -> base.ProcessNode:
        # create a single process node from the descriptor (mapping)
        RUN_KEY = 'run'
        PROCESS_KEY = '__process__'
        CONFIG_KEY = 'config'
        PARAMS_KEY = 'params'

        # check if the process contains a `run` or `__process__` element
        if RUN_KEY not in process:
            if PROCESS_KEY in process:
                return Workflow._create(parent, process[PROCESS_KEY])
            raise ValueError(
                'The process parameters do not contain a `run` element.\n'
                + '\n'.join([f'{key}: {value}' for key, value in process.items()])
            )

        # get runner
        runner = get_runner(process[RUN_KEY], **process.get(CONFIG_KEY, dict()))

        # get keyword arguments (anything except reserved keys)
        params = {}
        if PARAMS_KEY in process:
            params = Workflow._create_params(**process[PARAMS_KEY])

        # invoke process
        return base.ProcessNode(parent=parent, runner=runner, params=params)

    @staticmethod
    def _create_sequence(
        parent: Optional[base.ProcessNode], sequence: Sequence[WorkflowDescriptorType]
    ) -> base.ProcessNode:
        # create the process sequence and return the last process in the chain
        # (each process holds a reference to the previous/parent process in the chain)
        if not sequence:
            raise ValueError('The process sequence contains no elements.')

        seq = deque(sequence)
        process = Workflow._create(parent, seq.popleft())
        while seq:
            process = Workflow._create(process, seq.popleft())
        return process
