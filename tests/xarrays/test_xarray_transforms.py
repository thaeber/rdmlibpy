from pathlib import Path

import numpy as np
import pint
import xarray as xr
import pint_xarray

from rdmlibpy.xarrays import (
    XArrayAttributes,
    XArrayUnits,
)


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
        assert pint.Unit(ds.x.attrs['units']) == pint.Unit('1/cm')

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
        assert pint.Unit(ds.x.attrs['units']) == pint.Unit('1/cm')

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
        assert pint.Unit(da.x.attrs['units']) == pint.Unit('1/cm')

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
        assert pint.Unit(da.x.attrs['units']) == pint.Unit('1/cm')


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
