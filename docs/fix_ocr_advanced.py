#!/usr/bin/env python3
"""
Advanced OCR error fixing for Larsson thesis chapters.
"""

import re
from pathlib import Path

# Additional OCR fixes
ADDITIONAL_FIXES = {
    # Special characters
    "±": "ffi",
    "¯": "fi",
    "°": "fl",
    "®": "ff",
    "º": "Å",
    "Ä": "ö",
    "Ã": "Ö",
    # Common phrase fixes
    "su±cient": "sufficient",
    "ful¯l": "fulfill",
    "su±ciently": "sufficiently",
    # More words
    "de¯ned": "defined",
    "de¯nition": "definition",
    "de¯ning": "defining",
    "speci¯c": "specific",
    "speci¯cation": "specification",
    "speci¯ed": "specified",
    "identi¯ed": "identified",
    "identi¯er": "identifier",
    "satis¯ed": "satisfied",
    "satis¯es": "satisfies",
    "con¯rm": "confirm",
    "con¯rmation": "confirmation",
    "Ã": "ü",
}


def fix_word_spacing(text: str) -> str:
    """Fix missing spaces between words using common patterns."""

    # Fix patterns like "wordAnother" where capital letter follows lowercase
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # Common word boundary issues
    patterns = [
        (r"(\w)\.([A-Z])", r"\1. \2"),  # Period followed by capital
        (r"([a-z])([0-9])", r"\1 \2"),  # Letter followed by number
        (r"([0-9])([a-z])", r"\1 \2"),  # Number followed by letter
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    return text


def fix_section_headings(text: str) -> str:
    """Fix section numbering and headings."""

    # Fix patterns like "1.1Theaimofthisstudy" -> "1.1 The aim of this study"
    text = re.sub(
        r"(\d+\.\d+(?:\.\d+)?)([A-Z][a-z]+)",
        lambda m: f"{m.group(1)} {' '.join(re.findall('[A-Z][a-z]*', m.group(2)))}",
        text,
    )

    return text


def fix_references(text: str) -> str:
    """Fix common reference formatting issues."""

    # Fix "Allenetal." -> "Allen et al."
    text = re.sub(r"(\w+)etal\.", r"\1 et al.", text)

    # Fix year references
    text = re.sub(r"\((\d{4})\)\.", r"(\1).", text)

    return text


def comprehensive_ocr_fix(text: str) -> str:
    """Apply all OCR fixes."""

    # Apply character-level fixes
    for error, fix in ADDITIONAL_FIXES.items():
        text = text.replace(error, fix)

    # Apply pattern-based fixes
    text = fix_word_spacing(text)
    text = fix_section_headings(text)
    text = fix_references(text)

    return text


def process_chapter_file(file_path: Path):
    """Process a single chapter file to fix OCR errors."""

    print(f"Processing {file_path.name}...")

    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Apply fixes
    text = comprehensive_ocr_fix(text)

    # Write back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  Fixed {file_path.name}")


def main():
    """Process all chapter files."""

    thesis_dir = Path("/Users/brewc/PycharmProjects/ibdm/docs/larsson_thesis")

    # Process all markdown files except README
    for md_file in thesis_dir.glob("*.md"):
        if md_file.name != "README.md":
            process_chapter_file(md_file)

    print("\nAll chapter files processed!")


if __name__ == "__main__":
    main()
