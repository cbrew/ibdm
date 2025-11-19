"""Interactive demo application for IBDM.

Showcases IBiS3 question accommodation and IBiS2 grounding in action.
"""

# Lazy imports to avoid pulling in heavy dependencies (burr, etc.)
# when only using visualization classes
from ibdm.demo.scenarios import (
    DemoScenario,
    ScenarioStep,
    get_ibis2_scenarios,
    get_ibis3_scenarios,
    get_scenario,
    list_scenarios,
)
from ibdm.demo.visualization import DialogueHistory, DialogueVisualizer, TurnRecord


def __getattr__(name: str):
    """Lazy import for InteractiveDemo to avoid burr dependency."""
    if name == "InteractiveDemo":
        from ibdm.demo.interactive_demo import InteractiveDemo

        return InteractiveDemo
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "InteractiveDemo",
    "DemoScenario",
    "ScenarioStep",
    "get_scenario",
    "list_scenarios",
    "get_ibis3_scenarios",
    "get_ibis2_scenarios",
    "DialogueHistory",
    "DialogueVisualizer",
    "TurnRecord",
]
