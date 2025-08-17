from typing import Any, Dict


from ...dataframes.dataframes_io import DataFrameReadCSVBase, ParseDatesType


class ChannelEurothermLoggerLoader(DataFrameReadCSVBase):
    name: str = 'channel.eurotherm'
    version: str = '1'

    decimal: str = '.'
    separator: str = ';'
    parse_dates: ParseDatesType = ['timestamp']
    date_format: str = 'ISO8601'
    options: Dict[str, Any] = dict(
        names=['timestamp', 'temperature'],
    )


class ChannelEurothermLoggerLoaderV1_1(DataFrameReadCSVBase):
    name: str = 'channel.eurotherm'
    version: str = '1.1'

    decimal: str = '.'
    separator: str = ';'
    parse_dates: ParseDatesType = ['timestamp']
    date_format: str = 'ISO8601'
    options: Dict[str, Any] = dict(
        header='infer',
        # names=['timestamp', 'temperature', 'power'],
    )
