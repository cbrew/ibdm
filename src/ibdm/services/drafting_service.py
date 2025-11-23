"""Document Drafting Service with Revision Tracking.

Provides template-based document generation with revision history,
diff tracking, and rollback capabilities. Supports contracts, NDAs,
legal case reports, and other document types.

This is a mock/credible implementation - uses realistic patterns but
simplified logic suitable for dialogue interface demonstrations.
"""

import hashlib
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import litellm


class DocumentType(str, Enum):
    """Supported document types."""

    CONTRACT = "contract"
    NDA = "nda"
    LEGAL_REPORT = "legal_report"
    SOW = "statement_of_work"
    NCA = "non_compete_agreement"


class DocumentStatus(str, Enum):
    """Document lifecycle status."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REVISION_PENDING = "revision_pending"
    REJECTED = "rejected"


@dataclass
class DocumentRevision:
    """Single revision in document history."""

    revision_id: str
    """Unique identifier for this revision (hash)"""

    version: int
    """Version number (1, 2, 3, ...)"""

    content: str
    """Full document content at this revision"""

    timestamp: datetime
    """When this revision was created"""

    author: str
    """Who created this revision (user or 'system')"""

    change_description: str
    """Description of what changed in this revision"""

    parent_revision_id: str | None = None
    """ID of previous revision (None for initial draft)"""

    metadata: dict[str, Any] = field(default_factory=dict)  # type: ignore[misc]
    """Additional metadata (clauses added, parameters changed, etc.)"""

    def compute_hash(self) -> str:
        """Compute content hash for this revision.

        Returns:
            SHA-256 hash of content (first 12 chars)
        """
        content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        return content_hash[:12]


@dataclass
class DocumentDiff:
    """Diff between two document revisions."""

    from_revision: str
    """Source revision ID"""

    to_revision: str
    """Target revision ID"""

    added_lines: list[str]
    """Lines added in target"""

    removed_lines: list[str]
    """Lines removed from source"""

    changed_sections: list[str]
    """Section headers that changed"""

    summary: str
    """Human-readable summary of changes"""


@dataclass
class Document:
    """Document with full revision history."""

    document_id: str
    """Unique document identifier"""

    document_type: DocumentType
    """Type of document"""

    status: DocumentStatus
    """Current lifecycle status"""

    current_revision: DocumentRevision
    """Current/latest revision"""

    revisions: list[DocumentRevision] = field(default_factory=list)  # type: ignore[misc]
    """Complete revision history (oldest to newest)"""

    parameters: dict[str, Any] = field(default_factory=dict)  # type: ignore[misc]
    """Generation parameters (parties, dates, terms, etc.)"""

    approval_history: list[dict[str, Any]] = field(default_factory=list)  # type: ignore[misc]
    """Approval/rejection records"""

    def get_revision(self, version: int) -> DocumentRevision | None:
        """Get revision by version number.

        Args:
            version: Version number to retrieve

        Returns:
            DocumentRevision if found, None otherwise
        """
        for revision in self.revisions:
            if revision.version == version:
                return revision
        return None

    def get_latest_approved_revision(self) -> DocumentRevision | None:
        """Get most recent approved revision.

        Returns:
            Latest approved revision, or None if no approvals
        """
        # In this mock implementation, we'll look for approval metadata
        for revision in reversed(self.revisions):
            if revision.metadata.get("approved", False):
                return revision
        return None


class DraftingService:
    """Document drafting service with revision tracking.

    Features:
    - Template-based generation using LLM
    - Full revision history tracking
    - Diff computation between versions
    - Rollback to previous versions
    - Approval workflow support
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250929",
        api_key: str | None = None,
        temperature: float = 0.3,
    ):
        """Initialize drafting service.

        Args:
            model: Claude model for document generation
            api_key: Anthropic API key (defaults to IBDM_API_KEY)
            temperature: LLM temperature (lower for consistent legal text)
        """
        self.model = model
        self.api_key = api_key or os.getenv("IBDM_API_KEY")
        self.temperature = temperature
        self._documents: dict[str, Document] = {}

        if not self.api_key:
            raise ValueError(
                "API key required. Set IBDM_API_KEY environment variable or pass api_key parameter."
            )

    def create_document(
        self,
        document_type: DocumentType,
        parameters: dict[str, Any],
        author: str = "system",
    ) -> Document:
        """Create new document from parameters.

        Args:
            document_type: Type of document to create
            parameters: Generation parameters (parties, terms, etc.)
            author: Who is creating the document

        Returns:
            New Document with initial revision

        Example:
            >>> service = DraftingService()
            >>> doc = service.create_document(
            ...     DocumentType.CONTRACT,
            ...     {"parties": ["Acme Corp", "Beta Inc"], "terms": "Services agreement"}
            ... )
        """
        # Generate document content
        content = self._generate_content(document_type, parameters)

        # Create document ID
        doc_id = f"{document_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create initial revision
        initial_revision = DocumentRevision(
            revision_id=hashlib.sha256(content.encode()).hexdigest()[:12],
            version=1,
            content=content,
            timestamp=datetime.now(),
            author=author,
            change_description="Initial draft created",
            parent_revision_id=None,
            metadata={"parameters": parameters},
        )

        # Create document
        document = Document(
            document_id=doc_id,
            document_type=document_type,
            status=DocumentStatus.DRAFT,
            current_revision=initial_revision,
            revisions=[initial_revision],
            parameters=parameters,
        )

        # Store document
        self._documents[doc_id] = document

        return document

    def revise_document(
        self,
        document_id: str,
        changes: dict[str, Any],
        change_description: str,
        author: str = "system",
    ) -> Document:
        """Create new revision of document with changes.

        Args:
            document_id: ID of document to revise
            changes: Changes to apply (clauses to add, sections to modify, etc.)
            change_description: Human-readable description of changes
            author: Who is making the revision

        Returns:
            Updated Document with new revision

        Raises:
            ValueError: If document not found

        Example:
            >>> doc = service.revise_document(
            ...     "contract_20251123_120000",
            ...     {"add_clause": "non_compete"},
            ...     "Added non-compete clause"
            ... )
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        document = self._documents[document_id]

        # Apply changes to current content
        revised_content = self._apply_changes(
            document.current_revision.content, document.document_type, changes
        )

        # Create new revision
        new_version = len(document.revisions) + 1
        new_revision = DocumentRevision(
            revision_id=hashlib.sha256(revised_content.encode()).hexdigest()[:12],
            version=new_version,
            content=revised_content,
            timestamp=datetime.now(),
            author=author,
            change_description=change_description,
            parent_revision_id=document.current_revision.revision_id,
            metadata={"changes": changes},
        )

        # Update document
        document.current_revision = new_revision
        document.revisions.append(new_revision)
        document.status = DocumentStatus.REVISION_PENDING

        return document

    def rollback_document(self, document_id: str, target_version: int) -> Document:
        """Rollback document to previous version.

        Args:
            document_id: ID of document to rollback
            target_version: Version number to rollback to

        Returns:
            Document with current revision set to target version

        Raises:
            ValueError: If document or version not found

        Example:
            >>> doc = service.rollback_document("contract_20251123_120000", 1)
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        document = self._documents[document_id]

        target_revision = document.get_revision(target_version)
        if not target_revision:
            raise ValueError(f"Version {target_version} not found in revision history")

        # Create new revision that copies content from target
        rollback_revision = DocumentRevision(
            revision_id=hashlib.sha256(
                f"{target_revision.content}_rollback_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:12],
            version=len(document.revisions) + 1,
            content=target_revision.content,
            timestamp=datetime.now(),
            author="system",
            change_description=f"Rolled back to version {target_version}",
            parent_revision_id=document.current_revision.revision_id,
            metadata={"rollback_to_version": target_version},
        )

        # Update document
        document.current_revision = rollback_revision
        document.revisions.append(rollback_revision)
        document.status = DocumentStatus.DRAFT

        return document

    def compute_diff(self, document_id: str, from_version: int, to_version: int) -> DocumentDiff:
        """Compute diff between two versions.

        Args:
            document_id: ID of document
            from_version: Source version number
            to_version: Target version number

        Returns:
            DocumentDiff showing changes

        Raises:
            ValueError: If document or versions not found
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        document = self._documents[document_id]

        from_rev = document.get_revision(from_version)
        to_rev = document.get_revision(to_version)

        if not from_rev or not to_rev:
            raise ValueError(f"Versions {from_version} or {to_version} not found")

        # Simple diff: line-based comparison
        from_lines = set(from_rev.content.split("\n"))
        to_lines = set(to_rev.content.split("\n"))

        added = list(to_lines - from_lines)
        removed = list(from_lines - to_lines)

        # Find changed sections (lines starting with #)
        from_sections = {line for line in from_lines if line.startswith("#")}
        to_sections = {line for line in to_lines if line.startswith("#")}
        changed_sections = list((from_sections | to_sections) - (from_sections & to_sections))

        summary = f"{len(added)} lines added, {len(removed)} lines removed"
        if changed_sections:
            summary += f", {len(changed_sections)} sections modified"

        return DocumentDiff(
            from_revision=from_rev.revision_id,
            to_revision=to_rev.revision_id,
            added_lines=added,
            removed_lines=removed,
            changed_sections=changed_sections,
            summary=summary,
        )

    def approve_document(self, document_id: str, approver: str, notes: str = "") -> Document:
        """Approve current document revision.

        Args:
            document_id: ID of document to approve
            approver: Who is approving
            notes: Optional approval notes

        Returns:
            Updated Document with approval recorded

        Raises:
            ValueError: If document not found
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        document = self._documents[document_id]

        # Record approval
        approval_record = {
            "revision_id": document.current_revision.revision_id,
            "version": document.current_revision.version,
            "approver": approver,
            "timestamp": datetime.now().isoformat(),
            "approved": True,
            "notes": notes,
        }

        document.approval_history.append(approval_record)
        document.current_revision.metadata["approved"] = True
        document.status = DocumentStatus.APPROVED

        return document

    def reject_document(self, document_id: str, reviewer: str, reason: str) -> Document:
        """Reject current document revision.

        Args:
            document_id: ID of document to reject
            reviewer: Who is rejecting
            reason: Reason for rejection

        Returns:
            Updated Document with rejection recorded

        Raises:
            ValueError: If document not found
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        document = self._documents[document_id]

        # Record rejection
        rejection_record = {
            "revision_id": document.current_revision.revision_id,
            "version": document.current_revision.version,
            "reviewer": reviewer,
            "timestamp": datetime.now().isoformat(),
            "approved": False,
            "reason": reason,
        }

        document.approval_history.append(rejection_record)
        document.status = DocumentStatus.REJECTED

        return document

    def get_document(self, document_id: str) -> Document:
        """Get document by ID.

        Args:
            document_id: Document identifier

        Returns:
            Document instance

        Raises:
            ValueError: If document not found
        """
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")

        return self._documents[document_id]

    def _generate_content(self, document_type: DocumentType, parameters: dict[str, Any]) -> str:
        """Generate document content using LLM.

        Args:
            document_type: Type of document
            parameters: Generation parameters

        Returns:
            Generated document content (markdown)
        """
        prompt = self._build_generation_prompt(document_type, parameters)

        try:
            response = litellm.completion(  # type: ignore[misc]
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(document_type),
                    },
                    {"role": "user", "content": prompt},
                ],
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=4000,
            )

            generated_text = response.choices[0].message.content  # type: ignore[union-attr]
            if not generated_text:
                raise ValueError("LLM returned empty response")

            return generated_text  # type: ignore[return-value]

        except Exception as e:
            raise ValueError(f"Document generation failed: {str(e)}") from e

    def _apply_changes(
        self, current_content: str, document_type: DocumentType, changes: dict[str, Any]
    ) -> str:
        """Apply changes to document content.

        Args:
            current_content: Current document content
            document_type: Document type
            changes: Changes to apply

        Returns:
            Updated document content
        """
        # Mock implementation: generate new version with changes noted
        change_summary = ", ".join(f"{k}: {v}" for k, v in changes.items())

        prompt = f"""Revise the following {document_type.value} with these changes:

CHANGES REQUESTED:
{change_summary}

CURRENT DOCUMENT:
{current_content}

Generate the revised document incorporating these changes. Maintain the same format and structure.
Only modify the sections relevant to the requested changes."""

        try:
            response = litellm.completion(  # type: ignore[misc]
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(document_type),
                    },
                    {"role": "user", "content": prompt},
                ],
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=4000,
            )

            revised_text = response.choices[0].message.content  # type: ignore[union-attr]
            if not revised_text:
                raise ValueError("LLM returned empty response")

            return revised_text  # type: ignore[return-value]

        except Exception:
            # Fallback: simple text insertion for demo purposes
            return self._simple_change_application(current_content, changes)

    def _simple_change_application(self, content: str, changes: dict[str, Any]) -> str:
        """Simple fallback for applying changes without LLM.

        Args:
            content: Current content
            changes: Changes to apply

        Returns:
            Modified content with changes noted
        """
        # Add change notes at the end
        change_notes = "\n\n## REVISIONS\n\n"
        for key, value in changes.items():
            change_notes += f"- {key}: {value}\n"

        return content + change_notes

    def _get_system_prompt(self, document_type: DocumentType) -> str:
        """Get system prompt for document type.

        Args:
            document_type: Document type

        Returns:
            System prompt string
        """
        prompts = {
            DocumentType.CONTRACT: (
                "You are a legal document drafting assistant specializing in contracts. "
                "Generate professional, legally sound contracts with clear structure "
                "and precise language."
            ),
            DocumentType.NDA: (
                "You are a legal document drafting assistant specializing in NDAs. "
                "Generate professional, legally sound NDAs with standard structure "
                "and provisions."
            ),
            DocumentType.LEGAL_REPORT: (
                "You are a legal writing assistant specializing in case reports "
                "and legal analysis. Generate clear, well-structured legal reports "
                "with proper citations and analysis."
            ),
            DocumentType.SOW: (
                "You are a business document drafting assistant specializing in "
                "Statements of Work. Generate clear, detailed SOWs with scope, "
                "deliverables, timeline, and terms."
            ),
            DocumentType.NCA: (
                "You are a legal document drafting assistant specializing in "
                "Non-Compete Agreements. Generate enforceable NCAs with appropriate "
                "scope, duration, and geographic limitations."
            ),
        }

        return prompts.get(
            document_type,
            "You are a professional document drafting assistant. "
            "Generate clear, well-structured documents.",
        )

    def _build_generation_prompt(
        self, document_type: DocumentType, parameters: dict[str, Any]
    ) -> str:
        """Build generation prompt for document type.

        Args:
            document_type: Document type
            parameters: Generation parameters

        Returns:
            Formatted prompt string
        """
        # Generic prompt builder - can be specialized per document type
        param_text = "\n".join(f"- {k}: {v}" for k, v in parameters.items())

        return f"""Generate a professional {document_type.value} with the following parameters:

{param_text}

Requirements:
- Use markdown format
- Include all standard sections for this document type
- Use professional language appropriate for legal/business documents
- Make it production-ready and complete
- Include proper structure with numbered sections where appropriate

Generate the complete document now."""
