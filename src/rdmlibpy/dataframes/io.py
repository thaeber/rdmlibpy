import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import pandas.arrays
import pint_pandas
import pint_pandas.pint_array
import pydantic

from .._typing import FilePath, ReadCsvBuffer, WriteBuffer
from ..process import Cache, Loader, Writer

logger = logging.getLogger(__name__)

ParseDatesType = None | List[str] | Dict[str, List[str]]


class DataFrameReadCSVBase(Loader):
    decimal: str = '.'
    separator: str = ','
    options: Dict[str, Any] = pydantic.Field(default_factory=dict)  # type: ignore
    concatenate: bool = True
    date_format: str = 'ISO8601'
    parse_dates: ParseDatesType = None

    def run(self, source: FilePath | ReadCsvBuffer, **kwargs):
        if isinstance(source, FilePath):
            # load using filename (possible a glob pattern)
            data = [self._read_csv(path, **kwargs) for path in Loader.glob(source)]
            if self.concatenate:
                data = pd.concat(data)
            return data
        else:
            # load from text buffer (e.g. file buffer or StringIO)
            return self._read_csv(source, **kwargs)

    def _read_csv(self, source: FilePath | ReadCsvBuffer, **kwargs):
        df = self._load(source, **kwargs)
        df = self._parse_dates(df)
        return df

    def _load(self, source: FilePath | ReadCsvBuffer, **kwargs) -> pd.DataFrame:
        if isinstance(source, Path):
            logger.info(f'Loading CSV data from: {source.name} ({source.parent})')
            if not source.exists():
                logger.error('File does not exists')
                raise FileNotFoundError(source)
        else:
            logger.info('Reading CSV data from text buffer')

        # merge process configuration with runtime keyword arguments
        options = dict(sep=self.separator, decimal=self.decimal, **self.options)
        options |= kwargs

        # load csv data & return
        return pd.read_csv(source, **options)  # type: ignore

    def _parse_dates(self, df: pd.DataFrame):
        if self.parse_dates is None:
            return df

        match self.parse_dates:
            case [*column_names]:
                for col in column_names:
                    df = self._parse_dates_replacing_single_column(df, col)
            case {**nested}:
                # loop over mappings
                for key, column_names in nested.items():
                    if len(column_names) == 1:
                        name = column_names[0]
                        df = self._parse_dates_replacing_single_column(df, name)
                        if key != name:
                            df.rename(columns={name: key}, inplace=True, errors='raise')
                    else:
                        df = self._parse_dates_joining_columns(df, key, column_names)

        return df

    def _parse_dates_joining_columns(
        self, df: pd.DataFrame, target_name: str, column_names: List[str]
    ):

        def join_columns(column_names):
            return df[column_names].astype(str).agg(' '.join, axis=1)

        # generate datetime series from columns
        dt = pd.to_datetime(join_columns(column_names), format=self.date_format)

        # drop source columns
        df = df.drop(columns=column_names)

        # insert new column at the front (in place operation)
        df.insert(0, target_name, dt)

        return df

    def _parse_dates_replacing_single_column(self, df: pd.DataFrame, column: str):
        # get (index) location of original column
        index = df.columns.get_loc(column)
        if not isinstance(index, int):
            raise ValueError(
                f'Column label must be unique. Found multiple indices ({index}) for label ({column}).'
            )

        # "pop" column & generate datetime series
        dt = pd.to_datetime(df.pop(column), format=self.date_format)

        # insert new column at original index
        df.insert(index, column, dt)

        return df


class DataFrameReadCSV(DataFrameReadCSVBase):
    version: str = '1'
    name: str = 'dataframe.read.csv'


class DataFrameWriteCSV(Writer):
    name: str = 'dataframe.write.csv'
    version: str = '1'

    decimal: str = '.'
    separator: str = ','
    index: bool = False
    options: Dict[str, Any] = pydantic.Field(default_factory=dict)  # type: ignore
    date_format: Optional[str] = r'%Y-%m-%dT%H:%M:%S.%f'
    dequantify: bool = False

    def run(
        self,
        source: pd.DataFrame,
        filename: FilePath | WriteBuffer[str] | WriteBuffer[bytes],
        dequantify: bool = False,
        **kwargs,
    ):
        # merge process configuration with runtime keyword arguments
        options = dict(
            sep=self.separator,
            decimal=self.decimal,
            index=self.index,
            date_format=self.date_format,
        )
        options |= self.options
        options |= kwargs

        # create paths if necessary
        if isinstance(filename, FilePath):
            filename = self.ensure_path(filename)

        # promote units to multi-index header
        if dequantify or (dequantify and self.dequantify):
            source = source.pint.dequantify()

        # write data to csv
        source.to_csv(filename, **options)  # type: ignore

        # return unaltered data
        return source


class DataFrameFileCache(Cache):
    name: str = 'dataframe.cache'
    version: str = '1'

    def read(self, filename: FilePath, rebuild: bool = False, **kwargs):
        # load data from HDF5 file
        cached = pd.read_hdf(filename, key='data')

        # convert units back to PintArrays
        # cached = cached.pint.quantify(level=-1)

        # temporary fix until https://github.com/hgrecco/pint-pandas/pull/217
        # is released
        cached = quantify(cached, level=-1)

        # return cached data
        return cached

    def write(
        self, source: pd.DataFrame, filename: FilePath, rebuild: bool = False, **kwargs
    ):
        # promote units to multi-index
        source = source.pint.dequantify()

        # get around some HDF5 restrictions, which can't handle FloatingArray data
        # used by pint
        for i, col in enumerate(source.columns):
            if isinstance(source.iloc[:, i].values, pandas.arrays.FloatingArray):  # type: ignore
                source[col] = np.array(source[col])

        # write data to HDF5 file
        source.to_hdf(filename, key='data')

    def cache_is_valid(self, filename: FilePath, rebuild: bool = False):
        if rebuild:
            return False
        return Path(filename).exists()


def quantify(df, level=-1):
    # Fix for https://github.com/hgrecco/pint-pandas/pull/217
    # (remove once that fix is rolled out in the next release of
    # pint-pandas)
    df_columns = df.columns.to_frame()
    unit_col_name = df_columns.columns[level]
    units = df_columns[unit_col_name]
    df_columns = df_columns.drop(columns=unit_col_name)

    df_new = pd.DataFrame(
        {
            i: (
                pint_pandas.PintArray(df.iloc[:, i], unit)
                if unit != pint_pandas.pint_array.NO_UNIT
                else df.iloc[:, i]
            )
            for i, unit in enumerate(units.values)
        }
    )

    df_new.columns = df_columns.index.droplevel(unit_col_name)
    df_new.index = df.index

    return df_new
