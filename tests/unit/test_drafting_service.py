"""Tests for DraftingService.

Tests revision tracking, diff computation, rollback, and approval workflow.
"""

from unittest.mock import MagicMock, patch

import pytest

from ibdm.services.drafting_service import (
    Document,
    DocumentRevision,
    DocumentStatus,
    DocumentType,
    DraftingService,
)


@pytest.fixture
def mock_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set mock API key for tests."""
    monkeypatch.setenv("IBDM_API_KEY", "test-api-key-12345")


@pytest.fixture
def drafting_service(mock_api_key: None) -> DraftingService:
    """Create drafting service for tests."""
    return DraftingService()


@pytest.fixture
def mock_llm_response() -> str:
    """Mock LLM response for document generation."""
    return """# SERVICE AGREEMENT

Between Acme Corp and Beta Inc

## 1. Services
Beta Inc shall provide software development services to Acme Corp.

## 2. Terms
This agreement is effective for 12 months.

## 3. Compensation
Payment terms to be negotiated."""


class TestDraftingServiceInit:
    """Test DraftingService initialization."""

    def test_init_with_api_key(self, mock_api_key: None) -> None:
        """Test initialization with API key from environment."""
        service = DraftingService()
        assert service.api_key == "test-api-key-12345"
        assert service.model == "claude-sonnet-4-5-20250929"
        assert service.temperature == 0.3

    def test_init_with_custom_params(self, mock_api_key: None) -> None:
        """Test initialization with custom parameters."""
        service = DraftingService(
            model="claude-haiku-4-5-20251001", api_key="custom-key", temperature=0.5
        )
        assert service.api_key == "custom-key"
        assert service.model == "claude-haiku-4-5-20251001"
        assert service.temperature == 0.5

    def test_init_without_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test initialization fails without API key."""
        monkeypatch.delenv("IBDM_API_KEY", raising=False)

        with pytest.raises(ValueError, match="API key required"):
            DraftingService()


class TestDocumentCreation:
    """Test document creation."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_create_contract(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test creating a contract document."""
        # Mock LLM response
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )

        # Create document
        doc = drafting_service.create_document(
            DocumentType.CONTRACT,
            {
                "parties": ["Acme Corp", "Beta Inc"],
                "terms": "Software development services",
                "duration": "12 months",
            },
            author="test_user",
        )

        # Verify document created
        assert doc.document_type == DocumentType.CONTRACT
        assert doc.status == DocumentStatus.DRAFT
        assert len(doc.revisions) == 1
        assert doc.current_revision.version == 1
        assert doc.current_revision.author == "test_user"
        assert doc.current_revision.change_description == "Initial draft created"
        assert "SERVICE AGREEMENT" in doc.current_revision.content

        # Verify LLM was called
        mock_completion.assert_called_once()
        call_kwargs = mock_completion.call_args[1]
        assert call_kwargs["model"] == "claude-sonnet-4-5-20250929"
        assert call_kwargs["temperature"] == 0.3

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_create_nda(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
    ) -> None:
        """Test creating an NDA document."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="# NDA\n\nNon-Disclosure Agreement..."))]
        )

        doc = drafting_service.create_document(
            DocumentType.NDA, {"parties": ["Company A", "Company B"]}, author="system"
        )

        assert doc.document_type == DocumentType.NDA
        assert doc.status == DocumentStatus.DRAFT
        assert doc.current_revision.author == "system"


class TestDocumentRevision:
    """Test document revision functionality."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_revise_document(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test revising a document."""
        # Create initial document
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})
        doc_id = doc.document_id

        # Mock revised content
        revised_content = mock_llm_response + "\n\n## 4. Non-Compete\nNon-compete clause..."
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=revised_content))]
        )

        # Revise document
        revised_doc = drafting_service.revise_document(
            doc_id,
            {"add_clause": "non_compete"},
            "Added non-compete clause",
            author="legal_team",
        )

        # Verify revision created
        assert len(revised_doc.revisions) == 2
        assert revised_doc.current_revision.version == 2
        assert revised_doc.current_revision.author == "legal_team"
        assert revised_doc.current_revision.change_description == "Added non-compete clause"
        assert revised_doc.status == DocumentStatus.REVISION_PENDING
        assert "Non-Compete" in revised_doc.current_revision.content

        # Verify parent revision linked
        assert (
            revised_doc.current_revision.parent_revision_id == revised_doc.revisions[0].revision_id
        )

    def test_revise_nonexistent_document(self, drafting_service: DraftingService) -> None:
        """Test revising nonexistent document raises error."""
        with pytest.raises(ValueError, match="Document not found"):
            drafting_service.revise_document("nonexistent_id", {"change": "test"}, "Test change")


class TestDocumentRollback:
    """Test document rollback functionality."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_rollback_to_previous_version(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test rolling back to previous version."""
        # Create document with multiple revisions
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})
        doc_id = doc.document_id
        original_content = doc.current_revision.content

        # Make revision
        revised_content = mock_llm_response + "\n\nREVISION 1"
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=revised_content))]
        )
        drafting_service.revise_document(doc_id, {"add": "v1"}, "Version 1")

        # Rollback to version 1
        rolled_back = drafting_service.rollback_document(doc_id, 1)

        # Verify rollback
        assert len(rolled_back.revisions) == 3  # original + revision + rollback
        assert rolled_back.current_revision.version == 3
        assert rolled_back.current_revision.content == original_content
        assert "Rolled back to version 1" in rolled_back.current_revision.change_description
        assert rolled_back.status == DocumentStatus.DRAFT
        assert rolled_back.current_revision.metadata["rollback_to_version"] == 1

    def test_rollback_nonexistent_document(self, drafting_service: DraftingService) -> None:
        """Test rollback on nonexistent document raises error."""
        with pytest.raises(ValueError, match="Document not found"):
            drafting_service.rollback_document("nonexistent_id", 1)

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_rollback_nonexistent_version(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test rollback to nonexistent version raises error."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})

        with pytest.raises(ValueError, match="Version 99 not found"):
            drafting_service.rollback_document(doc.document_id, 99)


class TestDocumentDiff:
    """Test document diff computation."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_compute_diff(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test computing diff between versions."""
        # Create document
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})
        doc_id = doc.document_id

        # Revise document
        revised = mock_llm_response + "\n\n## 4. Warranties\nWarranty provisions..."
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=revised))]
        )
        drafting_service.revise_document(doc_id, {"add": "warranties"}, "Add warranties")

        # Compute diff
        diff = drafting_service.compute_diff(doc_id, 1, 2)

        # Verify diff
        assert diff.from_revision == doc.revisions[0].revision_id
        assert diff.to_revision == doc.revisions[1].revision_id
        assert len(diff.added_lines) > 0
        assert any("Warranties" in line for line in diff.added_lines)
        assert "added" in diff.summary

    def test_diff_nonexistent_document(self, drafting_service: DraftingService) -> None:
        """Test diff on nonexistent document raises error."""
        with pytest.raises(ValueError, match="Document not found"):
            drafting_service.compute_diff("nonexistent_id", 1, 2)


class TestApprovalWorkflow:
    """Test document approval/rejection workflow."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_approve_document(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test approving a document."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})

        # Approve document
        approved = drafting_service.approve_document(
            doc.document_id, approver="senior_partner", notes="Looks good"
        )

        # Verify approval
        assert approved.status == DocumentStatus.APPROVED
        assert len(approved.approval_history) == 1
        assert approved.approval_history[0]["approved"] is True
        assert approved.approval_history[0]["approver"] == "senior_partner"
        assert approved.approval_history[0]["notes"] == "Looks good"
        assert approved.current_revision.metadata["approved"] is True

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_reject_document(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test rejecting a document."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})

        # Reject document
        rejected = drafting_service.reject_document(
            doc.document_id, reviewer="legal_reviewer", reason="Missing indemnification clause"
        )

        # Verify rejection
        assert rejected.status == DocumentStatus.REJECTED
        assert len(rejected.approval_history) == 1
        assert rejected.approval_history[0]["approved"] is False
        assert rejected.approval_history[0]["reviewer"] == "legal_reviewer"
        assert rejected.approval_history[0]["reason"] == "Missing indemnification clause"

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_multiple_approval_rounds(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test multiple rounds of approval/rejection."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        doc = drafting_service.create_document(DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]})
        doc_id = doc.document_id

        # First rejection
        drafting_service.reject_document(doc_id, "reviewer1", "Needs work")

        # Revise
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response + "\nRevised"))]
        )
        drafting_service.revise_document(doc_id, {"fix": "issues"}, "Fixed issues")

        # Approve revised version
        final = drafting_service.approve_document(doc_id, "reviewer1", "Now approved")

        # Verify history
        assert len(final.approval_history) == 2
        assert final.approval_history[0]["approved"] is False
        assert final.approval_history[1]["approved"] is True
        assert final.status == DocumentStatus.APPROVED


class TestDocumentRetrieval:
    """Test document retrieval."""

    @patch("ibdm.services.drafting_service.litellm.completion")
    def test_get_document(
        self,
        mock_completion: MagicMock,
        drafting_service: DraftingService,
        mock_llm_response: str,
    ) -> None:
        """Test getting document by ID."""
        mock_completion.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_llm_response))]
        )
        created = drafting_service.create_document(
            DocumentType.CONTRACT, {"parties": ["Acme", "Beta"]}
        )

        # Get document
        retrieved = drafting_service.get_document(created.document_id)

        assert retrieved.document_id == created.document_id
        assert retrieved.current_revision.content == created.current_revision.content

    def test_get_nonexistent_document(self, drafting_service: DraftingService) -> None:
        """Test getting nonexistent document raises error."""
        with pytest.raises(ValueError, match="Document not found"):
            drafting_service.get_document("nonexistent_id")


class TestDocumentRevisionModel:
    """Test DocumentRevision model."""

    def test_compute_hash(self) -> None:
        """Test revision hash computation."""
        from datetime import datetime

        revision = DocumentRevision(
            revision_id="temp",
            version=1,
            content="Test content",
            timestamp=datetime.now(),
            author="test",
            change_description="Test",
        )

        hash_value = revision.compute_hash()
        assert isinstance(hash_value, str)
        assert len(hash_value) == 12  # First 12 chars of SHA-256


class TestDocumentModel:
    """Test Document model."""

    def test_get_revision(self) -> None:
        """Test getting revision by version number."""
        from datetime import datetime

        rev1 = DocumentRevision(
            revision_id="rev1",
            version=1,
            content="v1",
            timestamp=datetime.now(),
            author="test",
            change_description="v1",
        )
        rev2 = DocumentRevision(
            revision_id="rev2",
            version=2,
            content="v2",
            timestamp=datetime.now(),
            author="test",
            change_description="v2",
        )

        doc = Document(
            document_id="test",
            document_type=DocumentType.CONTRACT,
            status=DocumentStatus.DRAFT,
            current_revision=rev2,
            revisions=[rev1, rev2],
        )

        assert doc.get_revision(1) == rev1
        assert doc.get_revision(2) == rev2
        assert doc.get_revision(99) is None

    def test_get_latest_approved_revision(self) -> None:
        """Test getting latest approved revision."""
        from datetime import datetime

        rev1 = DocumentRevision(
            revision_id="rev1",
            version=1,
            content="v1",
            timestamp=datetime.now(),
            author="test",
            change_description="v1",
            metadata={"approved": True},
        )
        rev2 = DocumentRevision(
            revision_id="rev2",
            version=2,
            content="v2",
            timestamp=datetime.now(),
            author="test",
            change_description="v2",
        )

        doc = Document(
            document_id="test",
            document_type=DocumentType.CONTRACT,
            status=DocumentStatus.DRAFT,
            current_revision=rev2,
            revisions=[rev1, rev2],
        )

        latest_approved = doc.get_latest_approved_revision()
        assert latest_approved == rev1
