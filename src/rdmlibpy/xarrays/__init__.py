from ..registry import register
from .xarray_io import XArrayFileCache
from .xarray_selection import (
    XArraySelectRange,
    XArraySelectTimespan,
    XArraySelectVariable,
)
from .xarray_transforms import (
    XArrayAffineTransform,
    XArrayAssign,
    XArrayAttributes,
    XArraySqueeze,
    XArrayStatisticsMean,
    XArraySwapDims,
    XArrayUnits,
)

register(XArrayAffineTransform())
register(XArrayAssign())
register(XArrayAttributes())
register(XArrayFileCache())
register(XArraySelectRange())
register(XArraySelectTimespan())
register(XArraySelectVariable())
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArraySwapDims())
register(XArrayUnits())
