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
    """
    A transform class for setting attributes on an xarray DataArray or Dataset.
    This class provides functionality to update the attributes of an xarray
    object (DataArray or Dataset) by taking a deep copy of the provided keyword
    arguments and applying them as attributes.
    Attributes:
        name (str): The name of the transform, identifying it as 'xarray.set.attrs'.
        version (str): The version of the transform, set to '1'.
    Methods:
        run(source: xr.DataArray | xr.Dataset, **kwargs):
            Updates the attributes of the provided xarray object with the given
            keyword arguments. The attributes are deep-copied to ensure immutability
            and are serialized/deserialized using YAML for consistency.
            Args:
                source (xr.DataArray | xr.Dataset): The xarray object whose attributes
                    are to be updated.
                **kwargs: Arbitrary keyword arguments representing the attributes to
                    be added or updated on the xarray object.
            Returns:
                xr.DataArray | xr.Dataset: The xarray object with updated attributes.
    """

    name: str = 'xarray.set.attrs'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, **kwargs):
        """
        Executes a transformation on the given xarray object (DataArray or Dataset)
        by updating its attributes with the provided keyword arguments.
        Parameters:
            source (xr.DataArray | xr.Dataset): The xarray object (DataArray or Dataset)
                to be transformed.
            **kwargs: Arbitrary keyword arguments representing attributes to be added
                or updated in the `source` object's attributes.
        Returns:
            xr.DataArray | xr.Dataset: The transformed xarray object with updated attributes.
        Notes:
            - The attributes are deep-copied and serialized to YAML format before being
              applied to ensure immutability and consistency.
            - The `source` object is modified in-place, but the same object is also returned
              for convenience.
        """
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


class XArraySqueeze(Transform):
    """
    XArraySqueeze is a transform that applies the `squeeze` operation to an xarray DataArray or Dataset.
    Attributes:
        name (str): The name of the transform, set to 'xarray.squeeze'.
        version (str): The version of the transform, set to '1'.
    Methods:
        run(source: xr.DataArray | xr.Dataset, dim=None, **kwargs):
            Squeezes the input xarray object by removing dimensions of size 1.
            Parameters:
                source (xr.DataArray | xr.Dataset): The input xarray object to be squeezed.
                dim (str or iterable of str, optional): The dimension(s) to squeeze. If None, all dimensions of size 1 will be squeezed.
                **kwargs: Additional keyword arguments passed to the `squeeze` method.
            Returns:
                xr.DataArray or xr.Dataset: The squeezed xarray object.
    """

    name: str = 'xarray.squeeze'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, dim=None, **kwargs):
        """
        Squeeze the given xarray DataArray or Dataset along the specified dimension(s).

        Parameters:
            source (xr.DataArray | xr.Dataset): The input xarray object to be squeezed.
            dim (str or list of str, optional): The dimension(s) to squeeze. If None,
                all dimensions of size 1 will be squeezed.
            **kwargs: Additional keyword arguments passed to the `squeeze` method.

        Returns:
            xr.DataArray | xr.Dataset: The squeezed xarray object.
        """
        return source.squeeze(dim=dim)
