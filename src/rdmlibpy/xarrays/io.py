import logging
from pathlib import Path
from typing import Dict, List, Literal

import pint_xarray
from rdmlibpy.metadata.flattery import flatten, rebuild
import xarray as xr

from .._typing import FilePath
from ..process import Cache

logger = logging.getLogger(__name__)

ParseDatesType = None | List[str] | Dict[str, List[str]]

_ = pint_xarray.unit_registry


class XArrayFileCache(Cache):
    name: str = 'xarray.cache'
    version: str = '1'

    flatten_attributes: bool = True
    flatten_separator: str = ':::'
    chunks: None | str = None
    read_method: Literal['load', 'open'] = 'load'

    def read(self, filename: FilePath, rebuild: bool = False, **kwargs):
        # load data from netCDF4 file
        # cached = xr.load_dataset(filename, engine='netcdf4')
        if self.read_method == 'load':
            cached = xr.load_dataset(filename, engine='h5netcdf', chunks=self.chunks)
        else:
            cached = xr.open_dataset(filename, engine='h5netcdf', chunks=self.chunks)

        # rebuild nested dicts in attrs
        if self.flatten_attributes:
            cached = self._rebuild_attributes(cached)

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

        # flatten nested dicts in attrs
        if self.flatten_attributes:
            ds = self._flatten_attributes(ds)

        # create path (if necessary)
        self.ensure_path(filename)

        # write data to netCDF4 file
        # ds.to_netcdf(filename, format='NETCDF4', engine='netcdf4')
        ds.to_netcdf(filename, engine='h5netcdf')

    def cache_is_valid(self, filename: FilePath, rebuild: bool = False):
        if rebuild:
            return False
        return Path(filename).exists()

    def _flatten_attributes(self, source: xr.Dataset):
        def update(left, right):
            left.attrs.clear()
            left.attrs.update(**flatten(right.attrs, sep=self.flatten_separator))

        ds = source.copy()
        update(ds, source)
        for name in ds.data_vars:
            update(ds[name], source[name])
        for name in ds.coords:
            update(ds[name], source[name])

        return ds

    def _rebuild_attributes(self, source: xr.Dataset):
        def update(left, right):
            left.attrs.clear()
            left.attrs.update(**rebuild(right.attrs, sep=self.flatten_separator))

        ds = source.copy()
        update(ds, source)
        for name in ds.data_vars:
            update(ds[name], source[name])
        for name in ds.coords:
            update(ds[name], source[name])

        return ds
