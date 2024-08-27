"""Utility functions."""


def clean_text(text: str) -> str:
    """Remove non-ASCII characters from text."""
    return text.encode(encoding="ascii", errors="ignore").decode("ascii")
