"""Data interface schemas."""

from pydantic import BaseModel

from dbt2pdf.manifest import Column


class ExtractedDescription(BaseModel):
    """Column description extracted from the DBT manifest."""

    name: str
    description: str


class ExtractedModel(BaseModel):
    """Model extracted from the DBT manifest."""

    name: str
    description: str
    columns: dict[str, Column] = {}
    column_descriptions: list[ExtractedDescription] = []


class ExtractedMacro(BaseModel):
    """Macro extracted from the DBT manifest."""

    name: str
    description: str
    argument_descriptions: list[ExtractedDescription] = []


class ToCEntry(BaseModel):
    """Table of Contents entry."""

    title: str
    level: int
    page: int


class ToCSchema(BaseModel):
    """Schema for the Table of Contents."""

    toc_entries: list[ToCEntry]
    toc_pages: int
