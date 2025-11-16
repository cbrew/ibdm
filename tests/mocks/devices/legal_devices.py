"""Legal and document service mock devices.

Simulates legal document generation, e-signature, and compliance checking services.
"""

from typing import Any
import random
from datetime import datetime, timedelta

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import ActionResult, ActionStatus, DeviceInterface


class DocumentGenerationDevice(DeviceInterface):
    """Mock legal document generation service (e.g., ContractExpress, HotDocs).

    Simulates automated generation of legal documents like NDAs, contracts,
    employment agreements, etc.

    Actions:
    - generate_nda: Generate non-disclosure agreement
    - generate_contract: Generate service/sales contract
    - generate_employment: Generate employment agreement
    - review_document: Review document for completeness

    Preconditions:
    - Required template parameters (party_names, effective_date, jurisdiction)
    - Valid document type

    Postconditions:
    - document_generated(doc_id=...)
    - document_status(status=draft|ready)
    """

    DOCUMENT_TYPES = {
        "nda": "Non-Disclosure Agreement",
        "service_contract": "Service Agreement",
        "sales_contract": "Sales Contract",
        "employment": "Employment Agreement",
        "consulting": "Consulting Agreement",
    }

    def __init__(self, fail_rate: float = 0.0):
        """Initialize document generation device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        self.documents: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.generation_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute document generation action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required document parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Document generation service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "generate_nda":
            return self._generate_nda(action)
        elif action.name == "generate_contract":
            return self._generate_contract(action)
        elif action.name == "generate_employment":
            return self._generate_employment(action)
        elif action.name == "review_document":
            return self._review_document(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if document generation preconditions are satisfied."""
        params = action.parameters

        if action.name in ["generate_nda", "generate_contract", "generate_employment"]:
            # Require party names and effective date
            required = ["party1_name", "party2_name", "effective_date"]
            return all(key in params for key in required)
        elif action.name == "review_document":
            # Require document ID
            return "document_id" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for document action."""
        if action.name in ["generate_nda", "generate_contract", "generate_employment"]:
            doc_id = f"DOC-{self.generation_count:06d}"
            return [
                f"document_generated(doc_id={doc_id})",
                "document_status(status=draft)",
            ]
        elif action.name == "review_document":
            return ["document_reviewed", "document_status(status=ready)"]

        return []

    def _generate_nda(self, action: Action) -> ActionResult:
        """Generate non-disclosure agreement."""
        self.generation_count += 1
        doc_id = f"DOC-{self.generation_count:06d}"

        params = action.parameters

        document = {
            "doc_id": doc_id,
            "type": "nda",
            "party1": params["party1_name"],
            "party2": params["party2_name"],
            "effective_date": params["effective_date"],
            "confidentiality_period": params.get("confidentiality_period", "2 years"),
            "jurisdiction": params.get("jurisdiction", "Delaware"),
            "status": "draft",
            "created_at": datetime.now().isoformat(),
        }

        self.documents[doc_id] = document

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "document_id": doc_id,
                "document_type": "Non-Disclosure Agreement",
                "status": "draft",
                "download_url": f"https://api.legal.example/documents/{doc_id}",
            },
            postconditions=[
                f"document_generated(doc_id={doc_id})",
                "document_status(status=draft)",
            ],
        )

    def _generate_contract(self, action: Action) -> ActionResult:
        """Generate service or sales contract."""
        self.generation_count += 1
        doc_id = f"DOC-{self.generation_count:06d}"

        params = action.parameters
        contract_type = params.get("contract_type", "service")

        document = {
            "doc_id": doc_id,
            "type": contract_type + "_contract",
            "party1": params["party1_name"],
            "party2": params["party2_name"],
            "effective_date": params["effective_date"],
            "contract_value": params.get("contract_value", "$0"),
            "term": params.get("term", "1 year"),
            "jurisdiction": params.get("jurisdiction", "Delaware"),
            "status": "draft",
            "created_at": datetime.now().isoformat(),
        }

        self.documents[doc_id] = document

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "document_id": doc_id,
                "document_type": self.DOCUMENT_TYPES.get(contract_type + "_contract", "Contract"),
                "status": "draft",
                "download_url": f"https://api.legal.example/documents/{doc_id}",
            },
            postconditions=[
                f"document_generated(doc_id={doc_id})",
                "document_status(status=draft)",
            ],
        )

    def _generate_employment(self, action: Action) -> ActionResult:
        """Generate employment agreement."""
        self.generation_count += 1
        doc_id = f"DOC-{self.generation_count:06d}"

        params = action.parameters

        document = {
            "doc_id": doc_id,
            "type": "employment",
            "employer": params["party1_name"],
            "employee": params["party2_name"],
            "effective_date": params["effective_date"],
            "position": params.get("position", "Employee"),
            "salary": params.get("salary", "$0"),
            "employment_type": params.get("employment_type", "full-time"),
            "jurisdiction": params.get("jurisdiction", "Delaware"),
            "status": "draft",
            "created_at": datetime.now().isoformat(),
        }

        self.documents[doc_id] = document

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "document_id": doc_id,
                "document_type": "Employment Agreement",
                "status": "draft",
                "download_url": f"https://api.legal.example/documents/{doc_id}",
            },
            postconditions=[
                f"document_generated(doc_id={doc_id})",
                "document_status(status=draft)",
            ],
        )

    def _review_document(self, action: Action) -> ActionResult:
        """Review document for completeness."""
        doc_id = action.parameters.get("document_id")

        if not doc_id or doc_id not in self.documents:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Document {doc_id} not found",
            )

        document = self.documents[doc_id]
        document["status"] = "ready"
        document["reviewed_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "document_id": doc_id,
                "status": "ready",
                "review_notes": "Document complete and ready for signature",
            },
            postconditions=["document_reviewed", "document_status(status=ready)"],
        )


class SignatureDevice(DeviceInterface):
    """Mock e-signature service (e.g., DocuSign, Adobe Sign).

    Simulates electronic signature workflows for legal documents.

    Actions:
    - send_for_signature: Send document to signers
    - check_signature_status: Check signing progress
    - download_signed: Download fully executed document
    - cancel_signature: Cancel signature request

    Preconditions:
    - Valid document ID
    - Signer email addresses

    Postconditions:
    - signature_requested(envelope_id=...)
    - signature_status(status=sent|completed|cancelled)
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize signature device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        self.envelopes: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.envelope_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute signature action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required signature parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Signature service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "send_for_signature":
            return self._send_for_signature(action)
        elif action.name == "check_signature_status":
            return self._check_signature_status(action)
        elif action.name == "download_signed":
            return self._download_signed(action)
        elif action.name == "cancel_signature":
            return self._cancel_signature(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if signature preconditions are satisfied."""
        params = action.parameters

        if action.name == "send_for_signature":
            # Require document ID and signers
            return "document_id" in params and "signers" in params
        elif action.name in ["check_signature_status", "download_signed", "cancel_signature"]:
            # Require envelope ID
            return "envelope_id" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for signature action."""
        if action.name == "send_for_signature":
            envelope_id = f"ENV-{self.envelope_count:06d}"
            return [
                f"signature_requested(envelope_id={envelope_id})",
                "signature_status(status=sent)",
            ]
        elif action.name == "check_signature_status":
            return ["signature_status_checked"]
        elif action.name == "download_signed":
            return ["signed_document_downloaded"]
        elif action.name == "cancel_signature":
            return ["signature_status(status=cancelled)"]

        return []

    def _send_for_signature(self, action: Action) -> ActionResult:
        """Send document for signature."""
        self.envelope_count += 1
        envelope_id = f"ENV-{self.envelope_count:06d}"

        params = action.parameters
        signers = params["signers"]  # List of email addresses

        envelope = {
            "envelope_id": envelope_id,
            "document_id": params["document_id"],
            "signers": signers,
            "status": "sent",
            "sent_at": datetime.now().isoformat(),
            "signatures_collected": 0,
            "signatures_required": len(signers),
            "message": params.get("message", "Please review and sign"),
        }

        self.envelopes[envelope_id] = envelope

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "envelope_id": envelope_id,
                "status": "sent",
                "signers": signers,
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            },
            postconditions=[
                f"signature_requested(envelope_id={envelope_id})",
                "signature_status(status=sent)",
            ],
        )

    def _check_signature_status(self, action: Action) -> ActionResult:
        """Check signature status."""
        envelope_id = action.parameters.get("envelope_id")

        if not envelope_id or envelope_id not in self.envelopes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Envelope {envelope_id} not found",
            )

        envelope = self.envelopes[envelope_id]

        # Simulate progressive signing (30% chance of progress)
        if envelope["status"] == "sent" and random.random() < 0.3:
            envelope["signatures_collected"] += 1
            if envelope["signatures_collected"] >= envelope["signatures_required"]:
                envelope["status"] = "completed"
                envelope["completed_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "envelope_id": envelope_id,
                "status": envelope["status"],
                "signatures_collected": envelope["signatures_collected"],
                "signatures_required": envelope["signatures_required"],
            },
            postconditions=["signature_status_checked"],
        )

    def _download_signed(self, action: Action) -> ActionResult:
        """Download signed document."""
        envelope_id = action.parameters.get("envelope_id")

        if not envelope_id or envelope_id not in self.envelopes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Envelope {envelope_id} not found",
            )

        envelope = self.envelopes[envelope_id]

        if envelope["status"] != "completed":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Document not fully signed yet",
            )

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "envelope_id": envelope_id,
                "document_url": f"https://api.signature.example/download/{envelope_id}",
                "format": "pdf",
                "completed_at": envelope.get("completed_at"),
            },
            postconditions=["signed_document_downloaded"],
        )

    def _cancel_signature(self, action: Action) -> ActionResult:
        """Cancel signature request."""
        envelope_id = action.parameters.get("envelope_id")

        if not envelope_id or envelope_id not in self.envelopes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Envelope {envelope_id} not found",
            )

        envelope = self.envelopes[envelope_id]

        if envelope["status"] == "completed":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Cannot cancel completed signature request",
            )

        envelope["status"] = "cancelled"
        envelope["cancelled_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "envelope_id": envelope_id,
                "status": "cancelled",
            },
            postconditions=["signature_status(status=cancelled)"],
        )


class ComplianceCheckDevice(DeviceInterface):
    """Mock legal compliance checking service.

    Simulates automated compliance verification for contracts, policies,
    and regulatory requirements (e.g., GDPR, HIPAA, SOC2).

    Actions:
    - check_gdpr_compliance: Verify GDPR compliance
    - check_hipaa_compliance: Verify HIPAA compliance
    - check_contract_terms: Verify contract terms compliance
    - generate_compliance_report: Generate compliance report

    Preconditions:
    - Document or policy to check
    - Compliance standard specified

    Postconditions:
    - compliance_checked(standard=...)
    - compliance_status(passed=true|false)
    - issues_found(count=...)
    """

    COMPLIANCE_STANDARDS = {
        "gdpr": "General Data Protection Regulation",
        "hipaa": "Health Insurance Portability and Accountability Act",
        "soc2": "SOC 2 Type II",
        "pci_dss": "Payment Card Industry Data Security Standard",
        "ccpa": "California Consumer Privacy Act",
    }

    def __init__(self, fail_rate: float = 0.0):
        """Initialize compliance checking device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        self.checks: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.check_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute compliance check action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required compliance check parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Compliance service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "check_gdpr_compliance":
            return self._check_gdpr_compliance(action)
        elif action.name == "check_hipaa_compliance":
            return self._check_hipaa_compliance(action)
        elif action.name == "check_contract_terms":
            return self._check_contract_terms(action)
        elif action.name == "generate_compliance_report":
            return self._generate_compliance_report(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if compliance check preconditions are satisfied."""
        params = action.parameters

        if action.name in [
            "check_gdpr_compliance",
            "check_hipaa_compliance",
            "check_contract_terms",
        ]:
            # Require document or policy content
            return "document_id" in params or "policy_text" in params
        elif action.name == "generate_compliance_report":
            # Require check ID
            return "check_id" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for compliance action."""
        if action.name in ["check_gdpr_compliance", "check_hipaa_compliance"]:
            standard = "gdpr" if "gdpr" in action.name else "hipaa"
            return [
                f"compliance_checked(standard={standard})",
                "compliance_status(passed=unknown)",
            ]
        elif action.name == "check_contract_terms":
            return [
                "compliance_checked(standard=contract_terms)",
                "compliance_status(passed=unknown)",
            ]
        elif action.name == "generate_compliance_report":
            return ["compliance_report_generated"]

        return []

    def _check_gdpr_compliance(self, action: Action) -> ActionResult:
        """Check GDPR compliance."""
        self.check_count += 1
        check_id = f"CHK-{self.check_count:06d}"

        # Simulate compliance check (random pass/fail with issues)
        passed = random.random() > 0.3
        issues_count = 0 if passed else random.randint(1, 5)

        issues = []
        if not passed:
            possible_issues = [
                "Missing data subject consent mechanism",
                "No clear privacy policy link",
                "Data retention period not specified",
                "Right to erasure not implemented",
                "No data processing agreement with third parties",
            ]
            issues = random.sample(possible_issues, issues_count)

        check_result = {
            "check_id": check_id,
            "standard": "gdpr",
            "passed": passed,
            "issues": issues,
            "checked_at": datetime.now().isoformat(),
        }

        self.checks[check_id] = check_result

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "check_id": check_id,
                "standard": "GDPR",
                "passed": passed,
                "issues_found": issues_count,
                "issues": issues,
            },
            postconditions=[
                "compliance_checked(standard=gdpr)",
                f"compliance_status(passed={str(passed).lower()})",
                f"issues_found(count={issues_count})",
            ],
        )

    def _check_hipaa_compliance(self, action: Action) -> ActionResult:
        """Check HIPAA compliance."""
        self.check_count += 1
        check_id = f"CHK-{self.check_count:06d}"

        # Simulate compliance check
        passed = random.random() > 0.3
        issues_count = 0 if passed else random.randint(1, 5)

        issues = []
        if not passed:
            possible_issues = [
                "Missing encryption for data at rest",
                "Insufficient access controls",
                "No audit logging mechanism",
                "Missing business associate agreement",
                "Inadequate backup and disaster recovery",
            ]
            issues = random.sample(possible_issues, issues_count)

        check_result = {
            "check_id": check_id,
            "standard": "hipaa",
            "passed": passed,
            "issues": issues,
            "checked_at": datetime.now().isoformat(),
        }

        self.checks[check_id] = check_result

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "check_id": check_id,
                "standard": "HIPAA",
                "passed": passed,
                "issues_found": issues_count,
                "issues": issues,
            },
            postconditions=[
                "compliance_checked(standard=hipaa)",
                f"compliance_status(passed={str(passed).lower()})",
                f"issues_found(count={issues_count})",
            ],
        )

    def _check_contract_terms(self, action: Action) -> ActionResult:
        """Check contract terms compliance."""
        self.check_count += 1
        check_id = f"CHK-{self.check_count:06d}"

        # Simulate contract terms check
        passed = random.random() > 0.2
        issues_count = 0 if passed else random.randint(1, 4)

        issues = []
        if not passed:
            possible_issues = [
                "Missing force majeure clause",
                "Unclear termination conditions",
                "No dispute resolution mechanism specified",
                "Liability limitations missing",
            ]
            issues = random.sample(possible_issues, min(issues_count, len(possible_issues)))

        check_result = {
            "check_id": check_id,
            "standard": "contract_terms",
            "passed": passed,
            "issues": issues,
            "checked_at": datetime.now().isoformat(),
        }

        self.checks[check_id] = check_result

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "check_id": check_id,
                "standard": "Contract Terms",
                "passed": passed,
                "issues_found": issues_count,
                "issues": issues,
            },
            postconditions=[
                "compliance_checked(standard=contract_terms)",
                f"compliance_status(passed={str(passed).lower()})",
                f"issues_found(count={issues_count})",
            ],
        )

    def _generate_compliance_report(self, action: Action) -> ActionResult:
        """Generate compliance report."""
        check_id = action.parameters.get("check_id")

        if not check_id or check_id not in self.checks:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Check {check_id} not found",
            )

        check_result = self.checks[check_id]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "check_id": check_id,
                "report_url": f"https://api.compliance.example/reports/{check_id}",
                "format": "pdf",
                "summary": {
                    "standard": check_result["standard"],
                    "passed": check_result["passed"],
                    "issues_count": len(check_result["issues"]),
                },
            },
            postconditions=["compliance_report_generated"],
        )
