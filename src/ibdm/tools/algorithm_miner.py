"""
Algorithm Mining Tool for PDF Documents

Extracts algorithmic descriptions, procedures, and pseudocode from academic PDFs,
particularly focused on extracting algorithms from Larsson (2002) thesis.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pdfplumber


@dataclass
class Algorithm:
    """Represents an extracted algorithm."""

    title: str
    section: str
    page_num: int
    content: str
    context_before: str = ""
    context_after: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "section": self.section,
            "page": self.page_num,
            "content": self.content,
            "context_before": self.context_before,
            "context_after": self.context_after,
        }


class AlgorithmMiner:
    """Mines algorithmic descriptions from PDF documents."""

    # Patterns that indicate algorithmic content
    ALGORITHM_PATTERNS = [
        r"(?i)algorithm\s+\d+",
        r"(?i)procedure\s+\w+",
        r"(?i)function\s+\w+\s*\(",
        r"(?i)update\s+rules?:",
        r"(?i)rule\s+\d+",
        r"(?i)definition\s+\d+",
    ]

    # Patterns for section headers
    SECTION_PATTERN = r"^\d+\.[\d.]*\s+[A-Z]"

    # Patterns for pseudocode structures
    PSEUDOCODE_PATTERNS = [
        r"\bif\s+.*\s+then\b",
        r"\bwhile\s+.*\s+do\b",
        r"\bfor\s+each\b",
        r"\breturn\b",
        r"^\s*\d+\.",  # Numbered steps
        r"^-\s+",  # Bulleted steps
        r"::=",  # BNF notation
        r"→",  # Transition notation
    ]

    def __init__(self, pdf_path: str | Path):
        """Initialize with path to PDF."""
        self.pdf_path = Path(pdf_path)
        self.algorithms: list[Algorithm] = []
        self.current_section = ""

    def extract_text_by_page(self) -> list[tuple[int, str]]:
        """Extract text from PDF, page by page."""
        pages: list[tuple[int, str]] = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                pages.append((i, text))
        return pages

    def is_section_header(self, line: str) -> bool:
        """Check if line is a section header."""
        return bool(re.match(self.SECTION_PATTERN, line.strip()))

    def update_section(self, text: str) -> None:
        """Update current section based on text."""
        lines = text.split("\n")
        for line in lines:
            if self.is_section_header(line):
                self.current_section = line.strip()

    def has_algorithm_marker(self, text: str) -> bool:
        """Check if text contains algorithm markers."""
        for pattern in self.ALGORITHM_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def has_pseudocode_patterns(self, text: str) -> bool:
        """Check if text contains pseudocode patterns."""
        pattern_count = 0
        for pattern in self.PSEUDOCODE_PATTERNS:
            if re.search(pattern, text, re.MULTILINE):
                pattern_count += 1
        return pattern_count >= 2  # At least 2 pseudocode patterns

    def extract_algorithm_title(self, text: str) -> str:
        """Extract algorithm title from text."""
        for pattern in self.ALGORITHM_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Get the line containing the match
                lines = text[: match.end()].split("\n")
                if lines:
                    title_line = lines[-1].strip()
                    # Extend to next line if it looks like a continuation
                    remaining = text[match.end() :].split("\n")
                    if remaining and not remaining[0].strip().startswith(
                        ("if", "while", "for", "return", "1.", "-")
                    ):
                        title_line += " " + remaining[0].strip()
                    return title_line
        return "Untitled Algorithm"

    def extract_algorithm_block(self, text: str, start_pos: int, page_num: int) -> Algorithm | None:
        """Extract a complete algorithm block from position."""
        # Find the algorithm block boundaries
        lines = text[start_pos:].split("\n")
        algorithm_lines: list[str] = []
        blank_count = 0

        for line in lines:
            stripped = line.strip()

            # Stop at next section header
            if self.is_section_header(line):
                break

            # Track consecutive blank lines
            if not stripped:
                blank_count += 1
                if blank_count > 2:  # More than 2 blank lines = end of block
                    break
                continue
            else:
                blank_count = 0

            algorithm_lines.append(line)

            # Stop if we've collected substantial content and hit a new algorithm
            if len(algorithm_lines) > 10 and self.has_algorithm_marker(stripped):
                break

        if not algorithm_lines:
            return None

        content = "\n".join(algorithm_lines).strip()

        # Extract context
        context_before = text[max(0, start_pos - 500) : start_pos].strip()
        context_after = text[start_pos + len(content) : start_pos + len(content) + 500].strip()

        title = self.extract_algorithm_title(content)

        return Algorithm(
            title=title,
            section=self.current_section,
            page_num=page_num,
            content=content,
            context_before=context_before,
            context_after=context_after,
        )

    def mine_algorithms(self) -> list[Algorithm]:
        """Mine all algorithms from the PDF."""
        pages = self.extract_text_by_page()

        for page_num, text in pages:
            self.update_section(text)

            # Find all positions with algorithm markers
            for pattern in self.ALGORITHM_PATTERNS:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    start_pos = match.start()
                    algorithm = self.extract_algorithm_block(text, start_pos, page_num)
                    if algorithm and len(algorithm.content) > 100:
                        self.algorithms.append(algorithm)

            # Also look for sections with heavy pseudocode patterns
            # Split by paragraphs (double newline)
            paragraphs = re.split(r"\n\s*\n", text)
            for para in paragraphs:
                if (
                    len(para) > 200
                    and self.has_pseudocode_patterns(para)
                    and not any(
                        alg.content in para or para in alg.content for alg in self.algorithms
                    )
                ):
                    title = f"Procedure/Rule in {self.current_section or 'Section'}"
                    algorithm = Algorithm(
                        title=title,
                        section=self.current_section,
                        page_num=page_num,
                        content=para.strip(),
                        context_before="",
                        context_after="",
                    )
                    self.algorithms.append(algorithm)

        return self.algorithms

    def save_to_markdown(self, output_path: str | Path) -> None:
        """Save extracted algorithms to a markdown file."""
        output_path = Path(output_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Algorithms Extracted from {self.pdf_path.name}\n\n")
            f.write(f"Total algorithms found: {len(self.algorithms)}\n\n")
            f.write("---\n\n")

            for i, alg in enumerate(self.algorithms, start=1):
                f.write(f"## Algorithm {i}: {alg.title}\n\n")
                f.write(f"**Section:** {alg.section or 'Unknown'}\n")
                f.write(f"**Page:** {alg.page_num}\n\n")

                if alg.context_before:
                    f.write("**Context Before:**\n")
                    f.write(f"> {alg.context_before[:200]}...\n\n")

                f.write("**Algorithm:**\n\n")
                f.write("```\n")
                f.write(alg.content)
                f.write("\n```\n\n")

                if alg.context_after:
                    f.write("**Context After:**\n")
                    f.write(f"> {alg.context_after[:200]}...\n\n")

                f.write("---\n\n")

    def save_to_json(self, output_path: str | Path) -> None:
        """Save extracted algorithms to a JSON file."""
        import json

        output_path = Path(output_path)

        data = {
            "source": str(self.pdf_path),
            "total_algorithms": len(self.algorithms),
            "algorithms": [alg.to_dict() for alg in self.algorithms],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def mine_larsson_algorithms(
    pdf_path: str | Path = "docs/Larsson_Tesis.pdf",
    output_dir: str | Path = "reports/algorithms",
) -> list[Algorithm]:
    """
    Mine algorithms from Larsson thesis and save to reports.

    Args:
        pdf_path: Path to Larsson thesis PDF
        output_dir: Directory to save extracted algorithms

    Returns:
        List of extracted algorithms
    """
    import subprocess
    from datetime import datetime

    # Get git hash for tagging
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except Exception:
        git_hash = "unknown"

    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Mine algorithms
    miner = AlgorithmMiner(pdf_path)
    algorithms = miner.mine_algorithms()

    # Save outputs with timestamp and git hash
    base_name = f"larsson_algorithms_{timestamp}_{git_hash}"
    miner.save_to_markdown(output_dir / f"{base_name}.md")
    miner.save_to_json(output_dir / f"{base_name}.json")

    # Also save a "latest" version
    miner.save_to_markdown(output_dir / "larsson_algorithms_latest.md")
    miner.save_to_json(output_dir / "larsson_algorithms_latest.json")

    return algorithms


if __name__ == "__main__":
    algorithms = mine_larsson_algorithms()
    print(f"Extracted {len(algorithms)} algorithms from Larsson thesis")
    for i, alg in enumerate(algorithms[:5], start=1):  # Show first 5
        print(f"{i}. {alg.title} (Page {alg.page_num})")
