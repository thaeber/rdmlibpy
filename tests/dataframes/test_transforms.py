from pathlib import Path

import numpy as np
import pandas as pd
import pandas._testing as tm
import pint_pandas

import pytest
from rdmlibpy.dataframes import (
    DataFrameAttributes,
    DataFrameFillNA,
    DataFrameJoin,
    DataFrameSetIndex,
    DataFrameTimeOffset,
    DataFrameUnits,
)
from rdmlibpy.loaders import ChannelTCLoggerLoader


class TestDataFrameJoin:
    def test_create_loader(self):
        transform = DataFrameJoin()

        assert transform.name == 'dataframe.join'
        assert transform.version == '1'

    def _get_test_data(self):
        left = pd.DataFrame(
            data=dict(
                A=[0, 2, 4, 6, 8, 10, 12],
                B=[0, 1, 2, 3, 4, 5, 6],
            ),
            dtype=np.float64,
        ).set_index('A')
        right = pd.DataFrame(
            data=dict(
                A=[0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12],
                C=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            ),
            dtype=np.float64,
        ).set_index('A')
        return left, right

    def test_join_outer_with_interpolation(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right, interpolate=True)

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 1.5, 2, 3, 4, 4.5, 6, 7.5, 8, 9, 10, 10.5, 12]
        assert np.allclose(
            df.B,
            [0, 0.75, 1, 1.5, 2, 2.25, 3, 3.75, 4, 4.5, 5, 5.25, 6],
            equal_nan=True,
        )
        assert np.allclose(
            df.C,
            [0, 1, 1 + 1 / 3, 2, 2 + 2 / 3, 3, 4, 5, 5 + 1 / 3, 6, 6 + 2 / 3, 7, 8],
            equal_nan=True,
        )

    def test_join_outer(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right)

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 1.5, 2, 3, 4, 4.5, 6, 7.5, 8, 9, 10, 10.5, 12]
        assert np.allclose(
            df.B,
            [0, np.nan, 1, np.nan, 2, np.nan, 3, np.nan, 4, np.nan, 5, np.nan, 6],
            equal_nan=True,
        )
        assert np.allclose(
            df.C,
            [0, 1, np.nan, 2, np.nan, 3, 4, 5, np.nan, 6, np.nan, 7, 8],
            equal_nan=True,
        )

    def test_join_right_with_interpolation(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right, how='right', interpolate=True)

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12]
        assert np.allclose(
            df.B,
            [0, 0.75, 1.5, 2.25, 3, 3.75, 4.5, 5.25, 6],
            equal_nan=True,
        )
        assert list(df.C) == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_join_right(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right, how='right')

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12]
        assert np.allclose(
            df.B,
            [0, np.nan, np.nan, np.nan, 3, np.nan, np.nan, np.nan, 6],
            equal_nan=True,
        )
        assert list(df.C) == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def test_join_left_with_interpolation(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right, how='left', interpolate=True)

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 2, 4, 6, 8, 10, 12]
        assert list(df.B) == [0, 1, 2, 3, 4, 5, 6]
        assert np.allclose(
            df.C, [0, 1 + 1 / 3, 2 + 2 / 3, 4, 5 + 1 / 3, 6 + 2 / 3, 8], equal_nan=True
        )

    def test_join_left(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()

        df = transform.run(left, right, how='left')

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 2, 4, 6, 8, 10, 12]
        assert list(df.B) == [0, 1, 2, 3, 4, 5, 6]
        assert np.allclose(
            df.C, [0, np.nan, np.nan, 4, np.nan, np.nan, 8], equal_nan=True
        )

    def test_join_pintarray_with_interpolation(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()
        right['C'] = pint_pandas.PintArray(right['C'], dtype='pint[m]')

        df = transform.run(left, right, how='left', interpolate=True)

        assert isinstance(df, pd.DataFrame)
        assert list(df.index) == [0, 2, 4, 6, 8, 10, 12]
        assert list(df.B) == [0, 1, 2, 3, 4, 5, 6]
        assert df.C.dtype == 'pint[m][float64]'
        assert np.allclose(
            df.C.pint.m,
            [0, 1 + 1 / 3, 2 + 2 / 3, 4, 5 + 1 / 3, 6 + 2 / 3, 8],
            equal_nan=True,
        )

    def test_ignore_nonnumeric_on_interpolate(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()
        right['C'] = pint_pandas.PintArray(right['C'], dtype='pint[m]')
        right['obj'] = [
            'start',
            'on',
            np.nan,
            np.nan,
            'off',
            np.nan,
            'on',
            np.nan,
            999,
        ]

        df = transform.run(left, right, how='left', interpolate=True)
        assert list(df['obj']) == ['start', np.nan, np.nan, 'off', np.nan, np.nan, 999]

    def test_ffill_nonnumeric_on_interpolate(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()
        right['C'] = pint_pandas.PintArray(right['C'], dtype='pint[m]')
        right['obj'] = [
            np.nan,
            'on',
            np.nan,
            np.nan,
            'off',
            np.nan,
            'on',
            np.nan,
            np.nan,
        ]

        df = transform.run(
            left, right, how='left', interpolate=True, non_numeric='fill forward'
        )
        assert list(df['obj']) == [np.nan, 'on', 'on', 'off', 'off', 'on', 'on']

    def test_bfill_nonnumeric_on_interpolate(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()
        right['C'] = pint_pandas.PintArray(right['C'], dtype='pint[m]')
        right['obj'] = [
            np.nan,
            'on',
            np.nan,
            np.nan,
            'off',
            np.nan,
            'on',
            np.nan,
            np.nan,
        ]

        df = transform.run(
            left, right, how='left', interpolate=True, non_numeric='fill backward'
        )
        assert list(df['obj']) == ['on', 'off', 'off', 'off', 'on', np.nan, np.nan]

    def test_raise_on_nonnumeric_on_interpolate(self):
        transform = DataFrameJoin()
        left, right = self._get_test_data()
        right['C'] = pint_pandas.PintArray(right['C'], dtype='pint[m]')
        right['obj'] = [
            'start',
            'on',
            np.nan,
            np.nan,
            'off',
            np.nan,
            'on',
            np.nan,
            999,
        ]

        with pytest.raises(ValueError):
            transform.run(
                left, right, how='left', interpolate=True, non_numeric='raise'
            )


class TestDataFrameSetIndex:
    def test_create_loader(self):
        transform = DataFrameSetIndex()

        assert transform.name == 'dataframe.setindex'
        assert transform.version == '1'

    def test_process(self, data_path: Path):
        loader = ChannelTCLoggerLoader()
        df = loader.run(
            source=data_path / 'ChannelV2TCLog/2024-01-16T11-26-54.csv',
        )
        assert isinstance(df, pd.DataFrame)

        transform = DataFrameSetIndex()
        df = transform.run(
            df,
            index_var=['timestamp'],
        )

        assert len(df) == 10  # type: ignore
        assert df.index.name == 'timestamp'


class TestDataFrameFillNA:
    def test_create_instance(self):
        transform = DataFrameFillNA()

        assert transform.name == 'dataframe.fillna'
        assert transform.version == '1'

    def test_process(self):
        transform = DataFrameFillNA()
        df = pd.DataFrame(dict(A=[1, 2, 3, 4, 5], B=[1.0, np.nan, np.nan, 4.0, np.nan]))

        filled = transform.run(df)
        assert list(filled.A) == [1, 2, 3, 4, 5]
        assert list(filled.B) == [1.0, 1.0, 1.0, 4.0, 4.0]

    def test_forward(self):
        transform = DataFrameFillNA()
        df = pd.DataFrame(dict(A=[1, 2, 3, 4, 5], B=[1.0, np.nan, np.nan, 4.0, np.nan]))

        filled = transform.run(df, method='forward')
        assert list(filled.A) == [1, 2, 3, 4, 5]
        assert list(filled.B) == [1.0, 1.0, 1.0, 4.0, 4.0]

    def test_backward(self):
        transform = DataFrameFillNA()
        df = pd.DataFrame(dict(A=[1, 2, 3, 4, 5], B=[1.0, np.nan, np.nan, 4.0, 5.0]))

        filled = transform.run(df, method='backward')
        assert list(filled.A) == [1, 2, 3, 4, 5]
        assert list(filled.B) == [1.0, 4.0, 4.0, 4.0, 5.0]


class TestDataFrameUnits:
    def test_create_loader(self):
        transform = DataFrameUnits()

        assert transform.name == 'dataframe.units'
        assert transform.version == '1'

    def test_process(self, data_path: Path):
        loader = ChannelTCLoggerLoader()
        df = loader.run(
            source=data_path / 'ChannelV2TCLog/2024-01-16T11-26-54.csv',
        )
        assert isinstance(df, pd.DataFrame)
        df = df.set_index('timestamp')
        df = df[['sample-downstream', 'inlet', 'outlet']]

        transform = DataFrameUnits()
        df = transform.run(
            df,
            units={'sample-downstream': 'K'},
        )
        assert df['sample-downstream'].dtype == 'pint[K][float64]'
        assert df['inlet'].dtype == 'float64'
        assert df['outlet'].dtype == 'float64'

    def test_process_with_default(self, data_path: Path):
        loader = ChannelTCLoggerLoader()
        df = loader.run(
            source=data_path / 'ChannelV2TCLog/2024-01-16T11-26-54.csv',
        )
        assert isinstance(df, pd.DataFrame)
        df = df.set_index('timestamp')
        df = df[['sample-downstream', 'inlet', 'outlet']]

        transform = DataFrameUnits()
        df = transform.run(
            df,
            units={'sample-downstream': 'K'},
            default_unit='degC',
        )
        assert df['sample-downstream'].dtype == 'pint[K][float64]'
        assert df['inlet'].dtype == 'pint[degC][float64]'
        assert df['outlet'].dtype == 'pint[degC][float64]'


class TestDataFrameAttributes:
    def test_create(self):
        process = DataFrameAttributes()

        assert process.name == 'dataframe.set.attrs'

    def test_add_attributes(self):
        df = pd.DataFrame(
            data=dict(
                A=[1.1, 2.2, 3.3],
                B=['aa', 'bb', 'cc'],
            ),
        )

        process = DataFrameAttributes()
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
        actual = process.run(df, **attrs)

        # check that run returns the same instance
        assert actual is df
        tm.assert_frame_equal(actual, df)

        assert actual.attrs == attrs

    def test_makes_deep_copy_of_parameters(self):
        df = pd.DataFrame(
            data=dict(
                A=[1.1, 2.2, 3.3],
                B=['aa', 'bb', 'cc'],
            ),
        )

        process = DataFrameAttributes()
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
        actual = process.run(df, **attrs)

        # check that attributes are equal
        assert actual.attrs == attrs

        # modify source dictionary and check again; now the
        # dictionaries should not be equal
        attrs['A4']['B4']['C4'] = 'test'  # type: ignore
        assert not (dict(actual.attrs) == dict(attrs))


class TestDataFrameTimeOffset:
    def test_create(self):
        process = DataFrameTimeOffset()

        assert process.name == 'dataframe.timeoffset'
        assert process.version == '1'

    def test_apply_offset_as_string(self):
        source = pd.DataFrame(
            dict(
                timestamp=[
                    np.datetime64('2024-11-19T16:17:15'),
                    np.datetime64('2024-11-19T16:23:30'),
                    np.datetime64('2024-11-19T16:50:45'),
                ],
                A=[1, 2, 3],
            )
        )

        df = DataFrameTimeOffset().run(source, offset='-10s', column='timestamp')

        assert list(df.timestamp) == [
            np.datetime64('2024-11-19T16:17:05'),
            np.datetime64('2024-11-19T16:23:20'),
            np.datetime64('2024-11-19T16:50:35'),
        ]

    def test_apply_offset_as_string_with_fractional_seconds(self):
        source = pd.DataFrame(
            dict(
                timestamp=[
                    np.datetime64('2024-11-19T16:17:15'),
                    np.datetime64('2024-11-19T16:23:30'),
                    np.datetime64('2024-11-19T16:50:45'),
                ],
                A=[1, 2, 3],
            )
        )

        df = DataFrameTimeOffset().run(source, offset='-9.4s', column='timestamp')

        assert list(df.timestamp) == [
            np.datetime64('2024-11-19T16:17:05.6'),
            np.datetime64('2024-11-19T16:23:20.6'),
            np.datetime64('2024-11-19T16:50:35.6'),
        ]

    def test_apply_offset_without_column(self):
        source = pd.DataFrame(
            dict(
                timestamp=[
                    np.datetime64('2024-11-19T16:17:15'),
                    np.datetime64('2024-11-19T16:23:30'),
                    np.datetime64('2024-11-19T16:50:45'),
                ],
                A=[1, 2, 3],
            )
        )

        df = DataFrameTimeOffset().run(source, offset='-9.4s')

        assert df is source

    def test_apply_offset_without_offset(self):
        source = pd.DataFrame(
            dict(
                timestamp=[
                    np.datetime64('2024-11-19T16:17:15'),
                    np.datetime64('2024-11-19T16:23:30'),
                    np.datetime64('2024-11-19T16:50:45'),
                ],
                A=[1, 2, 3],
            )
        )

        df = DataFrameTimeOffset().run(source, column='timestamp')

        assert df is source
