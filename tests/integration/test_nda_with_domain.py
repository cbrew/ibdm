"""Integration test: NDA workflow with domain model.

Tests that the complete NDA workflow uses the domain model correctly:
- Domain provides semantic grounding for predicates
- Integration rules use domain.get_plan() to create plans
- Questions use predicates defined in domain
- Domain validates answers (type checking)
"""

from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.questions import WhQuestion
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.rules.integration_rules import create_integration_rules


class TestNDAWorkflowWithDomain:
    """Integration tests for NDA workflow using domain model."""

    def test_nda_domain_is_available(self):
        """Test that NDA domain can be retrieved."""
        domain = get_nda_domain()

        assert domain is not None
        assert domain.name == "nda_drafting"
        assert len(domain.predicates) == 5
        assert len(domain.sorts) == 2

    def test_integration_rules_include_form_task_plan(self):
        """Test that integration rules include form_task_plan rule."""
        rules = create_integration_rules()

        rule_names = [rule.name for rule in rules]
        assert "form_task_plan" in rule_names

        # Should be highest priority
        form_task_plan_rule = next(r for r in rules if r.name == "form_task_plan")
        assert form_task_plan_rule.priority == 13

    def test_form_task_plan_uses_domain(self):
        """Test that form_task_plan effect uses domain.get_plan()."""
        from ibdm.rules.integration_rules import _form_task_plan

        # Create state with command move
        state = InformationState(agent_id="system")
        command_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user",
        )
        state.private.beliefs["_temp_move"] = command_move

        # Execute effect
        new_state = _form_task_plan(state)

        # Should have created plan
        assert len(new_state.private.plan) == 1
        plan = new_state.private.plan[0]

        # Plan should be from domain
        assert plan.plan_type == "nda_drafting"
        assert len(plan.subplans) == 5

    def test_form_task_plan_pushes_question_to_qud(self):
        """Test that form_task_plan pushes first question to QUD."""
        from ibdm.rules.integration_rules import _form_task_plan

        state = InformationState(agent_id="system")
        command_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user",
        )
        state.private.beliefs["_temp_move"] = command_move

        # Execute effect
        new_state = _form_task_plan(state)

        # Should have pushed question to QUD
        assert len(new_state.shared.qud) == 1

        question = new_state.shared.qud[-1]  # Get last element (top of stack)
        assert isinstance(question, WhQuestion)
        assert question.predicate == "legal_entities"

    def test_plan_questions_use_domain_predicates(self):
        """Test that plan questions use predicates defined in domain."""
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Collect predicates from plan
        plan_predicates = set()
        for subplan in plan.subplans:
            if isinstance(subplan.content, WhQuestion):
                plan_predicates.add(subplan.content.predicate)

        # All should be defined in domain
        for pred in plan_predicates:
            assert pred in domain.predicates, f"Undefined predicate: {pred}"

    def test_domain_validates_answer(self):
        """Test that domain can validate answers via resolves()."""
        from ibdm.core.answers import Answer

        domain = get_nda_domain()

        question = WhQuestion(variable="x", predicate="legal_entities")
        valid_answer = Answer(content="Acme Corp, Beta Industries")

        # Should resolve
        assert domain.resolves(valid_answer, question) is True

    def test_domain_rejects_empty_answer(self):
        """Test that domain rejects empty answers."""
        from ibdm.core.answers import Answer

        domain = get_nda_domain()

        question = WhQuestion(variable="x", predicate="legal_entities")
        empty_answer = Answer(content=None)

        # Should not resolve
        assert domain.resolves(empty_answer, question) is False

    def test_complete_nda_workflow_simulation(self):
        """Simulate complete NDA workflow with domain model.

        This test simulates:
        1. User requests NDA drafting
        2. System creates plan from domain
        3. System asks first question (using domain predicate)
        4. Verification that all components use domain correctly
        """
        from ibdm.rules.integration_rules import _form_task_plan, _is_task_request_move

        # Initial state
        state = InformationState(agent_id="system")

        # User command: "I need to draft an NDA"
        command_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user",
            metadata={"intent": "draft_document", "task_type": "NDA"},
        )
        state.private.beliefs["_temp_move"] = command_move

        # Check precondition
        assert _is_task_request_move(state) is True

        # Execute task plan formation
        state = _form_task_plan(state)

        # Verify domain was used
        domain = get_nda_domain()

        # 1. Plan should be created from domain
        assert len(state.private.plan) == 1
        plan = state.private.plan[0]
        assert plan.plan_type == "nda_drafting"

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

    def test_domain_plan_matches_documentation(self):
        """Test that domain plan matches specification.

        Verifies that the NDA domain plan has:
        - 5 subplans (per specification)
        - Correct predicates for each step
        - All predicates defined in domain
        """
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Should have exactly 5 subplans
        assert len(plan.subplans) == 5

        # Verify each subplan
        expected_predicates = [
            "legal_entities",  # Step 1: parties
            None,  # Step 2: AltQuestion (NDA type)
            "date",  # Step 3: effective date
            "time_period",  # Step 4: duration
            None,  # Step 5: AltQuestion (jurisdiction)
        ]

        for i, (subplan, expected_pred) in enumerate(zip(plan.subplans, expected_predicates)):
            if expected_pred:
                assert isinstance(subplan.content, WhQuestion)
                assert subplan.content.predicate == expected_pred
                assert expected_pred in domain.predicates


class TestDomainModelExtensibility:
    """Tests for domain model extensibility."""

    def test_can_add_new_predicate_to_domain(self):
        """Test that new predicates can be added to domain."""
        from ibdm.core.domain import DomainModel

        domain = DomainModel(name="test")
        domain.add_predicate("new_predicate", arity=1, arg_types=["test_type"], description="Test")

        assert "new_predicate" in domain.predicates

    def test_can_register_new_plan_builder(self):
        """Test that new plan builders can be registered."""
        from ibdm.core.domain import DomainModel
        from ibdm.core.plans import Plan

        domain = DomainModel(name="test")

        def new_plan_builder(context):
            return Plan(plan_type="new_task", content="test", status="active")

        domain.register_plan_builder("new_task", new_plan_builder)

        plan = domain.get_plan("new_task", {})
        assert plan.plan_type == "new_task"

    def test_domain_singleton_can_be_reused(self):
        """Test that domain singleton is reusable across calls."""
        domain1 = get_nda_domain()
        plan1 = domain1.get_plan("nda_drafting", {})

        domain2 = get_nda_domain()
        plan2 = domain2.get_plan("nda_drafting", {})

        # Should be same domain instance
        assert domain1 is domain2

        # Plans should be equivalent (but not same object)
        assert plan1.plan_type == plan2.plan_type
        assert len(plan1.subplans) == len(plan2.subplans)


class TestDomainSemanticGrounding:
    """Tests for semantic grounding via domain model."""

    def test_predicates_have_semantic_meaning(self):
        """Test that predicates have descriptions (semantic meaning)."""
        domain = get_nda_domain()

        for pred_name, pred_spec in domain.predicates.items():
            assert pred_spec.description, f"{pred_name} missing description"
            assert len(pred_spec.description) > 10, f"{pred_name} has too short description"

    def test_sorts_define_valid_values(self):
        """Test that sorts define valid value sets."""
        domain = get_nda_domain()

        for sort_name, individuals in domain.sorts.items():
            assert len(individuals) > 0, f"{sort_name} has no individuals"
            assert all(isinstance(ind, str) for ind in individuals), (
                f"{sort_name} has non-string individuals"
            )

    def test_predicates_reference_sorts(self):
        """Test that predicate arg_types reference defined sorts."""
        domain = get_nda_domain()

        # Some predicates should reference sorts
        nda_type_pred = domain.predicates["nda_type"]
        assert "nda_kind" in nda_type_pred.arg_types

        # nda_kind should be a defined sort
        assert "nda_kind" in domain.sorts

    def test_domain_provides_type_constraints(self):
        """Test that domain provides type constraints via sorts."""
        domain = get_nda_domain()

        # nda_kind sort should constrain values
        nda_kinds = domain.sorts["nda_kind"]
        assert "mutual" in nda_kinds
        assert "one-way" in nda_kinds

        # This provides type constraint for NDA type answers
