from pathlib import Path

import numpy as np
import pint
import pint_xarray
import pytest
import xarray as xr

from rdmlibpy.xarrays import XArrayAttributes, XArrayUnits
from rdmlibpy.xarrays.xarray_transforms import XArraySqueeze
from rdmlibpy.xarrays.xarray_transforms import XArrayStatisticsMean
from rdmlibpy.xarrays.xarray_transforms import XArrayAffineTransform

_ = pint_xarray.unit_registry


class TestDataFrameUnits:
    def test_create_loader(self):
        transform = XArrayUnits()

        assert transform.name == 'xarray.units'
        assert transform.version == '1'

    def test_dataset(self, data_path: Path):
        # create test data
        N = 10
        source = xr.Dataset(
            dict(
                A=('x', 2 * np.arange(N)),
                B=('x', np.linspace(0, 1, N)),
                C=('x', np.logspace(1, 2, N)),
            ),
            coords=dict(x=np.arange(10)),
        )

        transform = XArrayUnits()
        ds = transform.run(
            source,
            units={
                'A': 'K',
                'B': 'm/s',
                'x': '1/cm',
            },
        )
        assert ds.A.pint.units == pint.Unit('K')
        assert ds.B.pint.units == pint.Unit('m/s')
        assert ds.C.pint.units is None
        if pint_xarray.__version__ <= '0.5':
            assert pint.Unit(ds.x.attrs['units']) == pint.Unit('1/cm')
        else:
            assert ds.x.pint.units == pint.Unit('1/cm')

    def test_dataset_with_default_unit(self, data_path: Path):
        # create test data
        N = 10
        source = xr.Dataset(
            dict(
                A=('x', 2 * np.arange(N)),
                B=('x', np.linspace(0, 1, N)),
                C=('x', np.logspace(1, 2, N)),
            ),
            coords=dict(x=np.arange(10)),
        )

        transform = XArrayUnits()
        ds = transform.run(
            source,
            units={
                'A': 'K',
                'B': 'm/s',
                'x': '1/cm',
            },
            default_unit='ppm',
        )
        assert ds.A.pint.units == pint.Unit('K')
        assert ds.B.pint.units == pint.Unit('m/s')
        assert ds.C.pint.units == pint.Unit('ppm')
        if pint_xarray.__version__ <= '0.5':
            assert pint.Unit(ds.x.attrs['units']) == pint.Unit('1/cm')
        else:
            assert ds.x.pint.units == pint.Unit('1/cm')

    def test_data_array(self, data_path: Path):
        # create test data
        N = 10
        source = xr.DataArray(
            np.linspace(0, 1, N),
            coords=dict(x=np.arange(10)),
        )

        transform = XArrayUnits()
        da = transform.run(
            source,
            units={
                'x': '1/cm',
                'units': 'K',
            },
        )
        assert da.pint.units == pint.Unit('K')
        if pint_xarray.__version__ <= '0.5':
            assert pint.Unit(da.x.attrs['units']) == pint.Unit('1/cm')
        else:
            assert da.x.pint.units == pint.Unit('1/cm')

    def test_data_array_with_default_unit(self, data_path: Path):
        # create test data
        N = 10
        source = xr.DataArray(
            np.linspace(0, 1, N),
            coords=dict(x=np.arange(10)),
        )

        transform = XArrayUnits()
        da = transform.run(
            source,
            units={
                'x': '1/cm',
            },
            default_unit='K',
        )
        assert da.pint.units == pint.Unit('K')
        if pint_xarray.__version__ <= '0.5':
            assert pint.Unit(da.x.attrs['units']) == pint.Unit('1/cm')
        else:
            assert da.x.pint.units == pint.Unit('1/cm')

    def test_units_keeps_attributes(self):
        transform = XArrayUnits()
        data = xr.DataArray(
            np.random.rand(10),
            dims=["x"],
            coords={"x": range(10)},
            attrs={"description": "Test data"},
        )

        result = transform.run(data, units={"x": "1/cm", "units": "K"})

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("x",)
        assert result.attrs["description"] == "Test data"
        assert result.pint.units == pint.Unit("K")
        if pint_xarray.__version__ <= "0.5":
            assert pint.Unit(result.x.attrs["units"]) == pint.Unit("1/cm")
        else:
            assert result.x.pint.units == pint.Unit("1/cm")


class TestDataFrameAttributes:
    def test_create(self):
        process = XArrayAttributes()

        assert process.name == 'xarray.set.attrs'
        assert process.version == '1'

    def test_add_attributes(self):
        da = xr.DataArray([1.1, 2.2, 3.3])

        process = XArrayAttributes()
        attrs = {
            'date': '2024-04-15',
            'title': 'NH3 oxidation over Pd; blind test w/o O2',
            'sample-id': 'Plate2302F',
            'sample-note': '2.4% Pd/Al2O3 (RefCat4)',
            'inlet': {
                'flow_rate': '1.0L/min',
                'temperature': '293K',
                'composition': {'NH3': '1000ppm', 'O2': '0%', 'N2': '*'},
            },
            'id': '2024-04-15A01',
            'tag': 'light-off',
            'start': '2024-04-15T06:17:00',
            'stop': '2024-04-15T09:17:00',
        }
        actual = process.run(da, **attrs)

        # check that run returns the same instance
        assert actual is da

        assert actual.attrs == attrs

    def test_makes_deep_copy_of_parameters(self):
        da = xr.DataArray([1.1, 2.2, 3.3])

        process = XArrayAttributes()
        attrs = dict(
            A1='a1',
            A2=2,
            A3=3.0,
            A4=dict(
                B1='b1',
                B2=4,
                B3=9.0,
                B4=dict(C1='c1', C2=8, C3=27.0),
            ),
        )
        actual = process.run(da, **attrs)

        # check that attributes are equal
        assert actual.attrs == attrs

        # modify source dictionary and check again; now the
        # dictionaries should not be equal
        attrs['A4']['B4']['C4'] = 'test'  # type: ignore

        assert not (dict(actual.attrs) == dict(attrs))


class TestXArraySqueeze:
    def test_create_instance(self):
        transform = XArraySqueeze()

        assert transform.name == 'xarray.squeeze'
        assert transform.version == '1'

    def test_squeeze_all_dimensions(self):
        transform = XArraySqueeze()
        data = xr.DataArray(
            np.random.rand(1, 10, 1),
            dims=["x", "y", "z"],
            coords={"x": [0], "y": range(10), "z": [0]},
        )

        result = transform.run(data)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)

    def test_squeeze_specific_dimension(self):
        transform = XArraySqueeze()
        data = xr.DataArray(
            np.random.rand(1, 10, 1),
            dims=["x", "y", "z"],
            coords={"x": [0], "y": range(10), "z": [0]},
        )

        result = transform.run(data, dim="x")

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y", "z")
        assert result.shape == (10, 1)

    def test_squeeze_multiple_dimensions(self):
        transform = XArraySqueeze()
        data = xr.DataArray(
            np.random.rand(1, 10, 1),
            dims=["x", "y", "z"],
            coords={"x": [0], "y": range(10), "z": [0]},
        )

        result = transform.run(data, dim=["x", "z"])

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)

    def test_squeeze_no_size_one_dimensions(self):
        transform = XArraySqueeze()
        data = xr.DataArray(
            np.random.rand(5, 10),
            dims=["x", "y"],
            coords={"x": range(5), "y": range(10)},
        )

        result = transform.run(data)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("x", "y")
        assert result.shape == (5, 10)

    def test_squeeze_dataset(self):
        transform = XArraySqueeze()
        data = xr.Dataset(
            {
                "var1": (["x", "y", "z"], np.random.rand(1, 10, 1)),
                "var2": (["x", "y", "z"], np.random.rand(1, 10, 1)),
            },
            coords={"x": [0], "y": range(10), "z": [0]},
        )

        result = transform.run(data)

        assert isinstance(result, xr.Dataset)
        assert result.sizes == {"y": 10}
        assert result["var1"].shape == (10,)
        assert result["var2"].shape == (10,)

    def test_squeeze_keeps_attributes(self):
        transform = XArraySqueeze()
        data = xr.DataArray(
            np.random.rand(1, 10, 1),
            dims=["x", "y", "z"],
            coords={"x": [0], "y": range(10), "z": [0]},
            attrs={"description": "Test data", "units": "kg"},
        )

        result = transform.run(data)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)
        assert result.attrs["description"] == "Test data"
        assert result.attrs["units"] == "kg"


class TestXArrayStatisticsMean:
    def test_create_instance(self):
        transform = XArrayStatisticsMean()

        assert transform.name == 'xarray.statistics.mean'
        assert transform.version == '1'

    def test_mean_along_single_dimension(self):
        transform = XArrayStatisticsMean()
        values = np.random.rand(5, 10)
        data = xr.DataArray(
            values,
            dims=["x", "y"],
            coords={"x": range(5), "y": range(10)},
        )

        result = transform.run(data, dim="x")

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)
        assert np.allclose(result.values, values.mean(axis=0))

    def test_mean_along_multiple_dimensions(self):
        transform = XArrayStatisticsMean()
        values = np.random.rand(5, 10, 15)
        data = xr.DataArray(
            values,
            dims=["x", "y", "z"],
            coords={"x": range(5), "y": range(10), "z": range(15)},
        )

        result = transform.run(data, dim=["x", "z"])

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)
        assert np.allclose(result.values, values.mean((0, 2)))

    def test_mean_without_specifying_dimension(self):
        transform = XArrayStatisticsMean()
        values = np.random.rand(5, 10)
        data = xr.DataArray(
            values,
            dims=["x", "y"],
            coords={"x": range(5), "y": range(10)},
        )

        result = transform.run(data)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ()
        assert result.shape == ()
        assert np.allclose(result.values, values.mean())

    def test_mean_on_dataset(self):
        transform = XArrayStatisticsMean()
        values1 = np.random.rand(5, 10)
        values2 = np.random.rand(5, 10)
        data = xr.Dataset(
            {
                "var1": (["x", "y"], values1),
                "var2": (["x", "y"], values2),
            },
            coords={"x": range(5), "y": range(10)},
        )

        result = transform.run(data, dim="x")

        assert isinstance(result, xr.Dataset)
        assert result.sizes == {"y": 10}
        assert result["var1"].shape == (10,)
        assert result["var2"].shape == (10,)
        assert np.allclose(result["var1"].values, values1.mean(axis=0))
        assert np.allclose(result["var2"].values, values2.mean(axis=0))

    def test_mean_keeps_attributes(self):
        transform = XArrayStatisticsMean()
        data = xr.DataArray(
            np.random.rand(5, 10),
            dims=["x", "y"],
            coords={"x": range(5), "y": range(10)},
            attrs={"description": "Test data", "units": "m/s"},
        )

        result = transform.run(data, dim="x")

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y",)
        assert result.shape == (10,)
        assert np.allclose(result.values, data.values.mean(axis=0))
        assert result.attrs["description"] == "Test data"
        assert result.attrs["units"] == "m/s"

    def test_mean_keeps_attributes_on_dataset(self):
        transform = XArrayStatisticsMean()
        values1 = np.random.rand(5, 10)
        values2 = np.random.rand(5, 10)
        data = xr.Dataset(
            {
                "var1": (
                    ["x", "y"],
                    values1,
                    dict(description="Variable 1", xunits="m/s"),
                ),
                "var2": (
                    ["x", "y"],
                    values2,
                    dict(description="Variable 2", xunits="s"),
                ),
            },
            coords={"x": range(5), "y": range(10)},
            attrs={"experiment": "Test Experiment", "date": "2024-04-15"},
        )

        result = transform.run(data, dim="x")

        assert isinstance(result, xr.Dataset)
        assert result.sizes == {"y": 10}
        assert result["var1"].shape == (10,)
        assert result["var2"].shape == (10,)
        assert np.allclose(result["var1"].values, values1.mean(axis=0))
        assert np.allclose(result["var2"].values, values2.mean(axis=0))
        assert result.attrs["experiment"] == "Test Experiment"
        assert result.attrs["date"] == "2024-04-15"
        assert result["var1"].attrs["description"] == "Variable 1"
        assert result["var1"].attrs["xunits"] == "m/s"
        assert result["var2"].attrs["description"] == "Variable 2"
        assert result["var2"].attrs["xunits"] == "s"


class TestXArrayAffineTransform:
    def test_create_instance(self):
        transform = XArrayAffineTransform()

        assert transform.name == 'xarray.affine.transform'
        assert transform.version == '1'

    def test_affine_transform_on_dataarray(self):
        transform = XArrayAffineTransform()
        values = np.random.rand(10, 10)
        data = xr.DataArray(
            values,
            dims=["y", "x"],
            coords={"y": range(10), "x": range(10)},
        )
        matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        result = transform.run(data, matrix)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y", "x")
        assert result.shape == (10, 10)
        assert result.values == pytest.approx(values)

    def test_affine_transform_on_dataset(self):
        transform = XArrayAffineTransform()
        values1 = np.random.rand(10, 10)
        values2 = np.random.rand(10, 10)
        data = xr.Dataset(
            {
                "var1": (["y", "x"], values1),
                "var2": (["y", "x"], values2),
            },
            coords={"y": range(10), "x": range(10)},
        )
        matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        result = transform.run(data, matrix)

        assert isinstance(result, xr.Dataset)
        assert result.sizes == {"y": 10, "x": 10}
        assert result["var1"].shape == (10, 10)
        assert result["var2"].shape == (10, 10)
        assert result["var1"].values == pytest.approx(values1)
        assert result["var2"].values == pytest.approx(values2)

    def test_affine_transform_keeps_attributes(self):
        transform = XArrayAffineTransform()
        data = xr.DataArray(
            np.random.rand(10, 10),
            dims=["y", "x"],
            coords={"y": range(10), "x": range(10)},
            attrs={"description": "Test data", "units": "m"},
        )
        matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        result = transform.run(data, matrix)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y", "x")
        assert result.shape == (10, 10)
        assert result.attrs["description"] == "Test data"
        assert result.attrs["units"] == "m"

    def test_affine_transform_with_non_identity_matrix(self):
        transform = XArrayAffineTransform()
        values = np.random.rand(10, 10)
        data = xr.DataArray(
            values,
            dims=["y", "x"],
            coords={"y": range(10), "x": range(10)},
        )
        matrix = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]])

        result = transform.run(data, matrix)

        assert isinstance(result, xr.DataArray)
        assert result.dims == ("y", "x")
        assert result.shape == (10, 10)
        # TODO: Check if the transformation is applied correctly
        # expected_values = np.roll(np.roll(values, 2, axis=1), 3, axis=0)
        # assert result.values == pytest.approx(expected_values)
