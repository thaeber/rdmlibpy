import pytest
from rdmlibpy.common import ScalarSource


class TestScalarSource:
    def setup_method(self):
        self.scalar_source = ScalarSource()

    def test_run_with_value(self):
        result = self.scalar_source.run(value=42)
        assert result == 42

    def test_run_without_value(self):
        self.scalar_source.value = 100  # Set the default value
        result = self.scalar_source.run()
        assert result == 100

    def test_run_without_value_and_no_default(self):
        self.scalar_source.value = None  # Ensure no default value is set
        result = self.scalar_source.run()
        assert result is None
