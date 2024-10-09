"""Test the module initialization and version information."""

import sys
from importlib import reload
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch


class TestInit:
    """Test the module initialization and version information."""

    @patch("importlib.metadata.version", side_effect=PackageNotFoundError)
    def test_version_not_found(self, mock_version):
        """Test `__version__` when the package is not found."""
        if "dbt2pdf" in sys.modules:
            del sys.modules["dbt2pdf"]

        import dbt2pdf

        reload(dbt2pdf)
        assert dbt2pdf.__version__ == "unknown"

    @patch("importlib.metadata.version")
    def test_version_found(self, mock_version):
        """Test `__version__` when the package is found."""
        mock_version.return_value = "0.1.0"
        if "dbt2pdf" in sys.modules:
            del sys.modules["dbt2pdf"]

        import dbt2pdf

        reload(dbt2pdf)
        assert dbt2pdf.__version__ == "0.1.0"
