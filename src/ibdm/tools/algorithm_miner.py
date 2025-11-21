"""
Algorithm Mining Tool for Larsson Thesis

Extracts algorithmic descriptions, procedures, and pseudocode from the text version
of Larsson (2002) thesis.
"""

import re
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, List, Dict

@dataclass
class Algorithm:
    """Represents an extracted algorithm."""
    title: str
    section: str
    page_num: int
    content: str
    category: str = "Uncategorized"
    rule_id: str = ""
    context_before: str = ""
    context_after: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "section": self.section,
            "page": self.page_num,
            "category": self.category,
            "rule_id": self.rule_id,
            "content": self.content,
            "context_before": self.context_before,
            "context_after": self.context_after,
        }

class AlgorithmMiner:
    """Mines algorithmic descriptions from text documents."""

    # Regex patterns
    # Pattern for Rule headers, e.g., "(rule 2.1) rule: getLatestMove" or "Rule 2.1: ..."
    RULE_PATTERN = re.compile(r"^\s*\(?rule\s+(\d+\.\d+)\)?\s*(?:rule:)?\s*(.+)", re.IGNORECASE | re.MULTILINE)
    
    # Pattern for Algorithm headers, e.g., "Algorithm 2.2: Main Control Loop"
    ALGO_PATTERN = re.compile(r"^\s*Algorithm\s+(\d+\.\d+)\s*:?\s*(.+)", re.IGNORECASE | re.MULTILINE)
    
    # Pattern for Definitions
    DEF_PATTERN = re.compile(r"^\s*Definition\s+(\d+\.\d+)\s*:?\s*(.+)", re.IGNORECASE | re.MULTILINE)

    # Section header pattern (approximate for the text file)
    SECTION_PATTERN = re.compile(r"^\s*(\d+\.\d+)\s+([A-Z][a-zA-Z\s]+)")

    def __init__(self, text_path: str | Path):
        self.text_path = Path(text_path)
        self.algorithms: List[Algorithm] = []
        self.full_text = ""
        self.pages: List[str] = [] # Split by form feed character

    def load_text(self):
        if not self.text_path.exists():
            raise FileNotFoundError(f"Text file not found: {self.text_path}")
            
        with open(self.text_path, 'r', encoding='utf-8') as f:
            self.full_text = f.read()
        
        # pdftotext uses \x0c (form feed) for page breaks
        self.pages = self.full_text.split('\x0c')

    def clean_text(self, text: str) -> str:
        """Clean common OCR artifacts."""
        replacements = [
            ("flnd", "find"),
            ("efiect", "effect"),
            ("difierent", "different"),
            ("su–cient", "sufficient"),
            ("insu–cient", "insufficient"),
            ("–", "-"),
            ("ﬂ", "fl"),
            ("fi", "fi"),
            ("qud", "QUD"),
            ("ibis", "IBiS"),
            ("IBIS", "IBiS"),
            ("TrindiKit", "TrindiKit"),
            ("(cid:176)", "fl"),
            (" .", "."),
            (" ,", ","),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def categorize(self, title: str, content: str) -> str:
        t = title.lower()
        c = content.lower()
        if "control" in t or "loop" in t: return "Control Algorithm"
        if "information state" in t or "structure" in t: return "Information State Structures"
        if "select" in t: return "Selection Rules"
        if "integrate" in t or "update" in t or "exec" in t or "downdate" in t: return "Update Rules"
        if "resolves" in t or "combines" in t or "relevant" in t: return "Semantic Operations"
        return "Other Algorithms"

    def mine(self):
        self.load_text()
        
        for page_idx, page_content in enumerate(self.pages):
            page_num = page_idx + 1
            lines = page_content.split('\n')
            current_section = "Unknown"
            
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check for section
                sec_match = self.SECTION_PATTERN.match(line)
                if sec_match:
                    current_section = f"{sec_match.group(1)} {sec_match.group(2).strip()}"
                
                # Check for algorithms
                match = None
                kind = ""
                
                rule_match = self.RULE_PATTERN.search(line)
                if rule_match:
                    match = rule_match
                    kind = "Rule"
                
                if not match:
                    algo_match = self.ALGO_PATTERN.search(line)
                    if algo_match:
                        match = algo_match
                        kind = "Algorithm"
                
                if match:
                    # Found a start. Let's extract the block.
                    rule_id = match.group(1)
                    title_suffix = match.group(2).strip()
                    title = f"{kind} {rule_id}: {title_suffix}"
                    
                    block_lines = [line]
                    j = i + 1
                    empty_lines = 0
                    
                    # Capture lines until we hit a stop condition
                    while j < len(lines):
                        next_line = lines[j]
                        stripped = next_line.strip()
                        
                        # Stop if we see another rule/algo header
                        if self.RULE_PATTERN.search(next_line) or self.ALGO_PATTERN.search(next_line):
                            break
                            
                        # Stop if we see a section header
                        if self.SECTION_PATTERN.match(next_line):
                            break
                        
                        if not stripped:
                            empty_lines += 1
                            if empty_lines > 2: # Stop after 2 empty lines
                                break
                        else:
                            empty_lines = 0
                        
                        block_lines.append(next_line)
                        j += 1
                    
                    content = "\n".join(block_lines)
                    content = self.clean_text(content)
                    
                    # Context
                    ctx_before = "\n".join(lines[max(0, i-5):i])
                    ctx_after = "\n".join(lines[j:min(len(lines), j+5)])
                    
                    alg = Algorithm(
                        title=title,
                        section=current_section,
                        page_num=page_num,
                        content=content,
                        category=self.categorize(title, content),
                        rule_id=rule_id,
                        context_before=ctx_before,
                        context_after=ctx_after
                    )
                    
                    # Avoid duplicates
                    if not any(a.rule_id == rule_id and a.title == title for a in self.algorithms):
                        self.algorithms.append(alg)
                    
                    # Advance i to j to skip processed lines
                    i = j
                    continue
                
                i += 1

    def save_markdown(self, output_path: Path):
        """Save extracted algorithms to a structured markdown file."""
        # Group by category
        categories = {
            "Core Architecture": [],
            "Control Algorithm": [],
            "Information State Structures": [],
            "Semantic Operations": [],
            "Update Rules": [],
            "Selection Rules": [],
            "Other Algorithms": []
        }
        
        for alg in self.algorithms:
            if alg.category in categories:
                categories[alg.category].append(alg)
            else:
                categories["Other Algorithms"].append(alg)

        # Sort within categories by rule ID
        for cat in categories:
            categories[cat].sort(key=lambda x: (float(x.rule_id) if x.rule_id.replace('.', '', 1).isdigit() else 999, x.page_num))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Larsson (2002) - IBDM Algorithmic Reference\n\n")
            f.write(f"**Source**: Larsson, S. (2002). Issue-Based Dialogue Management. Doctoral dissertation.\n")
            f.write(f"**Status**: Extracted from `docs/Larsson_Tesis_full.txt` via `algorithm_miner.py`\n")
            f.write(f"**Total Items**: {len(self.algorithms)}\n\n")
            f.write("---\n\n")
            
            f.write("## Table of Contents\n\n")
            for cat in categories:
                if categories[cat]:
                    anchor = cat.lower().replace(" ", "-")
                    f.write(f"- [{cat}](#{anchor}) ({len(categories[cat])} items)\n")
            f.write("\n---\n\n")

            for cat, algs in categories.items():
                if not algs:
                    continue
                    
                f.write(f"## {cat}\n\n")
                
                for alg in algs:
                    f.write(f"### {alg.title}\n\n")
                    f.write(f"**Source**: Page {alg.page_num} (Section {alg.section or 'Unknown'})\n\n")
                    
                    f.write("```\n")
                    f.write(alg.content)
                    f.write("\n```\n\n")
                    
                    f.write("---\n\n")

    def save_json(self, output_path: Path):
        """Save extracted algorithms to a JSON file."""
        data = {
            "source": str(self.text_path),
            "total_algorithms": len(self.algorithms),
            "algorithms": [alg.to_dict() for alg in self.algorithms],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def mine_larsson_algorithms(
    text_path: str | Path = "docs/Larsson_Tesis_full.txt",
    output_dir: str | Path = "reports/algorithms",
) -> List[Algorithm]:
    """
    Mine algorithms from Larsson thesis text and save to reports.
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
    miner = AlgorithmMiner(text_path)
    miner.mine()

    # Save outputs with timestamp and git hash
    base_name = f"larsson_algorithms_{timestamp}_{git_hash}"
    miner.save_markdown(output_dir / f"{base_name}.md")
    miner.save_json(output_dir / f"{base_name}.json")

    # Also save a "latest" version
    miner.save_markdown(output_dir / "larsson_algorithms_latest.md")
    miner.save_json(output_dir / "larsson_algorithms_latest.json")

    return miner.algorithms


if __name__ == "__main__":
    algorithms = mine_larsson_algorithms()
    print(f"Extracted {len(algorithms)} algorithms from Larsson thesis")
    for i, alg in enumerate(algorithms[:5], start=1):  # Show first 5
        print(f"{i}. {alg.title} (Page {alg.page_num})")
