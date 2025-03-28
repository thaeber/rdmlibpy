import re
from typing import Any

import numpy as np
from omegaconf import DictConfig, ListConfig, OmegaConf
from omegaconf.base import Box
from omegaconf.errors import OmegaConfBaseException


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


def _parse_time_delta_string(value: str):
    match = re.match(r'\s*(-?\d+)\s*(ms|us|ns|ps|fs|as|D|h|m|s)', value)
    if match:
        number, unit = match.groups()
        return np.timedelta64(number, unit)
    else:
        try:
            dt = np.timedelta64(value)
            if not np.isnat(dt):
                return dt
            else:
                raise ValueError(f'>{value}< is not a valid time delta: {dt}.')
        except ValueError:
            raise ValueError(f'>{value}< is not a valid time delta.')


def subtract_timedelta(timestamp: Any, value: str):
    is_string = isinstance(timestamp, str)
    if is_string:
        timestamp = np.datetime64(timestamp)
    delta = _parse_time_delta_string(value)
    t = timestamp - delta
    if is_string:
        return str(t)
    else:
        return t


def add_timedelta(timestamp: Any, value: str):
    is_string = isinstance(timestamp, str)
    if is_string:
        timestamp = np.datetime64(timestamp)
    delta = _parse_time_delta_string(value)
    t = timestamp + delta
    if is_string:
        return str(t)
    else:
        return t


def timedelta(t1: Any, t2: Any):
    return np.datetime64(t1) - np.datetime64(t2)


def register_custom_resolvers():
    OmegaConf.register_new_resolver('meta.get', get_metadata_property, replace=True)
    OmegaConf.register_new_resolver(
        'meta.subtract-timedelta', subtract_timedelta, replace=True
    )
    OmegaConf.register_new_resolver('meta.add-timedelta', add_timedelta, replace=True)
    OmegaConf.register_new_resolver('meta.timedelta', timedelta, replace=True)
