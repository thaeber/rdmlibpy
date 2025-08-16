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


class XArraySelectRange(Transform):
    name: str = 'xarray.select.range'
    version: str = '1'

    drop: bool = True  # drop non-matching data from xarray

    def run(self, source: xr.DataArray | xr.Dataset, dim: str, start=None, stop=None):
        values = source[dim]
        if (start is not None) and (stop is not None):
            selector = (start <= values) & (values <= stop)
        elif (start is None) and (stop is not None):
            selector = values <= stop
        elif (start is not None) and (stop is None):
            selector = start <= values
        else:
            return source

        if isinstance(source, xr.DataArray):
            return source.where(selector, drop=self.drop)
        elif isinstance(source, xr.Dataset):

            def select(da: xr.DataArray):
                if set(selector.dims).issubset(da.dims):
                    return da.where(selector, drop=self.drop)
                else:
                    return da

            return source.map(select)
        else:
            raise TypeError("Source must be an xarray DataArray or Dataset.")


class XArraySelectVariable(Transform):
    name: str = 'xarray.select.variable'
    version: str = '1'

    keep_parent_attributes: bool = False  # keep attributes from the parent dataset

    def run(self, source: xr.Dataset, variable: str):
        if variable in source.data_vars:
            result = source[variable]
            if self.keep_parent_attributes:
                result.attrs.update(source.attrs)
            return result
        else:
            raise ValueError(f"Variable '{variable}' not found in source.")
