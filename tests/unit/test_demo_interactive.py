"""Tests for interactive demo module."""

from __future__ import annotations

from ibdm.core import InformationState, WhQuestion
from ibdm.demo.interactive_demo import InteractiveDemo


class TestInteractiveDemoCreation:
    """Test InteractiveDemo initialization."""

    def test_creation_default(self) -> None:
        """Test default InteractiveDemo creation."""
        demo = InteractiveDemo()

        assert demo.agent_id == "system"
        assert demo.user_id == "user"
        assert demo.show_state is True
        assert demo.show_moves is True
        assert demo.confidence_mode == "heuristic"

    def test_creation_custom(self) -> None:
        """Test custom InteractiveDemo creation."""
        demo = InteractiveDemo(
            agent_id="agent",
            user_id="alice",
            show_state=False,
            show_moves=False,
            confidence_mode="optimistic",
        )

        assert demo.agent_id == "agent"
        assert demo.user_id == "alice"
        assert demo.show_state is False
        assert demo.show_moves is False
        assert demo.confidence_mode == "optimistic"

    def test_state_initialization(self) -> None:
        """Test information state is initialized."""
        demo = InteractiveDemo()

        assert isinstance(demo.state, InformationState)
        assert demo.state.shared.qud == []
        assert demo.state.shared.commitments == []
        assert demo.state.private.issues == []

    def test_history_initialization(self) -> None:
        """Test dialogue history is initialized."""
        demo = InteractiveDemo()

        assert demo.history == []
        assert demo.turn_count == 0
        assert len(demo.dialogue_history.turns) == 0
        assert demo.dialogue_history.session_id.startswith("demo-")

    def test_visualizer_initialization(self) -> None:
        """Test visualizer is initialized."""
        demo = InteractiveDemo()

        assert demo.visualizer is not None
        assert demo.visualizer.width == 70


class TestConfidenceSimulation:
    """Test confidence simulation methods."""

    def test_simulate_confidence_heuristic_short(self) -> None:
        """Test heuristic mode with short utterance."""
        demo = InteractiveDemo(confidence_mode="heuristic")

        confidence = demo.simulate_confidence("Hi")

        assert 0.0 <= confidence <= 1.0
        assert confidence == 0.4  # Short utterance

    def test_simulate_confidence_heuristic_medium(self) -> None:
        """Test heuristic mode with medium utterance."""
        demo = InteractiveDemo(confidence_mode="heuristic")

        confidence = demo.simulate_confidence("Hello there, how are you?")

        assert confidence == 0.65  # Medium length

    def test_simulate_confidence_heuristic_long(self) -> None:
        """Test heuristic mode with long utterance."""
        demo = InteractiveDemo(confidence_mode="heuristic")

        confidence = demo.simulate_confidence("This is a longer utterance with many words")

        assert confidence == 0.9  # Long utterance

    def test_simulate_confidence_random(self) -> None:
        """Test random confidence mode."""
        demo = InteractiveDemo(confidence_mode="random")

        confidence = demo.simulate_confidence("Hello")

        assert 0.3 <= confidence <= 1.0

    def test_simulate_confidence_optimistic(self) -> None:
        """Test optimistic confidence mode."""
        demo = InteractiveDemo(confidence_mode="optimistic")

        confidence = demo.simulate_confidence("Hello")

        assert confidence == 0.9

    def test_simulate_confidence_cautious(self) -> None:
        """Test cautious confidence mode."""
        demo = InteractiveDemo(confidence_mode="cautious")

        confidence = demo.simulate_confidence("Hello")

        assert confidence == 0.65

    def test_simulate_confidence_pessimistic(self) -> None:
        """Test pessimistic confidence mode."""
        demo = InteractiveDemo(confidence_mode="pessimistic")

        confidence = demo.simulate_confidence("Hello")

        assert confidence == 0.4


class TestQuestionTextGeneration:
    """Test natural language question generation."""

    def test_generate_question_text_legal_entities(self) -> None:
        """Test NDA legal_entities question generation."""
        demo = InteractiveDemo()

        question = WhQuestion(predicate="legal_entities")
        text = demo._generate_question_text(question)

        assert text == "What are the parties to the NDA?"

    def test_generate_question_text_date(self) -> None:
        """Test NDA date question generation."""
        demo = InteractiveDemo()

        question = WhQuestion(predicate="date")
        text = demo._generate_question_text(question)

        assert text == "What is the effective date?"

    def test_generate_question_text_time_period(self) -> None:
        """Test NDA time_period question generation."""
        demo = InteractiveDemo()

        question = WhQuestion(predicate="time_period")
        text = demo._generate_question_text(question)

        assert text == "What is the duration of confidentiality obligations?"

    def test_generate_question_text_jurisdiction(self) -> None:
        """Test NDA jurisdiction question generation."""
        demo = InteractiveDemo()

        question = WhQuestion(predicate="jurisdiction")
        text = demo._generate_question_text(question)

        assert text == "What is the governing law jurisdiction?"

    def test_generate_question_text_unknown(self) -> None:
        """Test unknown predicate question generation."""
        demo = InteractiveDemo()

        question = WhQuestion(predicate="unknown_predicate")
        text = demo._generate_question_text(question)

        assert "unknown_predicate" in text


class TestProcessUserInput:
    """Test user input processing."""

    def test_process_command_input(self) -> None:
        """Test processing a command input."""
        demo = InteractiveDemo()

        # Process command-like input
        demo.process_user_input("I need to draft an NDA")

        # Should have incremented turn count
        assert demo.turn_count == 1

        # Should have recorded in history
        assert len(demo.history) == 1
        assert demo.history[0] == ("user", "I need to draft an NDA")

        # Should have recorded in dialogue history
        assert demo.dialogue_history.turns is not None
        assert len(demo.dialogue_history.turns) >= 1

    def test_process_multiple_turns(self) -> None:
        """Test processing multiple turns."""
        demo = InteractiveDemo()

        demo.process_user_input("I need to draft an NDA")
        demo.process_user_input("Acme Corp and Smith Inc")

        assert demo.turn_count == 2
        assert len(demo.history) >= 2


class TestStateDisplay:
    """Test state display methods."""

    def test_display_state_toggle(self) -> None:
        """Test toggling state display."""
        demo = InteractiveDemo(show_state=True)

        assert demo.show_state is True

        # Should not crash when displaying state
        demo.display_state()

        # Toggle off
        demo.show_state = False
        demo.display_state()  # Should do nothing


class TestHistoryManagement:
    """Test dialogue history management."""

    def test_reset_dialogue(self) -> None:
        """Test resetting dialogue."""
        demo = InteractiveDemo()

        # Add some history
        demo.process_user_input("Hello")
        assert demo.turn_count > 0

        # Reset
        demo._reset_dialogue()

        # Check everything is reset
        assert demo.turn_count == 0
        assert len(demo.history) == 0
        assert demo.state.shared.qud == []
        assert len(demo.dialogue_history.turns) == 0

    def test_confidence_mode_change(self) -> None:
        """Test changing confidence mode."""
        demo = InteractiveDemo(confidence_mode="heuristic")

        assert demo.confidence_mode == "heuristic"

        # Manually change (simulating command)
        demo.confidence_mode = "optimistic"

        assert demo.confidence_mode == "optimistic"

        # Check it affects simulation
        confidence = demo.simulate_confidence("test")
        assert confidence == 0.9


class TestDemoMetadata:
    """Test demo metadata tracking."""

    def test_dialogue_history_metadata(self) -> None:
        """Test dialogue history has correct metadata."""
        demo = InteractiveDemo(
            agent_id="agent",
            user_id="alice",
            confidence_mode="optimistic",
        )

        metadata = demo.dialogue_history.metadata

        assert metadata is not None
        assert metadata["agent_id"] == "agent"
        assert metadata["user_id"] == "alice"
        assert metadata["confidence_mode"] == "optimistic"

    def test_session_id_unique(self) -> None:
        """Test each demo gets unique session ID."""
        demo1 = InteractiveDemo()
        demo2 = InteractiveDemo()

        assert demo1.dialogue_history.session_id != demo2.dialogue_history.session_id
        assert demo1.dialogue_history.session_id.startswith("demo-")
        assert demo2.dialogue_history.session_id.startswith("demo-")
