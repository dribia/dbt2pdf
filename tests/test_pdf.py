"""Test the manifest parsing version."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from dbt2pdf.pdf import PDF

runner = CliRunner()


class TestPDF:
    """Test the PDF class."""

    def test_pdf_initialization(self):
        """Test PDF class initialization."""
        title = "Test Document"
        authors = ["Author One", "Author Two"]
        logos = [Path("/path/to/logo1.png"), Path("/path/to/logo2.png")]

        pdf = PDF(title=title, authors=authors, logos=logos)

        assert pdf.title == title
        assert pdf.authors == authors
        assert pdf.logos == logos

    def test_pdf_initialization_invalid_logo_number(self):
        """Test PDF class initialization with invalid number of logos."""
        title = "Test Document"
        authors = ["Author One", "Author Two"]
        logos = [
            Path("/path/to/logo1.png"),
            Path("/path/to/logo2.png"),
            Path("/path/to/logo3.png"),
        ]

        with pytest.raises(ValueError, match="Only two logos at maximum are allowed."):
            PDF(title=title, authors=authors, logos=logos)
