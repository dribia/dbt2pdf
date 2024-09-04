"""Test the manifest parsing version."""

import sys
from importlib import reload
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from dbt2pdf import manifest
from dbt2pdf.manifest import pydantic

runner = CliRunner()


class MockManifest:
    """Mock the Manifest class."""

    def parse_obj(self):
        """Mock the parse_obj method."""
        pass

    def model_validate(self):
        """Mock the model_validate method."""
        pass


class MockBaseModel:
    """Mock Pydantic BaseModel class."""

    pass


class TestManifest:
    """Test the manifest parsing version."""

    @patch.object(pydantic, "__version__", "1.X")
    @patch("dbt2pdf.manifest.Manifest.parse_obj")
    def test_parse_manifest_pydantic_compat_v1(
        self, mock_manifest_parsing_method: MagicMock
    ):
        """Manifest parsing function Pydantic compatibility."""
        # Set the version
        manifest.parse_manifest({})
        mock_manifest_parsing_method.assert_called_once_with({})

    @patch.object(pydantic, "__version__", "2.X")
    @patch("dbt2pdf.manifest.Manifest.model_validate")
    def test_parse_manifest_pydantic_compat_v2(
        self, mock_manifest_parsing_method: MagicMock
    ):
        """Manifest parsing function Pydantic compatibility."""
        # Set the version
        manifest.parse_manifest({})
        mock_manifest_parsing_method.assert_called_once_with({})

    @patch.object(pydantic, "__version__", "1.X")
    @patch("pydantic.BaseModel", new=MockBaseModel)
    def test_manifest_base_pydantic_compat_v1(self):
        """Manifest parsing function Pydantic compatibility."""
        # Set the version
        if "dbt2pdf.manifest" in sys.modules:
            del sys.modules["dbt2pdf.manifest"]
        import dbt2pdf.manifest

        reload(dbt2pdf.manifest)
        with pytest.raises(AttributeError):
            _ = dbt2pdf.manifest._BaseSchema.model_config
        assert isinstance(dbt2pdf.manifest._BaseSchema.Config, object)

    @patch.object(pydantic, "__version__", "2.X")
    @patch("pydantic.BaseModel", new=MockBaseModel)
    def test_manifest_base_pydantic_compat_v2(self):
        """Manifest parsing function Pydantic compatibility."""
        # Set the version
        if "dbt2pdf.manifest" in sys.modules:
            del sys.modules["dbt2pdf.manifest"]
        import dbt2pdf.manifest

        reload(dbt2pdf.manifest)
        assert isinstance(dbt2pdf.manifest._BaseSchema.model_config, dict)
