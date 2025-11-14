"""
Complete NDA workflow integration test.

Tests the full pipeline: NLU → Domain → IBDM → NLG

This verifies:
- Task plan formation using domain model
- Question pushing to QUD
- Plan-aware NLG with domain descriptions
- Complete multi-turn dialogue
"""

import pytest

from ibdm.core import DialogueMove, InformationState, WhQuestion
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import RuleSet, create_integration_rules, create_selection_rules


class TestCompleteNDAWorkflow:
    """Test complete NDA workflow with domain integration."""

    def test_task_plan_formation_creates_domain_plan(self):
        """Test that task request triggers domain-based plan formation."""
        # Setup
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Create command move (as NLU engine would create)
        move = DialogueMove(
            move_type="command", content="I need to draft an NDA", speaker="user"
        )

        # Integrate the move (should trigger form_task_plan rule)
        result_state = engine.integrate(move, state)

        # Verify plan was created from domain
        assert len(result_state.private.plan) == 1, "Plan should be created"

        plan = result_state.private.plan[0]
        assert plan.plan_type == "nda_drafting", "Should be NDA plan"
        assert len(plan.subplans) == 5, "NDA plan should have 5 subplans"

        # Verify plan comes from domain model
        domain = get_nda_domain()
        expected_plan = domain.get_plan("nda_drafting", {})
        assert len(plan.subplans) == len(expected_plan.subplans)

    def test_first_question_pushed_to_qud(self):
        """Test that first question from plan is pushed to QUD."""
        # Setup
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Create command move
        move = DialogueMove(
            move_type="command", content="I need to draft an NDA", speaker="user"
        )

        # Integrate
        result_state = engine.integrate(move, state)

        # Verify QUD has first question
        assert len(result_state.shared.qud) == 1, "QUD should have one question"

        question = result_state.shared.qud[-1]  # Top of QUD
        assert isinstance(question, WhQuestion), "First question should be WhQuestion"
        assert question.predicate == "legal_entities", "First question should ask for parties"

    def test_plan_questions_use_domain_predicates(self):
        """Test that all plan questions use domain predicates."""
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Check that all questions use domain predicates
        for i, subplan in enumerate(plan.subplans):
            question = subplan.content
            if isinstance(question, WhQuestion):
                assert (
                    question.predicate in domain.predicates
                ), f"Question {i} predicate '{question.predicate}' not in domain"

    def test_domain_validates_answer(self):
        """Test that domain model validates answers."""
        domain = get_nda_domain()

        # Valid answer
        question = WhQuestion(variable="parties", predicate="legal_entities")
        from ibdm.core import Answer

        valid_answer = Answer(content="Acme Corp and Beta Inc")
        assert domain.resolves(
            valid_answer, question
        ), "Domain should resolve valid organization answer"

        # Empty answer
        empty_answer = Answer(content="")
        assert not domain.resolves(
            empty_answer, question
        ), "Domain should reject empty answer"

    def test_selection_chooses_qud_question(self):
        """Test that selection phase chooses to ask QUD top question."""
        # Setup with both integration and selection rules
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Create and integrate command move
        move = DialogueMove(
            move_type="command", content="I need to draft an NDA", speaker="user"
        )
        integrated_state = engine.integrate(move, state)

        # Select response (should choose to ask QUD question)
        response_move, final_state = engine.select_action(integrated_state)

        # Verify system chose to ask a question
        assert response_move is not None, "System should select a move"
        assert response_move.move_type == "ask", "System should select ask move"

        # Verify it's the question from QUD
        assert response_move.speaker == "system", "Move should be from system"
        question = response_move.content
        assert isinstance(question, WhQuestion), "Should be asking WhQuestion"
        assert question.predicate == "legal_entities", "Should ask for parties"


class TestDomainIntegrationEndToEnd:
    """End-to-end tests verifying domain integration."""

    def test_complete_workflow_structure(self):
        """Test complete workflow creates correct state structure."""
        # Setup
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Turn 1: User requests NDA
        user_move = DialogueMove(
            move_type="command", content="I need to draft an NDA", speaker="user"
        )

        # Integrate
        state = engine.integrate(user_move, state)

        # Verify state structure
        assert len(state.private.plan) == 1, "Should have one plan"
        assert len(state.shared.qud) == 1, "Should have one question on QUD"
        assert state.shared.qud[-1].predicate == "legal_entities"

        # Select response
        response_move, state = engine.select_action(state)

        # Verify response
        assert response_move.move_type == "ask"
        assert isinstance(response_move.content, WhQuestion)

    def test_domain_plan_matches_documentation(self):
        """Test that domain plan structure matches documentation."""
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Verify plan structure from documentation
        assert plan.plan_type == "nda_drafting"
        assert len(plan.subplans) == 5

        # Verify predicates match domain
        expected_predicates = ["legal_entities", "nda_type", "date", "time_period", "jurisdiction"]

        for i, (subplan, expected_pred) in enumerate(zip(plan.subplans, expected_predicates)):
            question = subplan.content
            if isinstance(question, WhQuestion):
                assert (
                    question.predicate == expected_pred
                ), f"Subplan {i} should have predicate {expected_pred}"


class TestPlanAwareGeneration:
    """Test that generation uses plan context and domain descriptions."""

    def test_generation_with_active_plan(self):
        """Test that generation detects active plan."""
        from ibdm.rules.generation_rules import _get_active_plan

        # Create state with active plan
        state = InformationState(agent_id="system")
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})
        state.private.plan.append(plan)

        # Get active plan
        active_plan = _get_active_plan(state)

        assert active_plan is not None, "Should find active plan"
        assert active_plan.plan_type == "nda_drafting"

    def test_plan_progress_tracking(self):
        """Test plan progress calculation."""
        from ibdm.rules.generation_rules import _get_plan_progress

        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Initially no progress
        completed, total = _get_plan_progress(plan)
        assert completed == 0, "Initially no subplans completed"
        assert total == 5, "Total should be 5 subplans"

        # Mark first subplan complete
        plan.subplans[0].status = "completed"
        completed, total = _get_plan_progress(plan)
        assert completed == 1, "One subplan completed"
        assert total == 5

    def test_domain_for_plan_retrieval(self):
        """Test getting domain model for plan."""
        from ibdm.rules.generation_rules import _get_domain_for_plan

        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Get domain for plan
        retrieved_domain = _get_domain_for_plan(plan)

        assert retrieved_domain is not None, "Should retrieve domain"
        assert retrieved_domain.name == "nda_drafting"
        assert "legal_entities" in retrieved_domain.predicates
