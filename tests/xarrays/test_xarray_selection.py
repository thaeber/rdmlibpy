from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from rdmlibpy.xarrays import XArraySelectTimespan
from rdmlibpy.xarrays import XArraySelectRange


class TestSelectTimespan:
    def test_create_loader(self):
        loader = XArraySelectTimespan()

        assert loader.name == 'xarray.select.timespan'
        assert loader.version == '1'

        assert loader.drop is True

    def test_timestamp_as_coord(self, data_path: Path):
        # create test data
        t0 = np.datetime64('2024-10-25T15:14:00', 'ns')
        dt = np.timedelta64(2, 's')
        N = 20
        source = xr.DataArray(
            np.arange(N), coords=dict(timestamp=[t0 + k * dt for k in np.arange(N)])
        )

        transform = XArraySelectTimespan()
        da = transform.run(
            source,
            'timestamp',
            start='2024-10-25T15:14:09',
            stop='2024-10-25T15:14:19',
        )

        assert len(da) == 5  # type: ignore

    def test_timestamp_as_var(self, data_path: Path):
        # create test data
        t0 = np.datetime64('2024-10-25T15:14:00', 'ns')
        dt = np.timedelta64(2, 's')
        N = 20
        source = xr.Dataset(
            dict(
                some_data=('x', np.arange(N)),
                time=('x', [t0 + k * dt for k in np.arange(N)]),
            ),
            coords=dict(x=np.arange(N)),
        )

        transform = XArraySelectTimespan()
        ds = transform.run(
            source,
            'time',
            start='2024-10-25T15:14:09',
            stop='2024-10-25T15:14:19',
        )

        assert len(ds.x) == 5  # type: ignore


class TestSelectRange:
    def test_create_loader(self):
        selector = XArraySelectRange()

        assert selector.name == 'xarray.select.range'
        assert selector.version == '1'

        assert selector.drop is True

    def test_range_as_coord(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(da.dropna(dim='x')) == 6  # type: ignore
        assert da.values == pytest.approx(np.arange(5, 11))
        assert da.x.values == pytest.approx(np.arange(5, 11))

    def test_range_as_var(self):
        # create test data
        N = 20
        source = xr.Dataset(
            dict(
                some_data=('x', np.arange(N)),
                other_data=('x', np.arange(N)),
            ),
            coords=dict(x=np.arange(N)),
        )

        transform = XArraySelectRange()
        ds = transform.run(
            source,
            'other_data',
            start=5,
            stop=10,
        )

        assert len(ds.x.dropna(dim='x')) == 6  # type: ignore
        assert ds.some_data.values == pytest.approx(np.arange(5, 11))
        assert ds.other_data.values == pytest.approx(np.arange(5, 11))
        assert ds.x.values == pytest.approx(np.arange(5, 11))

    def test_no_start(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=10,
        )

        assert len(da.dropna(dim='x')) == 11  # type: ignore
        assert da.values == pytest.approx(np.arange(0, 11))

    def test_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=10,
            stop=None,
        )

        assert len(da.dropna(dim='x')) == 10  # type: ignore
        assert da.values == pytest.approx(np.arange(10, 20))

    def test_no_start_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=None,
        )

        assert len(da) == N  # type: ignore
        assert da.values == pytest.approx(np.arange(N))
