"""Module for font handling."""

from enum import Enum
from typing import Dict

from matplotlib.font_manager import findSystemFonts
from pydantic import BaseModel, field_validator


class FontStyle(Enum):
    """Font style enumeration."""

    REGULAR = ""
    BOLD = "B"
    ITALIC = "I"
    UNDERLINE = "U"


# Mapping for common style abbreviations to full names
STYLE_ALIASES = {
    "R": "Regular",
    "B": "Bold",
    "I": "Italic",
    "U": "Underline",
    "OBLIQUE": "Italic",
}


class Font(BaseModel):
    """Font class to store font information."""

    path: str
    family: str
    style: FontStyle

    @field_validator("style", mode="before")
    def validate_style(cls, value):
        """Validate the font style."""
        if isinstance(value, str):
            value = value.upper()
            value = STYLE_ALIASES.get(value, value)
            if value in FontStyle.__members__:
                return FontStyle[value]
            raise Warning(f"Invalid font style: {value}")
        return value

    def __init__(self, path: str):
        """Initialize the Font class."""
        family_style = path.split("/")[-1].split(".")[0]
        family_style_split = family_style.split("-")
        family = family_style_split[0]
        style = family_style_split[1] if len(family_style_split) > 1 else "Regular"

        # Handle different style abbreviations
        style = STYLE_ALIASES.get(style.upper(), style)

        # Call Pydantic's __init__ method with the fields
        super().__init__(path=path, family=family, style=style)


def find(family: str | None) -> Dict[FontStyle, Font]:
    """Find fonts in the system by family."""
    font_dict = {}
    if family is not None:
        for font_path in findSystemFonts():
            try:
                font = Font(font_path)
                if font.family.lower() == family.lower():
                    if font.style in [
                        FontStyle.REGULAR,
                        FontStyle.BOLD,
                        FontStyle.ITALIC,
                    ]:
                        font_dict[font.style] = font
            except Exception as e:
                print(f"Error processing font at {font_path}: {e}")

    if not font_dict:
        raise ValueError(
            f"No fonts found with family '{family}' having styles '', 'B', or 'I'."
        )

    return font_dict
