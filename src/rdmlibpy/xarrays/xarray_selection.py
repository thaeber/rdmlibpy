import numpy as np
import xarray as xr

from ..process import Transform
from .xarray_utils import KeepAttributesContext


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

        with KeepAttributesContext():
            return source.where(selector, drop=self.drop)


class XArraySelectTimespanV1_1(XArraySelectTimespan):
    version: str = '1.1'

    def run(
        self, source: xr.DataArray | xr.Dataset, variable: str, start=None, stop=None
    ):
        return super().run(source, variable, start, stop)


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

        with KeepAttributesContext():
            if isinstance(source, xr.DataArray):
                return source.where(selector, drop=self.drop)
            elif isinstance(source, xr.Dataset):

                def select(da: xr.DataArray):
                    if set(selector.dims).issubset(da.dims):
                        return da.where(selector, drop=self.drop)
                    else:
                        return da

                return source.map(select, keep_attrs=True)
            else:
                raise TypeError("Source must be an xarray DataArray or Dataset.")


class XArraySelectRangeV1_1(XArraySelectRange):
    version: str = '1.1'

    def run(
        self, source: xr.DataArray | xr.Dataset, variable: str, start=None, stop=None
    ):
        return super().run(source, variable, start, stop)


class XArraySelectIndexRange(Transform):
    name: str = 'xarray.select.index_range'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, dim: str, start=None, stop=None):
        source[dim]
        if (start is not None) and (stop is not None):
            selector = slice(start, stop)
        elif (start is None) and (stop is not None):
            selector = slice(None, stop)
        elif (start is not None) and (stop is None):
            selector = slice(start, None)
        else:
            return source

        with KeepAttributesContext():
            return source.isel({dim: selector})


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


class XArraySelectStrContains(Transform):
    name: str = 'xarray.select.str.contains'
    version: str = '1'

    regex: bool = True
    ignore_case: bool = False

    def run(self, source: xr.DataArray | xr.Dataset, variable: str, pattern: str):
        if isinstance(source, xr.DataArray):
            col = source
        else:
            if variable not in source:
                raise ValueError(f"Variable '{variable}' not found in source.")
            col = source[variable]

        selector = col.str.contains(
            pattern,
            regex=self.regex,
            case=not self.ignore_case,
        )

        with KeepAttributesContext():
            result = source.where(selector, drop=True)

            # coerce variable types if the differ between source and result
            if isinstance(source, xr.Dataset):
                for var in source.data_vars:
                    if var in result.data_vars:
                        result[var] = result[var].astype(source[var].dtype)
            elif isinstance(source, xr.DataArray):
                result = result.astype(source.dtype)

            return result
