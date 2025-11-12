#!/usr/bin/env python3
"""
Demo 3: IBDM-NLU Integration - Legal Document Generation

This demo showcases the integration between IBDM theoretical concepts and
practical NLU components through a legal document generation scenario.

Domain: Non-Disclosure Agreement (NDA) Generation
Participants: Attorney (User) ↔ Legal Document System (Agent)

Key Demonstrations:
- Natural language utterances → IBDM structures (Questions, Moves, Answers)
- Question Under Discussion (QUD) stack evolution
- Entity extraction for legal entities (organizations, dates, jurisdictions)
- Task accommodation (system infers document requirements)
- Hybrid fallback strategy (pattern matching → Haiku → Sonnet)
- Cost optimization and performance metrics

Requirements:
- IBDM_API_KEY environment variable must be set
- Uses Claude models via LiteLLM for NLU tasks

Usage:
    python demos/03_nlu_integration_basic.py [--verbose] [--no-color]

Options:
    --verbose, -v    Show detailed NLU processing information
    --no-color       Disable colored output
    --help, -h       Show this help message

Run: python demos/03_nlu_integration_basic.py
"""

import argparse
import os
import sys

from rich.console import Console
from rich.panel import Panel

# IBDM Core imports

# IBDM Engine imports

# NLU imports


def check_api_key() -> bool:
    """Verify that IBDM_API_KEY is available.

    Returns:
        True if API key is found, False otherwise
    """
    api_key = os.getenv("IBDM_API_KEY")
    if not api_key:
        return False
    return True


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="IBDM-NLU Integration Demo: Legal Document Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed NLU processing information"
    )

    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    return parser.parse_args()


def main():
    """Main entry point for the demo."""
    # Parse arguments
    args = parse_arguments()

    # Initialize console
    console = Console(
        force_terminal=not args.no_color, color_system="auto" if not args.no_color else None
    )

    # Display header
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]IBDM-NLU Integration Demo[/bold cyan]\n"
            "[white]Legal Document Generation: Non-Disclosure Agreement[/white]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()

    # Check API key
    if not check_api_key():
        console.print(
            "[bold red]Error:[/bold red] IBDM_API_KEY environment variable not found.", style="red"
        )
        console.print()
        console.print("Please set your API key:")
        console.print("  export IBDM_API_KEY='your-key-here'")
        console.print()
        console.print("The API key should be available in the .env file.")
        return 1

    # Display setup info
    if args.verbose:
        console.print("[dim]✓ API key found[/dim]")
        console.print("[dim]✓ Initializing NLU components...[/dim]")
        console.print()

    # Main demo will go here
    console.print("[yellow]Demo implementation in progress...[/yellow]")
    console.print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
