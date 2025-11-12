# IBDM System Demonstrations

This directory contains executable demonstrations of the IBDM system's capabilities.

## Quick Start

```bash
# Run from project root
cd /home/user/ibdm

# Ensure dependencies are installed
uv pip install --system -e ".[dev]"

# Run any demo
python demos/01_core_concepts.py
python demos/02_cost_analysis.py
```

## Available Demos

### 1. Core Concepts (`01_core_concepts.py`)

**Duration**: 5 minutes
**Audience**: Everyone
**Prerequisites**: None (no API keys needed)

Demonstrates the fundamental IBDM concepts:
- Semantic question representation
- Question resolution matching
- Information State structure
- Dialogue moves
- QUD stack evolution

**Run**:
```bash
python demos/01_core_concepts.py
```

### 2. Cost Analysis (`02_cost_analysis.py`)

**Duration**: 3 minutes
**Audience**: Technical leads, product managers
**Prerequisites**: None (no API keys needed)

Compares costs between:
- Always-LLM approach (using Sonnet 4.5 for everything)
- Hybrid approach (rules + Haiku + Sonnet)

Shows:
- Cost breakdown by volume
- ROI analysis
- Performance comparison

**Run**:
```bash
python demos/02_cost_analysis.py
```

## Demo Order Recommendations

### For Technical Audiences
1. `01_core_concepts.py` - Understand the foundation
2. `02_cost_analysis.py` - See the business value

### For Business Audiences
1. `02_cost_analysis.py` - See the value prop first
2. `01_core_concepts.py` - Understand how it works

### For Academic Audiences
1. `01_core_concepts.py` - Theoretical foundation
2. Reference papers in README.md

## Creating Your Own Demos

Demos should be:
- **Self-contained**: Run without external setup
- **Well-documented**: Clear comments and print statements
- **Progressive**: Build complexity gradually
- **Instructive**: Explain what's happening

Example structure:
```python
#!/usr/bin/env python3
"""
Demo X: Brief Description

What this demo shows and why it matters.

Run: python demos/0X_demo_name.py
"""

def demo_feature_1():
    """Demonstrate specific feature"""
    print("=" * 60)
    print("DEMO X.1: Feature Name")
    print("=" * 60)

    # Your demo code
    # ...

    print("\n✓ Key takeaway!")

def main():
    """Run all demo sections"""
    print("\n" + "=" * 60)
    print("DEMO TITLE")
    print("=" * 60)

    demo_feature_1()
    # ... more demos

    print("\nSUMMARY:")
    print("  • Key point 1")
    print("  • Key point 2")

if __name__ == "__main__":
    main()
```

## Testing Demos

Before presenting:
```bash
# Test all demos run without errors
python demos/01_core_concepts.py
python demos/02_cost_analysis.py

# Check code quality
ruff check demos/
ruff format demos/
```

## Related Documentation

- **DEMO_PLAN.md**: Complete demo script with talking points
- **SYSTEM_ACHIEVEMENTS.md**: Full system documentation
- **GETTING_STARTED.md**: Tutorial for using IBDM
- **README.md**: Project overview

## Questions?

See DEMO_PLAN.md for:
- Common questions and answers
- Detailed explanations of each concept
- Tips for presenting

## Contributing Demos

New demos welcome! Consider creating demos for:
- Multi-turn dialogue examples
- Domain-specific applications
- Integration examples
- Performance benchmarks
- Comparison with other systems
