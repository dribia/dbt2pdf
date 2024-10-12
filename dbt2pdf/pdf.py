"""Module to define a DBT documentation PDF file class."""

from __future__ import annotations

import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fpdf import FPDF

from dbt2pdf.font import find
from dbt2pdf.schemas import ExtractedDescription, TableOfContents, TableOfContentsEntry
from dbt2pdf.warnings import NoFontFamily, NoRegularStyle


class PDF(FPDF):
    """Class to generate a PDF with the models and macros documentation."""

    def __init__(
        self,
        *,
        title: str,
        authors: list[str],
        logos: list[Path],
        font_family: str,
        **kwargs: Any,
    ) -> None:
        """Initialize the PDF with custom margins and auto page breaks.

        Args:
            title: Document title (title page and headers).
            authors: List of authors to list them in the title page.
            logos: List of paths to logos (max 2).
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
        self.bold_style: Literal["", "B"] = ""

        if self.font_family != "":
            fonts = find(font_family)

            if not fonts:
                self.set_font("Times")
                self.bold_style = "B"
                warnings.warn(
                    message=(
                        f"No fonts having supported styles found with family "
                        f"'{font_family}'. Setting font to default."
                    ),
                    category=NoFontFamily,
                    stacklevel=1,
                )
            elif not any(font.style.value == "" for _, font in fonts.items()):
                self.set_font("Times")
                self.bold_style = "B"
                warnings.warn(
                    message=(
                        "No Regular style for the picked font. "
                        "Setting font to default."
                    ),
                    category=NoRegularStyle,
                    stacklevel=1,
                )
            else:
                for _, font in fonts.items():
                    # Add regular font style.
                    if font.style.value == "":
                        self.add_font(
                            family=self.font_family, style="", fname=font.path
                        )

                    # Add bold style if available.
                    if font.style.value == "B":
                        self.bold_style = "B"
                        self.add_font(
                            family=self.font_family,
                            style=self.bold_style,
                            fname=font.path,
                        )
        else:
            self.set_font("Times")
            self.bold_style = "B"

        self.logos = logos
        if len(logos) > 2:
            raise ValueError("Only two logos at maximum are allowed.")

        # Keep track sections for ToC
        self.sections: list = []

    def add_section_toc(self, title, level=0):
        """Adds a section with a title, its level and page number."""
        self.sections.append((title, level, self.page_no()))

    def header(self) -> None:
        """Add a header to the PDF."""
        if self.is_first_page:
            return
        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=10)
        self.set_text_color(r=54, g=132, b=235)
        self.cell(w=0, h=13, text=self.title, border=0, align="L")
        y = self.get_y()

        # Get page number and total pages
        page_number = self.page_no()
        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=10)
        self.set_text_color(r=87, g=87, b=87)
        if self.total_pages is not None:
            self.set_x(190)  # Move to the right side
            self.cell(
                w=0,
                h=13,
                text=f"{page_number}/{self.total_pages}",
                border=0,
                align="R",
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
        if len(self.logos) > 0:
            self.image(name=self.logos[0], x=165, y=self.get_y() - 10, w=30)
        if len(self.logos) > 1:
            self.image(name=self.logos[1], x=15, y=self.get_y() - 10, w=30)

    def page_title(self) -> None:
        """Add a page title to the PDF."""
        self.add_page()
        self.is_first_page = False
        self.is_intro_page = True
        logo_width = 100
        page_width = self.w
        x_centered = (page_width - logo_width) / 2
        if len(self.logos) > 0:
            self.image(name=self.logos[0], x=x_centered, y=55, w=logo_width)

        self.ln(100)

        if self.font_family != "":
            self.set_font(family=self.font_family, style=self.bold_style, size=35)

        self.set_text_color(r=0, g=76, b=183)
        self.cell(w=0, h=10, text=self.title, border=0, align="C")

        logo_width = 40
        page_width = self.w
        x_centered = (page_width - logo_width) / 2  # noqa: F841
        if len(self.logos) > 1:
            self.image(name=self.logos[1], x=x_centered, y=140, w=logo_width)

        self.ln(80)

        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=14)

        self.set_text_color(r=0, g=0, b=78)
        self.cell(
            w=0, h=10, text=datetime.today().strftime("%Y-%m-%d"), border=0, align="C"
        )
        self.ln(7)
        for author in self.authors:
            self.ln(7)
            self.cell(w=0, h=10, text=author, border=0, align="C")

    def chapter_title(self, title: str) -> None:
        """Add a chapter title to the PDF."""
        if self.font_family != "":
            self.set_font(family=self.font_family, style=self.bold_style, size=24)

        self.set_text_color(r=0, g=76, b=183)
        self.cell(w=0, h=10, text=title, border=0, align="L")
        self.ln(7)

    def subchapter_title(self, title: str, level: int | None) -> None:
        """Add a chapter title to the PDF."""
        self.ln(5)
        if self.font_family != "":
            self.set_font(family=self.font_family, style=self.bold_style, size=16)

        self.set_text_color(r=54, g=132, b=235)
        self.start_section(title)
        self.cell(w=0, h=10, text=title, border=0, align="L")
        self.ln(10)

        if level is not None:
            self.add_section_toc(title=title, level=level)

    def chapter_body(
        self,
        body: str,
        column_descriptions: list[ExtractedDescription] | None = None,
        argument_descriptions: list[ExtractedDescription] | None = None,
    ) -> None:
        """Add a chapter body to the PDF."""
        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=11)
        self.set_text_color(r=0, g=0, b=0)

        lines = body.split("\n")
        for line in lines:
            if (
                line.startswith("Description")
                or line.startswith("Columns")
                or line.startswith("Arguments")
            ):
                if self.font_family != "":
                    self.set_font(
                        family=self.font_family, style=self.bold_style, size=11
                    )

                self.set_text_color(r=54, g=132, b=235)
                self.cell(w=0, h=10, text=line, new_x="LMARGIN", new_y="TOP")
                self.ln(10)
                if self.font_family != "":
                    self.set_font(family=self.font_family, style="", size=11)
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
        if self.font_family != "":
            self.set_font(family=self.font_family, style=self.bold_style, size=11)

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
        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=11)

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

    def add_page_with_title(self, title: str, level: int | None) -> None:
        """Add a page with title."""
        self.ln(10)
        self.is_intro_page = False
        self.start_section(title)
        self.chapter_title(title)
        if level is not None:
            self.add_section_toc(title=title, level=level)

    def add_intro(self, intro_text: str) -> None:
        """Add introductory text to the PDF."""
        self.add_page()
        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=12)
        self.set_text_color(r=0, g=0, b=0)
        self.multi_cell(w=0, h=6, text=intro_text)
        self.is_intro_page = False

    def create_toc(self) -> TableOfContents:
        """Creates table of content entries and estimates the num. of pages required."""
        entries = []

        for title, level, page in self.sections:
            entry = TableOfContentsEntry(title=title, level=level, page=page)
            entries.append(entry)

        return TableOfContents(entries=entries, pages=round(len(entries) / 34))

    def add_toc(self, toc_info: TableOfContents) -> None:
        """Generates the table of contents on a separate page."""
        self.add_page()
        self.chapter_title("Table of Contents")
        self.set_text_color(r=0, g=0, b=0)
        self.ln(5)

        if self.font_family != "":
            self.set_font(family=self.font_family, style="", size=12)

        # List all sections with page numbers
        for entry in toc_info.entries:
            title = entry.title
            level = entry.level
            page = entry.page + toc_info.pages
            link = self.add_link()

            self.set_link(link, page=page)

            # self.set_font(family="Roboto", size=12)
            indent = 10 * level + 0.001
            self.cell(indent)

            cell_height = 10
            page_width = self.w - 20

            left_text = f"{title}"
            right_text = f"{page}"

            left_text_width = self.get_string_width(left_text)
            right_text_width = self.get_string_width(right_text)
            if level != 0:
                dot_space_width = (
                    page_width - left_text_width - right_text_width - 10 - 10 * level
                )
            else:
                dot_space_width = page_width - left_text_width - right_text_width - 10

            dots = "." * (int(dot_space_width / self.get_string_width(".")) - 5)

            right_text_width = self.get_string_width(right_text)

            self.cell(
                left_text_width,
                cell_height,
                left_text,
                align="L",
                link=link,  # type: ignore[arg-type]
            )
            self.cell(dot_space_width, cell_height, dots, align="C")
            self.cell(
                right_text_width,
                cell_height,
                right_text,
                align="R",
                link=link,  # type: ignore[arg-type]
            )

            self.ln(7)
