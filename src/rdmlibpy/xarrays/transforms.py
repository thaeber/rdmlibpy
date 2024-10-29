from typing import Mapping

import pint_xarray
import xarray as xr
from omegaconf import OmegaConf

from ..process import Transform

_ = pint_xarray.unit_registry


class XArrayUnits(Transform):
    name: str = 'xarray.units'
    version: str = '1'

    def run(
        self,
        source: xr.DataArray | xr.Dataset,
        units: Mapping[str, str] | None = None,
        default_unit: str | None = None,
    ):
        units_to_set = {}
        if default_unit is not None:
            if isinstance(source, xr.Dataset):
                units_to_set.update({name: default_unit for name in source.keys()})
            elif isinstance(source, xr.DataArray):
                if source.name:
                    units_to_set[source.name] = default_unit
                else:
                    units_to_set['units'] = default_unit
        if units is not None:
            units_to_set.update(units)

        result = source.pint.quantify(**units_to_set)
        return result


class XArrayAttributes(Transform):
    name: str = 'xarray.set.attrs'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, **kwargs):
        # make deep copy of attributes
        # (roundtrip serialization to yaml)
        attrs = OmegaConf.to_object(
            OmegaConf.create(
                OmegaConf.to_yaml(
                    OmegaConf.create(kwargs),
                ),
            ),
        )

        source.attrs.update(attrs)  # type: ignore
        return source
