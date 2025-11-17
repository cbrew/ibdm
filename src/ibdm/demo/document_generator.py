"""Document generation from dialogue commitments.

Demonstrates how information collected during dialogue is used to generate
actual documents (template injection).
"""

from typing import Any


def generate_nda_from_commitments(commitments: set[str] | dict[str, Any]) -> str:
    """Generate an NDA document from dialogue commitments.

    This demonstrates template injection - using information collected
    during the dialogue to populate a document template.

    Args:
        commitments: Either a set of commitment strings or a dict of values

    Returns:
        Formatted NDA document with injected values

    Example:
        >>> commitments = {
        ...     "parties": "Acme Corp and Smith Inc",
        ...     "nda_type": "mutual",
        ...     "effective_date": "January 1, 2025",
        ...     "duration": "5 years",
        ...     "governing_law": "California"
        ... }
        >>> nda = generate_nda_from_commitments(commitments)
        >>> "Acme Corp" in nda
        True
    """
    # Extract values from commitments
    if isinstance(commitments, set):
        # Parse commitment strings like "parties(Acme Corp and Smith Inc)"
        values = _parse_commitment_set(commitments)
    else:
        values = commitments

    # Default values if not provided
    parties = values.get("parties", "Party A and Party B")
    nda_type = values.get("nda_type", "mutual").lower()
    effective_date = values.get("effective_date", "[EFFECTIVE DATE]")
    duration = values.get("duration", "[DURATION]")
    governing_law = values.get("governing_law", "[STATE]")

    # Parse parties into first and second party
    if " and " in parties:
        party_list = parties.split(" and ", 1)
        first_party = party_list[0].strip()
        second_party = party_list[1].strip()
    else:
        first_party = parties
        second_party = "[Second Party]"

    # Determine NDA type for title
    nda_type_title = "MUTUAL" if nda_type == "mutual" else "ONE-WAY"

    # Template injection - this is where the magic happens!
    document = f"""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    {nda_type_title} NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This {nda_type_title.title()} Non-Disclosure Agreement (the "Agreement") is entered into
as of {effective_date} (the "Effective Date") by and between:

    {first_party} ("First Party")
    and
    {second_party} ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of {duration} from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of {governing_law}, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
{first_party}                             {second_party}
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using your specifications
✓ Document created from dialogue commitments:
  • Parties: {first_party} and {second_party}
  • Type: {nda_type_title}
  • Effective Date: {effective_date}
  • Duration: {duration}
  • Governing Law: {governing_law}
✓ Ready for review and execution"""

    return document


def _parse_commitment_set(commitments: set[str]) -> dict[str, str]:
    """Parse commitment strings into a dictionary.

    Args:
        commitments: Set of commitment strings like "parties(Acme Corp and Smith Inc)"

    Returns:
        Dictionary mapping predicates to values
    """
    result: dict[str, str] = {}

    for commitment in commitments:
        if "(" in commitment and commitment.endswith(")"):
            # Parse "predicate(value)" format
            predicate, value = commitment.split("(", 1)
            value = value.rstrip(")")
            result[predicate.strip()] = value.strip()

    return result


def generate_document_from_state(state: Any, document_type: str = "nda") -> str:
    """Generate a document from dialogue state.

    Args:
        state: InformationState object with commitments
        document_type: Type of document to generate

    Returns:
        Generated document string
    """
    if document_type == "nda":
        return generate_nda_from_commitments(state.shared.commitments)
    else:
        raise ValueError(f"Unknown document type: {document_type}")
