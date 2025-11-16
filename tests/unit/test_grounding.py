"""Unit tests for grounding module."""

from ibdm.core.grounding import (
    ActionLevel,
    EvidenceRequirement,
    GroundingStatus,
    GroundingStrategy,
    get_evidence_requirement,
    requires_confirmation,
    select_grounding_strategy,
)


class TestGroundingStatus:
    """Tests for GroundingStatus enum."""

    def test_enum_values(self):
        """Test GroundingStatus enum values."""
        assert GroundingStatus.UNGROUNDED.value == "ungrounded"
        assert GroundingStatus.PENDING.value == "pending"
        assert GroundingStatus.GROUNDED.value == "grounded"

    def test_all_statuses_defined(self):
        """Test that all grounding statuses are defined."""
        statuses = {s.value for s in GroundingStatus}
        assert "ungrounded" in statuses
        assert "pending" in statuses
        assert "grounded" in statuses


class TestGroundingStrategy:
    """Tests for GroundingStrategy enum."""

    def test_enum_values(self):
        """Test GroundingStrategy enum values."""
        assert GroundingStrategy.OPTIMISTIC.value == "optimistic"
        assert GroundingStrategy.CAUTIOUS.value == "cautious"
        assert GroundingStrategy.PESSIMISTIC.value == "pessimistic"

    def test_all_strategies_defined(self):
        """Test that all grounding strategies are defined."""
        strategies = {s.value for s in GroundingStrategy}
        assert "optimistic" in strategies
        assert "cautious" in strategies
        assert "pessimistic" in strategies


class TestActionLevel:
    """Tests for ActionLevel enum."""

    def test_enum_values(self):
        """Test ActionLevel enum values (Larsson Section 3.6.5)."""
        assert ActionLevel.CONTACT.value == "con"
        assert ActionLevel.PERCEPTION.value == "per"
        assert ActionLevel.SEMANTIC.value == "sem"
        assert ActionLevel.UNDERSTANDING.value == "und"
        assert ActionLevel.ACCEPTANCE.value == "acc"

    def test_all_levels_defined(self):
        """Test that all ICM action levels are defined."""
        levels = {level.value for level in ActionLevel}
        assert "con" in levels
        assert "per" in levels
        assert "sem" in levels
        assert "und" in levels
        assert "acc" in levels


class TestEvidenceRequirement:
    """Tests for EvidenceRequirement class."""

    def test_creation(self):
        """Test creating an EvidenceRequirement."""
        req = EvidenceRequirement(move_type="ask")
        assert req.move_type == "ask"
        assert req.min_confidence == 0.7
        assert req.requires_confirmation is False
        assert req.action_level == ActionLevel.UNDERSTANDING

    def test_custom_values(self):
        """Test creating an EvidenceRequirement with custom values."""
        req = EvidenceRequirement(
            move_type="request",
            min_confidence=0.9,
            requires_confirmation=True,
            action_level=ActionLevel.ACCEPTANCE,
        )
        assert req.move_type == "request"
        assert req.min_confidence == 0.9
        assert req.requires_confirmation is True
        assert req.action_level == ActionLevel.ACCEPTANCE

    def test_str_representation(self):
        """Test string representation of EvidenceRequirement."""
        req = EvidenceRequirement(move_type="answer", min_confidence=0.8)
        s = str(req)
        assert "answer" in s
        assert "0.8" in s


class TestSelectGroundingStrategy:
    """Tests for select_grounding_strategy function."""

    def test_high_confidence_optimistic(self):
        """Test high confidence selects optimistic strategy."""
        strategy = select_grounding_strategy("answer", 0.9)
        assert strategy == GroundingStrategy.OPTIMISTIC

    def test_medium_confidence_cautious(self):
        """Test medium confidence selects cautious strategy."""
        strategy = select_grounding_strategy("answer", 0.6)
        assert strategy == GroundingStrategy.CAUTIOUS

    def test_low_confidence_pessimistic(self):
        """Test low confidence selects pessimistic strategy."""
        strategy = select_grounding_strategy("answer", 0.3)
        assert strategy == GroundingStrategy.PESSIMISTIC

    def test_ask_move_high_confidence(self):
        """Test ask move with high confidence (0.8 threshold)."""
        # Ask requires 0.8 confidence
        strategy = select_grounding_strategy("ask", 0.85)
        assert strategy == GroundingStrategy.OPTIMISTIC

        strategy = select_grounding_strategy("ask", 0.75)
        assert strategy == GroundingStrategy.CAUTIOUS

    def test_greet_move_low_threshold(self):
        """Test greet move with lower threshold (0.6)."""
        # Greet only requires 0.6 confidence
        strategy = select_grounding_strategy("greet", 0.65)
        assert strategy == GroundingStrategy.OPTIMISTIC

    def test_quit_move_high_threshold(self):
        """Test quit move with high threshold (0.9)."""
        # Quit requires 0.9 confidence
        strategy = select_grounding_strategy("quit", 0.95)
        assert strategy == GroundingStrategy.OPTIMISTIC

        strategy = select_grounding_strategy("quit", 0.85)
        assert strategy == GroundingStrategy.CAUTIOUS

    def test_unknown_move_type_defaults(self):
        """Test unknown move type uses default thresholds."""
        strategy = select_grounding_strategy("unknown", 0.8)
        assert strategy == GroundingStrategy.OPTIMISTIC

        strategy = select_grounding_strategy("unknown", 0.4)
        assert strategy == GroundingStrategy.PESSIMISTIC

    def test_custom_evidence_requirements(self):
        """Test with custom evidence requirements."""
        custom_reqs = {
            "custom": EvidenceRequirement(
                move_type="custom", min_confidence=0.95, requires_confirmation=True
            )
        }

        # Below custom threshold
        strategy = select_grounding_strategy("custom", 0.9, custom_reqs)
        assert strategy == GroundingStrategy.CAUTIOUS

        # Above custom threshold
        strategy = select_grounding_strategy("custom", 0.96, custom_reqs)
        assert strategy == GroundingStrategy.OPTIMISTIC


class TestRequiresConfirmation:
    """Tests for requires_confirmation function."""

    def test_quit_always_requires_confirmation(self):
        """Test quit always requires confirmation."""
        assert requires_confirmation("quit", 0.95) is True
        assert requires_confirmation("quit", 0.5) is True

    def test_answer_requires_confirmation(self):
        """Test answer requires confirmation (critical info)."""
        assert requires_confirmation("answer", 0.9) is True
        assert requires_confirmation("answer", 0.5) is True

    def test_greet_no_confirmation_needed(self):
        """Test greet doesn't require confirmation when confidence high."""
        assert requires_confirmation("greet", 0.9) is False
        # But does when confidence low
        assert requires_confirmation("greet", 0.4) is True

    def test_ask_no_confirmation_when_confident(self):
        """Test ask doesn't require confirmation when confidence high."""
        assert requires_confirmation("ask", 0.9) is False
        # But does when confidence low
        assert requires_confirmation("ask", 0.5) is True

    def test_request_requires_confirmation(self):
        """Test request requires confirmation."""
        assert requires_confirmation("request", 0.95) is True
        assert requires_confirmation("request", 0.5) is True

    def test_low_confidence_always_confirms(self):
        """Test low confidence always triggers confirmation."""
        # Even for moves that don't normally require it
        assert requires_confirmation("greet", 0.3) is True
        assert requires_confirmation("icm", 0.3) is True

    def test_custom_evidence_requirements(self):
        """Test with custom evidence requirements."""
        custom_reqs = {
            "custom": EvidenceRequirement(
                move_type="custom",
                min_confidence=0.5,
                requires_confirmation=False,
            )
        }

        # High confidence, no confirmation required
        assert requires_confirmation("custom", 0.8, custom_reqs) is False

        # Low confidence, confirmation required
        assert requires_confirmation("custom", 0.4, custom_reqs) is True


class TestGetEvidenceRequirement:
    """Tests for get_evidence_requirement function."""

    def test_get_ask_requirement(self):
        """Test getting evidence requirement for ask."""
        req = get_evidence_requirement("ask")
        assert req.move_type == "ask"
        assert req.min_confidence == 0.8
        assert req.requires_confirmation is False

    def test_get_answer_requirement(self):
        """Test getting evidence requirement for answer."""
        req = get_evidence_requirement("answer")
        assert req.move_type == "answer"
        assert req.min_confidence == 0.7
        assert req.requires_confirmation is True

    def test_get_quit_requirement(self):
        """Test getting evidence requirement for quit."""
        req = get_evidence_requirement("quit")
        assert req.move_type == "quit"
        assert req.min_confidence == 0.9
        assert req.requires_confirmation is True

    def test_get_greet_requirement(self):
        """Test getting evidence requirement for greet."""
        req = get_evidence_requirement("greet")
        assert req.move_type == "greet"
        assert req.min_confidence == 0.6
        assert req.action_level == ActionLevel.PERCEPTION

    def test_get_unknown_requirement_creates_default(self):
        """Test getting evidence requirement for unknown move type."""
        req = get_evidence_requirement("unknown")
        assert req.move_type == "unknown"
        assert req.min_confidence == 0.7  # Default
        assert req.requires_confirmation is False  # Default

    def test_custom_evidence_requirements(self):
        """Test with custom evidence requirements."""
        custom_reqs = {
            "special": EvidenceRequirement(
                move_type="special",
                min_confidence=0.99,
                requires_confirmation=True,
                action_level=ActionLevel.ACCEPTANCE,
            )
        }

        req = get_evidence_requirement("special", custom_reqs)
        assert req.move_type == "special"
        assert req.min_confidence == 0.99
        assert req.action_level == ActionLevel.ACCEPTANCE


class TestGroundingIntegration:
    """Integration tests for grounding module."""

    def test_complete_grounding_workflow(self):
        """Test complete grounding workflow for a move."""
        # User says "quit" with high confidence
        move_type = "quit"
        confidence = 0.95

        # Select strategy
        strategy = select_grounding_strategy(move_type, confidence)
        assert strategy == GroundingStrategy.OPTIMISTIC

        # Check if confirmation needed
        needs_confirm = requires_confirmation(move_type, confidence)
        assert needs_confirm is True  # Quit always needs confirmation

        # Get evidence requirement
        req = get_evidence_requirement(move_type)
        assert req.min_confidence == 0.9
        assert req.action_level == ActionLevel.ACCEPTANCE

    def test_low_confidence_answer_workflow(self):
        """Test grounding workflow for low-confidence answer."""
        move_type = "answer"
        confidence = 0.4

        # Should use pessimistic strategy
        strategy = select_grounding_strategy(move_type, confidence)
        assert strategy == GroundingStrategy.PESSIMISTIC

        # Should require confirmation
        needs_confirm = requires_confirmation(move_type, confidence)
        assert needs_confirm is True

    def test_greeting_workflow(self):
        """Test grounding workflow for greeting."""
        move_type = "greet"
        confidence = 0.8

        # Should use optimistic strategy (low threshold)
        strategy = select_grounding_strategy(move_type, confidence)
        assert strategy == GroundingStrategy.OPTIMISTIC

        # Should not require confirmation
        needs_confirm = requires_confirmation(move_type, confidence)
        assert needs_confirm is False

        # Should only need perception-level evidence
        req = get_evidence_requirement(move_type)
        assert req.action_level == ActionLevel.PERCEPTION
