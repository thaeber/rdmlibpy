from typing import Any, Dict, Mapping


def flatten(mapping: Mapping[str, Any], sep: str = '.'):
    def _flatten_dict(d: Mapping[str, Any], parent_key: str):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, Mapping):
                items.extend(_flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    return _flatten_dict(mapping, '')


def rebuild(mapping: Mapping[str, Any], sep: str = '.'):
    def _insert_key(key: str, value: Any, current: Dict[str, Any]):
        index = key.find(sep)
        if index == -1:
            # final level
            if key in current:
                raise ValueError(f'Key "{key}" already exists.')
            current[key] = value
        else:
            # go one level down
            level = key[:index]
            if (level in current) and (not isinstance(current[level], dict)):
                raise ValueError(f'Item at key "{level}" must be a dictionary.')
            elif level not in current:
                current[level] = dict()
            _insert_key(key[index + len(sep) :], value, current[level])

    result: Dict[str, Any] = {}
    for key, value in mapping.items():
        _insert_key(key, value, result)

    return result
