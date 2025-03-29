import re
from typing import Any, cast

import numpy as np
import pint
from omegaconf import DictConfig, ListConfig, OmegaConf
from omegaconf.base import Box
from omegaconf.errors import OmegaConfBaseException
from pint.facets.plain import PlainQuantity


def _get_inherited_property(key, node: Box, *, default=None):
    parent = node._get_parent()
    if (parent is not None) and (isinstance(parent, (DictConfig, ListConfig))):
        try:
            return parent[key]
        except OmegaConfBaseException:
            return _get_inherited_property(key, parent, default=default)
    else:
        return default


def get_metadata_property(name, *, _parent_):
    return _get_inherited_property(name, _parent_)


def numpy_datetime64_resolution(value: np.datetime64 | np.timedelta64) -> str:
    regex = re.compile(r'^[^\[]+\[([^\]]+)\]$')
    s = str(value.dtype)
    match = regex.match(s)
    if match is None:
        raise ValueError(f'Could not parse time resolution from {s}')
    else:
        return match.group(1)


_datetime64_resolution_mapping = {
    'Y': 'years',
    'M': 'months',
    'W': 'weeks',
    'D': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds',
    'ms': 'milliseconds',
    'us': 'microseconds',
    'µs': 'microseconds',
    'ns': 'nanoseconds',
    'ps': 'picoseconds',
    'fs': 'femtoseconds',
    'as': 'attoseconds',
}


def numpy_datetime64_resolution_to_pint_unit(value: str):
    ureg = pint.application_registry.get()
    ureg = cast(pint.UnitRegistry, ureg)

    if value in _datetime64_resolution_mapping:
        return ureg.Unit(_datetime64_resolution_mapping[value])
    else:
        raise ValueError(f'Could not convert {value} to a valid time unit.')


def timedelta64_to_pint(value: np.timedelta64):
    ureg = pint.application_registry.get()
    ureg = cast(pint.UnitRegistry, ureg)
    np_unit = numpy_datetime64_resolution(value)
    pint_unit = numpy_datetime64_resolution_to_pint_unit(np_unit)
    return ureg.Quantity(value / np.timedelta64(1, np_unit), pint_unit)


def pint_to_timedelta64(value: PlainQuantity):
    ureg = pint.application_registry.get()
    ureg = cast(pint.UnitRegistry, ureg)

    for np_unit, pint_unit in _datetime64_resolution_mapping.items():
        converted = value.m_as(pint_unit)
        eps = np.spacing(converted)
        if converted - int(converted) < 2 * eps:
            break
    return np.timedelta64(int(converted), np_unit)


def parse_timespan_string(value: str):
    try:
        ureg = pint.application_registry.get()
        ureg = cast(pint.UnitRegistry, ureg)
        timespan = ureg.Quantity(value)
        if timespan.check('[time]'):
            return timespan
    except (ValueError, AssertionError, pint.UndefinedUnitError):
        pass
    raise ValueError(f'>{value}< is not a valid time span.')


def add_timespan(date_str: str, value: str):
    timestamp = np.datetime64(date_str)
    delta = parse_timespan_string(value)
    t = timestamp + pint_to_timedelta64(delta)
    return str(t)


def subtract_timespan(date_str: str, value: str):
    timestamp = np.datetime64(date_str)
    delta = parse_timespan_string(value)
    t = timestamp - pint_to_timedelta64(delta)
    return str(t)


def timedelta(t1: Any, t2: Any):
    dt = np.datetime64(t1) - np.datetime64(t2)

    ureg = pint.application_registry.get()
    ureg = cast(pint.UnitRegistry, ureg)
    converted = timedelta64_to_pint(dt)  # type: ignore
    return f'{converted}'


def register_custom_resolvers():
    OmegaConf.register_new_resolver(
        'meta.get',
        get_metadata_property,
        replace=True,
    )
    OmegaConf.register_new_resolver(
        'meta.plus.timedelta',
        add_timespan,
        replace=True,
    )
    OmegaConf.register_new_resolver(
        'meta.minus.timedelta',
        subtract_timespan,
        replace=True,
    )
    OmegaConf.register_new_resolver(
        'meta.timedelta',
        timedelta,
        replace=True,
    )
