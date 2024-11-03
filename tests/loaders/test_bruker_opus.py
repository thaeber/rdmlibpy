from pathlib import Path

import numpy as np
import xarray as xr

from rdmlibpy.loaders import BrukerOpusLoader


class TestBrukerOpusLoader:
    def test_create_loader(self):
        loader = BrukerOpusLoader()

        assert loader.name == 'bruker.opus'
        assert loader.version == '1'

        assert loader.spectrum == 'a'
        assert loader.concatenate is True
        assert loader.concat_dim == 'timestamp'
        assert loader.date_format == '%d/%m/%Y %H:%M:%S.%f'
        assert loader.squeeze is True

    def test_load_single(self, data_path: Path):
        loader = BrukerOpusLoader()
        da = loader.run(
            source=data_path / 'bruker/LC003.3448',
        )
        assert isinstance(da, xr.DataArray)
        assert da.dims == ('timestamp', 'nu')
        assert len(da.nu) == 4978  # type: ignore

        assert da.timestamp[0] == np.datetime64('2024-10-17T16:19:04.075000')

    def test_load_single_no_squeeze(self, data_path: Path):
        loader = BrukerOpusLoader(concatenate=False, squeeze=False)
        data = loader.run(
            source=data_path / 'bruker/LC003.3448',
        )
        assert isinstance(data, list)
        assert len(data) == 1

    def test_load_multiple(self, data_path: Path):
        loader = BrukerOpusLoader()
        da = loader.run(
            source=data_path / 'bruker/LC003.*',
        )
        assert isinstance(da, xr.DataArray)
        assert da.dims == ('timestamp', 'nu')
        assert len(da.nu) == 4978  # type: ignore
        assert len(da.timestamp) == 3  # type: ignore

        assert da.timestamp[0] == np.datetime64('2024-10-17T16:19:04.075')
        assert da.timestamp[1] == np.datetime64('2024-10-17T16:19:08.559')
        assert da.timestamp[2] == np.datetime64('2024-10-17T16:19:13.069')
