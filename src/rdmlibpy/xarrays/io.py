import logging
from pathlib import Path
from typing import Dict, List

import netCDF4
import numpy as np
import pint_xarray
import xarray as xr

from .._typing import FilePath
from ..process import Cache

logger = logging.getLogger(__name__)

ParseDatesType = None | List[str] | Dict[str, List[str]]

_ = pint_xarray.unit_registry


class XArrayFileCache(Cache):
    name: str = 'xarray.cache'
    version: str = '1'

    def read(self, filename: FilePath, rebuild: bool = False, **kwargs):
        # load data from netCDF4 file
        # cached = xr.load_dataset(filename, engine='netcdf4')
        cached = xr.load_dataset(filename, engine='h5netcdf')

        # convert to pint units, if present
        cached = cached.pint.quantify()

        # check if data was actually a DataArray
        if name := cached.attrs.get('xarray:name', None):
            da = cached[name]

            unnamed = bool(cached.attrs.get('xarray:unnamed', False))
            if unnamed:
                da.name = None

            # return cached DataArray
            return da
        else:
            # return cached Dataset
            return cached

    def write(
        self,
        source: xr.Dataset | xr.DataArray,
        filename: FilePath,
        rebuild: bool = False,
        **kwargs,
    ):
        # convert DataArray to Dataset
        if isinstance(source, xr.DataArray):
            unnamed = source.name is None
            if unnamed:
                name = 'unnamed'
            else:
                name = source.name
            ds = source.to_dataset(name=name)
            ds.attrs['xarray:unnamed'] = 1 if unnamed else 0
            ds.attrs['xarray:name'] = name
        else:
            ds = source
        assert isinstance(ds, xr.Dataset)

        # promote units to attributes
        ds = ds.pint.dequantify()

        # create path (if necessary)
        self.ensure_path(filename)

        # write data to netCDF4 file
        # ds.to_netcdf(filename, format='NETCDF4', engine='netcdf4')
        ds.to_netcdf(filename, engine='h5netcdf')

    def cache_is_valid(self, filename: FilePath, rebuild: bool = False):
        if rebuild:
            return False
        return Path(filename).exists()


# def dequantify(df: pd.DataFrame):
#     df_new = df.pint.dequantify()
#     df_new = cast(pd.DataFrame, df_new)

#     # preserve attrs dictionary
#     df_new.attrs.update(df.attrs)

#     return df_new


# def quantify(df, level=-1):
#     # Fix for https://github.com/hgrecco/pint-pandas/pull/217
#     # (remove once that fix is rolled out in the next release of
#     # pint-pandas)
#     df_columns = df.columns.to_frame()
#     unit_col_name = df_columns.columns[level]
#     units = df_columns[unit_col_name]
#     df_columns = df_columns.drop(columns=unit_col_name)

#     df_new = pd.DataFrame(
#         {
#             i: (
#                 pint_pandas.PintArray(df.iloc[:, i], unit)
#                 if unit != pint_pandas.pint_array.NO_UNIT
#                 else df.iloc[:, i]
#             )
#             for i, unit in enumerate(units.values)
#         }
#     )

#     df_new.columns = df_columns.index.droplevel(unit_col_name)
#     df_new.index = df.index

#     # preserve attrs dictionary
#     df_new.attrs.update(df.attrs)

#     return df_new
