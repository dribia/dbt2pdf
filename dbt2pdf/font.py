"""Module for font handling."""

from enum import Enum
from typing import Dict

from matplotlib.font_manager import findSystemFonts
from pydantic import BaseModel

from dbt2pdf.logger import logger


class FontStyle(Enum):
    """Font style enumeration."""

    REGULAR = ""
    BOLD = "B"
    ITALIC = "I"
    UNDERLINE = "U"
    ASSAMESE = "AS"
    BDITA = "BD"
    BENGALI = "BE"
    BLACK = "BL"
    BLACKITALIC = "BLI"
    BOLDITALIC = "BI"
    BOOK = "BO"
    BOOKOBLIQUE = "BOO"
    C = "C"
    DEMI = "D"
    DEMIITALIC = "DI"
    DEMIOBLIQUE = "DO"
    DEVANAGARI = "DE"
    EXTRABOLD = "EB"
    EXTRALIGHT = "EL"
    GUJARATI = "GU"
    GURMUKHI = "G"
    HAIRLINE = "H"
    HAIRLINEITALIC = "HI"
    HALFLINGS = "HALF"
    HEAVY = "HV"
    HEAVYITALIC = "HVI"
    KANNADA = "KA"
    LIGHT = "L"
    LIGHTITALIC = "LI"
    MALAYALAM = "MA"
    MATH = "MATH"
    MEDIUM = "M"
    MEDIUMITALIC = "MI"
    ODIA = "O"
    RI = "RI"
    ROMAN = "RO"
    SEMIBOLD = "SB"
    SEMIBOLDITALIC = "SBI"
    TAMIL = "TA"
    TELUGU = "TE"
    THIN = "TH"
    THINITALIC = "THI"
    WEBFONT = "WF"


# Mapping for common style abbreviations to full names
STYLE_ALIASES = {
    "R": "Regular",
    "B": "Bold",
    "I": "Italic",
    "U": "Underline",
    "OBLIQUE": "Italic",
    "BI": "BoldItalic",
    "BOLDOBLIQUE": "BoldItalic",
    "LI": "LightItalic",
    "L": "Light",
    "LIGHTOBLIQUE": "LightItalic",
    "M": "Medium",
    "MI": "MediumItalic",
    "TH": "Thin",
}


class Font(BaseModel):
    """Font class to store font information."""

    path: str
    family: str
    style: FontStyle

    @staticmethod
    def get_font(path: str):
        """Initialize the Font class."""
        family_style = path.split("/")[-1].split(".")[0]
        family_style_split = family_style.split("-")
        family = family_style_split[0]
        style = family_style_split[1] if len(family_style_split) > 1 else "Regular"

        # Handle different style abbreviations
        style = STYLE_ALIASES.get(style.upper(), style)
        if isinstance(style, str):
            style = style.upper()
            style = STYLE_ALIASES.get(style, style)
            if style not in FontStyle.__members__:
                raise Warning(f"Invalid font style: {style}")

        return Font(path=path, family=family, style=FontStyle[style.upper()])


def find(family: str) -> Dict[FontStyle, Font]:
    """Find fonts in the system by family."""
    font_dict = {}
    if family != "":
        for font_path in findSystemFonts():
            try:
                font = Font.get_font(font_path)
                if font.family.lower() == family.lower():
                    if font.style in [
                        FontStyle.REGULAR,
                        FontStyle.BOLD,
                        FontStyle.ITALIC,
                    ]:
                        font_dict[font.style] = font
            except Exception as e:
                logger.debug(f"Error processing font at {font_path}: {e}")

    return font_dict
