#!/usr/bin/env python3
"""Demo: Generate real NDA from nda_comprehensive scenario data.

This script demonstrates the complete workflow:
1. Extract information from nda_comprehensive scenario
2. Use NDA generation service to create real NDA via Claude Sonnet
3. Save the generated NDA to file
"""

import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ibdm.services.nda_generator import NDAGenerator, NDAParameters


def extract_nda_params_from_scenario() -> NDAParameters:
    """Extract NDA parameters from nda_comprehensive scenario.

    Based on the final commitments after the comprehensive dialogue:
    - Parties: Current company and Global Industries
    - Type: Mutual
    - Effective Date: February 1st, 2025
    - Duration: 3 years
    - Jurisdiction: Delaware
    """
    return NDAParameters(
        parties=["Acme Corporation", "Global Industries Inc."],
        nda_type="mutual",
        effective_date="February 1, 2025",
        duration="3 years",
        jurisdiction="Delaware",
    )


def main() -> int:
    """Run NDA generation demo."""
    print("=" * 80)
    print("NDA GENERATION DEMO")
    print("=" * 80)
    print()
    print("This demo generates a real NDA using Claude Sonnet based on")
    print("information gathered in the nda_comprehensive scenario.")
    print()

    # Extract parameters
    print("📋 Extracting NDA parameters from dialogue...")
    params = extract_nda_params_from_scenario()

    print(f"   ✓ Parties: {', '.join(params.parties)}")
    print(f"   ✓ Type: {params.nda_type}")
    print(f"   ✓ Effective Date: {params.effective_date}")
    print(f"   ✓ Duration: {params.duration}")
    print(f"   ✓ Jurisdiction: {params.jurisdiction}")
    print()

    # Initialize generator
    print("🤖 Initializing NDA Generator (Claude Sonnet 4.5)...")
    try:
        generator = NDAGenerator()
        print("   ✓ Generator initialized")
    except ValueError as e:
        print(f"   ✗ Error: {e}")
        print()
        print("Please set IBDM_API_KEY environment variable with your Anthropic API key.")
        return 1
    print()

    # Generate NDA
    print("📝 Generating NDA document (this may take 10-30 seconds)...")
    print()
    try:
        nda_text = generator.generate_nda(params)
        print("   ✓ NDA generated successfully!")
        print()
    except Exception as e:
        print(f"   ✗ Generation failed: {e}")
        return 1

    # Display preview
    print("=" * 80)
    print("GENERATED NDA PREVIEW")
    print("=" * 80)
    print()

    # Show first 50 lines
    lines = nda_text.split("\n")
    preview_lines = lines[:50]
    print("\n".join(preview_lines))

    if len(lines) > 50:
        print()
        print(f"... ({len(lines) - 50} more lines)")
    print()

    # Save to file
    output_dir = Path("demos/generated_documents")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"nda_mutual_acme_global_{timestamp}.md"

    with open(output_file, "w") as f:
        f.write(f"# Generated NDA - {params.effective_date}\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("**Model**: Claude Sonnet 4.5\n")
        f.write("**Source**: IBDM nda_comprehensive scenario\n")
        f.write("\n---\n\n")
        f.write(nda_text)

    print("=" * 80)
    print("SAVED TO FILE")
    print("=" * 80)
    print()
    print(f"📄 Full NDA saved to: {output_file}")
    print(f"📊 Document length: {len(lines)} lines, {len(nda_text)} characters")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("✓ Information gathered through IBDM dialogue (nda_comprehensive)")
    print("✓ NDA generated using Claude Sonnet 4.5")
    print("✓ Professional legal document ready for review")
    print()
    print("⚠️  NOTE: This is AI-generated legal content. Always have a licensed")
    print("   attorney review any legal documents before use.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
