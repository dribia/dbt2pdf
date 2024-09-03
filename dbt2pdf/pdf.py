"""Module to define a DBT documentation PDF file class."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fpdf import FPDF

from dbt2pdf.font import find
from dbt2pdf.schemas import ExtractedDescription

# FONTS_PATH = Path("fonts")
# LOGOS_PATH = Path("logos")
TITLE = "DBT Documentation"


class PDF(FPDF):
    """Class to generate a PDF with the models and macros documentation."""

    def __init__(
        self, *, title: str, authors: list[str], font_family: str, **kwargs: Any
    ) -> None:
        """Initialize the PDF with custom margins and auto page breaks.

        Args:
            title: Document title (title page and headers).
            authors: List of authors to list them in the title page.
            font_family: Font family to use in the PDF document.
            **kwargs: Keyword arguments to the FPDF constructor.
        """
        super().__init__(**kwargs)
        # Document personalization
        self.title: str = title
        self.authors = authors

        # Document settings
        self.bottom_margin: int = 30
        self.set_auto_page_break(auto=True, margin=self.bottom_margin)
        self.is_first_page: bool = True
        self.is_intro_page: bool = True
        self.total_pages: int | None = None

        # Find Font objects by font_family
        self.font_family = font_family
        fonts = find(font_family)
        self.is_bold = False
        for _, font in fonts.items():
            if font.style.value == "B":
                self.is_bold = True

            self.add_font(family=font.family, style=font.style.value, fname=font.path)

        self.set_font(family=font_family, style="B")

    def header(self) -> None:
        """Add a header to the PDF."""
        if self.is_first_page:
            return
        self.set_font(family=self.font_family, size=10)
        self.set_text_color(r=54, g=132, b=235)
        self.cell(w=0, h=13, text=TITLE, border=0, align="L")
        y = self.get_y()

        # Get page number and total pages
        page_number = self.page_no()
        self.set_font(family=self.font_family, size=10)
        self.set_text_color(r=87, g=87, b=87)
        if self.total_pages is not None:
            self.set_x(190)  # Move to the right side
            self.cell(
                w=0, h=13, text=f"{page_number}/{self.total_pages}", border=0, align="R"
            )
        self.set_draw_color(r=169, g=169, b=169)
        self.set_y(y + 10)
        self.set_line_width(0.25)
        self.line(x1=15, y1=self.get_y(), x2=195, y2=self.get_y())

        self.ln(5)

    def footer(self) -> None:
        """Add a footer to the PDF."""
        if self.is_first_page or self.is_intro_page:
            return
        self.set_text_color(r=169, g=169, b=169)
        self.set_y(-15)
        # self.image(
        #     name=str(LOGOS_PATH / "logo_dribia.png"), x=165, y=self.get_y() - 5, w=30
        # )
        # self.image(
        #     name=str(LOGOS_PATH / "logo_client.png"), x=15, y=self.get_y() - 7, w=20
        # )

    def page_title(self) -> None:
        """Add a page title to the PDF."""
        self.add_page()
        self.is_first_page = False
        self.is_intro_page = True
        logo_width = 100
        page_width = self.w
        x_centered = (page_width - logo_width) / 2
        # self.image(
        #     name=str(LOGOS_PATH / "logo_dribia.png"), x=x_centered, y=55, w=logo_width
        # )

        self.ln(100)

        if self.is_bold:
            self.set_font(family=self.font_family, style="B", size=35)
        else:
            self.set_font(family=self.font_family, size=35)

        self.set_text_color(r=0, g=76, b=183)
        self.cell(w=0, h=10, text=self.title, border=0, align="C")

        logo_width = 40
        page_width = self.w
        x_centered = (page_width - logo_width) / 2  # noqa: F841
        # self.image(
        #     name=str(LOGOS_PATH / "logo_client.png"), x=x_centered, y=140, w=logo_width
        # )

        self.ln(80)

        if self.is_bold:
            self.set_font(family=self.font_family, style="B", size=14)
        else:
            self.set_font(family=self.font_family, size=14)

        self.set_text_color(r=0, g=0, b=78)
        self.cell(
            w=0, h=10, text=datetime.today().strftime("%Y-%m-%d"), border=0, align="C"
        )
        for author in self.authors:
            self.ln(7)
            self.cell(w=0, h=10, text=author, border=0, align="C")

    def chapter_title(self, title: str) -> None:
        """Add a chapter title to the PDF."""
        if self.is_bold:
            self.set_font(family=self.font_family, style="B", size=24)
        else:
            self.set_font(family=self.font_family, size=24)

        self.set_text_color(r=0, g=76, b=183)
        self.cell(w=0, h=10, text=title, border=0, align="L")
        self.ln(7)

    def subchapter_title(self, title: str) -> None:
        """Add a chapter title to the PDF."""
        self.ln(5)
        if self.is_bold:
            self.set_font(family=self.font_family, style="B", size=16)
        else:
            self.set_font(family=self.font_family, size=16)

        self.set_text_color(r=54, g=132, b=235)
        self.cell(w=0, h=10, text=title, border=0, align="L")
        self.ln(10)

    def chapter_body(
        self,
        body: str,
        column_descriptions: list[ExtractedDescription] | None = None,
        argument_descriptions: list[ExtractedDescription] | None = None,
    ) -> None:
        """Add a chapter body to the PDF."""
        self.set_font(family=self.font_family, size=11)
        self.set_text_color(r=0, g=0, b=0)

        lines = body.split("\n")
        for line in lines:
            if (
                line.startswith("Description")
                or line.startswith("Columns")
                or line.startswith("Arguments")
            ):
                if self.is_bold:
                    self.set_font(family=self.font_family, style="B", size=11)
                else:
                    self.set_font(family=self.font_family, size=11)

                self.set_text_color(r=54, g=132, b=235)
                self.cell(w=0, h=10, text=line, new_x="LMARGIN", new_y="TOP")
                self.ln(10)
                self.set_font(family=self.font_family, size=11)
                self.set_text_color(r=0, g=0, b=0)
            else:
                self.multi_cell(w=0, h=10, text=line, new_x="LMARGIN", new_y="TOP")
                self.ln(12)

        if column_descriptions:
            self.create_table(column_descriptions, table_type="columns")
        if argument_descriptions:
            self.create_table(argument_descriptions, table_type="arguments")

    def create_table(self, data: list[ExtractedDescription], table_type: str) -> None:
        """Create a table with the provided data."""
        col_widths = [80, 100]  # Width of columns
        line_height = self.font_size * 2.5  # Adjust line height based on font size
        if self.is_bold:
            self.set_font(family=self.font_family, style="B", size=11)
        else:
            self.set_font(family=self.font_family, size=11)

        self.set_fill_color(r=200, g=220, b=255)

        # Header
        if table_type == "columns":
            self.cell(
                w=col_widths[0],
                h=line_height,
                text="Column Name",
                border="T",
                fill=True,
            )
            self.cell(
                w=col_widths[1],
                h=line_height,
                text="Description",
                border="T",
                fill=True,
            )
        elif table_type == "arguments":
            self.cell(
                w=col_widths[0],
                h=line_height,
                text="Argument Name",
                border="T",
                fill=True,
            )
            self.cell(
                w=col_widths[1],
                h=line_height,
                text="Description",
                border="T",
                fill=True,
            )
        self.ln(line_height)
        self.set_font(family=self.font_family, size=11)

        for row in data:
            # Save the current X position
            x_start = self.get_x()
            y_start = self.get_y()

            self.cell(w=col_widths[0], h=line_height, text=row.name, border="T")
            self.set_x(x_start + col_widths[0])
            self.multi_cell(
                w=col_widths[1], h=line_height, text=row.description, border="T"
            )
            row_height = self.get_y() - y_start
            self.set_y(y_start + row_height)

    def add_page_with_title(self, title: str) -> None:
        """Add a page with title."""
        self.ln(10)
        self.is_intro_page = False
        self.chapter_title(title)

    def add_intro(self, intro_text: str) -> None:
        """Add introductory text to the PDF."""
        self.add_page()
        self.set_font(family=self.font_family, size=12)
        self.set_text_color(r=0, g=0, b=0)
        self.multi_cell(w=0, h=6, text=intro_text)
        self.is_intro_page = False
