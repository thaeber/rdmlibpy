from ..registry import register
from .xarray_io import XArrayFileCache
from .xarray_selection import (
    XArraySelectTimespan,
    XArraySelectRange,
    XArraySelectVariable,
)
from .xarray_transforms import (
    XArrayAffineTransform,
    XArrayAttributes,
    XArraySqueeze,
    XArrayStatisticsMean,
    XArrayUnits,
)

register(XArrayAffineTransform())
register(XArrayAttributes())
register(XArrayFileCache())
register(XArraySelectRange())
register(XArraySelectTimespan())
register(XArraySelectVariable())
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArrayUnits())
