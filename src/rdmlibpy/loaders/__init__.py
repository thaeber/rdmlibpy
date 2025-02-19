from ..registry import register
from .bruker_opus import BrukerOpusLoader
from .channel.eurotherm import (
    ChannelEurothermLoggerLoader,
    ChannelEurothermLoggerLoaderV1_1,
)
from .channel.tclogger import ChannelTCLoggerLoader
from .hiden_rga import HidenRGALoader
from .mks_ftir import MksFTIRLoader
from .davis import DavisImageSetLoader

register(BrukerOpusLoader())
register(ChannelEurothermLoggerLoader())
register(ChannelEurothermLoggerLoaderV1_1())
register(ChannelTCLoggerLoader())
register(HidenRGALoader())
register(MksFTIRLoader())
register(DavisImageSetLoader())
