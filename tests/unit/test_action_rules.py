"""Tests for IBiS-4 action execution rules.

Tests action execution mechanisms including:
- Action execution with device interface
- Action confirmation requests
- Result handling (success/failure)
- Action rollback on failure

Based on Larsson (2002) Section 5.6.
"""

from ibdm.core import Answer, InformationState
from ibdm.core.actions import Action, ActionType
from ibdm.core.moves import DialogueMove
from ibdm.interfaces.device import ActionResult, ActionStatus
from ibdm.rules.action_rules import (
    create_action_integration_rules,
    create_action_selection_rules,
)
from tests.mocks.mock_device import MockDevice


class TestActionExecution:
    """Tests for action execution integration rule."""

    def test_has_action_to_execute_when_confirmed(self):
        """Test detection of ready-to-execute action."""
        from ibdm.rules.action_rules import _has_action_to_execute

        state = InformationState()

        # Add non-critical action (doesn't need confirmation)
        action = Action(
            action_type=ActionType.GET,
            name="get_status",
            parameters={"resource": "booking"},
        )
        state.private.actions.append(action)

        # Should be ready to execute (no confirmation needed)
        assert _has_action_to_execute(state)

    def test_has_action_waits_for_confirmation(self):
        """Test that critical actions wait for confirmation."""
        from ibdm.rules.action_rules import _has_action_to_execute

        state = InformationState()

        # Add critical action (needs confirmation)
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        # Should NOT be ready (waiting for confirmation)
        assert not _has_action_to_execute(state)

    def test_has_action_ready_after_confirmation(self):
        """Test that action is ready after user confirms."""
        from ibdm.rules.action_rules import _has_action_to_execute

        state = InformationState()

        # Add critical action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        # User confirms
        answer = Answer(content="yes", question_ref=None)
        confirm_move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = confirm_move

        # Should be ready now
        assert _has_action_to_execute(state)

    def test_execute_action_success(self):
        """Test successful action execution."""
        from ibdm.rules.action_rules import _execute_action

        state = InformationState()

        # Setup device
        device = MockDevice()
        device.configure(should_fail=False)
        state.private.beliefs["device_interface"] = device

        # Add action
        action = Action(
            action_type=ActionType.GET,
            name="get_status",
            parameters={},
        )
        state.private.actions.append(action)

        # Execute
        new_state = _execute_action(state)

        # Should have result in beliefs
        assert "action_result" in new_state.private.beliefs
        result = new_state.private.beliefs["action_result"]
        assert result.is_successful()
        assert result.action == action

    def test_execute_action_failure(self):
        """Test failed action execution."""
        from ibdm.rules.action_rules import _execute_action

        state = InformationState()

        # Setup device to fail
        device = MockDevice()
        device.configure(should_fail=True, failure_message="Network error")
        state.private.beliefs["device_interface"] = device

        # Add action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        # Execute
        new_state = _execute_action(state)

        # Should have failure result
        assert "action_result" in new_state.private.beliefs
        result = new_state.private.beliefs["action_result"]
        assert result.is_failed()
        assert "Network error" in result.error_message

    def test_execute_action_no_device(self):
        """Test action execution without device interface."""
        from ibdm.rules.action_rules import _execute_action

        state = InformationState()

        # No device interface
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={},
        )
        state.private.actions.append(action)

        # Execute
        new_state = _execute_action(state)

        # Should have failure result
        assert "action_result" in new_state.private.beliefs
        result = new_state.private.beliefs["action_result"]
        assert result.is_failed()
        assert "No device interface" in result.error_message


class TestActionResultProcessing:
    """Tests for action result processing."""

    def test_has_action_result_to_process(self):
        """Test detection of action results."""
        from ibdm.rules.action_rules import _has_action_result_to_process

        state = InformationState()

        # No result
        assert not _has_action_result_to_process(state)

        # With result
        action = Action(action_type=ActionType.GET, name="test", parameters={})
        result = ActionResult(status=ActionStatus.SUCCESS, action=action)
        state.private.beliefs["action_result"] = result

        assert _has_action_result_to_process(state)

    def test_process_successful_result(self):
        """Test processing successful action result."""
        from ibdm.rules.action_rules import _process_action_result

        state = InformationState()

        # Add executed action and result
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        result = ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            postconditions=["booked(hotel_id=H123)"],
        )
        state.private.beliefs["action_result"] = result

        # Process
        new_state = _process_action_result(state)

        # Postconditions should be added to commitments
        assert "booked(hotel_id=H123)" in new_state.shared.commitments

        # Action should be removed from queue
        assert len(new_state.private.actions) == 0

        # Should have success feedback
        assert "action_feedback" in new_state.private.beliefs
        feedback = new_state.private.beliefs["action_feedback"]
        assert feedback["status"] == "success"

        # Result should be cleared
        assert "action_result" not in new_state.private.beliefs

    def test_process_failed_result(self):
        """Test processing failed action result."""
        from ibdm.rules.action_rules import _process_action_result

        state = InformationState()

        # Add executed action and result
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        result = ActionResult(
            status=ActionStatus.FAILURE,
            action=action,
            error_message="No availability",
        )
        state.private.beliefs["action_result"] = result

        # Process
        new_state = _process_action_result(state)

        # No postconditions should be added
        assert len(new_state.shared.commitments) == 0

        # Action should be removed from queue
        assert len(new_state.private.actions) == 0

        # Should have failure feedback
        assert "action_feedback" in new_state.private.beliefs
        feedback = new_state.private.beliefs["action_feedback"]
        assert feedback["status"] == "failure"
        assert "No availability" in feedback["error"]


class TestActionConfirmation:
    """Tests for action confirmation requests."""

    def test_should_confirm_critical_action(self):
        """Test confirmation request for critical actions."""
        from ibdm.rules.action_rules import _should_confirm_action

        state = InformationState()

        # Add critical action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        # Should request confirmation
        assert _should_confirm_action(state)

    def test_no_confirmation_for_safe_action(self):
        """Test no confirmation for safe actions."""
        from ibdm.rules.action_rules import _should_confirm_action

        state = InformationState()

        # Add safe action
        action = Action(
            action_type=ActionType.GET,
            name="get_hotels",
            parameters={},
        )
        state.private.actions.append(action)

        # Should NOT request confirmation
        assert not _should_confirm_action(state)

    def test_request_action_confirmation(self):
        """Test generation of confirmation request."""
        from ibdm.rules.action_rules import _request_action_confirmation

        state = InformationState()

        # Add critical action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
        )
        state.private.actions.append(action)

        # Request confirmation
        new_state = _request_action_confirmation(state)

        # Should have confirmation move in agenda
        assert len(new_state.private.agenda) == 1
        confirm_move = new_state.private.agenda[0]
        assert confirm_move.move_type == "ask"
        assert confirm_move.metadata["confirmation_request"] is True
        assert "book_hotel" in str(confirm_move.content)


class TestActionRollback:
    """Tests for action rollback mechanisms."""

    def test_should_rollback_when_committed(self):
        """Test rollback detection when action was committed."""
        from ibdm.core.actions import Proposition
        from ibdm.core.domain import DomainModel
        from ibdm.rules.action_rules import _should_rollback

        state = InformationState()

        # Setup domain
        domain = DomainModel(name="test")

        def book_postcond(action):
            return [
                Proposition(
                    predicate="booked",
                    arguments={"hotel_id": action.parameters["hotel_id"]},
                )
            ]

        domain.register_postcond_function("book_hotel", book_postcond)
        state.private.beliefs["domain"] = domain

        # Action that was committed
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.shared.commitments.add("booked(hotel_id=H123)")

        result = ActionResult(
            status=ActionStatus.FAILURE,
            action=action,
            error_message="Payment failed",
        )

        # Should rollback (commitment exists)
        assert _should_rollback(result, state)

    def test_no_rollback_when_not_committed(self):
        """Test no rollback when nothing was committed."""
        from ibdm.rules.action_rules import _should_rollback

        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        result = ActionResult(
            status=ActionStatus.FAILURE,
            action=action,
            error_message="Preconditions not met",
        )

        # Should NOT rollback (nothing committed)
        assert not _should_rollback(result, state)

    def test_rollback_action(self):
        """Test action rollback removes postconditions."""
        from ibdm.core.actions import Proposition
        from ibdm.core.domain import DomainModel
        from ibdm.rules.action_rules import _rollback_action

        state = InformationState()

        # Setup domain
        domain = DomainModel(name="test")

        def book_postcond(action):
            return [
                Proposition(
                    predicate="booked",
                    arguments={"hotel_id": action.parameters["hotel_id"]},
                )
            ]

        domain.register_postcond_function("book_hotel", book_postcond)
        state.private.beliefs["domain"] = domain

        # Add commitment
        state.shared.commitments.add("booked(hotel_id=H123)")

        # Action to rollback
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        # Rollback
        new_state = _rollback_action(action, state)

        # Commitment should be removed
        assert "booked(hotel_id=H123)" not in new_state.shared.commitments

        # Should have rollback notification
        assert "rollback_performed" in new_state.private.beliefs


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_action_needs_confirmation_for_booking(self):
        """Test confirmation requirement for booking actions."""
        from ibdm.rules.action_rules import _action_needs_confirmation

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={},
        )

        assert _action_needs_confirmation(action)

    def test_action_needs_confirmation_for_payment(self):
        """Test confirmation requirement for payment actions."""
        from ibdm.rules.action_rules import _action_needs_confirmation

        action = Action(
            action_type=ActionType.SET,
            name="process_payment",
            parameters={},
        )

        assert _action_needs_confirmation(action)

    def test_no_confirmation_for_get(self):
        """Test no confirmation for read-only actions."""
        from ibdm.rules.action_rules import _action_needs_confirmation

        action = Action(
            action_type=ActionType.GET,
            name="get_hotels",
            parameters={},
        )

        assert not _action_needs_confirmation(action)


class TestRuleCreation:
    """Tests for rule creation functions."""

    def test_create_action_integration_rules(self):
        """Test that action integration rules are created correctly."""
        rules = create_action_integration_rules()

        assert len(rules) >= 2
        rule_names = [r.name for r in rules]
        assert "execute_action" in rule_names
        assert "process_action_result" in rule_names

    def test_create_action_selection_rules(self):
        """Test that action selection rules are created correctly."""
        rules = create_action_selection_rules()

        assert len(rules) >= 1
        rule_names = [r.name for r in rules]
        assert "request_action_confirmation" in rule_names


class TestIntegrationScenarios:
    """Integration tests for complete action execution scenarios."""

    def test_complete_action_flow_with_confirmation(self):
        """Test complete flow: request confirmation → confirm → execute → process."""
        from ibdm.rules.action_rules import (
            _execute_action,
            _process_action_result,
            _request_action_confirmation,
        )

        # 1. Request confirmation
        state = InformationState()
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
        )
        state.private.actions.append(action)

        state = _request_action_confirmation(state)
        assert len(state.private.agenda) == 1

        # 2. User confirms
        answer = Answer(content="yes", question_ref=None)
        confirm_move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.last_utterance = confirm_move

        # 3. Execute action
        device = MockDevice()
        device.configure(should_fail=False)
        state.private.beliefs["device_interface"] = device

        state = _execute_action(state)
        assert "action_result" in state.private.beliefs

        # 4. Process result
        state = _process_action_result(state)
        assert len(state.shared.commitments) > 0
        assert "action_feedback" in state.private.beliefs
        assert state.private.beliefs["action_feedback"]["status"] == "success"

    def test_action_failure_and_rollback(self):
        """Test action failure with rollback."""
        from ibdm.core.actions import Proposition
        from ibdm.core.domain import DomainModel
        from ibdm.rules.action_rules import _execute_action, _process_action_result

        state = InformationState()

        # Setup domain
        domain = DomainModel(name="test")

        def book_postcond(action):
            return [
                Proposition(
                    predicate="booked",
                    arguments={"hotel_id": action.parameters["hotel_id"]},
                )
            ]

        domain.register_postcond_function("book_hotel", book_postcond)
        state.private.beliefs["domain"] = domain

        # Optimistically commit (before execution - this is the rollback scenario)
        state.shared.commitments.add("booked(hotel_id=H123)")

        # Setup action that will fail
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        state.private.actions.append(action)

        # Setup device to fail
        device = MockDevice()
        device.configure(should_fail=True, failure_message="Payment declined")
        state.private.beliefs["device_interface"] = device

        # Execute (fails)
        state = _execute_action(state)

        # Process result (should rollback)
        state = _process_action_result(state)

        # Should have rollback notification
        assert "rollback_performed" in state.private.beliefs

        # Commitment should be removed
        assert "booked(hotel_id=H123)" not in state.shared.commitments
