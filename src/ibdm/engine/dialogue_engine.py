"""Dialogue Move Engine for Issue-Based Dialogue Management.

The DialogueMoveEngine orchestrates the core IBDM control loop:
Interpret → Integrate → Select → Generate

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ibdm.core import Answer, DialogueMove, InformationState, Question, WhQuestion, YNQuestion
from ibdm.rules import RuleSet

if TYPE_CHECKING:
    from ibdm.nlu.nlu_result import NLUResult


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

        The engine is now stateless - all methods accept InformationState as a parameter.

        Args:
            agent_id: Unique identifier for this agent
            rules: Rule set for dialogue processing (creates empty if None)
        """
        self.agent_id = agent_id
        self.rules = rules if rules is not None else RuleSet()

    def process_input(
        self, utterance: str, speaker: str, state: InformationState
    ) -> tuple[InformationState, DialogueMove | None]:
        """Process user input through the complete IBDM loop.

        This is the main entry point for dialogue processing.

        Args:
            utterance: The input utterance to process
            speaker: ID of the speaker who produced the utterance
            state: Current information state

        Returns:
            Tuple of (updated state, response move or None)
        """
        # 1. Interpretation: utterance → dialogue moves
        moves = self.interpret(utterance, speaker, state)

        # 2. Integration: apply moves to update state
        current_state = state
        for move in moves:
            current_state = self.integrate(move, current_state)

        # 3. Selection: choose next action if it's our turn
        response_move = None
        if current_state.control.next_speaker == self.agent_id:
            response_move, current_state = self.select_action(current_state)

            # 4. Generation: produce utterance and integrate our move
            if response_move:
                utterance_text = self.generate(response_move, current_state)
                response_move.content = utterance_text
                current_state = self.integrate(response_move, current_state)

        return current_state, response_move

    def interpret(
        self, utterance: str, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        """Apply interpretation rules to map utterance to dialogue moves.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker
            state: Information state to use for rule application

        Returns:
            List of interpreted dialogue moves
        """
        # Store utterance in a temporary state field for rules to access
        temp_state = state.clone()
        temp_state.private.beliefs["_temp_utterance"] = utterance
        temp_state.private.beliefs["_temp_speaker"] = speaker

        # Apply interpretation rules
        new_state = self.rules.apply_rules("interpretation", temp_state)

        # Extract moves from agenda (interpretation rules add them there)
        moves = new_state.private.agenda.copy()

        # If no interpretation rules matched, return empty list
        return moves

    def interpret_from_nlu_result(
        self, nlu_result: NLUResult, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        """Create dialogue moves from NLU result.

        This method is used in the 6-stage pipeline where NLU processing
        happens in a separate stage. It creates DialogueMoves based on the
        structured NLU result rather than interpreting a raw utterance.

        Args:
            nlu_result: Structured NLU result from NLU engine
            speaker: ID of the speaker
            state: Current information state

        Returns:
            List of dialogue moves
        """
        moves: list[DialogueMove] = []
        dialogue_act = nlu_result.dialogue_act

        # Create move based on dialogue act
        if dialogue_act == "question" or dialogue_act == "ask":
            # Create question move
            if nlu_result.question_details:
                # Try to create a proper Question object
                question = self._create_question_from_details(nlu_result.question_details)
                content = question if question else "question"
            else:
                content = "question"

            moves.append(
                DialogueMove(
                    move_type="ask",
                    content=content,
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "answer":
            # Create answer move
            if nlu_result.answer_content:
                # Check if there's a question on the QUD to answer
                top_qud = state.shared.top_qud()
                content_str = nlu_result.answer_content.get("content", "")
                answer = Answer(content=content_str, question_ref=top_qud)
                content = answer
            else:
                content = "answer"

            moves.append(
                DialogueMove(
                    move_type="answer",
                    content=content,
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "command":
            moves.append(
                DialogueMove(
                    move_type="command",
                    content=nlu_result.intent if nlu_result.intent else "command",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "assertion" or dialogue_act == "assert":
            moves.append(
                DialogueMove(
                    move_type="assert",
                    content="assertion",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "acknowledgment" or dialogue_act == "acknowledge":
            moves.append(
                DialogueMove(
                    move_type="acknowledge",
                    content="acknowledgment",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "clarification" or dialogue_act == "clarify":
            moves.append(
                DialogueMove(
                    move_type="clarify",
                    content="clarification",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "greeting" or dialogue_act == "greet":
            moves.append(
                DialogueMove(
                    move_type="greet",
                    content="greeting",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        elif dialogue_act == "quit" or dialogue_act == "goodbye":
            moves.append(
                DialogueMove(
                    move_type="quit",
                    content="quit",
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        else:
            # Default: create generic inform move
            moves.append(
                DialogueMove(
                    move_type="inform",
                    content=dialogue_act,
                    speaker=speaker,
                    metadata={"nlu_confidence": nlu_result.confidence},
                )
            )

        return moves

    def _create_question_from_details(
        self, question_details: dict[str, Any]
    ) -> Question | None:
        """Create a Question object from NLU question details.

        Args:
            question_details: Question details from NLU result

        Returns:
            Question object or None
        """
        question_type = str(question_details.get("question_type", "unknown"))

        try:
            if question_type == "wh":
                return WhQuestion(
                    variable=str(question_details.get("variable", "x")),
                    predicate=str(question_details.get("focus", "unknown")),
                    constraints={},
                )
            elif question_type in ["yes_no", "yn", "yes-no"]:
                proposition = str(question_details.get("proposition", "unknown"))
                return YNQuestion(proposition=proposition)
            # Note: AltQuestion would need alternatives list
            # We can add that when question_details includes it
        except Exception:
            # If we can't create a proper Question object, return None
            return None

        return None

    def integrate(self, move: DialogueMove, state: InformationState) -> InformationState:
        """Apply integration rules to update state based on a move.

        This is a pure function - it returns a new state without modifying the input.

        Args:
            move: The dialogue move to integrate
            state: Current information state

        Returns:
            Updated information state
        """
        # Store the move temporarily for rules to access
        temp_state = state.clone()
        temp_state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        new_state = self.rules.apply_rules("integration", temp_state)

        # Clean up temporary field
        if "_temp_move" in new_state.private.beliefs:
            del new_state.private.beliefs["_temp_move"]

        return new_state

    def select_action(
        self, state: InformationState
    ) -> tuple[DialogueMove | None, InformationState]:
        """Apply selection rules to choose next system action.

        This is a pure function - it returns a new state without modifying the input.

        Args:
            state: Current information state

        Returns:
            Tuple of (selected move or None, updated state with item removed from agenda)
        """
        # First check if there's something on the agenda
        if state.private.agenda:
            # Clone state and pop from agenda
            new_state = state.clone()
            move = new_state.private.agenda.pop(0)
            return move, new_state

        # Otherwise, apply selection rules to determine what to do
        # Selection rules should add moves to the agenda
        new_state, _ = self.rules.apply_first_matching("selection", state)

        # Check agenda again after selection rules
        if new_state.private.agenda:
            # Clone and pop from agenda
            final_state = new_state.clone()
            move = final_state.private.agenda.pop(0)
            return move, final_state

        return None, new_state

    def generate(self, move: DialogueMove, state: InformationState) -> str:
        """Apply generation rules to produce utterance from move.

        Args:
            move: The dialogue move to generate utterance for
            state: Current information state (used for context in generation rules)

        Returns:
            Generated utterance text
        """
        # Store the move temporarily for rules to access
        temp_state = state.clone()
        temp_state.private.beliefs["_temp_generate_move"] = move

        # Apply generation rules
        new_state = self.rules.apply_rules("generation", temp_state)

        # Extract generated text from beliefs (generation rules put it there)
        generated_text = new_state.private.beliefs.get("_temp_generated_text", "")

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

    def create_initial_state(self) -> InformationState:
        """Create a new initial InformationState for this agent.

        Returns:
            New initial information state
        """
        return InformationState(agent_id=self.agent_id)

    def __str__(self) -> str:
        """Return string representation."""
        return f"DialogueMoveEngine(agent={self.agent_id}, rules={self.rules.rule_count()})"
