"""Integration test: Travel booking workflow with domain model.

Tests that the complete travel booking workflow uses the domain model correctly:
- Domain provides semantic grounding for travel predicates
- Integration rules use domain.get_plan() to create travel plans
- Questions use predicates defined in travel domain
- Domain validates answers (type checking)

Based on Larsson (2002) travel agency example.
"""

from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.domains.travel_domain import get_travel_domain
from ibdm.rules.integration_rules import create_integration_rules


class TestTravelWorkflowWithDomain:
    """Integration tests for travel booking workflow using domain model."""

    def test_travel_domain_is_available(self):
        """Test that travel domain can be retrieved."""
        domain = get_travel_domain()

        assert domain is not None
        assert domain.name == "travel_booking"
        assert len(domain.predicates) == 8
        assert len(domain.sorts) == 5

    def test_integration_rules_include_form_task_plan(self):
        """Test that integration rules include form_task_plan rule."""
        rules = create_integration_rules()

        rule_names = [rule.name for rule in rules]
        assert "form_task_plan" in rule_names

        # Should be highest priority
        form_task_plan_rule = next(r for r in rules if r.name == "form_task_plan")
        assert form_task_plan_rule.priority == 13

    def test_form_task_plan_creates_travel_plan(self):
        """Test that form_task_plan effect creates travel booking plan."""
        from ibdm.rules.integration_rules import _form_task_plan

        # Create state with travel booking command
        state = InformationState(agent_id="system")
        command_move = DialogueMove(
            move_type="command",
            content="I need to book a flight",
            speaker="user",
        )
        state.private.beliefs["_temp_move"] = command_move

        # Execute effect
        new_state = _form_task_plan(state)

        # Should have created plan
        assert len(new_state.private.plan) == 1
        plan = new_state.private.plan[0]

        # Plan should be from travel domain
        assert plan.plan_type == "travel_booking"
        assert len(plan.subplans) == 8  # Default includes return trip

    def test_form_task_plan_pushes_first_question_to_qud(self):
        """Test that form_task_plan pushes first question to QUD."""
        from ibdm.rules.integration_rules import _form_task_plan

        state = InformationState(agent_id="system")
        command_move = DialogueMove(
            move_type="command",
            content="I want to book a train ticket",
            speaker="user",
        )
        state.private.beliefs["_temp_move"] = command_move

        # Execute effect
        new_state = _form_task_plan(state)

        # Should have pushed question to QUD
        assert len(new_state.shared.qud) == 1

        question = new_state.shared.qud[-1]  # Get last element (top of stack)
        assert isinstance(question, WhQuestion)
        assert question.predicate == "transport_mode"

    def test_plan_questions_use_domain_predicates(self):
        """Test that plan questions use predicates defined in domain."""
        domain = get_travel_domain()
        plan = domain.get_plan("travel_booking", {})

        # Collect predicates from plan
        plan_predicates = set()
        for subplan in plan.subplans:
            if isinstance(subplan.content, WhQuestion):
                plan_predicates.add(subplan.content.predicate)

        # All should be defined in domain
        for pred in plan_predicates:
            assert pred in domain.predicates, f"Undefined predicate: {pred}"

    def test_domain_validates_transport_mode_answer(self):
        """Test that domain can validate transport mode answers."""
        from ibdm.core.answers import Answer

        domain = get_travel_domain()

        question = WhQuestion(variable="mode", predicate="transport_mode")
        valid_answer = Answer(content="plane")

        # Should resolve
        assert domain.resolves(valid_answer, question) is True

    def test_domain_validates_city_answer(self):
        """Test that domain validates city answers."""
        from ibdm.core.answers import Answer

        domain = get_travel_domain()

        question = WhQuestion(variable="dest", predicate="dest_city")
        valid_answer = Answer(content="paris")

        # Should resolve
        assert domain.resolves(valid_answer, question) is True

    def test_domain_rejects_empty_answer(self):
        """Test that domain rejects empty answers."""
        from ibdm.core.answers import Answer

        domain = get_travel_domain()

        question = WhQuestion(variable="mode", predicate="transport_mode")
        empty_answer = Answer(content=None)

        # Should not resolve
        assert domain.resolves(empty_answer, question) is False

    def test_complete_travel_workflow_simulation(self):
        """Simulate complete travel booking workflow with domain model.

        This test simulates:
        1. User requests travel booking
        2. System creates plan from domain
        3. System asks first question (using domain predicate)
        4. Verification that all components use domain correctly
        """
        from ibdm.rules.integration_rules import _form_task_plan, _is_task_request_move

        # Initial state
        state = InformationState(agent_id="system")

        # User command: "I need to book a trip"
        command_move = DialogueMove(
            move_type="command",
            content="I need to book a trip",
            speaker="user",
            metadata={"intent": "book_travel", "task_type": "BOOK_TRAVEL"},
        )
        state.private.beliefs["_temp_move"] = command_move

        # Check precondition
        assert _is_task_request_move(state) is True

        # Execute task plan formation
        state = _form_task_plan(state)

        # Verify domain was used
        domain = get_travel_domain()

        # 1. Plan should be created from domain
        assert len(state.private.plan) == 1
        plan = state.private.plan[0]
        assert plan.plan_type == "travel_booking"

        # 2. First question should be on QUD
        assert len(state.shared.qud) == 1
        question = state.shared.qud[-1]  # Get last element (top of stack)

        # 3. Question should use domain predicate
        assert question.predicate in domain.predicates

        # 4. Predicate should have description (for NLG)
        pred_spec = domain.predicates[question.predicate]
        assert pred_spec.description != ""

        # 5. Next speaker should be system
        assert state.control.next_speaker == "system"

    def test_domain_plan_has_correct_structure(self):
        """Test that domain plan has correct structure per Larsson (2002).

        Verifies that the travel booking plan has:
        - Correct number of subplans (8 with return trip by default)
        - Correct predicates for each step
        - All predicates defined in domain
        """
        domain = get_travel_domain()
        plan = domain.get_plan("travel_booking", {})

        # Should have 8 subplans (with return trip)
        assert len(plan.subplans) == 8

        # Verify sequence matches Larsson's travel agency example
        expected_sequence = [
            ("transport_mode", WhQuestion),
            ("depart_city", WhQuestion),
            ("dest_city", WhQuestion),
            ("depart_day", WhQuestion),
            ("travel_class", WhQuestion),
            ("return_trip", YNQuestion),  # Gate for return trip
            ("return_day", WhQuestion),
            ("price_quote", WhQuestion),  # Final perform action
        ]

        for i, (expected_pred, expected_type) in enumerate(expected_sequence):
            subplan = plan.subplans[i]
            assert isinstance(subplan.content, expected_type)

            if isinstance(subplan.content, WhQuestion):
                assert subplan.content.predicate == expected_pred
                assert expected_pred in domain.predicates
            elif isinstance(subplan.content, YNQuestion):
                assert subplan.content.proposition == expected_pred

    def test_domain_plan_without_return(self):
        """Test that domain plan supports one-way trips."""
        domain = get_travel_domain()
        plan = domain.get_plan("travel_booking", {"include_return": False})

        # Should have 6 subplans (no return questions)
        assert len(plan.subplans) == 6

        # Collect predicates
        predicates = []
        for subplan in plan.subplans:
            if isinstance(subplan.content, WhQuestion):
                predicates.append(subplan.content.predicate)

        # Should not include return_day
        assert "return_day" not in predicates

    def test_travel_keywords_trigger_task_request(self):
        """Test that travel-related keywords trigger task request detection."""
        from ibdm.rules.integration_rules import _is_task_request_move

        state = InformationState(agent_id="system")

        # Test various travel keywords
        keywords = ["book a flight", "need to travel", "book a train", "plan a trip"]

        for keyword in keywords:
            move = DialogueMove(
                move_type="command",
                content=f"I {keyword}",
                speaker="user",
            )
            state.private.beliefs["_temp_move"] = move
            assert _is_task_request_move(state) is True, f"Failed for: {keyword}"

    def test_get_active_domain_returns_travel_domain(self):
        """Test that _get_active_domain returns travel domain for travel plans."""
        from ibdm.rules.integration_rules import _form_task_plan, _get_active_domain

        # Create travel booking state
        state = InformationState(agent_id="system")
        command_move = DialogueMove(
            move_type="command",
            content="I need to book a flight",
            speaker="user",
        )
        state.private.beliefs["_temp_move"] = command_move

        # Form plan
        new_state = _form_task_plan(state)

        # Get active domain
        domain = _get_active_domain(new_state)

        # Should be travel domain
        assert domain.name == "travel_booking"


class TestTravelDomainSemanticGrounding:
    """Tests for semantic grounding via travel domain model."""

    def test_predicates_have_semantic_meaning(self):
        """Test that predicates have descriptions (semantic meaning)."""
        domain = get_travel_domain()

        for pred_name, pred_spec in domain.predicates.items():
            assert pred_spec.description, f"{pred_name} missing description"
            assert len(pred_spec.description) > 10, f"{pred_name} has too short description"

    def test_sorts_define_valid_values(self):
        """Test that sorts define valid value sets."""
        domain = get_travel_domain()

        for sort_name, individuals in domain.sorts.items():
            assert len(individuals) > 0, f"{sort_name} has no individuals"
            assert all(isinstance(ind, str) for ind in individuals), (
                f"{sort_name} has non-string individuals"
            )

    def test_predicates_reference_sorts(self):
        """Test that predicate arg_types reference defined sorts."""
        domain = get_travel_domain()

        # Transport mode should reference transport_means sort
        transport_pred = domain.predicates["transport_mode"]
        assert "transport_means" in transport_pred.arg_types

        # transport_means should be a defined sort
        assert "transport_means" in domain.sorts

    def test_domain_provides_type_constraints(self):
        """Test that domain provides type constraints via sorts."""
        domain = get_travel_domain()

        # transport_means sort should constrain values
        transport_modes = domain.sorts["transport_means"]
        assert "plane" in transport_modes
        assert "train" in transport_modes

        # city sort should constrain values
        cities = domain.sorts["city"]
        assert "paris" in cities
        assert "london" in cities
        assert "berlin" in cities
