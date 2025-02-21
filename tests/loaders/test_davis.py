from rdmlibpy.loaders import DavisImageSetLoader


class TestDavisImageSet:
    def test_create_loader(self):
        loader = DavisImageSetLoader()

        assert loader.name == 'davis.image_set'
        assert loader.version == '1'

    def test_dimensions(self, data_path):
        loader = DavisImageSetLoader()

        images = loader.run(data_path / 'davis' / 'SimpleImageSet')

        assert list(images.dims) == ['buffer', 'frame', 'z', 'y', 'x']
        assert len(images.buffer) == 10
        assert len(images.frame) == 1
        assert len(images.z) == 1
        assert len(images.y) == 250
        assert len(images.x) == 2560

    def test_dimensions_with_squeeze(self, data_path):
        loader = DavisImageSetLoader()

        images = loader.run(data_path / 'davis' / 'SimpleImageSet', squeeze=True)

        assert list(images.dims) == ['buffer', 'y', 'x']
        assert len(images.buffer) == 10
        assert len(images.y) == 250
        assert len(images.x) == 2560
