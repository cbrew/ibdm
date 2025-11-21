"""Test clean commitment creation (ibdm-209).

Verifies that answers create clean semantic commitments like "nda_type(mutual)"
instead of verbose Q+A pairs like "?{mutual, one-way}: I think mutual...".
"""

import pytest

from ibdm.core.answers import Answer
from ibdm.core.domain import DomainModel
from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.questions import AltQuestion, WhQuestion
from ibdm.domains.nda_domain import create_nda_domain
from ibdm.rules.integration_rules import _extract_semantic_value, _integrate_answer


class TestCreateProposition:
    """Test DomainModel.create_proposition() method."""

    def test_create_proposition_simple(self) -> None:
        """Test basic proposition creation."""
        domain = DomainModel(name="test")

        prop = domain.create_proposition("nda_type", "mutual")
        assert prop == "nda_type(mutual)"

        prop = domain.create_proposition("jurisdiction", "Delaware")
        assert prop == "jurisdiction(Delaware)"

    def test_create_proposition_with_spaces(self) -> None:
        """Test proposition creation with values containing spaces."""
        domain = DomainModel(name="test")

        prop = domain.create_proposition("time_period", "3 years")
        assert prop == "time_period(3 years)"

    def test_create_proposition_strips_quotes(self) -> None:
        """Test that proposition creation strips quotes from values."""
        domain = DomainModel(name="test")

        prop = domain.create_proposition("nda_type", '"mutual"')
        assert prop == "nda_type(mutual)"

        prop = domain.create_proposition("nda_type", "'mutual'")
        assert prop == "nda_type(mutual)"


class TestExtractSemanticValue:
    """Test _extract_semantic_value() helper function."""

    def test_extract_from_alt_question(self) -> None:
        """Test extraction from AltQuestion answer."""
        question = AltQuestion(alternatives=["mutual", "one-way"])
        answer = Answer(content="I think mutual makes sense")

        value = _extract_semantic_value(answer, question)
        assert value == "mutual"

    def test_extract_from_alt_question_case_insensitive(self) -> None:
        """Test case-insensitive extraction."""
        question = AltQuestion(alternatives=["Delaware", "California"])
        answer = Answer(content="Let's go with delaware")

        value = _extract_semantic_value(answer, question)
        assert value == "Delaware"  # Returns original casing from alternatives

    def test_extract_from_alt_question_not_found(self) -> None:
        """Test extraction when no alternative found."""
        question = AltQuestion(alternatives=["mutual", "one-way"])
        answer = Answer(content="I don't know")

        value = _extract_semantic_value(answer, question)
        assert value is None

    def test_extract_from_wh_question(self) -> None:
        """Test extraction from WhQuestion answer."""
        question = WhQuestion(variable="parties", predicate="legal_entities")
        answer = Answer(content="Acme Corp, Beta Inc")

        value = _extract_semantic_value(answer, question)
        assert value == "Acme Corp, Beta Inc"

    def test_extract_yes_from_yn_answer(self) -> None:
        """Test extraction of 'yes' from various affirmative answers."""
        from ibdm.core.questions import YNQuestion

        question = YNQuestion(proposition="confirmed")

        for content in ["yes", "Yes, that's correct", "sure", "ok", "yeah"]:
            answer = Answer(content=content)
            value = _extract_semantic_value(answer, question)
            assert value == "yes", f"Failed for: {content}"

    def test_extract_no_from_yn_answer(self) -> None:
        """Test extraction of 'no' from negative answers."""
        from ibdm.core.questions import YNQuestion

        question = YNQuestion(proposition="confirmed")
        answer = Answer(content="no")

        value = _extract_semantic_value(answer, question)
        assert value == "no"


class TestAltQuestionPredicate:
    """Test AltQuestion with predicate field."""

    def test_alt_question_with_predicate(self) -> None:
        """Test AltQuestion with predicate."""
        question = AltQuestion(
            alternatives=["mutual", "one-way"],
            predicate="nda_type"
        )

        assert question.predicate == "nda_type"
        assert question.alternatives == ["mutual", "one-way"]

    def test_alt_question_without_predicate(self) -> None:
        """Test backward compatibility - AltQuestion without predicate."""
        question = AltQuestion(alternatives=["mutual", "one-way"])

        assert question.predicate == ""  # Empty string default
        assert question.alternatives == ["mutual", "one-way"]

    def test_alt_question_str_with_predicate(self) -> None:
        """Test string representation with predicate."""
        question = AltQuestion(
            alternatives=["mutual", "one-way"],
            predicate="nda_type"
        )

        assert str(question) == "?nda_type{mutual, one-way}"

    def test_alt_question_str_without_predicate(self) -> None:
        """Test string representation without predicate."""
        question = AltQuestion(alternatives=["mutual", "one-way"])

        assert str(question) == "?{mutual, one-way}"

    def test_alt_question_to_dict_with_predicate(self) -> None:
        """Test to_dict() with predicate."""
        question = AltQuestion(
            alternatives=["mutual", "one-way"],
            predicate="nda_type"
        )

        data = question.to_dict()
        assert data["type"] == "alt"
        assert data["alternatives"] == ["mutual", "one-way"]
        assert data["predicate"] == "nda_type"

    def test_alt_question_to_dict_without_predicate(self) -> None:
        """Test to_dict() without predicate."""
        question = AltQuestion(alternatives=["mutual", "one-way"])

        data = question.to_dict()
        assert data["type"] == "alt"
        assert data["alternatives"] == ["mutual", "one-way"]
        assert "predicate" not in data  # Not included if empty

    def test_alt_question_from_dict_with_predicate(self) -> None:
        """Test from_dict() with predicate."""
        from ibdm.core.questions import Question

        data = {
            "type": "alt",
            "alternatives": ["mutual", "one-way"],
            "predicate": "nda_type",
            "required": True
        }

        question = Question.from_dict(data)
        assert isinstance(question, AltQuestion)
        assert question.predicate == "nda_type"
        assert question.alternatives == ["mutual", "one-way"]

    def test_alt_question_from_dict_without_predicate(self) -> None:
        """Test from_dict() without predicate (backward compatibility)."""
        from ibdm.core.questions import Question

        data = {
            "type": "alt",
            "alternatives": ["mutual", "one-way"],
            "required": True
        }

        question = Question.from_dict(data)
        assert isinstance(question, AltQuestion)
        assert question.predicate == ""  # Default to empty string
        assert question.alternatives == ["mutual", "one-way"]


class TestIntegrateAnswerCleanCommitments:
    """Test _integrate_answer creates clean commitments."""

    def test_integrate_answer_alt_question_with_predicate(self) -> None:
        """Test clean commitment creation for AltQuestion with predicate."""
        state = InformationState()
        domain = create_nda_domain()
        state.control.active_domain = domain

        # Push question to QUD
        question = AltQuestion(
            alternatives=["mutual", "one-way"],
            predicate="nda_type"
        )
        state.shared.qud.append(question)

        # Create answer move
        answer = Answer(content="I think mutual makes sense")
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Integrate
        new_state = _integrate_answer(state)

        # Check commitment is clean
        assert "nda_type(mutual)" in new_state.shared.commitments
        # Check old format is NOT present
        commitments_str = " ".join(new_state.shared.commitments)
        assert "?{mutual, one-way}" not in commitments_str
        assert "I think mutual makes sense" not in commitments_str

    def test_integrate_answer_alt_question_without_predicate_fallback(self) -> None:
        """Test fallback to old format when question has no predicate."""
        state = InformationState()
        domain = create_nda_domain()
        state.control.active_domain = domain

        # Push question WITHOUT predicate
        question = AltQuestion(alternatives=["mutual", "one-way"])
        state.shared.qud.append(question)

        # Create answer move
        answer = Answer(content="I think mutual makes sense")
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Integrate
        new_state = _integrate_answer(state)

        # Check falls back to old format
        commitments_str = " ".join(new_state.shared.commitments)
        assert "?{mutual, one-way}" in commitments_str  # Old format present

    def test_integrate_answer_wh_question(self) -> None:
        """Test clean commitment creation for WhQuestion."""
        state = InformationState()
        domain = create_nda_domain()
        state.control.active_domain = domain

        # Push WhQuestion to QUD
        question = WhQuestion(variable="duration", predicate="time_period")
        state.shared.qud.append(question)

        # Create answer move
        answer = Answer(content="3 years")
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Integrate
        new_state = _integrate_answer(state)

        # Check commitment is clean
        assert "time_period(3 years)" in new_state.shared.commitments

    def test_integrate_answer_jurisdiction(self) -> None:
        """Test jurisdiction answer creates clean commitment."""
        state = InformationState()
        domain = create_nda_domain()
        state.control.active_domain = domain

        # Push jurisdiction question to QUD
        question = AltQuestion(
            alternatives=["California", "Delaware", "New York"],
            predicate="jurisdiction"
        )
        state.shared.qud.append(question)

        # Create answer move
        answer = Answer(content="Let's go with Delaware")
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Integrate
        new_state = _integrate_answer(state)

        # Check commitment is clean
        assert "jurisdiction(Delaware)" in new_state.shared.commitments
        # Check old format is NOT present
        commitments_str = " ".join(new_state.shared.commitments)
        assert "Let's go with Delaware" not in commitments_str


class TestNDADomainQuestionsHavePredicates:
    """Test that NDA domain questions include predicates."""

    def test_nda_plan_questions_have_predicates(self) -> None:
        """Test NDA plan builder creates questions with predicates."""
        domain = create_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Check nda_type question (subplan 1)
        nda_type_plan = plan.subplans[1]
        assert nda_type_plan.plan_type == "findout"
        question = nda_type_plan.content
        assert isinstance(question, AltQuestion)
        assert question.predicate == "nda_type"
        assert question.alternatives == ["mutual", "one-way"]

        # Check jurisdiction question (subplan 4)
        jurisdiction_plan = plan.subplans[4]
        assert jurisdiction_plan.plan_type == "findout"
        question = jurisdiction_plan.content
        assert isinstance(question, AltQuestion)
        assert question.predicate == "jurisdiction"
        assert question.alternatives == ["California", "Delaware", "New York"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
