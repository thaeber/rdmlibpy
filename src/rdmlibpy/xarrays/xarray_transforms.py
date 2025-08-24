from typing import List, Literal, Mapping, Optional

import numpy as np
import pint_xarray
import xarray as xr
import scipy.ndimage
import skimage.transform
from omegaconf import OmegaConf

from ..process import Transform

_ = pint_xarray.__version__


class XArrayTransform(Transform):
    keep_attributes: bool = True

    class KeepAttributesContext:
        def __init__(self, transform: 'XArrayTransform'):
            self._previous_value = None
            self.transform = transform

        def __enter__(self):
            self._previous_value = xr.get_options().get('keep_attrs', False)
            xr.set_options(keep_attrs=self.transform.keep_attributes)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            xr.set_options(keep_attrs=self._previous_value)

    def keep_attrs(self):
        """
        Context manager to temporarily set the keep_attributes option for xarray
        operations.
        """
        return self.KeepAttributesContext(self)


class XArrayUnits(XArrayTransform):
    name: str = 'xarray.units'
    version: str = '1'

    quantify: bool = False

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
        if not self.quantify:
            result = result.pint.dequantify()

        return result


class XArrayUnitsDequantify(XArrayTransform):
    name: str = 'xarray.units.dequantify'
    version: str = '1'

    def run(self, ds: xr.Dataset):
        return ds.pint.dequantify()


class XArrayAttributes(XArrayTransform):
    """
    A transform class for setting attributes on an xarray DataArray or Dataset.
    This class provides functionality to update the attributes of an xarray
    object (DataArray or Dataset) by taking a deep copy of the provided keyword
    arguments and applying them as attributes.

    Attributes:
        name (str): The name of the transform, identifying it as
            'xarray.set.attrs'.
        version (str): The version of the transform, set to '1'.

    Methods:
        run(source: xr.DataArray | xr.Dataset, **kwargs):
            Updates the attributes of the provided xarray object with the given
            keyword arguments. The attributes are deep-copied to ensure
            immutability and are serialized/deserialized using YAML for
            consistency.

            Args:
                source (xr.DataArray | xr.Dataset): The xarray object whose
                    attributes are to be updated.
                **kwargs: Arbitrary keyword arguments representing the
                    attributes to be added or updated on the xarray object.

            Returns:
                xr.DataArray | xr.Dataset: The xarray object with updated
                attributes.
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
            xr.DataArray | xr.Dataset: The transformed xarray object with updated
            attributes.

        Notes:
            - The attributes are deep-copied and serialized to YAML format before
              being applied to ensure immutability and consistency.
            - The `source` object is modified in-place, but the same object is also
              returned for convenience.
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


class XArraySqueeze(XArrayTransform):
    """
    XArraySqueeze is a transform that applies the `squeeze` operation to an xarray
    DataArray or Dataset.

    Attributes:
        name (str): The name of the transform, set to 'xarray.squeeze'.
        version (str): The version of the transform, set to '1'.

    Methods:
        run(source: xr.DataArray | xr.Dataset, dim=None, **kwargs):
            Squeezes the input xarray object by removing dimensions of size 1.

            Parameters:
                source (xr.DataArray | xr.Dataset): The input xarray object to be
                    squeezed.
                dim (str or iterable of str, optional): The dimension(s) to squeeze.
                    If None, all dimensions of size 1 will be squeezed.
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
            source (xr.DataArray | xr.Dataset): The input xarray object to be
            squeezed.
            dim (str or list of str, optional): The dimension(s) to squeeze. If
            None, all dimensions of size 1 will be squeezed.
            **kwargs: Additional keyword arguments passed to the `squeeze` method.

        Returns:
            xr.DataArray | xr.Dataset: The squeezed xarray object.
        """
        return source.squeeze(dim=dim)


class XArrayStatisticsMean(XArrayTransform):
    """
    XArrayStatisticsMean is a transform that computes the mean along the
    specified dimension(s) of an xarray DataArray or Dataset.

    Attributes:
        name (str): The name of the transform, set to 'xarray.statistics.mean'.
        version (str): The version of the transform, set to '1'.

    Methods:
        run(source: xr.DataArray | xr.Dataset, dim=None, **kwargs):
            Computes the mean of the input xarray object along the specified
            dimension(s).

            Parameters:
                source (xr.DataArray | xr.Dataset): The input xarray object.
                dim (str or list of str, optional): The dimension(s) along which
                to compute the mean.
                **kwargs: Additional keyword arguments passed to the `mean`
                method.

            Returns:
                xr.DataArray or xr.Dataset: The xarray object with the mean
                computed.
    """

    name: str = 'xarray.statistics.mean'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, dim=None, **kwargs):
        """
        Compute the mean of the given xarray DataArray or Dataset along the
        specified dimension(s).

        Parameters:
            source (xr.DataArray | xr.Dataset): The input xarray object.
            dim (str or list of str, optional): The dimension(s) along which to
            compute the mean.
            **kwargs: Additional keyword arguments passed to the `mean` method.

        Returns:
            xr.DataArray | xr.Dataset: The xarray object with the mean computed.
        """
        with self.keep_attrs():
            return source.mean(dim=dim, **kwargs)


class XArrayAffineTransform(XArrayTransform):
    name: str = 'xarray.affine.transform'
    version: str = '1'

    def run(
        self, source: xr.DataArray | xr.Dataset, matrix=None, dims=('y', 'x'), **kwargs
    ):
        with self.keep_attrs():
            if matrix is None:
                matrix = np.eye(len(dims) + 1)
            return self.transform_image(
                source,
                transform=skimage.transform.AffineTransform(matrix),
                dims=dims,
                **kwargs,
            )

    def transform_image(
        self,
        image: xr.DataArray | xr.Dataset,
        transform: Optional[skimage.transform.AffineTransform] = None,
        dims=('y', 'x'),
    ) -> xr.DataArray:
        new_x = transform([[x, 0] for x in image.x]).T[0]
        new_y = transform([[0, y] for y in image.y]).T[1]
        ndims = len(dims)

        coords = np.dstack(np.meshgrid(new_x, new_y))
        new_coords = transform.inverse(
            coords.reshape(-1, 2)
        )  # .reshape(da.shape+ (2,))

        def _transform(arr: np.ndarray):
            # print(arr.shape)
            shape = arr.shape
            out = np.empty(shape)
            for index in np.ndindex(shape[:-ndims]):
                out[tuple(index) + (...,)] = scipy.ndimage.map_coordinates(
                    arr[index].T, new_coords.T, mode='nearest', cval=np.nan
                ).reshape(arr.shape[-ndims:])

            return out

        result = xr.apply_ufunc(
            _transform,
            image,
            input_core_dims=[dims],
            output_core_dims=[dims],
            on_missing_core_dim='copy',
            dask='parallelized',
            dask_gufunc_kwargs={
                'meta': np.ones((1,) * len(image.dims)),
                'allow_rechunk': True,
            },
        )
        result = result.assign_coords(x=new_x, y=new_y)
        return result


class XArrayAssign(XArrayTransform):
    name: str = 'xarray.assign'
    version: str = '1'

    def run(self, source: xr.Dataset, **kwargs):
        with self.keep_attrs():
            return source.assign(**kwargs)


class XArraySwapDims(XArrayTransform):
    name: str = 'xarray.swap_dims'
    version: str = '1'

    def run(self, source: xr.DataArray | xr.Dataset, dims_dict=None, **dims_kwargs):
        with self.keep_attrs():
            return source.swap_dims(dims_dict, **dims_kwargs)


class XArraySetCoords(XArrayTransform):
    name: str = 'xarray.set_coords'
    version: str = '1'

    def run(self, source: xr.Dataset, coords: str | List[str]):
        with self.keep_attrs():
            return source.set_coords(coords)


class XArrayMerge(XArrayTransform):
    name: str = 'xarray.merge'
    version: str = '1'

    interpolate: bool = False
    interpolate_on: Optional[str] = None
    combine_attrs: Literal['drop', 'identical', 'no_conflicts', 'override'] = 'override'

    def run(self, source: xr.Dataset, other: xr.Dataset | xr.DataArray):
        with self.keep_attrs():
            if self.interpolate:
                if self.interpolate_on is None:
                    other = other.interp_like(source)
                else:
                    other = other.interp(
                        {self.interpolate_on: source[self.interpolate_on]}
                    )
        return source.merge(
            other,
            compat='no_conflicts',
            join='outer',
            fill_value=np.nan,
            combine_attrs=self.combine_attrs,
        )


class XArrayCreateDataTree(XArrayTransform):
    name: str = 'xarray.create.data_tree'
    version: str = '1'

    interpolate: bool = False

    def run(
        self,
        root: xr.Dataset,
        groups: dict[str, xr.Dataset] | None = None,
        **groups_kwargs: xr.Dataset
    ):
        _groups = {'./': root}

        def interpolate_if_needed(ds: dict[str, xr.Dataset]) -> dict[str, xr.Dataset]:
            if self.interpolate:
                return {k: v.interp_like(root) for k, v in ds.items()}
            return ds

        if groups is not None:
            _groups.update(interpolate_if_needed(groups))
        _groups.update(interpolate_if_needed(groups_kwargs))

        return xr.DataTree.from_dict(_groups)
