"""Dialogue Move Engine for Issue-Based Dialogue Management.

The DialogueMoveEngine orchestrates the core IBDM control loop:
Interpret → Integrate → Select → Generate

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import DialogueMove, InformationState
from ibdm.rules import RuleSet


class DialogueMoveEngine:
    """Core dialogue manager implementing IBDM control algorithm.

    The engine manages a single agent's dialogue processing through four stages:
    1. Interpretation: Map utterances to dialogue moves
    2. Integration: Update information state based on moves
    3. Selection: Choose next system action
    4. Generation: Produce utterance from selected move
    """

    def __init__(self, agent_id: str, rules: RuleSet | None = None) -> None:
        """Initialize the dialogue move engine.

        Args:
            agent_id: Unique identifier for this agent
            rules: Rule set for dialogue processing (creates empty if None)
        """
        self.agent_id = agent_id
        self.rules = rules if rules is not None else RuleSet()
        self.state = InformationState(agent_id=agent_id)

    def process_input(
        self, utterance: str, speaker: str
    ) -> tuple[InformationState, DialogueMove | None]:
        """Process user input through the complete IBDM loop.

        This is the main entry point for dialogue processing.

        Args:
            utterance: The input utterance to process
            speaker: ID of the speaker who produced the utterance

        Returns:
            Tuple of (updated state, response move or None)
        """
        # 1. Interpretation: utterance → dialogue moves
        moves = self.interpret(utterance, speaker)

        # 2. Integration: apply moves to update state
        for move in moves:
            self.state = self.integrate(move)

        # 3. Selection: choose next action if it's our turn
        response_move = None
        if self.state.control.next_speaker == self.agent_id:
            response_move = self.select_action()

            # 4. Generation: produce utterance and integrate our move
            if response_move:
                utterance_text = self.generate(response_move)
                response_move.content = utterance_text
                self.state = self.integrate(response_move)

        return self.state, response_move

    def interpret(self, utterance: str, speaker: str) -> list[DialogueMove]:
        """Apply interpretation rules to map utterance to dialogue moves.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker

        Returns:
            List of interpreted dialogue moves
        """
        # Store utterance in a temporary state field for rules to access
        temp_state = self.state.clone()
        temp_state.private.beliefs["_temp_utterance"] = utterance
        temp_state.private.beliefs["_temp_speaker"] = speaker

        # Apply interpretation rules
        new_state = self.rules.apply_rules("interpretation", temp_state)

        # Extract moves from agenda (interpretation rules add them there)
        moves = new_state.private.agenda.copy()

        # Clean up temporary fields
        if "_temp_utterance" in self.state.private.beliefs:
            del self.state.private.beliefs["_temp_utterance"]
        if "_temp_speaker" in self.state.private.beliefs:
            del self.state.private.beliefs["_temp_speaker"]

        # If no interpretation rules matched, return empty list
        return moves

    def integrate(self, move: DialogueMove) -> InformationState:
        """Apply integration rules to update state based on a move.

        Args:
            move: The dialogue move to integrate

        Returns:
            Updated information state
        """
        # Store the move temporarily for rules to access
        temp_state = self.state.clone()
        temp_state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        new_state = self.rules.apply_rules("integration", temp_state)

        # Clean up temporary field
        if "_temp_move" in new_state.private.beliefs:
            del new_state.private.beliefs["_temp_move"]

        return new_state

    def select_action(self) -> DialogueMove | None:
        """Apply selection rules to choose next system action.

        Returns:
            Selected dialogue move, or None if no action is chosen
        """
        # First check if there's something on the agenda
        if self.state.private.agenda:
            return self.state.private.agenda.pop(0)

        # Otherwise, apply selection rules to determine what to do
        # Selection rules should add moves to the agenda
        new_state, _ = self.rules.apply_first_matching("selection", self.state)

        # Update state if selection rules modified it
        if new_state != self.state:
            self.state = new_state

        # Check agenda again after selection rules
        if self.state.private.agenda:
            return self.state.private.agenda.pop(0)

        return None

    def generate(self, move: DialogueMove) -> str:
        """Apply generation rules to produce utterance from move.

        Args:
            move: The dialogue move to generate utterance for

        Returns:
            Generated utterance text
        """
        # Store the move temporarily for rules to access
        temp_state = self.state.clone()
        temp_state.private.beliefs["_temp_generate_move"] = move

        # Apply generation rules
        new_state = self.rules.apply_rules("generation", temp_state)

        # Extract generated text from beliefs (generation rules put it there)
        generated_text = new_state.private.beliefs.get("_temp_generated_text", "")

        # Clean up temporary fields
        if "_temp_generate_move" in self.state.private.beliefs:
            del self.state.private.beliefs["_temp_generate_move"]
        if "_temp_generated_text" in self.state.private.beliefs:
            del self.state.private.beliefs["_temp_generated_text"]

        # If no text was generated, use a default based on move type
        if not generated_text:
            generated_text = self._default_generation(move)

        return generated_text

    def _default_generation(self, move: DialogueMove) -> str:
        """Provide default text generation if no generation rules match.

        Args:
            move: The dialogue move to generate text for

        Returns:
            Default generated text
        """
        if move.move_type == "greet":
            return "Hello!"
        elif move.move_type == "quit":
            return "Goodbye!"
        elif move.move_type == "ask":
            return f"Question: {move.content}"
        elif move.move_type == "answer":
            return f"Answer: {move.content}"
        else:
            return str(move.content)

    def reset(self) -> None:
        """Reset the engine to initial state."""
        self.state = InformationState(agent_id=self.agent_id)

    def get_state(self) -> InformationState:
        """Get the current information state.

        Returns:
            Current information state
        """
        return self.state

    def set_state(self, state: InformationState) -> None:
        """Set the information state.

        Args:
            state: New information state
        """
        self.state = state

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"DialogueMoveEngine(agent={self.agent_id}, "
            f"rules={self.rules.rule_count()}, "
            f"qud={len(self.state.shared.qud)})"
        )
