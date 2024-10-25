# %%
import logging
from datetime import datetime

import xarray as xr
from brukeropus import read_opus

from rdmlibpy._typing import FilePath
from rdmlibpy.process import Loader

# %%
logger = logging.getLogger(__name__)


# %%
class BrukerOpusLoader(Loader):
    name: str = 'bruker.opus'
    version: str = '1'

    spectrum: str = 'a'  # load absorbance spectra by default
    concatenate: bool = True  # concatenate spectra if a glob pattern is provided
    concat_dim: str = 'timestamp'
    date_format: str = '%d/%m/%Y %H:%M:%S.%f'
    squeeze: bool = (
        True  # return DataArray instance of List[DataArray] for single spectrum
    )

    def run(self, source):
        # load using filename (possible a glob pattern)
        generator = map(self._try_load_single_spectrum, Loader.glob(source))
        generator = filter(lambda a: a is not None, generator)
        if self.concatenate:
            data = xr.concat(generator, dim=self.concat_dim)
        else:
            data = list(generator)
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

        logger.debug(f'Extracting spectrum of type: {self.spectrum}')
        spectrum = getattr(opus_file, self.spectrum)
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


# da = BrukerOpusLoader(concatenate=True).run(
#     r'E:\2022-NOCO\raw\DRIFTS\2024-10-17\DRIFTS\300\LC003.*'
# )
# da
