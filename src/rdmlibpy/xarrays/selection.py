import numpy as np
import xarray as xr

from ..process import Transform


def parse(time):
    return np.datetime64(time)


class XArraySelectTimespan(Transform):
    name: str = 'xarray.select.timespan'
    version: str = '1'

    drop: bool = True  # drop non-matching data from xarray

    def run(
        self, source: xr.DataArray | xr.Dataset, column: str, start=None, stop=None
    ):
        col = source[column]
        if (start is not None) and (stop is not None):
            start = parse(start)
            stop = parse(stop)
            selector = (start <= col) & (col <= stop)
        elif start is None:
            stop = parse(stop)
            selector = col <= stop
        elif stop is None:
            start = parse(start)
            selector = start <= col
        else:
            return source

        return source.where(selector, drop=self.drop)
