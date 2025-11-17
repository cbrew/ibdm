"""Entry point for IBDM demo modules.

Usage:
    python -m ibdm.demo.interactive_demo    # Interactive demo
    python -m ibdm.demo.interactive_explorer # Scenario explorer
"""


def main() -> None:
    """Main entry point - shows usage."""
    print("IBDM Demo Tools")
    print("=" * 70)
    print()
    print("Available demos:")
    print("  python -m ibdm.demo.interactive_demo")
    print("    - Interactive dialogue demo with free-form conversation")
    print()
    print("  python -m ibdm.demo.interactive_explorer")
    print("    - Scenario explorer with choice-based navigation")
    print()
    print("For help:")
    print("  python -m ibdm.demo.interactive_demo --help")
    print("  python -m ibdm.demo.interactive_explorer --help")
    print()


if __name__ == "__main__":
    main()
