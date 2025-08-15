from ..registry import register
from .io import XArrayFileCache
from .xarray_selection import XArraySelectTimespan, XArraySelectRange
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
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArrayUnits())
