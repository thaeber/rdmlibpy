import logging
from datetime import datetime
from typing import Literal

import xarray as xr
from brukeropus import read_opus

from rdmlibpy._typing import FilePath
from rdmlibpy.process import Loader

logger = logging.getLogger(__name__)

TypeOfSpectrum = Literal[
    'absorbance',
    'a',
    'sample',
    'sm',
    'reference',
    'rf',
    'igsm',
    'igrf',
    'Kubelka-Munk',
    'km',
]


class BrukerOpusLoader(Loader):
    name: str = 'bruker.opus'
    version: str = '1'

    spectrum: TypeOfSpectrum = 'absorbance'  # load absorbance spectra by default
    concatenate: bool = True  # concatenate spectra if a glob pattern is provided
    concat_dim: str = 'timestamp'
    date_format: str = '%d/%m/%Y %H:%M:%S.%f'
    squeeze: bool = (
        True  # return DataArray instead of List[DataArray] for single spectrum
    )
    sort_by_timestamp: bool = True

    def run(self, source):
        # load using filename (possible a glob pattern)
        generator = map(self._try_load_single_spectrum, Loader.glob(source))
        generator = filter(lambda a: a is not None, generator)
        if self.concatenate:
            data = xr.concat(generator, dim=self.concat_dim)
            if self.sort_by_timestamp:
                data = data.sortby('timestamp')
        else:
            data = list(generator)
            if self.sort_by_timestamp:
                data = sorted(data, key=lambda da: da.timestamp)
            if self.squeeze and len(data) == 1:
                data = data[0]
        return data

    def _try_load_single_spectrum(self, source: FilePath, **kwargs):
        try:
            return self._load_single_spectrum(source, **kwargs)
        except AttributeError:
            return None

    def _load_single_spectrum(self, source: FilePath, **kwargs):
        logger.debug(f'Loading OPUS file: {source}')
        opus_file = read_opus(str(source))

        key = self.map_spectrum_key(self.spectrum)
        logger.debug(f'Extracting spectrum of type: {self.spectrum} (key: {key})')
        spectrum = getattr(opus_file, key)
        da = xr.DataArray(
            spectrum.y, coords=dict(nu=spectrum.x), dims='nu', name=self.spectrum
        )

        time_str = (
            spectrum.dat
            + ' '
            + spectrum.tim.split(' ')[0]  # get rid of the (GMT+2) part
        )
        da['timestamp'] = datetime.strptime(time_str, self.date_format)

        return da

    def map_spectrum_key(self, key: TypeOfSpectrum):
        if self.spectrum == 'absorbance':
            return 'a'
        elif self.spectrum == 'sample':
            return 'sm'
        elif self.spectrum == 'reference':
            return 'rf'
        elif self.spectrum == 'Kubelka-Munk':
            return 'km'
        else:
            return key
