"""Negotiation rules for IBiS-4 action-oriented dialogue.

Implements negotiation mechanisms from Larsson (2002) Chapter 5 Section 5.7:
- Issues Under Negotiation (IUN) management
- Alternative accommodation and tracking
- Accept/reject negotiation moves
- Counter-proposal generation based on dominance relations

Based on Larsson (2002) Section 5.7 (Negotiative Dialogue).
"""

from ibdm.core import Answer, InformationState
from ibdm.core.actions import Proposition
from ibdm.rules.update_rules import UpdateRule


def create_negotiation_rules() -> list[UpdateRule]:
    """Create IBiS-4 negotiation rules.

    Returns rules for managing negotiative dialogue including:
    - Alternative accommodation (add propositions to IUN)
    - Accept/reject handling (resolve or remove from IUN)
    - Counter-proposal generation (suggest better alternatives)

    Based on Larsson Section 5.7.

    Returns:
        List of negotiation update rules
    """
    return [
        # Alternative accommodation - add propositions to IUN
        UpdateRule(
            name="accommodate_alternative",
            preconditions=_has_alternative_to_accommodate,
            effects=_accommodate_alternative,
            priority=12,  # High priority - handle alternatives early
            rule_type="integration",
        ),
        # Accept proposal - move from IUN to commitments
        UpdateRule(
            name="accept_proposal",
            preconditions=_has_accepted_proposal,
            effects=_accept_proposal,
            priority=11,  # After accommodation
            rule_type="integration",
        ),
        # Reject proposal - remove from IUN
        UpdateRule(
            name="reject_proposal",
            preconditions=_has_rejected_proposal,
            effects=_reject_proposal,
            priority=11,  # Same as accept
            rule_type="integration",
        ),
    ]


def create_negotiation_selection_rules() -> list[UpdateRule]:
    """Create negotiation selection rules.

    Returns selection rules for generating counter-proposals and
    suggesting alternatives in negotiative dialogue.

    Based on Larsson Section 5.7.3 (Counter-proposals).

    Returns:
        List of selection update rules
    """
    return [
        # Generate counter-proposal after rejection
        UpdateRule(
            name="generate_counter_proposal",
            preconditions=_should_generate_counter_proposal,
            effects=_generate_counter_proposal,
            priority=15,  # High priority - generate alternatives early
            rule_type="selection",
        ),
    ]


# ============================================================================
# Precondition Functions
# ============================================================================


def _has_alternative_to_accommodate(state: InformationState) -> bool:
    """Check if there are alternatives to add to IUN.

    Detects when:
    - User asserts a proposition that conflicts with existing commitments
    - User provides multiple alternative answers
    - System generates multiple options for negotiation

    Args:
        state: Current information state

    Returns:
        True if alternatives should be accommodated to IUN
    """
    if not state.private.last_utterance:
        return False

    move = state.private.last_utterance

    # Check for assert move with proposition content
    if move.move_type != "assert":
        return False

    # Check if move content is a proposition or can be converted to one
    content = move.content
    if isinstance(content, Proposition):
        # Check if this conflicts with existing commitments
        return _conflicts_with_commitments(content, state.shared.commitments)

    # Check if move has alternatives metadata
    if move.metadata and "alternatives" in move.metadata:
        return True

    return False


def _has_accepted_proposal(state: InformationState) -> bool:
    """Check if user has accepted a proposal from IUN.

    Detects acceptance through:
    - Explicit "yes" answer when IUN has proposals
    - Specific selection of a proposal (e.g., "I'll take option B")
    - Affirmative answer referencing a proposal

    Args:
        state: Current information state

    Returns:
        True if user has accepted a proposal
    """
    if not state.private.last_utterance:
        return False

    if not state.private.iun:
        return False  # No proposals to accept

    move = state.private.last_utterance

    # Check for answer move with positive content
    if move.move_type == "answer":
        content = move.content
        if isinstance(content, Answer):
            # Check for affirmative answers
            answer_text = str(content.content).lower()
            if answer_text in ["yes", "ok", "sure", "accept", "agreed"]:
                return True

    # Check for assert move selecting a specific alternative
    if move.move_type == "assert":
        content = move.content
        if isinstance(content, Proposition):
            # Check if this proposition matches one in IUN
            for prop in state.private.iun:
                if _propositions_match(content, prop):
                    return True

    return False


def _has_rejected_proposal(state: InformationState) -> bool:
    """Check if user has rejected a proposal from IUN.

    Detects rejection through:
    - Explicit "no" answer when IUN has proposals
    - Rejection statements (e.g., "I don't want that")
    - Counter-proposal that conflicts with IUN proposals

    Args:
        state: Current information state

    Returns:
        True if user has rejected a proposal
    """
    if not state.private.last_utterance:
        return False

    if not state.private.iun:
        return False  # No proposals to reject

    move = state.private.last_utterance

    # Check for answer move with negative content
    if move.move_type == "answer":
        content = move.content
        if isinstance(content, Answer):
            # Check for negative answers
            answer_text = str(content.content).lower()
            if answer_text in ["no", "nope", "reject", "no thanks"]:
                return True

    # Check for assert move that conflicts with IUN
    if move.move_type == "assert":
        content = move.content
        if isinstance(content, Proposition):
            # Check if this conflicts with any IUN proposal
            for prop in state.private.iun:
                if _propositions_conflict(content, prop):
                    return True

    return False


# ============================================================================
# Effect Functions
# ============================================================================


def _accommodate_alternative(state: InformationState) -> InformationState:
    """Add alternative propositions to IUN.

    Accommodates alternatives from:
    - User assertions that conflict with commitments
    - Multiple options provided in move metadata
    - System-generated alternatives for negotiation

    Based on Larsson Section 5.7.4 (Accommodation of Alternatives).

    Args:
        state: Current information state

    Returns:
        Updated state with alternatives added to IUN
    """
    if not state.private.last_utterance:
        return state

    move = state.private.last_utterance
    new_state = state.clone()

    # Handle proposition content
    if isinstance(move.content, Proposition):
        new_state.private.iun.add(move.content)

    # Handle alternatives in metadata
    if move.metadata and "alternatives" in move.metadata:
        alternatives_list = move.metadata["alternatives"]
        if not isinstance(alternatives_list, list):
            return new_state
        for alt in alternatives_list:
            if isinstance(alt, Proposition):
                new_state.private.iun.add(alt)
            elif isinstance(alt, dict):
                # Convert dict to Proposition
                predicate = alt.get("predicate")
                arguments = alt.get("arguments")
                if isinstance(predicate, str) and isinstance(arguments, dict):
                    prop = Proposition(
                        predicate=predicate,
                        arguments=arguments,
                    )
                    new_state.private.iun.add(prop)

    return new_state


def _accept_proposal(state: InformationState) -> InformationState:
    """Move accepted proposal from IUN to commitments.

    When user accepts a proposal:
    1. Identify which proposal was accepted
    2. Add it to shared commitments
    3. Remove it (and conflicting alternatives) from IUN

    Based on Larsson Section 5.7.2 (Negotiation Moves).

    Args:
        state: Current information state

    Returns:
        Updated state with accepted proposal committed
    """
    if not state.private.last_utterance:
        return state

    move = state.private.last_utterance
    new_state = state.clone()

    # Find the proposal to accept
    accepted_prop = None

    # If move content is a proposition, accept that specific one
    if isinstance(move.content, Proposition):
        accepted_prop = move.content

    # If simple "yes", accept the most recent IUN proposal
    elif isinstance(move.content, Answer):
        answer_text = str(move.content.content).lower()
        if answer_text in ["yes", "ok", "sure", "accept", "agreed"]:
            # Accept the first (most recent) proposal in IUN
            if new_state.private.iun:
                accepted_prop = next(iter(new_state.private.iun))

    if accepted_prop:
        # Add to commitments
        args_str = ", ".join(
            f"{k}={v}" for k, v in accepted_prop.arguments.items()
        )
        commitment_str = f"{accepted_prop.predicate}({args_str})"
        new_state.shared.commitments.add(commitment_str)

        # Remove from IUN (and conflicting alternatives)
        proposals_to_remove: set[Proposition] = set()
        for prop in new_state.private.iun:
            if _propositions_match(prop, accepted_prop) or _propositions_conflict(
                prop, accepted_prop
            ):
                proposals_to_remove.add(prop)

        new_state.private.iun -= proposals_to_remove

    return new_state


def _reject_proposal(state: InformationState) -> InformationState:
    """Remove rejected proposal from IUN.

    When user rejects a proposal:
    1. Identify which proposal was rejected
    2. Remove it from IUN
    3. May trigger counter-proposal generation (handled by selection rules)

    Based on Larsson Section 5.7.2 (Negotiation Moves).

    Args:
        state: Current information state

    Returns:
        Updated state with rejected proposal removed from IUN
    """
    if not state.private.last_utterance:
        return state

    move = state.private.last_utterance
    new_state = state.clone()

    # Find the proposal to reject
    rejected_prop = None

    # If move content is a proposition, reject that specific one
    if isinstance(move.content, Proposition):
        rejected_prop = move.content

    # If simple "no", reject all current IUN proposals
    elif isinstance(move.content, Answer):
        answer_text = str(move.content.content).lower()
        if answer_text in ["no", "nope", "reject", "no thanks"]:
            # Reject all proposals in IUN
            new_state.private.iun.clear()
            return new_state

    if rejected_prop:
        # Remove from IUN
        proposals_to_remove: set[Proposition] = set()
        for prop in new_state.private.iun:
            if _propositions_match(prop, rejected_prop):
                proposals_to_remove.add(prop)

        new_state.private.iun -= proposals_to_remove

    return new_state


# ============================================================================
# Helper Functions
# ============================================================================


def _conflicts_with_commitments(prop: Proposition, commitments: set[str]) -> bool:
    """Check if a proposition conflicts with existing commitments.

    Args:
        prop: Proposition to check
        commitments: Set of commitment strings

    Returns:
        True if proposition conflicts with commitments
    """
    # Check for direct conflicts (same predicate, different arguments)
    prop_predicate = prop.predicate

    for commitment in commitments:
        # Extract predicate from commitment string
        if "(" in commitment:
            commit_predicate = commitment.split("(")[0]
            if commit_predicate == prop_predicate:
                # Same predicate - check if arguments differ
                # Simplified check: if predicate matches but string differs, it's a conflict
                prop_str = (
                    f"{prop.predicate}({', '.join(f'{k}={v}' for k, v in prop.arguments.items())})"
                )
                if commitment != prop_str:
                    return True

    return False


def _propositions_match(prop1: Proposition, prop2: Proposition) -> bool:
    """Check if two propositions are the same.

    Args:
        prop1: First proposition
        prop2: Second proposition

    Returns:
        True if propositions match (same predicate and arguments)
    """
    if prop1.predicate != prop2.predicate:
        return False

    # Check if arguments match
    return prop1.arguments == prop2.arguments


def _propositions_conflict(prop1: Proposition, prop2: Proposition) -> bool:
    """Check if two propositions conflict.

    Propositions conflict if they have:
    - Same predicate
    - Different values for the same argument

    Args:
        prop1: First proposition
        prop2: Second proposition

    Returns:
        True if propositions conflict
    """
    if prop1.predicate != prop2.predicate:
        return False

    # Check if any shared arguments have different values
    shared_keys = set(prop1.arguments.keys()) & set(prop2.arguments.keys())
    for key in shared_keys:
        if prop1.arguments[key] != prop2.arguments[key]:
            return True

    return False


# ============================================================================
# Counter-Proposal Functions (Selection Rules)
# ============================================================================


def _should_generate_counter_proposal(state: InformationState) -> bool:
    """Check if we should generate a counter-proposal.

    Generate counter-proposal when:
    - User rejected a proposal (IUN was cleared or reduced)
    - We have better alternatives in beliefs or domain knowledge
    - Rejection is recent (last move was rejection)

    Args:
        state: Current information state

    Returns:
        True if counter-proposal should be generated
    """
    # Check if last move was a rejection
    if not state.private.last_utterance:
        return False

    move = state.private.last_utterance

    # Look for rejection signals in metadata
    if move.metadata and move.metadata.get("rejection_detected") is True:
        return True

    # Check if move was negative answer
    if move.move_type == "answer":
        content = move.content
        if isinstance(content, Answer):
            answer_text = str(content.content).lower()
            if answer_text in ["no", "nope", "reject", "no thanks"]:
                # Only generate if we have a rejected proposition in metadata
                return bool(
                    move.metadata and "rejected_proposition" in move.metadata
                )

    return False


def _generate_counter_proposal(state: InformationState) -> InformationState:
    """Generate counter-proposal based on rejected proposition.

    Uses domain knowledge to find a better alternative that dominates
    the rejected proposition. Adds counter-proposal to agenda.

    Based on Larsson Section 5.7.3 (Dominance and Alternatives).

    Args:
        state: Current information state

    Returns:
        Updated state with counter-proposal in agenda
    """
    if not state.private.last_utterance:
        return state

    move = state.private.last_utterance
    new_state = state.clone()

    # Get rejected proposition from metadata
    if not (move.metadata and "rejected_proposition" in move.metadata):
        return state

    rejected_prop = move.metadata["rejected_proposition"]
    if not isinstance(rejected_prop, Proposition):
        return state

    # Get domain model to check for better alternatives
    # This would normally come from the dialogue engine context
    # For now, we check if there are alternatives in beliefs or IUN
    alternatives: set[Proposition] = set()

    # Add alternatives from beliefs if any
    if "alternatives" in new_state.private.beliefs:
        belief_alts = new_state.private.beliefs["alternatives"]
        if isinstance(belief_alts, set):
            # Filter to only include Propositions
            from typing import Any

            alt: Any
            for alt in belief_alts:
                if isinstance(alt, Proposition):
                    alternatives.add(alt)

    # If we have alternatives, find a better one
    # This is a simplified version - in a full system, we'd use
    # domain.get_better_alternative(rejected_prop, alternatives)
    if alternatives:
        # For now, just propose the first alternative
        # In production, we'd use dominance relations to find the best one
        counter_prop: Proposition = next(iter(alternatives))

        # Create counter-proposal move
        from ibdm.core.moves import DialogueMove

        counter_move = DialogueMove(
            speaker="system",
            move_type="assert",
            content=counter_prop,
            metadata={
                "counter_proposal": True,
                "in_response_to": rejected_prop.to_dict(),
            },
        )

        # Add to agenda
        new_state.private.agenda.append(counter_move)

    return new_state
