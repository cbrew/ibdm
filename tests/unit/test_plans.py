"""Unit tests for Plan class."""


from ibdm.core import Plan, WhQuestion


class TestPlan:
    """Tests for Plan class."""

    def test_creation(self):
        """Test creating a Plan."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="findout", content=q)
        assert plan.plan_type == "findout"
        assert plan.content == q
        assert plan.status == "active"
        assert plan.subplans == []

    def test_creation_with_subplans(self):
        """Test creating a Plan with subplans."""
        q1 = WhQuestion(variable="x", predicate="weather(x)")
        q2 = WhQuestion(variable="y", predicate="temperature(y)")
        subplan = Plan(plan_type="findout", content=q2)
        plan = Plan(plan_type="findout", content=q1, subplans=[subplan])
        assert plan.subplans == [subplan]
        assert len(plan.subplans) == 1

    def test_findout_plan(self):
        """Test creating a findout plan."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="findout", content=q)
        assert plan.plan_type == "findout"
        assert plan.content == q

    def test_raise_plan(self):
        """Test creating a raise plan."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="raise", content=q)
        assert plan.plan_type == "raise"
        assert plan.content == q

    def test_respond_plan(self):
        """Test creating a respond plan."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="respond", content=q)
        assert plan.plan_type == "respond"
        assert plan.content == q

    def test_perform_plan(self):
        """Test creating a perform plan."""
        plan = Plan(plan_type="perform", content="open_window")
        assert plan.plan_type == "perform"
        assert plan.content == "open_window"

    def test_is_active(self):
        """Test is_active method."""
        plan = Plan(plan_type="findout", content="test")
        assert plan.is_active()

    def test_complete(self):
        """Test complete method."""
        plan = Plan(plan_type="findout", content="test")
        plan.complete()
        assert plan.status == "completed"
        assert not plan.is_active()

    def test_abandon(self):
        """Test abandon method."""
        plan = Plan(plan_type="findout", content="test")
        plan.abandon()
        assert plan.status == "abandoned"
        assert not plan.is_active()

    def test_str_representation(self):
        """Test string representation."""
        q = WhQuestion(variable="x", predicate="weather(x)")
        plan = Plan(plan_type="findout", content=q)
        s = str(plan)
        assert "Plan" in s
        assert "findout" in s
        assert "active" in s

    def test_str_representation_with_subplans(self):
        """Test string representation with subplans."""
        q1 = WhQuestion(variable="x", predicate="weather(x)")
        q2 = WhQuestion(variable="y", predicate="temperature(y)")
        subplan = Plan(plan_type="findout", content=q2)
        plan = Plan(plan_type="findout", content=q1, subplans=[subplan])
        s = str(plan)
        assert "1 subplans" in s or "1 subplan" in s
