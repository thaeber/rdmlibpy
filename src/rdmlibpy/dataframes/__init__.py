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
    DataFrameToXArray,
)

register(DataFrameAttributes())
register(DataFrameFileCache())
register(DataFrameFillNA())
register(DataFrameInterpolate())
register(DataFrameJoin())
register(DataFrameReadCSV())
register(DataFrameSetIndex())
register(DataFrameTimeOffset())
register(DataFrameToXArray())
register(DataFrameUnits())
register(DataFrameWriteCSV())
register(SelectColumns())
register(SelectTimespan())
