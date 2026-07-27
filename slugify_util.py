import re


def slugify(text: str) -> str:
    """Convert a string into a URL-friendly slug."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
