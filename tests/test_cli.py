"""Test the Command Line Interface."""

import json
import sys
import tempfile
from importlib import reload
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from dbt2pdf.cli import app

runner = CliRunner()


class TestInit:
    """Test the module initialization and version information."""

    @patch("importlib.metadata.version")
    def test_version_output(self, mock_version):
        """Test `__version__` when the package is found."""
        # Set the version
        version = "12.13.14"
        mock_version.return_value = version

        # Reload the CLI
        if "dbt2pdf" in sys.modules:
            del sys.modules["dbt2pdf"]

        from dbt2pdf import cli

        reload(cli)

        # Run the CLI
        result = runner.invoke(app, ["--version"])

        # Assert the output
        assert result.exit_code == 0
        assert result.stdout.strip() == f"dbt2pdf, version {version}"


class TestSnapshotProcessing:
    """Test snapshot processing functionality."""

    @patch("dbt2pdf.cli.PDF")
    @patch("dbt2pdf.cli.parse_manifest")
    def test_snapshots_included_in_pdf(self, mock_parse_manifest, mock_pdf_class):
        """Test that snapshots are processed and included in PDF generation."""
        # Create mock manifest with snapshots
        mock_manifest = MagicMock()
        mock_manifest.nodes = {
            "model.project.test_model": MagicMock(
                name="test_model",
                description="Test model description",
                resource_type="model",
                columns={},
            ),
            "snapshot.project.test_snapshot": MagicMock(
                name="test_snapshot",
                description="Test snapshot description",
                resource_type="snapshot",
                columns={},
            ),
        }
        mock_manifest.macros = {}

        # Configure the MagicMock objects to return proper values
        mock_manifest.nodes["model.project.test_model"].name = "test_model"
        mock_manifest.nodes[
            "model.project.test_model"
        ].description = "Test model description"
        mock_manifest.nodes["model.project.test_model"].resource_type = "model"
        mock_manifest.nodes["model.project.test_model"].columns = {}

        mock_manifest.nodes["snapshot.project.test_snapshot"].name = "test_snapshot"
        mock_manifest.nodes[
            "snapshot.project.test_snapshot"
        ].description = "Test snapshot description"
        mock_manifest.nodes["snapshot.project.test_snapshot"].resource_type = "snapshot"
        mock_manifest.nodes["snapshot.project.test_snapshot"].columns = {}

        mock_parse_manifest.return_value = mock_manifest

        # Create temporary manifest file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({}, f)
            temp_manifest_path = f.name

        # Mock PDF instance
        mock_pdf_instance = MagicMock()
        mock_pdf_instance.page_no.return_value = 5
        mock_pdf_instance.create_toc.return_value = MagicMock(pages=2)
        mock_pdf_class.return_value = mock_pdf_instance

        try:
            # Run CLI command
            result = runner.invoke(
                app,
                [
                    "generate",
                    "test.pdf",
                    "--manifest-path",
                    temp_manifest_path,
                    "--title",
                    "Test Doc",
                ],
            )

            # Verify snapshots are processed
            if result.exit_code != 0:
                print(f"CLI failed with exit code {result.exit_code}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
            assert result.exit_code == 0

            # Check that PDF methods were called for snapshots
            snapshot_title_calls = [
                call
                for call in mock_pdf_instance.add_page_with_title.call_args_list
                if call[1]["title"] == "Snapshots"
            ]
            assert (
                len(snapshot_title_calls) >= 1
            )  # Should be called for both temp and final PDF
        finally:
            # Clean up temporary file
            Path(temp_manifest_path).unlink(missing_ok=True)
