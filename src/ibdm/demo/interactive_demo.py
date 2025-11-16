"""Interactive CLI demo for IBDM system.

Showcases IBiS3 question accommodation and IBiS2 grounding in action.
"""

from __future__ import annotations

from typing import Any

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import RuleSet, create_integration_rules, create_selection_rules


class InteractiveDemo:
    """Interactive CLI demo application for IBDM.

    Features:
    - IBiS3 question accommodation (incremental questioning, volunteer info,
      clarification, dependencies, reaccommodation)
    - IBiS2 grounding (ICM moves, confidence-based strategies)
    - Dialogue history display
    - Internal state visualization (QUD, issues, commitments, grounding status)
    - Session persistence (future)
    """

    def __init__(
        self,
        agent_id: str = "system",
        user_id: str = "user",
        show_state: bool = True,
        show_moves: bool = True,
    ) -> None:
        """Initialize the interactive demo.

        Args:
            agent_id: ID of the system agent
            user_id: ID of the user
            show_state: Whether to show internal state after each turn
            show_moves: Whether to show dialogue moves
        """
        self.agent_id = agent_id
        self.user_id = user_id
        self.show_state = show_state
        self.show_moves = show_moves

        # Setup domain
        self.domain = get_nda_domain()

        # Setup rule sets
        self.integration_rules = RuleSet()
        for rule in create_integration_rules():
            self.integration_rules.add_rule(rule)

        self.selection_rules = RuleSet()
        for rule in create_selection_rules():
            self.selection_rules.add_rule(rule)

        # Setup dialogue engine (not used directly in this demo - we use rules manually)
        self.engine = DialogueMoveEngine(agent_id=agent_id, rules=None)

        # Initialize information state
        self.state = InformationState(agent_id=agent_id)

        # Dialogue history
        self.history: list[tuple[str, str]] = []  # (speaker, utterance)
        self.turn_count = 0

    def display_banner(self) -> None:
        """Display welcome banner."""
        print("\n" + "=" * 70)
        print("IBDM Interactive Demo - Issue-Based Dialogue Management")
        print("=" * 70)
        print("\nShowcasing:")
        print("  - IBiS3: Question Accommodation (incremental questioning, volunteer info)")
        print("  - IBiS2: Grounding & ICM (confidence-based grounding strategies)")
        print("\nCommands:")
        print("  /help     - Show this help")
        print("  /state    - Toggle state display")
        print("  /history  - Show dialogue history")
        print("  /reset    - Reset the dialogue")
        print("  /quit     - Exit the demo")
        print("\nType your message and press Enter to interact.")
        print("=" * 70 + "\n")

    def display_state(self) -> None:
        """Display current information state."""
        if not self.show_state:
            return

        print("\n" + "-" * 70)
        print("Internal State:")
        print("-" * 70)

        # QUD (Questions Under Discussion)
        if self.state.shared.qud:
            print(f"QUD ({len(self.state.shared.qud)} questions):")
            for i, q in enumerate(reversed(self.state.shared.qud), 1):
                if isinstance(q, WhQuestion):
                    print(f"  {i}. {q.predicate} = ?")
                else:
                    print(f"  {i}. {q}")
        else:
            print("QUD: (empty)")

        # Private Issues
        if self.state.private.issues:
            print(f"\nPrivate Issues ({len(self.state.private.issues)} questions pending):")
            for i, q in enumerate(self.state.private.issues, 1):
                if isinstance(q, WhQuestion):
                    print(f"  {i}. {q.predicate} = ?")
                else:
                    print(f"  {i}. {q}")
        else:
            print("\nPrivate Issues: (empty)")

        # Commitments
        if self.state.shared.commitments:
            print(f"\nCommitments ({len(self.state.shared.commitments)} facts):")
            for commitment in self.state.shared.commitments:
                print(f"  - {commitment}")
        else:
            print("\nCommitments: (empty)")

        # Plans
        if self.state.private.plan:
            active_plans = [p for p in self.state.private.plan if p.status == "active"]
            if active_plans:
                print(f"\nActive Plans ({len(active_plans)}):")
                for plan in active_plans:
                    print(f"  - {plan.plan_type} ({len(plan.subplans)} subplans)")

        # Grounding status (if any moves tracked)
        if self.state.shared.moves:
            recent_moves = self.state.shared.moves[-3:]  # Last 3 moves
            print(f"\nRecent Moves ({len(recent_moves)}):")
            for move in recent_moves:
                status = move.metadata.get("grounding_status", "unknown")
                print(f"  - {move.speaker}:{move.move_type} [{status}]")

        print("-" * 70)

    def display_move(self, move: DialogueMove) -> None:
        """Display a dialogue move with color coding."""
        if not self.show_moves:
            return

        speaker = move.speaker
        move_type = move.move_type
        content = move.content if isinstance(move.content, str) else str(move.content)

        # Color codes (simple text, no ANSI for better compatibility)
        prefix = f"[{speaker}:{move_type}]"

        # Show ICM moves specially
        if move_type.startswith("icm:"):
            print(f"\n{prefix} (ICM) {content}")
        else:
            print(f"\n{prefix} {content}")

    def display_history(self) -> None:
        """Display dialogue history."""
        print("\n" + "=" * 70)
        print("Dialogue History:")
        print("=" * 70)
        for i, (speaker, utterance) in enumerate(self.history, 1):
            print(f"{i}. {speaker}: {utterance}")
        print("=" * 70)

    def process_command(self, user_input: str) -> bool:
        """Process special commands.

        Args:
            user_input: User input string

        Returns:
            True if command was processed, False otherwise
        """
        if not user_input.startswith("/"):
            return False

        command = user_input.lower().strip()

        if command == "/help":
            self.display_banner()
        elif command == "/state":
            self.show_state = not self.show_state
            print(f"\nState display: {'ON' if self.show_state else 'OFF'}")
        elif command == "/history":
            self.display_history()
        elif command == "/reset":
            self.state = InformationState(agent_id=self.agent_id)
            self.history = []
            self.turn_count = 0
            print("\nDialogue reset.")
        elif command == "/quit":
            print("\nGoodbye!")
            return True
        else:
            print(f"\nUnknown command: {command}")
            print("Type /help for available commands.")

        return True

    def _generate_question_text(self, question: Any) -> str:
        """Generate natural language text for a question.

        Args:
            question: Question object to generate text for

        Returns:
            Natural language question string
        """
        if isinstance(question, WhQuestion):
            # Map predicates to natural language questions
            predicate_questions = {
                "legal_entities": "What are the parties to the NDA?",
                "date": "What is the effective date?",
                "time_period": "What is the duration of confidentiality obligations?",
                "jurisdiction": "What is the governing law jurisdiction?",
            }

            # Get custom question or generate default
            return predicate_questions.get(question.predicate, f"What is the {question.predicate}?")
        else:
            # For other question types (AltQuestion, YNQuestion)
            return str(question)

    def simulate_confidence(self, utterance: str) -> float:
        """Simulate confidence score for grounding demonstration.

        This will be enhanced in ibdm-100.3 to support different strategies.
        For now, return high confidence.

        Args:
            utterance: User utterance

        Returns:
            Confidence score (0.0-1.0)
        """
        # Simple heuristic: longer utterances have higher confidence
        # This is just for demo purposes
        if len(utterance) > 20:
            return 0.9  # High confidence
        elif len(utterance) > 10:
            return 0.65  # Medium confidence
        else:
            return 0.4  # Low confidence

    def process_user_input(self, utterance: str) -> DialogueMove | None:
        """Process user input and generate system response.

        Args:
            utterance: User utterance

        Returns:
            System response move, or None if no response
        """
        self.turn_count += 1
        self.history.append((self.user_id, utterance))

        print(f"\n{'=' * 70}")
        print(f"Turn {self.turn_count}")
        print(f"{'=' * 70}")
        print(f"{self.user_id}: {utterance}")

        # Simulate confidence for grounding
        confidence = self.simulate_confidence(utterance)

        # Process through dialogue engine
        # For now, use simple heuristics to create moves

        # Detect command (simple pattern matching)
        if "draft" in utterance.lower() or "nda" in utterance.lower():
            # Command to initiate NDA drafting
            user_move = DialogueMove(
                move_type="command",
                content=utterance,
                speaker=self.user_id,
                metadata={"confidence": confidence},
            )
        else:
            # Assume it's an answer - create Answer object with question reference
            # Get the top question from QUD (if any)
            top_question = self.state.shared.qud[-1] if self.state.shared.qud else None

            if top_question:
                # Create proper Answer object
                answer = Answer(content=utterance, question_ref=top_question)
                user_move = DialogueMove(
                    move_type="answer",
                    content=answer,
                    speaker=self.user_id,
                    metadata={"confidence": confidence},
                )
            else:
                # No question to answer - treat as assertion
                user_move = DialogueMove(
                    move_type="assert",
                    content=utterance,
                    speaker=self.user_id,
                    metadata={"confidence": confidence},
                )

        # Store move for rules to process
        self.state.private.beliefs["_temp_move"] = user_move

        # INTEGRATION phase
        self.state = self.integration_rules.apply_rules("integration", self.state)

        # SELECTION phase
        self.state = self.selection_rules.apply_rules("selection", self.state)

        # Check if system has a response
        response_move = None
        if self.state.private.agenda:
            response_move = self.state.private.agenda[-1]

            # Generate natural language for the response
            # Simple generation based on move type
            if response_move.move_type == "ask":
                question = self.state.shared.qud[-1] if self.state.shared.qud else None
                if question:
                    response_text = self._generate_question_text(question)
                    response_move.content = response_text

                    # Add to history
                    self.history.append((self.agent_id, response_text))
                    print(f"\n{self.agent_id}: {response_text}")

        # Display state
        self.display_state()

        return response_move

    def run(self) -> None:
        """Run the interactive demo loop."""
        self.display_banner()

        # Start with system greeting
        greeting = (
            f"\n{self.agent_id}: Hello! I can help you draft an NDA. "
            "Just say 'I need to draft an NDA' to get started.\n"
        )
        print(greeting)

        while True:
            try:
                # Get user input
                user_input = input(f"\n{self.user_id}> ").strip()

                if not user_input:
                    continue

                # Check for commands
                if self.process_command(user_input):
                    if user_input.lower() == "/quit":
                        break
                    continue

                # Process regular input
                self.process_user_input(user_input)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Type /quit to exit or continue typing.")
            except EOFError:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                import traceback

                traceback.print_exc()


def main() -> None:
    """Main entry point for the demo."""
    demo = InteractiveDemo()
    demo.run()


if __name__ == "__main__":
    main()
