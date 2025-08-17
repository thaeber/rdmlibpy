import xarray as xr


class KeepAttributesContext:
    def __init__(self):
        self._previous_value = None

    def __enter__(self):
        self._previous_value = xr.get_options().get('keep_attrs', False)
        xr.set_options(keep_attrs=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        xr.set_options(keep_attrs=self._previous_value)
