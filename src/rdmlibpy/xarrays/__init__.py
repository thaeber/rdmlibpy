from ..registry import register
from .xarray_io import XArrayFileCache
from .xarray_selection import (
    XArraySelectIndexRange,
    XArraySelectRange,
    XArraySelectStrContains,
    XArraySelectTimespan,
    XArraySelectVariable,
)
from .xarray_transforms import (
    XArrayAffineTransform,
    XArrayAssign,
    XArrayAttributes,
    XArrayCreateDataTree,
    XArrayMerge,
    XArraySetCoords,
    XArraySqueeze,
    XArrayStatisticsMean,
    XArraySwapDims,
    XArrayUnits,
    XArrayUnitsDequantify,
)

register(XArrayAffineTransform())
register(XArrayAssign())
register(XArrayAttributes())
register(XArrayCreateDataTree())
register(XArrayFileCache())
register(XArrayMerge())
register(XArraySelectIndexRange())
register(XArraySelectRange())
register(XArraySelectStrContains())
register(XArraySelectTimespan())
register(XArraySelectVariable())
register(XArraySetCoords())
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArraySwapDims())
register(XArrayUnits())
register(XArrayUnitsDequantify())
