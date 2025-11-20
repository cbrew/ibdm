"""Interactive demo application for IBDM.

Showcases IBiS3 question accommodation and IBiS2 grounding in action.
"""

from ibdm.demo.execution_controller import ExecutionController, ExecutionMode
from ibdm.demo.interactive_demo import InteractiveDemo
from ibdm.demo.orchestrator import DemoDialogueOrchestrator
from ibdm.demo.scenario_loader import (
    Scenario,
    ScenarioLoader,
    ScenarioMetadata,
    ScenarioTurn,
    get_loader,
    list_scenarios as list_json_scenarios,
    list_scenarios_by_category,
    load_scenario,
    search_scenarios,
)
from ibdm.demo.scenario_runner import ScenarioRunner, run_scenario
from ibdm.demo.scenarios import (
    DemoScenario,
    ScenarioStep,
    get_ibis2_scenarios,
    get_ibis3_scenarios,
    get_scenario,
    list_scenarios,
)
from ibdm.demo.visualization import DialogueHistory, DialogueVisualizer, TurnRecord

__all__ = [
    # Execution Control
    "ExecutionController",
    "ExecutionMode",
    # Scenario System (JSON-based)
    "Scenario",
    "ScenarioLoader",
    "ScenarioMetadata",
    "ScenarioTurn",
    "ScenarioRunner",
    "get_loader",
    "list_json_scenarios",
    "list_scenarios_by_category",
    "load_scenario",
    "search_scenarios",
    "run_scenario",
    # Legacy Demo System
    "InteractiveDemo",
    "DemoDialogueOrchestrator",
    "DemoScenario",
    "ScenarioStep",
    "get_scenario",
    "list_scenarios",
    "get_ibis3_scenarios",
    "get_ibis2_scenarios",
    # Visualization
    "DialogueHistory",
    "DialogueVisualizer",
    "TurnRecord",
]
