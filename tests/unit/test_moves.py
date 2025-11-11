"""Unit tests for DialogueMove class."""

import time

from ibdm.core import Answer, DialogueMove, WhQuestion


class TestDialogueMove:
    """Tests for DialogueMove class."""

    def test_creation(self):
        """Test creating a DialogueMove."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        move = DialogueMove(move_type="ask", content=q, speaker="user")
        assert move.move_type == "ask"
        assert move.content == q
        assert move.speaker == "user"
        assert isinstance(move.timestamp, float)

    def test_timestamp_is_current(self):
        """Test that timestamp is approximately current time."""
        before = time.time()
        move = DialogueMove(move_type="greet", content="hello", speaker="system")
        after = time.time()
        assert before <= move.timestamp <= after

    def test_custom_timestamp(self):
        """Test creating a DialogueMove with custom timestamp."""
        custom_time = 1234567890.0
        move = DialogueMove(move_type="ask", content="test", speaker="user", timestamp=custom_time)
        assert move.timestamp == custom_time

    def test_ask_move(self):
        """Test creating an ask move."""
        q = WhQuestion(variable="x", predicate="location(stockholm, x)")
        move = DialogueMove(move_type="ask", content=q, speaker="user")
        assert move.move_type == "ask"
        assert move.content == q

    def test_answer_move(self):
        """Test creating an answer move."""
        a = Answer(content="sunny")
        move = DialogueMove(move_type="answer", content=a, speaker="system")
        assert move.move_type == "answer"
        assert move.content == a

    def test_assert_move(self):
        """Test creating an assert move."""
        move = DialogueMove(move_type="assert", content="It is raining", speaker="user")
        assert move.move_type == "assert"
        assert move.content == "It is raining"

    def test_request_move(self):
        """Test creating a request move."""
        move = DialogueMove(move_type="request", content="open window", speaker="user")
        assert move.move_type == "request"
        assert move.content == "open window"

    def test_greet_move(self):
        """Test creating a greet move."""
        move = DialogueMove(move_type="greet", content="Hello!", speaker="user")
        assert move.move_type == "greet"
        assert move.content == "Hello!"

    def test_quit_move(self):
        """Test creating a quit move."""
        move = DialogueMove(move_type="quit", content="Goodbye", speaker="user")
        assert move.move_type == "quit"
        assert move.content == "Goodbye"

    def test_icm_move(self):
        """Test creating an ICM (interactive communication management) move."""
        move = DialogueMove(move_type="icm", content="I didn't understand", speaker="system")
        assert move.move_type == "icm"
        assert move.content == "I didn't understand"

    def test_str_representation(self):
        """Test string representation."""
        move = DialogueMove(move_type="greet", content="hello", speaker="user")
        s = str(move)
        assert "user" in s
        assert "greet" in s
        assert "hello" in s
