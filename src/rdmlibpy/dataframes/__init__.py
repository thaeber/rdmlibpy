from ..registry import register
from .dataframes_io import DataFrameFileCache, DataFrameReadCSV, DataFrameWriteCSV
from .dataframes_selection import SelectColumns, SelectTimespan
from .dataframe_transforms import (
    DataFrameAttributes,
    DataFrameFillNA,
    DataFrameInterpolate,
    DataFrameJoin,
    DataFrameSetIndex,
    DataFrameTimeOffset,
    DataFrameUnits,
)

register(DataFrameReadCSV())
register(DataFrameWriteCSV())
register(DataFrameFileCache())

register(DataFrameAttributes())
register(DataFrameFillNA())
register(DataFrameInterpolate())
register(DataFrameJoin())
register(DataFrameSetIndex())
register(DataFrameTimeOffset())
register(DataFrameUnits())

register(SelectColumns())
register(SelectTimespan())
