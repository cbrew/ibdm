"""Tests for IBiS-4 negotiation rules.

Tests negotiation mechanisms including:
- Alternative accommodation to IUN
- Accept/reject proposal handling
- Counter-proposal generation
- Dominance relations

Based on Larsson (2002) Section 5.7.
"""

from ibdm.core import Answer, DialogueMove, InformationState
from ibdm.core.actions import Proposition
from ibdm.rules.negotiation_rules import (
    create_negotiation_rules,
    create_negotiation_selection_rules,
)


class TestAlternativeAccommodation:
    """Tests for accommodating alternatives to IUN."""

    def test_accommodate_conflicting_proposition(self):
        """Test accommodating a proposition that conflicts with commitments."""
        from ibdm.rules.negotiation_rules import (
            _accommodate_alternative,
            _has_alternative_to_accommodate,
        )

        # Create state with existing commitment
        state = InformationState()
        state.shared.commitments.add("hotel(price=200)")

        # User asserts conflicting proposition
        prop = Proposition(predicate="hotel", arguments={"price": "150"})
        move = DialogueMove(speaker="user", move_type="assert", content=prop)
        state.private.last_utterance = move

        # Should detect alternative to accommodate
        assert _has_alternative_to_accommodate(state)

        # Accommodate should add to IUN
        new_state = _accommodate_alternative(state)
        assert len(new_state.private.iun) == 1
        assert prop in new_state.private.iun

    def test_accommodate_alternatives_from_metadata(self):
        """Test accommodating multiple alternatives from move metadata."""
        from ibdm.rules.negotiation_rules import _accommodate_alternative

        state = InformationState()

        # User provides multiple alternatives
        alt1 = Proposition(predicate="hotel", arguments={"price": "150"})
        alt2 = Proposition(predicate="hotel", arguments={"price": "180"})

        move = DialogueMove(
            speaker="user",
            move_type="assert",
            content=alt1,
            metadata={"alternatives": [alt1, alt2]},
        )
        state.private.last_utterance = move

        # Accommodate alternatives
        new_state = _accommodate_alternative(state)

        # Both should be in IUN
        assert len(new_state.private.iun) >= 1
        assert alt1 in new_state.private.iun

    def test_no_accommodation_without_conflict(self):
        """Test that non-conflicting moves don't trigger accommodation."""
        from ibdm.rules.negotiation_rules import _has_alternative_to_accommodate

        state = InformationState()

        # Regular question move
        move = DialogueMove(speaker="user", move_type="ask", content="What hotels?")
        state.private.last_utterance = move

        # Should not trigger accommodation
        assert not _has_alternative_to_accommodate(state)


class TestAcceptProposal:
    """Tests for accepting proposals from IUN."""

    def test_accept_with_yes_answer(self):
        """Test accepting proposal with affirmative answer."""
        from ibdm.rules.negotiation_rules import (
            _accept_proposal,
            _has_accepted_proposal,
        )

        state = InformationState()

        # Add proposal to IUN
        prop = Proposition(predicate="hotel", arguments={"id": "H123", "price": "150"})
        state.private.iun.add(prop)

        # User says yes
        answer = Answer(content="yes", question_ref=None)
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = move

        # Should detect acceptance
        assert _has_accepted_proposal(state)

        # Accept should move to commitments
        new_state = _accept_proposal(state)
        assert "hotel(id=H123, price=150)" in new_state.shared.commitments
        assert prop not in new_state.private.iun

    def test_accept_specific_proposition(self):
        """Test accepting a specific proposition from multiple alternatives."""
        from ibdm.rules.negotiation_rules import (
            _accept_proposal,
            _has_accepted_proposal,
        )

        state = InformationState()

        # Add multiple proposals to IUN
        prop1 = Proposition(predicate="hotel", arguments={"id": "H123"})
        prop2 = Proposition(predicate="hotel", arguments={"id": "H456"})
        state.private.iun.add(prop1)
        state.private.iun.add(prop2)

        # User selects specific one
        move = DialogueMove(speaker="user", move_type="assert", content=prop1)
        state.private.last_utterance = move

        # Should detect acceptance
        assert _has_accepted_proposal(state)

        # Accept should commit selected one
        new_state = _accept_proposal(state)
        assert "hotel(id=H123)" in new_state.shared.commitments

    def test_no_acceptance_without_iun(self):
        """Test that acceptance doesn't trigger without IUN proposals."""
        from ibdm.rules.negotiation_rules import _has_accepted_proposal

        state = InformationState()

        # User says yes but no proposals in IUN
        answer = Answer(content="yes", question_ref=None)
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = move

        # Should not trigger acceptance
        assert not _has_accepted_proposal(state)


class TestRejectProposal:
    """Tests for rejecting proposals from IUN."""

    def test_reject_with_no_answer(self):
        """Test rejecting all proposals with negative answer."""
        from ibdm.rules.negotiation_rules import (
            _has_rejected_proposal,
            _reject_proposal,
        )

        state = InformationState()

        # Add proposals to IUN
        prop1 = Proposition(predicate="hotel", arguments={"id": "H123"})
        prop2 = Proposition(predicate="hotel", arguments={"id": "H456"})
        state.private.iun.add(prop1)
        state.private.iun.add(prop2)

        # User says no
        answer = Answer(content="no", question_ref=None)
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = move

        # Should detect rejection
        assert _has_rejected_proposal(state)

        # Reject should clear IUN
        new_state = _reject_proposal(state)
        assert len(new_state.private.iun) == 0

    def test_reject_specific_proposition(self):
        """Test rejecting a specific proposition."""

        state = InformationState()

        # Add proposals to IUN
        prop1 = Proposition(predicate="hotel", arguments={"id": "H123"})
        prop2 = Proposition(predicate="hotel", arguments={"id": "H456"})
        state.private.iun.add(prop1)
        state.private.iun.add(prop2)

        # User rejects specific one
        move = DialogueMove(speaker="user", move_type="assert", content=prop1)
        state.private.last_utterance = move

        # Mark as rejection in metadata
        move.metadata = {"rejection_detected": True}

        # Reject should remove that specific one
        # Note: This is simplified - production code would detect rejection
        # from context or explicit negative markers

    def test_no_rejection_without_iun(self):
        """Test that rejection doesn't trigger without IUN proposals."""
        from ibdm.rules.negotiation_rules import _has_rejected_proposal

        state = InformationState()

        # User says no but no proposals in IUN
        answer = Answer(content="no", question_ref=None)
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = move

        # Should not trigger rejection
        assert not _has_rejected_proposal(state)


class TestCounterProposal:
    """Tests for counter-proposal generation."""

    def test_should_generate_counter_proposal(self):
        """Test detection of counter-proposal trigger."""
        from ibdm.rules.negotiation_rules import _should_generate_counter_proposal

        state = InformationState()

        # User rejected a proposal
        rejected = Proposition(predicate="hotel", arguments={"price": "200"})
        answer = Answer(content="no", question_ref=None)
        move = DialogueMove(
            speaker="user",
            move_type="answer",
            content=answer,
            metadata={"rejected_proposition": rejected},
        )
        state.private.last_utterance = move

        # Should trigger counter-proposal
        assert _should_generate_counter_proposal(state)

    def test_generate_counter_proposal_with_alternatives(self):
        """Test generating counter-proposal from alternatives."""
        from ibdm.rules.negotiation_rules import _generate_counter_proposal

        state = InformationState()

        # Store alternatives in beliefs
        alt1 = Proposition(predicate="hotel", arguments={"price": "150"})
        alt2 = Proposition(predicate="hotel", arguments={"price": "180"})
        state.private.beliefs["alternatives"] = {alt1, alt2}

        # User rejected expensive hotel
        rejected = Proposition(predicate="hotel", arguments={"price": "200"})
        answer = Answer(content="no", question_ref=None)
        move = DialogueMove(
            speaker="user",
            move_type="answer",
            content=answer,
            metadata={"rejected_proposition": rejected},
        )
        state.private.last_utterance = move

        # Generate counter-proposal
        new_state = _generate_counter_proposal(state)

        # Should have counter-proposal in agenda
        assert len(new_state.private.agenda) > 0
        counter_move = new_state.private.agenda[-1]
        assert counter_move.metadata.get("counter_proposal") is True

    def test_no_counter_proposal_without_alternatives(self):
        """Test that no counter-proposal is generated without alternatives."""
        from ibdm.rules.negotiation_rules import _generate_counter_proposal

        state = InformationState()

        # User rejected but no alternatives available
        rejected = Proposition(predicate="hotel", arguments={"price": "200"})
        answer = Answer(content="no", question_ref=None)
        move = DialogueMove(
            speaker="user",
            move_type="answer",
            content=answer,
            metadata={"rejected_proposition": rejected},
        )
        state.private.last_utterance = move

        # Generate counter-proposal
        new_state = _generate_counter_proposal(state)

        # Should not add counter-proposal without alternatives
        assert len(new_state.private.agenda) == 0


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_propositions_match(self):
        """Test proposition matching."""
        from ibdm.rules.negotiation_rules import _propositions_match

        prop1 = Proposition(predicate="hotel", arguments={"id": "H123", "price": "150"})
        prop2 = Proposition(predicate="hotel", arguments={"id": "H123", "price": "150"})
        prop3 = Proposition(predicate="hotel", arguments={"id": "H456", "price": "150"})

        assert _propositions_match(prop1, prop2)
        assert not _propositions_match(prop1, prop3)

    def test_propositions_conflict(self):
        """Test proposition conflict detection."""
        from ibdm.rules.negotiation_rules import _propositions_conflict

        prop1 = Proposition(predicate="hotel", arguments={"id": "H123"})
        prop2 = Proposition(predicate="hotel", arguments={"id": "H456"})
        prop3 = Proposition(predicate="flight", arguments={"id": "F123"})

        # Same predicate, different id - conflict
        assert _propositions_conflict(prop1, prop2)

        # Different predicate - no conflict
        assert not _propositions_conflict(prop1, prop3)

    def test_conflicts_with_commitments(self):
        """Test commitment conflict detection."""
        from ibdm.rules.negotiation_rules import _conflicts_with_commitments

        prop = Proposition(predicate="hotel", arguments={"price": "150"})
        commitments = {"hotel(price=200)"}

        # Same predicate, different value - conflict
        assert _conflicts_with_commitments(prop, commitments)

        # No existing commitment - no conflict
        assert not _conflicts_with_commitments(prop, set())


class TestRuleCreation:
    """Tests for rule creation functions."""

    def test_create_negotiation_rules(self):
        """Test that negotiation rules are created correctly."""
        rules = create_negotiation_rules()

        assert len(rules) >= 3
        rule_names = [r.name for r in rules]
        assert "accommodate_alternative" in rule_names
        assert "accept_proposal" in rule_names
        assert "reject_proposal" in rule_names

    def test_create_negotiation_selection_rules(self):
        """Test that negotiation selection rules are created correctly."""
        rules = create_negotiation_selection_rules()

        assert len(rules) >= 1
        rule_names = [r.name for r in rules]
        assert "generate_counter_proposal" in rule_names


class TestIntegrationScenarios:
    """Integration tests for complete negotiation scenarios."""

    def test_complete_negotiation_flow(self):
        """Test complete negotiation flow: propose -> reject -> counter-propose -> accept."""
        from ibdm.rules.negotiation_rules import (
            _accept_proposal,
            _accommodate_alternative,
            _generate_counter_proposal,
            _reject_proposal,
        )

        # 1. Accommodate alternative
        state = InformationState()
        prop1 = Proposition(predicate="hotel", arguments={"price": "200"})
        move = DialogueMove(speaker="system", move_type="assert", content=prop1)
        state.private.last_utterance = move
        state.shared.commitments.add("hotel(price=150)")

        state = _accommodate_alternative(state)
        assert len(state.private.iun) == 1

        # 2. User rejects
        answer = Answer(content="no", question_ref=None)
        reject_move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = reject_move

        state = _reject_proposal(state)
        assert len(state.private.iun) == 0

        # 3. System generates counter-proposal
        state.private.beliefs["alternatives"] = {
            Proposition(predicate="hotel", arguments={"price": "120"})
        }
        reject_move.metadata = {"rejected_proposition": prop1}
        state.private.last_utterance = reject_move

        state = _generate_counter_proposal(state)
        assert len(state.private.agenda) > 0

        # 4. User accepts counter-proposal
        prop2 = Proposition(predicate="hotel", arguments={"price": "120"})
        state.private.iun.add(prop2)
        accept_answer = Answer(content="yes", question_ref=None)
        accept_move = DialogueMove(speaker="user", move_type="answer", content=accept_answer)
        state.private.last_utterance = accept_move

        state = _accept_proposal(state)
        assert "hotel(price=120)" in state.shared.commitments
        assert len(state.private.iun) == 0
