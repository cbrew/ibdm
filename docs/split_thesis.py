#!/usr/bin/env python3
"""
Split Larsson's thesis into separate chapter files and fix OCR errors.
"""

import re
from pathlib import Path

# Common OCR error corrections
OCR_FIXES = {
    "managemen t": "management",
    "implemen tation": "implementation",
    "represen ting": "representing",
    "orien ted": "oriented",
    "accommo dation": "accommodation",
    "participan t": "participant",
    "requiremen ts": "requirements",
    "Departmen t": "Department",
    "GÄoteborg": "Göteborg",
    "Sta®an": "Staffan",
    "¯": "fi",
    "°": "fl",
    "®": "ff",
    "di®erent": "different",
    "di®erences": "differences",
    "º": "Å",
    "Ä": "ö",
    "lev el": "level",
    "taxonom y": "taxonomy",
    "clari¯cation": "clarification",
    "classi¯cation": "classification",
    "successiv e": "successive",
    "negotiativ e": "negotiative",
    "alternativ es": "alternatives",
}


def fix_ocr_errors(text: str) -> str:
    """Fix common OCR errors in text."""
    for error, fix in OCR_FIXES.items():
        text = text.replace(error, fix)
    return text


def find_chapter_boundaries(lines: list[str]) -> list[tuple[int, str]]:
    """Find line numbers where chapters and major sections start."""
    boundaries = []
    chapter_pattern = re.compile(r"^Chapter (\d+)")
    appendix_pattern = re.compile(r"^(A|B)\.?\d*\s+")

    for i, line in enumerate(lines):
        line = line.strip()

        # Check for main content sections
        if line == "Abstract":
            boundaries.append((i, "00_front_matter"))
        elif line == "Contents":
            boundaries.append((i, "00_contents"))
        elif chapter_match := chapter_pattern.match(line):
            ch_num = chapter_match.group(1)
            boundaries.append((i, f"chapter_{ch_num}"))
        elif line.startswith("ATrindiKit"):
            boundaries.append((i, "appendix_a"))
        elif line.startswith("BRulesandclasses"):
            boundaries.append((i, "appendix_b"))

    return boundaries


def split_thesis(input_file: Path, output_dir: Path):
    """Split thesis into separate chapter files."""

    # Read the entire file, handling potential encoding issues
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Read {len(lines)} lines from {input_file}")

    # Find chapter boundaries
    boundaries = find_chapter_boundaries(lines)
    print(f"Found {len(boundaries)} chapter boundaries")

    # Add end boundary
    boundaries.append((len(lines), "end"))

    # Extract each section
    for i in range(len(boundaries) - 1):
        start_line, section_name = boundaries[i]
        end_line = boundaries[i + 1][0]

        # Get section content
        section_lines = lines[start_line:end_line]
        section_text = "".join(section_lines)

        # Fix OCR errors
        section_text = fix_ocr_errors(section_text)

        # Write to file
        output_file = output_dir / f"{section_name}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(section_text)

        print(f"Wrote {section_name}.md ({len(section_lines)} lines)")


def create_index(output_dir: Path):
    """Create an index document for navigation."""

    index_content = """# Larsson (2002) - Issue-Based Dialogue Management

**Author**: Staffan Larsson
**Institution**: Department of Linguistics, Göteborg University, Sweden
**Year**: 2002

This doctoral dissertation presents the theoretical foundation for Issue-Based Dialogue Management (IBDM),
an approach that uses questions (modeled semantically as issues) as the primary organizing and motivating
force in dialogue.

## Document Structure

### Front Matter
- [Front Matter & Abstract](00_front_matter.md) - Title, abstract, and acknowledgements
- [Table of Contents](00_contents.md) - Full table of contents

### Main Chapters

1. [Chapter 1: Introduction](chapter_1.md)
   - The aim of this study
   - Rationale
   - The IBiS family of systems
   - TrindiKit

2. [Chapter 2: Basic Issue-Based Dialogue Management](chapter_2.md)
   - Information exchange and inquiry-oriented dialogue
   - Shared and private information in dialogue
   - Overview of IBiS1
   - Semantics, dialogue moves, and plans
   - Update and selection modules

3. [Chapter 3: Grounding Issues](chapter_3.md)
   - Background on grounding theories (Clark, Ginzburg, Allwood)
   - Feedback and grounding strategies
   - Issue-based grounding in IBiS2
   - Interactive Communication Management

4. [Chapter 4: Addressing Unraised Issues](chapter_4.md)
   - The nature(s) of QUD (Questions Under Discussion)
   - Question accommodation
   - IBiS3 extensions
   - Dependent issue accommodation and clarification

5. [Chapter 5: Action-Oriented and Negotiative Dialogue](chapter_5.md)
   - Issues and actions in action-oriented dialogue
   - Interacting with menu-based devices
   - Issues Under Negotiation (IUN)
   - IBiS4 extensions

6. [Chapter 6: Conclusions and Future Research](chapter_6.md)
   - Summary
   - Dialogue typology
   - Dialogue structure
   - Future research areas

### Appendices

- [Appendix A: TrindiKit Functionality](appendix_a.md)
  - Datatypes, methods, and rule definition formats
  - DME-ADL and Control-ADL languages

- [Appendix B: Rules and Classes](appendix_b.md)
  - Complete rule definitions for IBiS1-4
  - Update and selection module rules

## Key Concepts

This thesis introduces and develops several key concepts:

- **Issues/Questions Under Discussion (QUD)**: The central organizing principle for dialogue
- **Information State**: Representation of shared and private information in dialogue
- **Dialogue Moves**: Actions that update the information state
- **Grounding**: How participants establish common ground
- **Accommodation**: Addressing issues not explicitly raised
- **TrindiKit**: A toolkit for building and experimenting with dialogue systems

## Relevance to IBDM Project

This thesis provides the theoretical foundation for the IBDM project. Key architectural elements:

- **Four-phase dialogue processing**: Interpretation → Integration → Selection → Generation
- **Information state architecture**: Separation of shared/private, QUD, plan, issues
- **Domain abstraction layer**: Predicates, sorts, and semantic operations
- **Question-based control flow**: Issues drive dialogue structure

## Citation

Larsson, S. (2002). *Issue-Based Dialogue Management*. Doctoral dissertation,
Department of Linguistics, Göteborg University, Sweden. ISBN 91-628-5301-5.
"""

    index_file = output_dir / "README.md"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"Created index: README.md")


if __name__ == "__main__":
    input_file = Path("/Users/brewc/PycharmProjects/ibdm/docs/Larsson_Tesis_nopages.md")
    output_dir = Path("/Users/brewc/PycharmProjects/ibdm/docs/larsson_thesis")

    output_dir.mkdir(exist_ok=True)

    print("Splitting Larsson thesis...")
    split_thesis(input_file, output_dir)

    print("\nCreating index...")
    create_index(output_dir)

    print("\nDone!")
