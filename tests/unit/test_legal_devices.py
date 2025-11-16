"""Unit tests for legal domain mock devices.

Tests DocumentGenerationDevice, SignatureDevice, and ComplianceCheckDevice.
"""

import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tests_dir))

from mocks.devices.legal_devices import (  # noqa: E402
    ComplianceCheckDevice,
    DocumentGenerationDevice,
    SignatureDevice,
)

from ibdm.core.actions import Action, ActionType  # noqa: E402
from ibdm.core.information_state import InformationState  # noqa: E402
from ibdm.interfaces.device import ActionStatus  # noqa: E402


class TestDocumentGenerationDevice:
    """Test DocumentGenerationDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = DocumentGenerationDevice()

        assert device.documents == {}
        assert device.generation_count == 0

    def test_generate_nda_success(self) -> None:
        """Test successful NDA generation."""
        device = DocumentGenerationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_nda",
            parameters={
                "party1_name": "Acme Corp",
                "party2_name": "Widget Inc",
                "effective_date": "2025-01-01",
                "confidentiality_period": "3 years",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "document_id" in result.return_value
        assert result.return_value["document_id"].startswith("DOC-")
        assert result.return_value["document_type"] == "Non-Disclosure Agreement"
        assert "document_generated" in result.postconditions[0]

    def test_generate_contract_success(self) -> None:
        """Test successful contract generation."""
        device = DocumentGenerationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_contract",
            parameters={
                "party1_name": "Seller Corp",
                "party2_name": "Buyer Inc",
                "effective_date": "2025-01-01",
                "contract_type": "service",
                "contract_value": "$100,000",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "document_id" in result.return_value
        assert result.return_value["status"] == "draft"

    def test_generate_employment_agreement(self) -> None:
        """Test employment agreement generation."""
        device = DocumentGenerationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_employment",
            parameters={
                "party1_name": "Tech Company",
                "party2_name": "John Developer",
                "effective_date": "2025-01-15",
                "position": "Senior Engineer",
                "salary": "$150,000",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        doc_id = result.return_value["document_id"]
        assert doc_id in device.documents
        assert device.documents[doc_id]["position"] == "Senior Engineer"

    def test_generate_missing_parameters(self) -> None:
        """Test generation with missing required parameters."""
        device = DocumentGenerationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_nda",
            parameters={"party1_name": "Acme Corp"},  # Missing party2 and date
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_review_document_success(self) -> None:
        """Test successful document review."""
        device = DocumentGenerationDevice()
        state = InformationState()

        # Generate document first
        gen_action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_nda",
            parameters={
                "party1_name": "Acme Corp",
                "party2_name": "Widget Inc",
                "effective_date": "2025-01-01",
            },
        )

        gen_result = device.execute_action(gen_action, state)
        doc_id = gen_result.return_value["document_id"]

        # Review it
        review_action = Action(
            action_type=ActionType.EXECUTE,
            name="review_document",
            parameters={"document_id": doc_id},
        )

        review_result = device.execute_action(review_action, state)

        assert review_result.is_successful()
        assert review_result.return_value["status"] == "ready"
        assert device.documents[doc_id]["status"] == "ready"

    def test_review_nonexistent_document(self) -> None:
        """Test reviewing non-existent document."""
        device = DocumentGenerationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="review_document",
            parameters={"document_id": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE


class TestSignatureDevice:
    """Test SignatureDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = SignatureDevice()

        assert device.envelopes == {}
        assert device.envelope_count == 0

    def test_send_for_signature_success(self) -> None:
        """Test sending document for signature."""
        device = SignatureDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={
                "document_id": "DOC-001",
                "signers": ["alice@example.com", "bob@example.com"],
                "message": "Please review and sign",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "envelope_id" in result.return_value
        assert result.return_value["envelope_id"].startswith("ENV-")
        assert result.return_value["status"] == "sent"
        assert len(result.return_value["signers"]) == 2

    def test_send_missing_parameters(self) -> None:
        """Test sending without required parameters."""
        device = SignatureDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={"document_id": "DOC-001"},  # Missing signers
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_check_signature_status(self) -> None:
        """Test checking signature status."""
        device = SignatureDevice()
        state = InformationState()

        # Send for signature first
        send_action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={
                "document_id": "DOC-001",
                "signers": ["alice@example.com"],
            },
        )

        send_result = device.execute_action(send_action, state)
        envelope_id = send_result.return_value["envelope_id"]

        # Check status
        status_action = Action(
            action_type=ActionType.GET,
            name="check_signature_status",
            parameters={"envelope_id": envelope_id},
        )

        status_result = device.execute_action(status_action, state)

        assert status_result.is_successful()
        assert "status" in status_result.return_value
        assert "signatures_collected" in status_result.return_value

    def test_download_signed_document(self) -> None:
        """Test downloading signed document."""
        device = SignatureDevice()
        state = InformationState()

        # Send for signature
        send_action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={
                "document_id": "DOC-001",
                "signers": ["alice@example.com"],
            },
        )

        send_result = device.execute_action(send_action, state)
        envelope_id = send_result.return_value["envelope_id"]

        # Manually complete signing
        device.envelopes[envelope_id]["status"] = "completed"

        # Download
        download_action = Action(
            action_type=ActionType.EXECUTE,
            name="download_signed",
            parameters={"envelope_id": envelope_id},
        )

        download_result = device.execute_action(download_action, state)

        assert download_result.is_successful()
        assert "document_url" in download_result.return_value

    def test_download_incomplete_document(self) -> None:
        """Test downloading document that's not fully signed."""
        device = SignatureDevice()
        state = InformationState()

        # Send for signature
        send_action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={
                "document_id": "DOC-001",
                "signers": ["alice@example.com"],
            },
        )

        send_result = device.execute_action(send_action, state)
        envelope_id = send_result.return_value["envelope_id"]

        # Try to download (still in "sent" status)
        download_action = Action(
            action_type=ActionType.EXECUTE,
            name="download_signed",
            parameters={"envelope_id": envelope_id},
        )

        download_result = device.execute_action(download_action, state)

        assert not download_result.is_successful()
        assert "not fully signed" in download_result.error_message

    def test_cancel_signature_request(self) -> None:
        """Test cancelling signature request."""
        device = SignatureDevice()
        state = InformationState()

        # Send for signature
        send_action = Action(
            action_type=ActionType.EXECUTE,
            name="send_for_signature",
            parameters={
                "document_id": "DOC-001",
                "signers": ["alice@example.com"],
            },
        )

        send_result = device.execute_action(send_action, state)
        envelope_id = send_result.return_value["envelope_id"]

        # Cancel
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_signature",
            parameters={"envelope_id": envelope_id},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert cancel_result.is_successful()
        assert device.envelopes[envelope_id]["status"] == "cancelled"


class TestComplianceCheckDevice:
    """Test ComplianceCheckDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = ComplianceCheckDevice()

        assert device.checks == {}
        assert device.check_count == 0

    def test_check_gdpr_compliance(self) -> None:
        """Test GDPR compliance check."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="check_gdpr_compliance",
            parameters={"document_id": "DOC-001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "check_id" in result.return_value
        assert result.return_value["standard"] == "GDPR"
        assert "passed" in result.return_value
        assert "issues_found" in result.return_value

    def test_check_hipaa_compliance(self) -> None:
        """Test HIPAA compliance check."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="check_hipaa_compliance",
            parameters={"policy_text": "Sample policy content"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.return_value["standard"] == "HIPAA"
        assert isinstance(result.return_value["passed"], bool)
        assert isinstance(result.return_value["issues"], list)

    def test_check_contract_terms(self) -> None:
        """Test contract terms compliance check."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="check_contract_terms",
            parameters={"document_id": "DOC-001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.return_value["standard"] == "Contract Terms"

    def test_missing_document(self) -> None:
        """Test compliance check with missing document."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="check_gdpr_compliance",
            parameters={},  # Missing document_id or policy_text
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_generate_compliance_report(self) -> None:
        """Test generating compliance report."""
        device = ComplianceCheckDevice()
        state = InformationState()

        # Run compliance check first
        check_action = Action(
            action_type=ActionType.EXECUTE,
            name="check_gdpr_compliance",
            parameters={"document_id": "DOC-001"},
        )

        check_result = device.execute_action(check_action, state)
        check_id = check_result.return_value["check_id"]

        # Generate report
        report_action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_compliance_report",
            parameters={"check_id": check_id},
        )

        report_result = device.execute_action(report_action, state)

        assert report_result.is_successful()
        assert "report_url" in report_result.return_value
        assert "summary" in report_result.return_value

    def test_report_for_nonexistent_check(self) -> None:
        """Test generating report for non-existent check."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_compliance_report",
            parameters={"check_id": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_postconditions_include_issues_count(self) -> None:
        """Test that postconditions include issues count."""
        device = ComplianceCheckDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="check_gdpr_compliance",
            parameters={"document_id": "DOC-001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()

        # Check postconditions
        postcond_strings = result.postconditions
        assert any("compliance_checked" in pc for pc in postcond_strings)
        assert any("compliance_status" in pc for pc in postcond_strings)
        assert any("issues_found" in pc for pc in postcond_strings)
