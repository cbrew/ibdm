#!/usr/bin/env python3
"""
Visualize Burr Application Graph

Creates a visual diagram of the IBDM Burr state machine showing:
- All actions (nodes)
- Transitions (edges)
- Conditional transitions

Requires graphviz to be installed:
  macOS: brew install graphviz
  Ubuntu: apt-get install graphviz

Usage:
    python scripts/visualize_burr_graph.py
    python scripts/visualize_burr_graph.py --output my_graph.png
    python scripts/visualize_burr_graph.py --nlu  # Include NLU engine
"""

import argparse
from pathlib import Path

from ibdm.burr_integration import DialogueStateMachine


def print_text_graph():
    """Print a text-based representation of the Burr graph."""
    print("\n" + "=" * 60)
    print("BURR APPLICATION GRAPH (Text Representation)")
    print("=" * 60)
    print("""
    ┌─────────────┐
    │ initialize  │ (Entry point)
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │     nlu     │ ◄───────────────┐
    └──────┬──────┘                 │
           │                        │
           ▼                        │
    ┌─────────────┐                 │
    │  interpret  │                 │
    └──────┬──────┘                 │
           │                        │
           ▼                        │
    ┌─────────────┐                 │
    │  integrate  │                 │
    └──────┬──────┘                 │
           │                        │
           ▼                        │
    ┌─────────────┐                 │
    │   select    │                 │
    └──────┬──────┘                 │
           │                        │
           ├─[has_response]─────────┤
           │                        │
           ▼                        │
    ┌─────────────┐                 │
    │     nlg     │                 │
    └──────┬──────┘                 │
           │                        │
           ▼                        │
    ┌─────────────┐                 │
    │  generate   │                 │
    └──────┬──────┘                 │
           │                        │
           └────────────────────────┘

    Legend:
    • Solid arrows (│,▼): Default transitions
    • Conditional [has_response]: Only if response available
    • Loop back to nlu: Waits for next user input
    """)
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Visualize IBDM Burr application graph"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="dialogue_flow.png",
        help="Output file path (default: dialogue_flow.png)",
    )
    parser.add_argument(
        "--nlu",
        action="store_true",
        help="Include NLU engine in the application",
    )
    parser.add_argument(
        "--nlg",
        action="store_true",
        help="Include NLG engine in the application",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("IBDM Burr Application Graph Visualizer")
    print("=" * 60)

    # Create dialogue state machine
    print("\n1. Creating dialogue state machine...")

    kwargs = {}

    if args.nlu:
        print("   - Including NLU engine")
        # Import NLU engine
        try:
            from ibdm.nlu import NLUDialogueEngine, NLUEngineConfig

            config = NLUEngineConfig()
            nlu_engine = NLUDialogueEngine(config=config)
            kwargs["nlu_engine"] = nlu_engine
            kwargs["engine_class"] = NLUDialogueEngine
            kwargs["engine_config"] = config
        except ImportError as e:
            print(f"   Warning: Could not import NLU engine: {e}")

    if args.nlg:
        print("   - Including NLG engine")
        try:
            from ibdm.nlg import NLGEngine

            nlg_engine = NLGEngine()
            kwargs["nlg_engine"] = nlg_engine
        except ImportError as e:
            print(f"   Warning: Could not import NLG engine: {e}")

    state_machine = DialogueStateMachine(**kwargs)
    print("   ✓ State machine created")

    # Visualize
    print(f"\n2. Generating graph visualization...")
    output_path = Path(args.output)

    try:
        state_machine.visualize(output_path=str(output_path))
        print(f"   ✓ Graph saved to: {output_path.absolute()}")
    except Exception as e:
        print(f"   ✗ Visualization failed: {e}")
        print("\n   Troubleshooting:")
        print("   1. Install system graphviz:")
        print("      macOS: brew install graphviz")
        print("      Ubuntu: apt-get install graphviz")
        print("   2. Install Python graphviz package:")
        print("      uv pip install --system graphviz")
        print("\n   Showing text-based representation instead:")
        print_text_graph()
        return 1

    # Show application structure
    print("\n3. Application Structure:")
    print(f"   - Entry point: initialize")
    print(f"   - Main loop: nlu → interpret → integrate → select → nlg → generate → nlu")
    print(f"   - Conditional: select → nlg (when has_response)")
    print(f"   - No-response: select → nlu (when not has_response)")

    print("\n" + "=" * 60)
    print("Graph Details:")
    print("=" * 60)
    print(f"Actions (nodes):")
    print(f"  • initialize - Create initial information state")
    print(f"  • nlu        - Process user input (utterance → moves)")
    print(f"  • interpret  - Apply interpretation rules")
    print(f"  • integrate  - Update information state")
    print(f"  • select     - Choose system response")
    print(f"  • nlg        - Natural language generation")
    print(f"  • generate   - Apply generation rules")

    print(f"\nTransitions (edges):")
    print(f"  • initialize → nlu (start)")
    print(f"  • nlu → interpret → integrate → select (pipeline)")
    print(f"  • select → nlg [if has_response]")
    print(f"  • select → nlu [if not has_response] (wait for input)")
    print(f"  • nlg → generate → nlu (complete response)")

    print("\n" + "=" * 60)
    print(f"✓ Visualization complete: {output_path.absolute()}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
