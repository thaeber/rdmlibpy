import pandas as pd
import pint
import pint_xarray
import xarray as xr
import xarray.testing

from rdmlibpy.base import PlainProcessParam, ProcessNode
from rdmlibpy.process import DelegatedSource
from rdmlibpy.xarrays import XArrayFileCache
import rdmlibpy as rdm

_ = pint_xarray.unit_registry


class TestXArrayFileCache:
    def test_create(self):
        cache = XArrayFileCache()

        assert cache.name == 'xarray.cache'
        assert cache.version == '1'

    def test_write_to_cache(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ],
                    ).astype('datetime64[us]'),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={'filename': PlainProcessParam(value=str(path))},
        )

        # verify cache does not exists yet
        assert not path.exists()

        # write to cache
        returned = workflow.run()

        # check that workflow returned original data
        assert source is returned

        # check cache exists
        assert path.exists()

        # check written data
        cached = xr.load_dataset(path)
        xarray.testing.assert_identical(source, cached)

    def test_write_to_cache_with_chunks(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ],
                    ).astype('datetime64[us]'),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )
        source = source.chunk(chunks='auto')

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={'filename': PlainProcessParam(value=str(path))},
        )

        # verify cache does not exists yet
        assert not path.exists()

        # write to cache
        returned = workflow.run()

        # check that workflow returned original data
        assert source is returned

        # check cache exists
        assert path.exists()

        # check written data
        cached = xr.load_dataset(path)
        xarray.testing.assert_identical(source, cached)

    def test_read_from_cache(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )
        source.to_netcdf(path)

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={'filename': PlainProcessParam(value=str(path))},
        )

        cached = workflow.run()

        # check that returned data is a different object instance
        assert source is not cached

        # check data integrity
        xarray.testing.assert_identical(source, cached)

    def test_rebuild_cache(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )
        source.to_netcdf(path)

        source['D'] = ['R1', 'R2', 'R3']
        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
                'rebuild': PlainProcessParam(value=True),
            },
        )

        cached = workflow.run()

        # check that returned data is the original object instance
        assert source is cached

        # check data integrity
        xarray.testing.assert_identical(source, cached)

    def test_dataset_with_datetime_index(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('t', [1.1, 2.2, 3.3]),
                B=('t', ['aa', 'bb', 'cc']),
            ),
            coords=dict(
                t=pd.to_datetime(
                    [
                        '2024-01-16T10:05:28.537',
                        '2024-01-16T10:05:29.735',
                        '2024-01-16T10:05:30.935',
                    ]
                )
            ),
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        cached = workflow.run()

        # modify dataframe and load from cache
        original_source = source.copy(deep=True)
        source['E'] = [1, 2, 3]
        cached = workflow.run()

        # check returned data is a different object instance
        assert source is not cached

        # check data integrity
        xarray.testing.assert_identical(original_source, cached)

    def test_dataset_with_datetime_index_and_chunked_array(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('t', [1.1, 2.2, 3.3]),
                B=('t', ['aa', 'bb', 'cc']),
            ),
            coords=dict(
                t=pd.to_datetime(
                    [
                        '2024-01-16T10:05:28.537',
                        '2024-01-16T10:05:29.735',
                        '2024-01-16T10:05:30.935',
                    ]
                )
            ),
        )
        source = source.chunk(chunks='auto')

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        cached = workflow.run()

        # modify dataframe and load from cache
        original_source = source.copy(deep=True)
        source['E'] = [1, 2, 3]
        cached = workflow.run()

        # check returned data is a different object instance
        assert source is not cached

        # check data integrity
        xarray.testing.assert_identical(original_source, cached)

    def test_dataframe_with_units(self, tmp_path):
        path = tmp_path / 'cache.nc'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )
        source = source.pint.quantify(x='s', A='m')
        original = source.copy(deep=True)

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        cached = workflow.run()

        # modify dataframe and load from cache
        source['E'] = [1, 2, 3]
        cached = workflow.run()

        # check returned data is a different object instance
        assert source is not cached

        # check data integrity
        xarray.testing.assert_identical(original, cached)

        # check units
        assert cached.A.pint.units == pint.Unit('m')
        assert cached.B.pint.units is None
        assert cached.C.pint.units is None
        assert pint.Unit(cached.x.attrs['units']) == pint.Unit('s')

    def test_preserve_attrs(self, tmp_path):
        path = tmp_path / 'cache.h5'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3]),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                ),
            ),
            coords=dict(x=[3, 4, 5]),
        )
        source = source.pint.quantify(x='s', A='m')
        source.attrs.update(
            {
                'date': '2024-04-26',
                'inlet.flow_rate': '1.0L/min',
                'inlet.scale': 2.0,
            }
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        workflow.run()

        # load cached version (by running process again)
        cached = workflow.run()
        assert cached is not source

        # check data integrity
        xarray.testing.assert_identical(source, cached)

        # assert content
        assert source.attrs == cached.attrs

    def test_preserve_attrs_on_variables(self, tmp_path):
        path = tmp_path / 'cache.h5'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3], {'a_type': 'float'}),
                B=('x', ['aa', 'bb', 'cc'], {'´b_type': 'string'}),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                    {'c_type': 'time'},
                ),
            ),
            coords=dict(x=('x', [3, 4, 5], {'x_type': 'int'})),
        )
        source = source.pint.quantify(x='s', A='m')
        source.attrs.update(
            {
                'date': '2024-04-26',
                'inlet.flow_rate': '1.0L/min',
                'inlet.scale': 2.0,
            }
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        workflow.run()

        # load cached version (by running process again)
        cached = workflow.run()
        assert cached is not source

        # check data integrity
        xarray.testing.assert_identical(source, cached)

        # assert content
        assert source.attrs == cached.attrs

    def test_avoid_pint_quantify_on_load_if_no_pint_units_present(self, tmp_path):
        path = tmp_path / 'cache.h5'
        source = xr.Dataset(
            dict(
                A=('x', [1.1, 2.2, 3.3], {'a_type': 'float', 'units': 'm'}),
                B=('x', ['aa', 'bb', 'cc'], {'b_type': 'string'}),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                    {'c_type': 'time'},
                ),
            ),
            coords=dict(x=('x', [3, 4, 5], {'x_type': 'int', 'units': 's'})),
        )
        source.attrs.update(
            {
                'date': '2024-04-26',
                'inlet.flow_rate': '1.0L/min',
                'inlet.scale': 2.0,
            }
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        workflow.run()

        # load cached version (by running process again)
        cached = workflow.run()
        assert cached is not source

        # check data integrity
        xarray.testing.assert_identical(source, cached)

        # assert content
        assert source.attrs == cached.attrs

    def test_preserve_nested_dicts_in_attrs(self, tmp_path):
        path = tmp_path / 'cache.h5'
        source = xr.Dataset(
            dict(
                A=(
                    'x',
                    [1.1, 2.2, 3.3],
                    {
                        'a': '2024-04-26',
                        'b': {
                            'c': 1,
                            'd': 2.0,
                        },
                    },
                ),
                B=('x', ['aa', 'bb', 'cc']),
                C=(
                    'x',
                    pd.to_datetime(
                        [
                            '2024-01-16T10:05:28.537',
                            '2024-01-16T10:05:29.735',
                            '2024-01-16T10:05:30.935',
                        ]
                    ),
                ),
            ),
            coords=dict(
                x=(
                    'x',
                    [3, 4, 5],
                    {
                        'a': '2024-04-26',
                        'b': {
                            'c': 1,
                            'd': 2.0,
                        },
                    },
                )
            ),
        )
        source = source.pint.quantify(x='s', A='m')
        source.attrs.update(
            {
                'date': '2024-04-26',
                'inlet': {
                    'flow_rate': '1.0L/min',
                    'scale': 2.0,
                },
            }
        )

        workflow = ProcessNode(
            parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
            runner=XArrayFileCache(),
            params={
                'filename': PlainProcessParam(value=str(path)),
            },
        )

        # create cache
        assert not path.exists()
        workflow.run()

        # load cached version (by running process again)
        cached = workflow.run()
        assert cached is not source

        # check data integrity
        xarray.testing.assert_identical(source, cached)

        # assert content
        assert source.attrs == cached.attrs

    class TestDataArray:
        def test_cache_data_array(self, tmp_path):
            path = tmp_path / 'cache.h5'
            source = xr.DataArray(
                [1.1, 2.2, 3.3],
                coords=dict(x=[3, 4, 5]),
                name='A',
            )
            source = source.pint.quantify(x='s', A='m')
            source.attrs.update(
                {
                    'date': '2024-04-26',
                    'inlet.flow_rate': '1.0L/min',
                    'inlet.scale': 2.0,
                }
            )

            workflow = ProcessNode(
                parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
                runner=XArrayFileCache(data_structure='DataArray'),
                params={
                    'filename': PlainProcessParam(value=str(path)),
                },
            )

            # create cache
            assert not path.exists()
            workflow.run()

            # load cached version (by running process again)
            cached = workflow.run()
            assert cached is not source

            # check data integrity
            xarray.testing.assert_identical(source, cached)

            # assert content
            assert source.attrs == cached.attrs

            # assert name
            assert source.name == cached.name

        def test_cache_unnamed_data_array(self, tmp_path):
            path = tmp_path / 'cache.h5'
            source = xr.DataArray(
                [1.1, 2.2, 3.3],
                coords=dict(x=[3, 4, 5]),
            )
            source = source.pint.quantify(x='s', A='m')
            source.attrs.update(
                {
                    'date': '2024-04-26',
                    'inlet.flow_rate': '1.0L/min',
                    'inlet.scale': 2.0,
                }
            )

            workflow = ProcessNode(
                parent=ProcessNode(runner=DelegatedSource(delegate=lambda: source)),
                runner=XArrayFileCache(data_structure='DataArray'),
                params={
                    'filename': PlainProcessParam(value=str(path)),
                },
            )

            # create cache
            assert not path.exists()
            workflow.run()

            # load cached version (by running process again)
            cached = workflow.run()
            assert cached is not source

            # check data integrity
            xarray.testing.assert_identical(source, cached)

            # assert content
            assert source.attrs == cached.attrs

            # assert name
            assert source.name == cached.name

    class TestDataTree:
        def test_cache_datatree(self, tmp_path):
            path = tmp_path / 'cache.h5'
            source = xr.DataTree.from_dict(
                {
                    './': xr.Dataset(
                        {
                            'A': ('x', [1.1, 2.2, 3.3]),
                            'B': ('x', [1, 2, 3]),
                            'C': ('x', ['a', 'b', 'c']),
                        },
                        coords=dict(x=[3, 4, 5]),
                        attrs={
                            'date': '2024-04-26',
                            'inlet.flow_rate': '1.0L/min',
                            'inlet.scale': 2.0,
                        },
                    ),
                    './error': xr.Dataset(
                        {
                            'A': ('x', [0.1, 0.2, 0.3]),
                            'B': ('x', [0.01, 0.02, 0.03]),
                        },
                        coords=dict(x=[3, 4, 5]),
                        attrs={
                            'date': '2024-04-26',
                            'inlet.flow_rate': '1.0L/min',
                            'inlet.scale': 2.0,
                        },
                    ),
                }
            )

            # source = source.pint.quantify(x='s', A='m')

            workflow = rdm.Workflow.create(
                [
                    rdm.DelegatedSource(delegate=lambda: source),
                    (
                        rdm.xarrays.XArrayFileCache(data_structure='DataTree'),
                        dict(filename=str(path)),
                    ),
                ]
            )

            # create cache
            assert not path.exists()
            workflow.run()

            # load cached version (by running process again)
            cached = workflow.run()
            assert cached is not source

            # check data integrity
            xarray.testing.assert_identical(source, cached)

            # assert content
            assert source.attrs == cached.attrs

            # assert name
            assert source.name == cached.name

        def test_cache_datatree_with_units(self, tmp_path):
            path = tmp_path / 'cache.h5'
            source = xr.DataTree.from_dict(
                {
                    './': xr.Dataset(
                        {
                            'A': ('x', [1.1, 2.2, 3.3]),
                            'B': ('x', [1, 2, 3]),
                            'C': ('x', ['a', 'b', 'c']),
                        },
                        coords=dict(x=[3, 4, 5]),
                        attrs={
                            'date': '2024-04-26',
                            'inlet.flow_rate': '1.0L/min',
                            'inlet.scale': 2.0,
                        },
                    ).pint.quantify(x='s', A='m'),
                    './error': xr.Dataset(
                        {
                            'A': ('x', [0.1, 0.2, 0.3]),
                            'B': ('x', [0.01, 0.02, 0.03]),
                        },
                        coords=dict(x=[3, 4, 5]),
                        attrs={
                            'date': '2024-04-26',
                            'inlet.flow_rate': '1.0L/min',
                            'inlet.scale': 2.0,
                        },
                    ).pint.quantify(x='s', A='m', B='ppm'),
                }
            )

            # source = source.pint.quantify(x='s', A='m')

            workflow = rdm.Workflow.create(
                [
                    rdm.DelegatedSource(delegate=lambda: source),
                    (
                        rdm.xarrays.XArrayFileCache(data_structure='DataTree'),
                        dict(filename=str(path)),
                    ),
                ]
            )

            # create cache
            assert not path.exists()
            workflow.run()

            # load cached version (by running process again)
            cached = workflow.run()
            assert cached is not source

            # check data integrity
            xarray.testing.assert_identical(source, cached)

            # assert content
            assert source.attrs == cached.attrs

            # assert name
            assert source.name == cached.name
