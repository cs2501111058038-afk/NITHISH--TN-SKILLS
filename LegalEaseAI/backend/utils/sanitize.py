import re
import unicodedata


REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u00a0": " ",
}


def sanitize_text(text: str) -> str:
    """
    Clean generated legal-document text so it is safe
    for display and document export.
    """

    if not isinstance(text, str):
        return ""

    # Replace problematic Unicode characters
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    # Normalize Unicode
    text = unicodedata.normalize("NFKC", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove trailing spaces
    text = re.sub(r"[ \t]+\n", "\n", text)

    # Avoid excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()