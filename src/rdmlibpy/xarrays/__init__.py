from ..registry import register
from .selection import XArraySelectTimespan
from .transforms import XArrayAttributes, XArrayUnits

register(XArraySelectTimespan())
register(XArrayAttributes())
register(XArrayUnits())
