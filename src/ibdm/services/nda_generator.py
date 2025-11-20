"""NDA Document Generation Service using LLM.

This service consumes information gathered through dialogue and generates
a professional Non-Disclosure Agreement using Claude Sonnet.
"""

import os
from dataclasses import dataclass
from typing import Any

import litellm


@dataclass
class NDAParameters:
    """Parameters for NDA generation extracted from dialogue state."""

    parties: list[str]
    """Legal entities entering into the NDA"""

    nda_type: str
    """Type of NDA: 'mutual', 'one-way', or 'unilateral'"""

    effective_date: str
    """Date when NDA takes effect (e.g., '2025-02-01' or 'February 1, 2025')"""

    duration: str
    """Confidentiality period (e.g., '3 years', '5 years')"""

    jurisdiction: str
    """Governing law jurisdiction (e.g., 'Delaware', 'California')"""

    additional_terms: dict[str, Any] | None = None
    """Optional additional terms or special provisions"""

    @classmethod
    def from_commitments(cls, commitments: set[str]) -> "NDAParameters":
        """Extract NDA parameters from dialogue commitments.

        Args:
            commitments: Set of commitment strings from dialogue state

        Returns:
            NDAParameters object with extracted values

        Example:
            >>> commitments = {
            ...     "legal_entities(Acme Corp, Global Industries)",
            ...     "nda_type(mutual)",
            ...     "date(2025-02-01)",
            ...     "time_period(3 years)",
            ...     "jurisdiction(Delaware)"
            ... }
            >>> params = NDAParameters.from_commitments(commitments)
            >>> params.nda_type
            'mutual'
        """
        params: dict[str, Any] = {}

        for commitment in commitments:
            # Parse commitment format: predicate(value)
            if "(" not in commitment or ")" not in commitment:
                continue

            predicate = commitment.split("(")[0]
            value = commitment.split("(")[1].rstrip(")")

            if predicate == "legal_entities":
                # Parse comma-separated parties
                params["parties"] = [p.strip() for p in value.split(",")]
            elif predicate == "nda_type":
                params["nda_type"] = value
            elif predicate == "date":
                params["effective_date"] = value
            elif predicate == "time_period":
                params["duration"] = value
            elif predicate == "jurisdiction":
                params["jurisdiction"] = value

        # Provide defaults for missing values
        return cls(
            parties=params.get("parties", ["Party A", "Party B"]),
            nda_type=params.get("nda_type", "mutual"),
            effective_date=params.get("effective_date", "the Effective Date"),
            duration=params.get("duration", "3 years"),
            jurisdiction=params.get("jurisdiction", "Delaware"),
            additional_terms=None,
        )


class NDAGenerator:
    """Generate NDA documents using Claude Sonnet LLM."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250929",
        api_key: str | None = None,
        temperature: float = 0.3,
    ):
        """Initialize NDA generator.

        Args:
            model: Claude model to use for generation
            api_key: Anthropic API key (defaults to IBDM_API_KEY env var)
            temperature: LLM temperature (0.3 for more consistent legal text)
        """
        self.model = model
        self.api_key = api_key or os.getenv("IBDM_API_KEY")
        self.temperature = temperature

        if not self.api_key:
            raise ValueError(
                "API key required. Set IBDM_API_KEY environment variable or pass api_key parameter."
            )

    def generate_nda(self, params: NDAParameters) -> str:
        """Generate complete NDA document from parameters.

        Args:
            params: NDA parameters extracted from dialogue

        Returns:
            Generated NDA document text (markdown format)

        Raises:
            ValueError: If required parameters are missing
            Exception: If LLM generation fails
        """
        # Validate required parameters
        if not params.parties or len(params.parties) < 2:
            raise ValueError("At least two parties required for NDA")

        # Build prompt
        prompt = self._build_generation_prompt(params)

        # Call LLM
        try:
            response = litellm.completion(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a legal document drafting assistant specializing "
                            "in Non-Disclosure Agreements. Generate professional, "
                            "legally sound NDAs based on provided parameters. "
                            "Use clear, precise legal language and standard NDA structure."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=4000,
            )

            generated_text = response.choices[0].message.content
            if not generated_text:
                raise ValueError("LLM returned empty response")

            return generated_text

        except Exception as e:
            raise Exception(f"NDA generation failed: {str(e)}") from e

    def _build_generation_prompt(self, params: NDAParameters) -> str:
        """Build LLM prompt for NDA generation.

        Args:
            params: NDA parameters

        Returns:
            Formatted prompt string
        """
        # Format parties list
        if len(params.parties) == 2:
            parties_text = f'"{params.parties[0]}" and "{params.parties[1]}"'
        else:
            parties_list = '", "'.join(params.parties[:-1])
            parties_text = f'"{parties_list}", and "{params.parties[-1]}"'

        # Determine NDA type description
        if params.nda_type.lower() in ["mutual", "bilateral"]:
            nda_type_desc = "mutual (both parties may disclose confidential information)"
        else:
            nda_type_desc = "one-way (only one party discloses confidential information)"

        prompt = f"""Generate a professional Non-Disclosure Agreement (NDA)
with the following specifications:

**Parties:**
- {parties_text}

**NDA Type:**
- {nda_type_desc}

**Effective Date:**
- {params.effective_date}

**Confidentiality Period:**
- {params.duration} from the date of disclosure

**Governing Law:**
- {params.jurisdiction}

**Requirements:**

1. **Structure**: Include standard NDA sections:
   - Preamble with parties and effective date
   - Recitals (WHEREAS clauses)
   - Definitions (Confidential Information, Disclosing Party, Receiving Party)
   - Confidentiality Obligations
   - Permitted Disclosures and Exclusions (standard 5 exceptions)
   - Term and Termination
   - Remedies
   - General Provisions (governing law, entire agreement, severability)
   - Signature blocks

2. **Legal Quality**:
   - Use precise legal language
   - Include standard exclusions (public domain, independently developed, etc.)
   - Specify {params.duration} confidentiality period
   - Reference {params.jurisdiction} as governing jurisdiction
   - Include appropriate remedies (injunctive relief, damages)

3. **Format**:
   - Use markdown format
   - Number sections clearly (1, 1.1, 1.2, etc.)
   - Use proper legal formatting conventions
   - Include placeholder signature blocks

4. **Completeness**:
   - This should be a production-ready NDA
   - Include all necessary legal provisions
   - Make it approximately 3-4 pages when printed

Generate the complete NDA document now. Use professional legal language
appropriate for a binding contract."""

        return prompt

    def generate_nda_from_commitments(self, commitments: set[str]) -> str:
        """Convenience method to generate NDA directly from commitments.

        Args:
            commitments: Set of commitment strings from dialogue state

        Returns:
            Generated NDA document text

        Example:
            >>> generator = NDAGenerator()
            >>> commitments = {
            ...     "legal_entities(Acme Corp, GlobalTech Inc)",
            ...     "nda_type(mutual)",
            ...     "date(February 1, 2025)",
            ...     "time_period(3 years)",
            ...     "jurisdiction(Delaware)"
            ... }
            >>> nda = generator.generate_nda_from_commitments(commitments)
        """
        params = NDAParameters.from_commitments(commitments)
        return self.generate_nda(params)


def generate_nda_from_dialogue_state(state: Any) -> str:
    """Generate NDA from dialogue information state.

    Args:
        state: InformationState object with commitments

    Returns:
        Generated NDA document text

    Example:
        >>> from ibdm.core import InformationState
        >>> state = InformationState()
        >>> # ... populate state through dialogue ...
        >>> nda_text = generate_nda_from_dialogue_state(state)
    """
    generator = NDAGenerator()
    return generator.generate_nda_from_commitments(state.shared.commitments)
