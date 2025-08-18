from ..registry import register
from .xarray_io import XArrayFileCache
from .xarray_selection import (
    XArraySelectIndexRange,
    XArraySelectRange,
    XArraySelectTimespan,
    XArraySelectVariable,
)
from .xarray_transforms import (
    XArrayAffineTransform,
    XArrayAssign,
    XArrayAttributes,
    XArrayCreateDataTree,
    XArrayMerge,
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
register(XArraySelectTimespan())
register(XArraySelectVariable())
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArraySwapDims())
register(XArrayUnits())
register(XArrayUnitsDequantify())
