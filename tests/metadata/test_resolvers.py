from typing import cast
import numpy as np
import pytest

from rdmlibpy.metadata import Metadata
from rdmlibpy.metadata import resolvers
import pint


class TestMetaGetResolver:
    def test_get_inherited_property(self):
        yaml = """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            data:
              - id: 2024-01-16A
                start: a1234
                steps: &steps
                - loader: tclogger@v1
                  params:
                    start: ${meta.get:start}
                - loader: mksftir@v1
                  params:
                    date: ${meta.get:date}
        """
        meta = Metadata.create(yaml)
        assert meta.data[0].steps[0].params.start == 'a1234'
        assert meta.data[0].steps[1].params.date == '2024-01-16'


class TestDatetimeStringParsing:
    def test_numpy_datetime64_resolution(self):
        func = resolvers.numpy_datetime64_resolution
        assert func(np.datetime64('2024')) == 'Y'
        assert func(np.datetime64('2024-01')) == 'M'
        assert func(np.datetime64('2024-01-16')) == 'D'
        assert func(np.datetime64('2024-01-16T12')) == 'h'
        assert func(np.datetime64('2024-01-16T12:03')) == 'm'
        assert func(np.datetime64('2024-01-16T12:03:02')) == 's'
        assert func(np.datetime64('2024-01-16T12:00:00')) == 's'
        assert func(np.datetime64('2024-01-16T12:00:00.123')) == 'ms'
        assert func(np.datetime64('2024-01-16T12:00:00.123456')) == 'us'
        assert func(np.datetime64('2024-01-16T12:00:00.123456789')) == 'ns'

    def test_numpy_datetime64_resolution_timedelta(self):
        func = resolvers.numpy_datetime64_resolution
        assert func(np.timedelta64(1, 'Y')) == 'Y'
        assert func(np.timedelta64(1, 'M')) == 'M'
        assert func(np.timedelta64(1, 'D')) == 'D'
        assert func(np.timedelta64(1, 'h')) == 'h'
        assert func(np.timedelta64(1, 'm')) == 'm'
        assert func(np.timedelta64(1, 's')) == 's'
        assert func(np.timedelta64(1, 'ms')) == 'ms'
        assert func(np.timedelta64(1, 'us')) == 'us'
        assert func(np.timedelta64(1, 'ns')) == 'ns'

    def test_numpy_datetime64_resolution_invalid(self):
        func = resolvers.numpy_datetime64_resolution
        with pytest.raises(ValueError):
            func(np.array(1.0))  # type: ignore

    def test_numpy_datetime64_resolution_to_pint_unit(self):
        func = resolvers.numpy_datetime64_resolution_to_pint_unit
        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)

        assert func('Y') == ureg('years')
        assert func('Y') == ureg('year')
        assert func('M') == ureg('months')
        assert func('W') == ureg('weeks')
        assert func('D') == ureg('days')
        assert func('h') == ureg('hours')
        assert func('m') == ureg('minutes')
        assert func('s') == ureg('seconds')
        assert func('ms') == ureg('milliseconds')
        assert func('us') == ureg('microseconds')
        assert func('µs') == ureg('microseconds')
        assert func('ns') == ureg('nanoseconds')
        assert func('ps') == ureg('picoseconds')
        assert func('fs') == ureg('femtoseconds')
        assert func('as') == ureg('attoseconds')

    def test_timedelta64_to_pint(self):
        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)

        assert resolvers.timedelta64_to_pint(np.timedelta64(1, 'Y')) == 1 * ureg.year

        timespan = resolvers.timedelta64_to_pint(np.timedelta64(104, 'ms'))
        assert timespan == ureg.Quantity(104, 'millisecond')
        assert timespan.magnitude == 104
        assert timespan.units == ureg.millisecond

        timespan = resolvers.timedelta64_to_pint(np.timedelta64(104, 'fs'))
        assert timespan == ureg.Quantity(104, 'femtosecond')
        assert timespan.magnitude == 104
        assert timespan.units == ureg.femtosecond

    def test_pint_to_timedelta64(self):
        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)

        assert resolvers.pint_to_timedelta64(1 * ureg.year) == np.timedelta64(1, 'Y')
        assert resolvers.pint_to_timedelta64(1.2 * ureg.day) == np.timedelta64(
            1728, 'm'
        )

        timespan = resolvers.pint_to_timedelta64(104 * ureg.ms)
        assert timespan == np.timedelta64(104, 'ms')

        timespan = resolvers.pint_to_timedelta64(104 * ureg.fs)
        assert timespan == np.timedelta64(104, 'fs')

        timespan = resolvers.pint_to_timedelta64(104.02 * ureg.ms)
        assert timespan == np.timedelta64(104020, 'us')

        timespan = resolvers.pint_to_timedelta64(104 * ureg.attoseconds)
        assert timespan == np.timedelta64(104, 'as')

        # the lowest possible resolution is 1 attoseconds
        timespan = resolvers.pint_to_timedelta64(104.045 * ureg.attoseconds)
        assert timespan == np.timedelta64(104, 'as')

    def test_parse_timespan_string(self):
        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)

        assert resolvers.parse_timespan_string('1min') == 1 * ureg.minute
        assert resolvers.parse_timespan_string('1 minute') == ureg.Quantity(1, 'minute')
        assert resolvers.parse_timespan_string('  1 min  ') == 1 * ureg.minute
        assert resolvers.parse_timespan_string('-1min') == -1 * ureg.minute
        assert resolvers.parse_timespan_string('-1 min') == -ureg.Quantity(1, 'minute')
        assert resolvers.parse_timespan_string('  -1 min  ') == -1 * ureg.minute

        assert resolvers.parse_timespan_string('1 day') == ureg.Quantity(1, 'day')
        assert resolvers.parse_timespan_string('1min') == ureg.Quantity(1, 'minute')
        assert resolvers.parse_timespan_string('2s') == ureg.Quantity(2, 'second')
        assert resolvers.parse_timespan_string('20ms') == ureg.Quantity(
            20, 'millisecond'
        )
        assert resolvers.parse_timespan_string('20us') == ureg.Quantity(
            20, 'microsecond'
        )
        assert resolvers.parse_timespan_string('20ns') == ureg.Quantity(
            20, 'nanosecond'
        )
        assert resolvers.parse_timespan_string('20ps') == ureg.Quantity(
            20, 'picosecond'
        )
        assert resolvers.parse_timespan_string('20fs') == ureg.Quantity(
            20, 'femtosecond'
        )
        assert resolvers.parse_timespan_string('20as') == ureg.Quantity(
            20, 'attosecond'
        )

        with pytest.raises(ValueError):
            resolvers.parse_timespan_string('')

        with pytest.raises(ValueError):
            resolvers.parse_timespan_string('   ')

        with pytest.raises(ValueError):
            resolvers.parse_timespan_string('m')

        with pytest.raises(ValueError):
            resolvers.parse_timespan_string('1Y')

        with pytest.raises(ValueError):
            resolvers.parse_timespan_string('1')


class TestMetaSubtractTimeDelta:
    def test_subtract_time_delta(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            start: ${meta.minus.timedelta:2024-01-16T12:00,12min}
            """
        )
        assert meta.start == '2024-01-16T11:48'

    def test_subtract_time_delta2(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            start: ${meta.minus.timedelta:2024-01-16T12:00,12ms}
            """
        )
        assert meta.start == '2024-01-16T11:59:59.988'

    def test_nested_resolvers(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            start: 2024-01-16T12:00
            data:
                - nested: ${meta.minus.timedelta:${meta.get:start},12min}
            """
        )
        assert meta.data[0].nested == '2024-01-16T11:48'


class TestMetaAddTimeDelta:
    def test_add_time_delta(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            start: ${meta.plus.timedelta:2024-01-16T12:00:00,12.5min}
            """
        )
        assert meta.start == '2024-01-16T12:12:30'


class TestMetaTimeDelta:
    def test_calculate_time_delta(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            delta: ${meta.timedelta:2024-01-16T12:00,2024-01-16T12:12}
            """
        )

        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)
        assert ureg(meta.delta) == ureg.Quantity(-12, 'minute')

    def test_nested_extrapolation(self):
        meta = Metadata.create(
            """
            date: 2024-01-16
            title: NH3 oxidation over Pt

            __timedelta__: ${meta.timedelta:2025-03-25T10:10:00,2025-03-25T10:00:00}

            start: 2025-03-25T10:25:00
            stop: 2025-03-25T10:35:02

            params:
                start: ${meta.plus.timedelta:${meta.get:start},${__timedelta__}}
                stop: ${meta.plus.timedelta:${meta.get:stop},${__timedelta__}}
            """
        )
        assert meta.params.start == '2025-03-25T10:35:00'
        assert meta.params.stop == '2025-03-25T10:45:02'
