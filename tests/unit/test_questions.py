"""Unit tests for Question classes."""


from ibdm.core import AltQuestion, Answer, WhQuestion, YNQuestion


class TestWhQuestion:
    """Tests for WhQuestion class."""

    def test_creation(self):
        """Test creating a WhQuestion."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        assert q.variable == "x"
        assert q.predicate == "weather(x)"
        assert q.constraints == {}

    def test_creation_with_constraints(self):
        """Test creating a WhQuestion with constraints."""
        q = WhQuestion(variable="x", predicate="weather(x)", constraints={"location": "Stockholm"})
        assert q.variable == "x"
        assert q.predicate == "weather(x)"
        assert q.constraints == {"location": "Stockholm"}

    def test_resolves_with_answer(self):
        """Test that WhQuestion resolves with a valid answer."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        a = Answer(content="sunny")
        assert q.resolves_with(a)

    def test_resolves_with_specific_answer(self):
        """Test that WhQuestion resolves with answer referencing it."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        a = Answer(content="sunny", question_ref=q)
        assert q.resolves_with(a)

    def test_does_not_resolve_with_none_content(self):
        """Test that WhQuestion does not resolve with None content."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        a = Answer(content=None)
        assert not q.resolves_with(a)

    def test_str_representation(self):
        """Test string representation."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        assert str(q) == "?x.weather(x)"

    def test_str_representation_with_constraints(self):
        """Test string representation with constraints."""
        q = WhQuestion(
            variable="x",
            predicate="weather(x)",
            constraints={"location": "Stockholm", "time": "today"},
        )
        s = str(q)
        assert s.startswith("?x.weather(x) [")
        assert "location=Stockholm" in s
        assert "time=today" in s


class TestYNQuestion:
    """Tests for YNQuestion class."""

    def test_creation(self):
        """Test creating a YNQuestion."""
        q = YNQuestion(proposition="raining")
        assert q.proposition == "raining"
        assert q.parameters == {}

    def test_creation_with_parameters(self):
        """Test creating a YNQuestion with parameters."""
        q = YNQuestion(proposition="raining", parameters={"location": "Stockholm"})
        assert q.proposition == "raining"
        assert q.parameters == {"location": "Stockholm"}

    def test_resolves_with_boolean_true(self):
        """Test that YNQuestion resolves with boolean answer."""
        q = YNQuestion(proposition="raining")
        a = Answer(content=True)
        assert q.resolves_with(a)

    def test_resolves_with_boolean_false(self):
        """Test that YNQuestion resolves with boolean false."""
        q = YNQuestion(proposition="raining")
        a = Answer(content=False)
        assert q.resolves_with(a)

    def test_resolves_with_yes_string(self):
        """Test that YNQuestion resolves with 'yes' string."""
        q = YNQuestion(proposition="raining")
        a = Answer(content="yes")
        assert q.resolves_with(a)

    def test_resolves_with_no_string(self):
        """Test that YNQuestion resolves with 'no' string."""
        q = YNQuestion(proposition="raining")
        a = Answer(content="no")
        assert q.resolves_with(a)

    def test_does_not_resolve_with_invalid_content(self):
        """Test that YNQuestion does not resolve with invalid content."""
        q = YNQuestion(proposition="raining")
        a = Answer(content="maybe")
        assert not q.resolves_with(a)

    def test_str_representation(self):
        """Test string representation."""
        q = YNQuestion(proposition="raining")
        assert str(q) == "?raining"

    def test_str_representation_with_parameters(self):
        """Test string representation with parameters."""
        q = YNQuestion(proposition="raining", parameters={"location": "Stockholm"})
        s = str(q)
        assert s.startswith("?raining [")
        assert "location=Stockholm" in s


class TestAltQuestion:
    """Tests for AltQuestion class."""

    def test_creation(self):
        """Test creating an AltQuestion."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        assert q.alternatives == ["tea", "coffee"]

    def test_creation_empty(self):
        """Test creating an empty AltQuestion."""
        q = AltQuestion()
        assert q.alternatives == []

    def test_resolves_with_first_alternative(self):
        """Test that AltQuestion resolves with first alternative."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        a = Answer(content="tea")
        assert q.resolves_with(a)

    def test_resolves_with_second_alternative(self):
        """Test that AltQuestion resolves with second alternative."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        a = Answer(content="coffee")
        assert q.resolves_with(a)

    def test_resolves_with_partial_match(self):
        """Test that AltQuestion resolves with partial match."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        a = Answer(content="I'll have tea please")
        assert q.resolves_with(a)

    def test_does_not_resolve_with_invalid_alternative(self):
        """Test that AltQuestion does not resolve with invalid alternative."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        a = Answer(content="juice")
        assert not q.resolves_with(a)

    def test_does_not_resolve_with_none_content(self):
        """Test that AltQuestion does not resolve with None content."""
        q = AltQuestion(alternatives=["tea", "coffee"])
        a = Answer(content=None)
        assert not q.resolves_with(a)

    def test_str_representation(self):
        """Test string representation."""
        q = AltQuestion(alternatives=["tea", "coffee", "water"])
        assert str(q) == "?{tea, coffee, water}"
