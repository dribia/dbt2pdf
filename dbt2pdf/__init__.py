"""Dbt2Pdf."""

from importlib.metadata import PackageNotFoundError, version

from . import manifest

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__", "manifest"]
