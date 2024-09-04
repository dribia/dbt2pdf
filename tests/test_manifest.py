"""Test the manifest parsing version."""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from dbt2pdf import manifest
from dbt2pdf.manifest import pydantic

runner = CliRunner()


class MockManifest:
    def parse_obj(self):
        """Mock the parse_obj method."""
        pass

    def model_validate(self):
        """Mock the model_validate method."""
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
