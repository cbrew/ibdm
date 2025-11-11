"""Unit tests for Answer class."""

from ibdm.core import Answer, WhQuestion


class TestAnswer:
    """Tests for Answer class."""

    def test_creation(self):
        """Test creating an Answer."""
        a = Answer(content="sunny")
        assert a.content == "sunny"
        assert a.question_ref is None
        assert a.certainty == 1.0

    def test_creation_with_question_ref(self):
        """Test creating an Answer with question reference."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        a = Answer(content="sunny", question_ref=q)
        assert a.content == "sunny"
        assert a.question_ref == q
        assert a.certainty == 1.0

    def test_creation_with_certainty(self):
        """Test creating an Answer with custom certainty."""
        a = Answer(content="probably sunny", certainty=0.7)
        assert a.content == "probably sunny"
        assert a.certainty == 0.7

    def test_boolean_content(self):
        """Test Answer with boolean content."""
        a = Answer(content=True)
        assert a.content is True

    def test_numeric_content(self):
        """Test Answer with numeric content."""
        a = Answer(content=42)
        assert a.content == 42

    def test_object_content(self):
        """Test Answer with object content."""
        obj = {"temperature": 20, "condition": "sunny"}
        a = Answer(content=obj)
        assert a.content == obj

    def test_str_representation(self):
        """Test string representation."""
        a = Answer(content="sunny")
        assert str(a) == "Answer(sunny)"

    def test_str_representation_with_low_certainty(self):
        """Test string representation with low certainty."""
        a = Answer(content="sunny", certainty=0.7)
        s = str(a)
        assert "Answer(sunny)" in s
        assert "0.70" in s
