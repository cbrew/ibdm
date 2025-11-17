"""Burr state machine for IBDM dialogue management.

This module provides the main state machine implementation that orchestrates
the IBDM control loop using Burr's application framework.
"""

from typing import TYPE_CHECKING, Any

from burr.core import ApplicationBuilder, State, default, expr

from ibdm.burr_integration.actions import (
    generate,
    initialize,
    integrate,
    interpret,
    nlg,
    nlu,
    select,
)
from ibdm.core import InformationState
from ibdm.rules import RuleSet

if TYPE_CHECKING:
    from ibdm.nlg import NLGEngine
    from ibdm.nlu import NLUEngine


def create_dialogue_application(
    agent_id: str = "system",
    rules: RuleSet | None = None,
    engine_class: type | None = None,
    engine_config: Any | None = None,
    nlu_engine: "NLUEngine | None" = None,
    nlg_engine: "NLGEngine | None" = None,
    app_id: str | None = None,
    storage_dir: str | None = None,
) -> Any:
    """Create a Burr application for dialogue management.

    The state machine implements the 6-stage IBDM control loop:
    initialize → nlu → interpret → integrate → select → nlg → generate → nlu (loop)

    User input (utterance, speaker) is passed as inputs to app.run(), which are
    received by the nlu action and written to state for subsequent actions.

    Args:
        agent_id: ID of the dialogue agent
        rules: Optional rule set for dialogue processing
        engine_class: Optional engine class (e.g., NLUDialogueEngine)
        engine_config: Optional configuration for the engine
        nlu_engine: NLU engine for processing utterances
        nlg_engine: NLG engine for generating responses
        app_id: Optional application ID for tracking
        storage_dir: Optional directory for state persistence

    Returns:
        Burr Application instance
    """
    # Import here (actions.py already imports it, so no circular import)
    from ibdm.engine import DialogueMoveEngine

    # Prepare initial state with engine_class always set
    initial_state: dict[str, Any] = {
        "agent_id": agent_id,
        "rules": rules,
        "engine_class": engine_class if engine_class is not None else DialogueMoveEngine,
    }
    if engine_config is not None:
        initial_state["engine_config"] = engine_config
    if nlu_engine is not None:
        initial_state["nlu_engine"] = nlu_engine
    if nlg_engine is not None:
        initial_state["nlg_engine"] = nlg_engine

    # 6-stage pipeline: initialize → nlu → interpret → integrate → select → nlg → generate → nlu
    # Loop back to nlu for next input
    builder = (
        ApplicationBuilder()
        .with_actions(
            # Initialization
            initialize=initialize,
            # 6-stage control loop actions
            nlu=nlu,
            interpret=interpret,
            integrate=integrate,
            select=select,
            nlg=nlg,
            generate=generate,
        )
        .with_transitions(
            # Initialization
            ("initialize", "nlu", default),
            # 6-stage pipeline
            ("nlu", "interpret", default),
            ("interpret", "integrate", default),
            ("integrate", "select", default),
            # Response path: select → nlg → generate → nlu (loop)
            ("select", "nlg", expr("has_response")),
            ("nlg", "generate", default),
            ("generate", "nlu", default),
            # No response path: halt at select (controlled by halt_after in process_utterance)
            # When has_response=False, halt_after=["select"] stops execution
            # Next process_utterance() call provides new inputs and resumes at nlu
        )
        .with_entrypoint("initialize")
        .with_state(**initial_state)
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
    the 6-stage Burr pipeline. User inputs are passed via app.run(inputs={...})
    following Burr best practices.
    """

    def __init__(
        self,
        agent_id: str = "system",
        rules: RuleSet | None = None,
        engine_class: type | None = None,
        engine_config: Any | None = None,
        nlu_engine: "NLUEngine | None" = None,
        nlg_engine: "NLGEngine | None" = None,
        app_id: str | None = None,
        storage_dir: str | None = None,
    ):
        """Initialize the dialogue state machine.

        Args:
            agent_id: ID of the dialogue agent
            rules: Optional rule set for dialogue processing
            engine_class: Optional engine class (e.g., NLUDialogueEngine)
            engine_config: Optional configuration for the engine
            nlu_engine: Optional NLU engine for 6-stage pipeline
            nlg_engine: Optional NLG engine for 6-stage pipeline
            app_id: Optional application ID for tracking
            storage_dir: Optional directory for state persistence
        """
        self.app = create_dialogue_application(
            agent_id=agent_id,
            rules=rules,
            engine_class=engine_class,
            engine_config=engine_config,
            nlu_engine=nlu_engine,
            nlg_engine=nlg_engine,
            app_id=app_id,
            storage_dir=storage_dir,
        )
        self._initialized = False

    def initialize(self) -> dict[str, Any]:
        """Initialize the state machine.

        Runs the initialize action and positions at nlu, ready to receive input.

        Returns:
            Result from initialization action
        """
        if not self._initialized:
            _, result, _ = self.app.run(halt_after=["initialize"])
            self._initialized = True
            return result
        return {"ready": True}

    def process_utterance(self, utterance: str, speaker: str = "user") -> dict[str, Any]:
        """Process a single utterance through the dialogue loop.

        Uses app.run() with inputs to pass utterance and speaker to the nlu action,
        then runs through the 6-stage pipeline until a response is generated or
        the system determines no response is needed.

        Args:
            utterance: The input utterance to process
            speaker: ID of the speaker (default: "user")

        Returns:
            Dictionary containing:
                - utterance_text: The generated response (if any)
                - has_response: Whether a response was generated
        """
        # Ensure initialized
        if not self._initialized:
            self.initialize()

        # Run through the pipeline with inputs, halt after response generated or no response
        # halt_after=["generate", "select"] stops after:
        #   - "generate": response path (select→nlg→generate)
        #   - "select": no response path (select→nlu)
        action, result, state = self.app.run(
            halt_after=["generate", "select"], inputs={"utterance": utterance, "speaker": speaker}
        )

        # Extract response from final state
        return {
            "has_response": state.get("has_response", False),
            "utterance_text": state.get("utterance_text", ""),
        }

    def get_state(self) -> State:
        """Get the current Burr state.

        Returns:
            Current state
        """
        return self.app.state

    def get_information_state(self) -> InformationState | None:
        """Get the current information state from Burr State.

        Returns:
            Current InformationState reconstructed from Burr State dict
        """
        info_state_dict = self.app.state.get("information_state")
        if info_state_dict is None:
            return None
        return InformationState.from_dict(info_state_dict)

    def reset(self) -> None:
        """Reset the state machine to initial state."""
        # Reset the iI nformation state in Burr State
        engine = self.app.state.get("engine")
        if engine is not None:
            initial_state = engine.create_initial_state()
            initial_state_dict = initial_state.to_dict()
            self.app._state = self.app.state.update(information_state=initial_state_dict)

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
