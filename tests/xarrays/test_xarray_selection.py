from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from rdmlibpy.xarrays import XArraySelectTimespan
from rdmlibpy.xarrays import XArraySelectRange
from rdmlibpy.xarrays import XArraySelectVariable
from rdmlibpy.xarrays import XArraySelectIndexRange


class TestSelectTimespan:
    def test_create_loader(self):
        loader = XArraySelectTimespan()

        assert loader.name == 'xarray.select.timespan'
        assert loader.version == '1'

        assert loader.drop is True

    def test_timestamp_as_coord(self, data_path: Path):
        # create test data
        t0 = np.datetime64('2024-10-25T15:14:00', 'ns')
        dt = np.timedelta64(2, 's')
        N = 20
        source = xr.DataArray(
            np.arange(N), coords=dict(timestamp=[t0 + k * dt for k in np.arange(N)])
        )

        transform = XArraySelectTimespan()
        da = transform.run(
            source,
            'timestamp',
            start='2024-10-25T15:14:09',
            stop='2024-10-25T15:14:19',
        )

        assert len(da) == 5  # type: ignore

    def test_timestamp_as_var(self, data_path: Path):
        # create test data
        t0 = np.datetime64('2024-10-25T15:14:00', 'ns')
        dt = np.timedelta64(2, 's')
        N = 20
        source = xr.Dataset(
            dict(
                some_data=('x', np.arange(N)),
                time=('x', [t0 + k * dt for k in np.arange(N)]),
            ),
            coords=dict(x=np.arange(N)),
        )

        transform = XArraySelectTimespan()
        ds = transform.run(
            source,
            'time',
            start='2024-10-25T15:14:09',
            stop='2024-10-25T15:14:19',
        )

        assert len(ds.x) == 5  # type: ignore


class TestSelectRange:
    def test_create_loader(self):
        selector = XArraySelectRange()

        assert selector.name == 'xarray.select.range'
        assert selector.version == '1'

        assert selector.drop is True

    def test_range_as_coord(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(da) == 6  # type: ignore
        assert da.values == pytest.approx(np.arange(5, 11))
        assert da.x.values == pytest.approx(np.arange(5, 11))

    def test_range_as_var(self):
        # create test data
        N = 20
        source = xr.Dataset(
            dict(
                some_data=('x', np.arange(N)),
                other_data=('x', np.arange(N)),
            ),
            coords=dict(x=np.arange(N)),
        )

        transform = XArraySelectRange()
        ds = transform.run(
            source,
            'other_data',
            start=5,
            stop=10,
        )

        assert len(ds.x) == 6  # type: ignore
        assert ds.some_data.values == pytest.approx(np.arange(5, 11))
        assert ds.other_data.values == pytest.approx(np.arange(5, 11))
        assert ds.x.values == pytest.approx(np.arange(5, 11))

    def test_no_start(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=10,
        )

        assert len(da) == 11  # type: ignore
        assert da.values == pytest.approx(np.arange(0, 11))

    def test_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=10,
            stop=None,
        )

        assert len(da) == 10  # type: ignore
        assert da.values == pytest.approx(np.arange(10, 20))

    def test_no_start_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=None,
        )

        assert len(da) == N  # type: ignore
        assert da.values == pytest.approx(np.arange(N))

    def test_keep_attributes(self):
        # create test data
        N = 20
        source = xr.DataArray(
            np.arange(N),
            coords=dict(x=np.arange(N)),
            attrs=dict(test_attr="test_value"),
        )

        transform = XArraySelectRange()
        da = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(da) == 6  # type: ignore
        assert da.values == pytest.approx(np.arange(5, 11))
        assert da.x.values == pytest.approx(np.arange(5, 11))
        assert da.attrs.get('test_attr') == "test_value"

    def test_keep_dataset_attributes(self):
        # create test data
        N = 20
        some_values = np.random.rand(4, N)
        source = xr.Dataset(
            dict(
                some_data=(('y', 'x'), some_values),
                other_data=('x', np.arange(N)),
            ),
            coords=dict(x=np.arange(N), y=np.arange(4)),
            attrs=dict(dataset_attr="dataset_value"),
        )

        transform = XArraySelectRange()
        ds = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(ds.x) == 6  # type: ignore
        assert ds.attrs.get('dataset_attr') == "dataset_value"
        assert ds.some_data.values == pytest.approx(some_values[:, 5:11])
        assert ds.other_data.values == pytest.approx(np.arange(5, 11))
        assert ds.x.values == pytest.approx(np.arange(5, 11))

    def test_keep_dataarray_attributes_in_dataset(self):
        # create test data
        N = 20
        source = xr.Dataset(
            dict(
                some_data=(
                    'x',
                    np.arange(N),
                    dict(dataarray_attr="dataarray_value"),
                ),
                other_data=('x', np.arange(N)),
            ),
            coords=dict(x=np.arange(N)),
        )

        transform = XArraySelectRange()
        ds = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(ds.x) == 6  # type: ignore
        assert ds.some_data.attrs.get('dataarray_attr') == "dataarray_value"
        assert ds.some_data.values == pytest.approx(np.arange(5, 11))
        assert ds.other_data.values == pytest.approx(np.arange(5, 11))
        assert ds.x.values == pytest.approx(np.arange(5, 11))


class TestSelectVariable:
    def test_create_transform(self):
        selector = XArraySelectVariable()

        assert selector.name == 'xarray.select.variable'
        assert selector.version == '1'
        assert selector.keep_parent_attributes is False

    def test_variable_found(self):
        # create test data
        source = xr.Dataset(
            dict(
                var1=('x', np.arange(10)),
                var2=('x', np.arange(10, 20)),
            ),
            attrs=dict(global_attr="test_attr"),
        )

        transform = XArraySelectVariable()
        result = transform.run(source, 'var1')

        assert isinstance(result, xr.DataArray)
        assert result.name == 'var1'
        assert result.values == pytest.approx(np.arange(10))

    def test_variable_not_found(self):
        # create test data
        source = xr.Dataset(
            dict(
                var1=('x', np.arange(10)),
            )
        )

        transform = XArraySelectVariable()

        with pytest.raises(ValueError, match="Variable 'var2' not found in source."):
            transform.run(source, 'var2')

    def test_keep_parent_attributes(self):
        # create test data
        source = xr.Dataset(
            dict(
                var1=('x', np.arange(10)),
            ),
            attrs=dict(global_attr="test_attr"),
        )

        transform = XArraySelectVariable()
        transform.keep_parent_attributes = True
        result = transform.run(source, 'var1')

        assert isinstance(result, xr.DataArray)
        assert result.attrs.get('global_attr') == "test_attr"


class TestSelectIndexRange:
    def test_create_transform(self):
        selector = XArraySelectIndexRange()

        assert selector.name == 'xarray.select.index_range'
        assert selector.version == '1'

    def test_index_range(self):
        # create test data
        N = 20
        source = xr.DataArray(15 + np.arange(N), coords=dict(x=10 + np.arange(N)))

        transform = XArraySelectIndexRange()
        da = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(da) == 5  # type: ignore
        assert da.values == pytest.approx(15 + np.arange(5, 10))
        assert da.x.values == pytest.approx(10 + np.arange(5, 10))

    def test_no_start(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectIndexRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=10,
        )

        assert len(da) == 10  # type: ignore
        assert da.values == pytest.approx(np.arange(0, 10))
        assert da.x.values == pytest.approx(np.arange(0, 10))

    def test_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectIndexRange()
        da = transform.run(
            source,
            'x',
            start=10,
            stop=None,
        )

        assert len(da) == 10  # type: ignore
        assert da.values == pytest.approx(np.arange(10, 20))
        assert da.x.values == pytest.approx(np.arange(10, 20))

    def test_no_start_no_stop(self):
        # create test data
        N = 20
        source = xr.DataArray(np.arange(N), coords=dict(x=np.arange(N)))

        transform = XArraySelectIndexRange()
        da = transform.run(
            source,
            'x',
            start=None,
            stop=None,
        )

        assert len(da) == N  # type: ignore
        assert da.values == pytest.approx(np.arange(N))
        assert da.x.values == pytest.approx(np.arange(N))

    def test_keep_attributes(self):
        # create test data
        N = 20
        source = xr.DataArray(
            np.arange(N),
            coords=dict(x=np.arange(N)),
            attrs=dict(test_attr="test_value"),
        )

        transform = XArraySelectIndexRange()
        da = transform.run(
            source,
            'x',
            start=5,
            stop=10,
        )

        assert len(da) == 5  # type: ignore
        assert da.values == pytest.approx(np.arange(5, 10))
        assert da.x.values == pytest.approx(np.arange(5, 10))
        assert da.attrs.get('test_attr') == "test_value"
