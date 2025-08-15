from ..registry import register
from .io import XArrayFileCache
from .selection import XArraySelectTimespan
from .xarray_transforms import (
    XArrayAttributes,
    XArraySqueeze,
    XArrayStatisticsMean,
    XArrayUnits,
)

register(XArrayAttributes())
register(XArrayFileCache())
register(XArraySelectTimespan())
register(XArraySqueeze())
register(XArrayStatisticsMean())
register(XArrayUnits())
