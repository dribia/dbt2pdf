"""Test the manifest parsing version."""

from pathlib import Path
from unittest import mock

import pytest

from dbt2pdf.pdf import PDF
from dbt2pdf.schemas import ExtractedDescription
from dbt2pdf.warnings import NoFontFamily


@pytest.fixture
def _extracted_description():
    """Return a dummy extracted description."""
    return ExtractedDescription(
        name="Column 1", description="This is an example description for the column."
    )


@pytest.fixture
def _body():
    """Return a dummy body."""
    return """This is an example description for the model.
    Description: This is a description for the model.
    Columns:
    Arguments:
    """


@pytest.fixture
def _intro_text():
    """Return a dummy intro text."""
    return (
        "This document provides an overview of the DBT models and macros used in the "
        "project. It includes detailed descriptions of each model and macro, "
        "including the columns or arguments associated with them. The models section "
        "lists the models with their descriptions and column details. The macros "
        "section includes information about macros, their descriptions, and arguments."
    )


class TestPDF:
    """Test the PDF class."""

    def test_pdf_initialization(self):
        """Test PDF class initialization."""
        title = "Test Document"
        authors = ["Author One", "Author Two"]
        logos = [Path("/path/to/logo1.png"), Path("/path/to/logo2.png")]
        font_family = ""

        pdf = PDF(title=title, authors=authors, logos=logos, font_family=font_family)

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
        font_family = ""

        with pytest.raises(ValueError, match=r"Only two logos at maximum are allowed."):
            PDF(title=title, authors=authors, logos=logos, font_family=font_family)

    def test_pdf_initialization_invalid_font_family(self):
        """Test PDF class initialization with invalid font family."""
        title = "Test Document"
        authors = ["Author One", "Author Two"]
        logos = [Path("/path/to/logo1.png"), Path("/path/to/logo2.png")]
        font_family = "Patata"

        with pytest.raises(NoFontFamily):
            PDF(title=title, authors=authors, logos=logos, font_family=font_family)

    def test_header_first_page(self):
        """Test header when it is first page."""
        pdf = PDF(
            title="Test Document", authors=["Author One"], logos=[], font_family=""
        )

        pdf.is_first_page = True
        with mock.patch.object(pdf, "cell") as mock_cell:
            pdf.header()

            mock_cell.assert_not_called()

    def test_header_not_first_page(self):
        """Test header when it is not first page."""
        pdf = PDF(
            title="Test Document", authors=["Author One"], logos=[], font_family=""
        )

        pdf.add_page()
        pdf.is_first_page = False
        with mock.patch.object(pdf, "cell") as mock_cell:
            pdf.header()

            assert mock_cell.call_count == 1
            assert pdf.total_pages is None

        pdf.total_pages = 1
        with mock.patch.object(pdf, "cell") as mock_cell:
            pdf.header()

            assert mock_cell.call_count == 2

    def test_footer_first_page(self):
        """Test footer when it is first page."""
        pdf = PDF(
            title="Test Document", authors=["Author One"], logos=[], font_family=""
        )

        pdf.is_first_page = True
        with mock.patch.object(pdf, "set_text_color") as mock_set_text_color:
            pdf.footer()

            mock_set_text_color.assert_not_called()

    def test_footer_intro_page(self):
        """Test footer when it is intro page."""
        pdf = PDF(
            title="Test Document", authors=["Author One"], logos=[], font_family=""
        )

        pdf.is_intro_page = True
        with mock.patch.object(pdf, "set_text_color") as mock_set_text_color:
            pdf.footer()

            mock_set_text_color.assert_not_called()

    def test_footer_not_first_intro_page(self):
        """Test footer when it is not first page or intro page."""
        pdf = PDF(
            title="Test Document", authors=["Author One"], logos=[], font_family=""
        )

        pdf.is_first_page = False
        pdf.is_intro_page = False
        with mock.patch.object(pdf, "set_text_color") as mock_set_text_color:
            pdf.footer()

            assert mock_set_text_color.call_count == 1

        logos = [Path("/path/to/logo1.png"), Path("/path/to/logo2.png")]
        pdf_w_logos = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=logos,
            font_family="",
        )

        pdf_w_logos.is_first_page = False
        pdf_w_logos.is_intro_page = False
        with mock.patch.object(pdf_w_logos, "image") as mock_image:
            pdf_w_logos.footer()

            assert mock_image.call_count == 2

    def test_footer_not_first_intro_page_w_logos(self):
        """Test footer when it is not first page or intro page."""
        pdf1 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[Path("/path/to/logo1.png")],
            font_family="",
        )

        pdf1.is_first_page = False
        pdf1.is_intro_page = False
        with mock.patch.object(pdf1, "image") as mock_image:
            pdf1.footer()

            assert mock_image.call_count == 1

        pdf2 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[Path("/path/to/logo1.png"), Path("/path/to/logo2.png")],
            font_family="",
        )

        pdf2.is_first_page = False
        pdf2.is_intro_page = False
        with mock.patch.object(pdf2, "image") as mock_image:
            pdf2.footer()

            assert mock_image.call_count == 2

    def test_page_title(self):
        """Test page_title when no logos are provided."""
        pdf = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )
        pdf.page_title()

        assert pdf.is_intro_page is True
        assert pdf.is_first_page is False

    def test_page_title_w_logos(self):
        """Test page_title when logos are provided."""
        pdf1 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[Path("/path/to/logo1.png")],
            font_family="",
        )
        with mock.patch.object(pdf1, "image") as mock_image:
            pdf1.page_title()
            assert mock_image.call_count == 1

        pdf2 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[Path("/path/to/logo1.png"), Path("/path/to/logo1.png")],
            font_family="",
        )
        with mock.patch.object(pdf2, "image") as mock_image:
            pdf2.page_title()
            assert mock_image.call_count == 2

    def test_add_page_with_title(self):
        """Test chapter_title."""
        pdf = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )
        with mock.patch.object(pdf, "cell") as mock_cell:
            assert pdf.is_intro_page is True
            pdf.add_page()
            pdf.add_page_with_title("Test Chapter", level=0)
            assert pdf.is_intro_page is False

            mock_cell.assert_called_once()

    def test_add_intro(self, _intro_text):
        """Test chapter_title."""
        pdf = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )
        with mock.patch.object(pdf, "multi_cell") as mock_multi_cell:
            assert pdf.is_intro_page is True
            pdf.add_intro(intro_text=_intro_text)
            assert pdf.is_intro_page is False

            mock_multi_cell.assert_called_once()

    def test_create_table(self, _extracted_description):
        """Test create_table."""
        pdf1 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )

        with mock.patch.object(pdf1, "cell") as mock_cell:
            pdf1.add_page()
            pdf1.create_table(data=[_extracted_description], table_type="columns")

            assert mock_cell.call_count == 3

            pdf1.create_table(data=[_extracted_description], table_type="arguments")

            assert mock_cell.call_count == 6

            pdf1.create_table(data=[_extracted_description], table_type="invalid")

            assert mock_cell.call_count == 7

        pdf2 = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )

        with mock.patch.object(pdf2, "cell") as mock_cell:
            pdf2.add_page()
            pdf2.create_table(
                data=[_extracted_description, _extracted_description],
                table_type="columns",
            )

            assert mock_cell.call_count == 4

    def test_chapter_body(self, _extracted_description, _body):
        """Test chapter body function."""
        pdf = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )

        with mock.patch.object(pdf, "create_table") as mock_create_table:
            pdf.add_page()
            pdf.chapter_body(
                body=_body,
                column_descriptions=[_extracted_description],
                argument_descriptions=[_extracted_description],
            )

            assert mock_create_table.call_count == 2

        with mock.patch.object(pdf, "create_table") as mock_create_table:
            pdf.chapter_body(
                body=_body,
            )

            assert mock_create_table.call_count == 0

    def test_subchapter_title(self):
        """Test subchapter title function."""
        pdf = PDF(
            title="Test Document",
            authors=["Author One"],
            logos=[],
            font_family="",
        )

        with mock.patch.object(pdf, "cell") as mock_cell:
            pdf.add_page()
            pdf.subchapter_title(title="Subchapter", level=1)

            assert mock_cell.call_count == 1
