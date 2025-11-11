"""Burr state machine for IBDM dialogue management.

This module provides the main state machine implementation that orchestrates
the IBDM control loop using Burr's application framework.
"""

from typing import Any

from burr.core import ApplicationBuilder, State, default, expr

from ibdm.burr_integration.actions import generate, idle, initialize, integrate, interpret, select
from ibdm.rules import RuleSet


def create_dialogue_application(
    agent_id: str = "system",
    rules: RuleSet | None = None,
    app_id: str | None = None,
    storage_dir: str | None = None,
) -> Any:
    """Create a Burr application for dialogue management.

    The state machine implements the IBDM control loop:
    - idle: Waiting for input
    - interpret: Map utterance to dialogue moves
    - integrate: Update information state
    - select: Choose next action
    - generate: Produce response utterance

    Args:
        agent_id: ID of the dialogue agent
        rules: Optional rule set for dialogue processing
        app_id: Optional application ID for tracking
        storage_dir: Optional directory for state persistence

    Returns:
        Burr Application instance
    """
    # Build the application
    builder = (
        ApplicationBuilder()
        .with_actions(
            # Initialization and idle
            initialize=initialize,
            idle=idle,
            # Main control loop actions
            interpret=interpret,
            integrate=integrate,
            select=select,
            generate=generate,
        )
        .with_transitions(
            # Start with initialization
            ("initialize", "idle", default),
            # From idle, wait for input trigger (handled externally)
            ("idle", "interpret", default),
            # After interpretation, always integrate
            ("interpret", "integrate", default),
            # After integration, decide what to do next
            ("integrate", "select", default),
            # From select, either generate or go idle
            ("select", "generate", expr("has_response")),
            ("select", "idle", default),
            # After generation, go back to idle
            ("generate", "idle", default),
        )
        .with_entrypoint("initialize")
        .with_state(agent_id=agent_id, rules=rules)
    )

    # Add tracking if app_id is provided
    if app_id:
        builder = builder.with_identifiers(app_id=app_id)

    # Add persistence if storage directory is provided
    if storage_dir and app_id:
        from burr.tracking import LocalTrackingClient

        # LocalTrackingClient expects a project name, not a path
        # Use app_id as project name and specify storage_dir separately
        tracker = LocalTrackingClient(project=app_id, storage_dir=storage_dir)
        builder = builder.with_tracker(tracker)

    # Build and return the application
    app = builder.build()

    return app


class DialogueStateMachine:
    """High-level interface for the Burr-based dialogue state machine.

    This class provides a simple API for processing dialogue turns using
    the Burr state machine implementation.
    """

    def __init__(
        self,
        agent_id: str = "system",
        rules: RuleSet | None = None,
        app_id: str | None = None,
        storage_dir: str | None = None,
    ):
        """Initialize the dialogue state machine.

        Args:
            agent_id: ID of the dialogue agent
            rules: Optional rule set for dialogue processing
            app_id: Optional application ID for tracking
            storage_dir: Optional directory for state persistence
        """
        self.app = create_dialogue_application(
            agent_id=agent_id, rules=rules, app_id=app_id, storage_dir=storage_dir
        )
        self._initialized = False

    def initialize(self) -> dict[str, Any]:
        """Initialize the state machine.

        Returns:
            Result from initialization action
        """
        if not self._initialized:
            action, result, state = self.app.step()
            self._initialized = True
            return result
        return {"ready": True}

    def process_utterance(self, utterance: str, speaker: str = "user") -> dict[str, Any]:
        """Process a single utterance through the dialogue loop.

        Args:
            utterance: The input utterance to process
            speaker: ID of the speaker (default: "user")

        Returns:
            Dictionary containing:
                - utterance_text: The generated response (if any)
                - has_response: Whether a response was generated
                - state: Current dialogue state
        """
        # Ensure initialized
        if not self._initialized:
            self.initialize()

        # Update state with input
        state = self.app.state
        state = state.update(utterance=utterance, speaker=speaker, integrated=False)
        self.app._state = state

        # Run through the control loop
        # The app should be at 'idle' state, so first step transitions idle -> interpret
        action, result, state = self.app.step()

        # If we're at idle, step again to get to interpret
        if action.name == "idle":
            action, result, state = self.app.step()

        # Now we should be at interpret
        if action.name != "interpret":
            raise AssertionError(f"Expected interpret after idle, got {action.name}")

        # Step 2: integrate
        action, result, state = self.app.step()
        if action.name != "integrate":
            raise AssertionError(f"Expected integrate, got {action.name}")

        # Step 3: select
        action, result, state = self.app.step()
        if action.name != "select":
            raise AssertionError(f"Expected select, got {action.name}")

        response_data = {
            "has_response": result.get("has_response", False),
            "utterance_text": "",
        }

        # Step 4: generate (if we have a response) or go to idle
        action, result, state = self.app.step()
        if action.name == "generate":
            response_data["utterance_text"] = result.get("utterance_text", "")
            # Step to idle after generate
            action, result, state = self.app.step()
        # else we're already at idle

        return response_data

    def get_state(self) -> State:
        """Get the current Burr state.

        Returns:
            Current state
        """
        return self.app.state

    def get_information_state(self) -> Any:
        """Get the current information state from the engine.

        Returns:
            Current InformationState
        """
        engine = self.app.state.get("engine")
        if engine is not None:
            return engine.state
        return None

    def reset(self) -> None:
        """Reset the state machine to initial state."""
        # Reset the engine if it exists
        engine = self.app.state.get("engine")
        if engine is not None:
            engine.reset()

    def visualize(self, output_path: str = "dialogue_flow.png") -> None:
        """Visualize the state machine graph.

        Args:
            output_path: Path to save the visualization
        """
        try:
            self.app.visualize(output_file_path=output_path, include_conditions=True)
        except Exception as e:
            print(f"Visualization failed: {e}")
            print("Make sure graphviz is installed: apt-get install graphviz")
