from omegaconf import OmegaConf

from rdmlibpy.metadata.flattery import flatten, rebuild


class TestFlattenDict:
    def test_flatten_dict(self):
        nested = {'a': {'b': 1, 'c': {'d': 2, 'e': 3}}, 'f': 4}

        flattened = flatten(nested)

        assert flattened == {'a.b': 1, 'a.c.d': 2, 'a.c.e': 3, 'f': 4}

    def test_flatten_dict_with_custom_separator(self):
        nested = {'a': {'b': 1, 'c': {'d': 2, 'e': 3}}, 'f': 4}

        flattened = flatten(nested, sep=':')

        assert flattened == {'a:b': 1, 'a:c:d': 2, 'a:c:e': 3, 'f': 4}

    def test_flatten_omegaconf_mapping(self):
        nested = OmegaConf.create({'a': {'b': 1, 'c': {'d': 2, 'e': 3}}, 'f': 4})

        flattened = flatten(nested)

        assert flattened == {'a.b': 1, 'a.c.d': 2, 'a.c.e': 3, 'f': 4}


class TestRebuildDict:
    def test_rebuild_dict(self):
        flat = {'a.b': 1, 'a.c.d': 2, 'a.c.e': 3, 'f': 4}

        nested = rebuild(flat)

        assert nested == {'a': {'b': 1, 'c': {'d': 2, 'e': 3}}, 'f': 4}

    def test_rebuild_dict_with_custom_separator(self):
        flat = {'a:b': 1, 'a:c:d': 2, 'a:c:e': 3, 'f': 4}

        nested = rebuild(flat, sep=':')

        assert nested == {'a': {'b': 1, 'c': {'d': 2, 'e': 3}}, 'f': 4}
