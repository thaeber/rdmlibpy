from ..registry import register
from .io import XArrayFileCache
from .selection import XArraySelectTimespan
from .transforms import XArrayAttributes, XArrayUnits

register(XArrayFileCache())
register(XArraySelectTimespan())
register(XArrayAttributes())
register(XArrayUnits())
