from pathlib import Path

import numpy as np
import xarray as xr

from rdmlibpy.xarrays import XArraySelectTimespan


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
