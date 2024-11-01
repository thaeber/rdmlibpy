# set package version
__version__ = '0.1.12'

import pint_pandas
import pint

from . import dataframes, loaders, metadata, serializers
from .process import DelegatedSource
from .registry import register
from .workflow import Workflow, run

# set default (short) format for saving/loading units
# pint.application_registry.get().formatter.default_format = "P~"

__all__ = [
    dataframes,
    loaders,
    metadata,
    serializers,
    DelegatedSource,
    register,
    Workflow,
    run,
]  # type: ignore
