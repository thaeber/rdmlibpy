# %%
from pathlib import Path
from typing import Dict

import davislib as dl
import xarray as xr

from .._typing import FilePath
from ..process import Loader


class DavisImageSetLoader(Loader):
    name: str = 'davis.image_set'
    version: str = '1'

    def run(
        self,
        source: FilePath,
        squeeze: bool = False,
        chunks: str = 'auto',
        attributes: None | Dict[str, str] = None,
    ):
        data = [
            self.open_image_set(
                path,
                squeeze=squeeze,
                chunks=chunks,
                attributes=attributes,
            )
            for path in Loader.glob(source)
        ]
        if len(data) == 1:
            return data[0]
        else:
            return xr.concat(data, dim='file')

    def open_image_set(self, path: Path, **kwargs):
        return xr.open_dataset(path, engine=dl.DavisBackend, **kwargs)
