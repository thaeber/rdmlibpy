import logging
from pathlib import Path
from typing import Dict, List, Literal

import numpy as np
import pint
import pint_xarray
import pydantic
from rdmlibpy.metadata.flattery import flatten, rebuild
import xarray as xr

from .._typing import FilePath
from ..process import Cache

logger = logging.getLogger(__name__)

ParseDatesType = None | List[str] | Dict[str, List[str]]

_ = pint_xarray.unit_registry


class TimeEncoding(pydantic.BaseModel):
    units: str = 'milliseconds since 1970-01-01 00:00:00'
    dtype: str = 'int64'
    calendar: Literal[
        'standard',
        'gregorian',
        'proleptic_gregorian',
        'noleap',
        '365_day',
        '360_day',
        'julian',
        'all_leap',
        '366_day',
    ] = 'proleptic_gregorian'


class XArrayFileCache(Cache):
    name: str = 'xarray.cache'
    version: str = '1'

    flatten_attributes: bool = True
    flatten_separator: str = ':::'
    chunks: None | str = None
    read_method: Literal['load', 'open'] = 'load'
    data_structure: Literal['Dataset', 'DataArray', 'DataTree'] = 'Dataset'
    time_encoding: TimeEncoding = TimeEncoding()

    def read(self, filename: FilePath, rebuild: bool = False, **kwargs):
        if self.data_structure == 'DataArray':
            return self._read_DataArray(filename, rebuild=rebuild, **kwargs)
        elif self.data_structure == 'Dataset':
            return self._read_Dataset(filename, rebuild=rebuild, **kwargs)
        elif self.data_structure == 'DataTree':
            return self._read_DataTree(filename, rebuild=rebuild, **kwargs)

    def _read_DataArray(self, filename: FilePath, rebuild: bool = False, **kwargs):
        cached = self._read_Dataset(filename, rebuild=rebuild, **kwargs)
        cached = self._post_process_dataset(cached)

        da = cached[list(cached.data_vars)[0]]
        if 'xarray:unnamed' in cached.attrs:
            da.name = None
        return da

    def _read_Dataset(self, filename: FilePath, rebuild: bool = False, **kwargs):
        # load data from netCDF4 file
        cached = xr.open_dataset(filename, engine='h5netcdf', chunks=self.chunks)
        if self.read_method == 'load':
            cached = cached.load()

        cached = self._post_process_dataset(cached)

        # return cached Dataset
        return cached

    def _read_DataTree(self, filename: FilePath, rebuild: bool = False, **kwargs):
        # load data from netCDF4 file
        cached = xr.open_datatree(filename, engine='h5netcdf', chunks=self.chunks)
        if self.read_method == 'load':
            cached = cached.load()

        cached = xr.map_over_datasets(self._post_process_dataset, cached)

        # return cached Dataset
        return cached

    def write(
        self,
        source: xr.Dataset | xr.DataArray | xr.DataTree,
        filename: FilePath,
        rebuild: bool = False,
        **kwargs,
    ):
        if self.data_structure == 'DataArray':
            if not isinstance(source, xr.DataArray):
                raise TypeError('`source` must be a DataArray')
            self._write_DataArray(source, filename, rebuild=rebuild, **kwargs)
        elif self.data_structure == 'Dataset':
            if not isinstance(source, xr.Dataset):
                raise TypeError('`source` must be a Dataset')
            self._write_Dataset(source, filename, rebuild=rebuild, **kwargs)
        elif self.data_structure == 'DataTree':
            if not isinstance(source, xr.DataTree):
                raise TypeError('`source` must be a DataTree')
            self._write_DataTree(source, filename, rebuild=rebuild, **kwargs)
        else:
            raise TypeError(
                '`data_structure` must be `Dataset`, `DataArray`, or `DataTree`'
            )

    def _write_DataArray(
        self,
        source: xr.DataArray,
        filename: FilePath,
        **kwargs,
    ):
        da = source

        if da.name is None:
            ds = da.to_dataset(name='unnamed')
            ds.attrs['xarray:unnamed'] = 1
        else:
            ds = da.to_dataset(name=da.name)

        self._write_Dataset(ds, filename, **kwargs)

    def _write_Dataset(
        self,
        source: xr.Dataset,
        filename: FilePath,
        **kwargs,
    ):
        ds = self._pre_process_dataset(source)

        # create path (if necessary)
        self.ensure_path(filename)

        # write data to netCDF4 file
        ds.to_netcdf(filename, engine='h5netcdf')

    def _write_DataTree(
        self,
        source: xr.DataTree,
        filename: FilePath,
        **kwargs,
    ):
        dt = xr.map_over_datasets(self._pre_process_dataset, source)

        # create path (if necessary)
        self.ensure_path(filename)

        # write data to netCDF4 file
        dt.to_netcdf(filename, engine='h5netcdf')

    def cache_is_valid(self, filename: FilePath, rebuild: bool = False, **kwargs):
        if rebuild:
            return False
        return Path(filename).exists()

    def _pre_process_dataset(self, ds: xr.Dataset):
        # check if dataset has any pint units or dimensions associated with it
        if any(
            [ds[key].pint.dimensionality is not None for key in list(ds.data_vars)]
            + [ds[key].pint.dimensionality is not None for key in list(ds.coords)]
            + [
                isinstance(ds[key].attrs.get('units', None), pint.Unit)
                for key in list(ds.coords)
            ]
        ):
            # promote units to attributes
            ds = ds.pint.dequantify()
            ds.attrs['pint:quantify'] = 1
        else:
            ds.attrs['pint:quantify'] = 0

        # flatten nested dicts in attrs
        if self.flatten_attributes:
            ds = self._flatten_attributes(ds)

        # in case of chunked arrays we need to specify the time
        # encoding, otherwise the time will be incorrectly stored
        names = list(ds.data_vars) + list(ds.coords)
        for name in names:
            if np.isdtype(ds[name].dtype, np.datetime64):
                ds[name].encoding.update(self.time_encoding.model_dump())

        return ds

    def _post_process_dataset(self, ds: xr.Dataset):
        # rebuild nested dicts in attrs
        if self.flatten_attributes:
            ds = self._rebuild_attributes(ds)

        # convert to pint units, if present
        if ds.attrs.get('pint:quantify', 0) == 1:
            ds = ds.pint.quantify()
            del ds.attrs['pint:quantify']

        return ds

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
