"""Unified scenario runner for executing and displaying dialogue scenarios.

This module provides a clean, reusable interface for running JSON-based scenarios
with professional console output, execution flow control, and rich formatting.

This runner ACTUALLY RUNS the Larsson dialogue engine - it's not just playback.
It integrates user moves, runs selection rules, and can optionally generate
system responses using real NLG.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ibdm.core import DialogueMove, InformationState
from ibdm.core.actions import Action
from ibdm.demo.execution_controller import ExecutionController, ExecutionMode
from ibdm.demo.orchestrator import DemoDialogueOrchestrator
from ibdm.demo.scenario_loader import Scenario, ScenarioTurn, load_scenario
from ibdm.demo.state_trace import StateTraceRecorder
from ibdm.domains.legal_domain import get_legal_domain
from ibdm.domains.nda_domain import get_doc_actions, get_nda_domain
from ibdm.rules import (
    RuleSet,
    create_action_integration_rules,
    create_action_selection_rules,
    create_generation_rules,
    create_integration_rules,
    create_negotiation_rules,
    create_negotiation_selection_rules,
    create_selection_rules,
)

if TYPE_CHECKING:
    from ibdm.nlg import NLGEngine


class ScenarioRunner:
    """Runs and displays dialogue scenarios with the real Larsson engine.

    This class orchestrates scenario execution by combining:
    - ScenarioLoader: Loads JSON scenarios
    - DemoDialogueOrchestrator: Runs real Larsson dialogue engine
    - ExecutionController: Controls timing and flow (step/auto/replay)
    - NLGEngine: Optional natural language generation
    - Rich formatting: Professional console output

    The runner ACTUALLY EXECUTES the Larsson dialogue cycle:
    - Mocks NLU (creates DialogueMoves from JSON)
    - Runs real INTEGRATE rules
    - Runs real SELECT rules
    - Optionally runs real GENERATE phase (NLG)

    Examples:
        >>> # Load and run a scenario (playback mode - no NLG)
        >>> scenario = load_scenario("nda_basic")
        >>> runner = ScenarioRunner(scenario, nlg_mode="off")
        >>> runner.run()

        >>> # Run with NLG comparison
        >>> runner = ScenarioRunner(scenario, nlg_mode="compare")
        >>> runner.run()

        >>> # Run with NLG only (replace scripted text)
        >>> runner = ScenarioRunner(scenario, nlg_mode="replace")
        >>> runner.run()

        >>> # Run in step mode with detailed state tracking
        >>> controller = ExecutionController(mode=ExecutionMode.STEP)
        >>> runner = ScenarioRunner(
        ...     scenario,
        ...     controller=controller,
        ...     nlg_mode="compare",
        ...     show_engine_state=True
        ... )
        >>> runner.run()
    """

    def __init__(
        self,
        scenario: Scenario,
        controller: ExecutionController | None = None,
        console: Console | None = None,
        nlg_mode: str = "off",
        show_explanations: bool = True,
        show_state_changes: bool = True,
        show_larsson_rules: bool = True,
        show_metrics: bool = True,
        show_engine_state: bool = False,
        trace_recorder: StateTraceRecorder | None = None,
    ):
        """Initialize scenario runner with real Larsson engine.

        Args:
            scenario: Scenario to run
            controller: Execution controller (default: AUTO mode)
            console: Rich console for output (default: create new)
            nlg_mode: NLG mode - "off" (scripted), "compare" (both), "replace" (NLG only)
            show_explanations: Show business explanations for each turn
            show_state_changes: Show state changes for each turn (from JSON)
            show_larsson_rules: Show Larsson rule references
            show_metrics: Show scenario metrics at the end
            show_engine_state: Show actual engine state after each turn
            trace_recorder: Optional trace recorder to capture structured state snapshots
        """
        self.scenario = scenario
        self.controller = controller or ExecutionController(mode=ExecutionMode.AUTO)
        self.console = console or Console()
        self.nlg_mode = nlg_mode
        self.show_explanations = show_explanations
        self.show_state_changes = show_state_changes
        self.show_larsson_rules = show_larsson_rules
        self.show_metrics = show_metrics
        self.show_engine_state = show_engine_state
        self.trace_recorder = trace_recorder

        # Detect domain from scenario metadata
        domain_name: str = getattr(self.scenario.metadata, "domain", "nda_drafting")
        if domain_name == "legal_consultation":
            self.domain = get_legal_domain()
        else:
            self.domain = get_nda_domain()

        # Initialize NLG engine conditionally (only if needed)
        self.nlg_engine: NLGEngine | None = None
        if self.nlg_mode != "off":
            from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig

            config = NLGEngineConfig(
                default_strategy="llm",
                use_plan_awareness=True,
                use_domain_descriptions=True,
                verbose_logging=False,
                use_structured_output=True,
            )
            self.nlg_engine = NLGEngine(config)

        # Initialize Real Dialogue Engine
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_action_integration_rules():
            rules.add_rule(rule)
        for rule in create_negotiation_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_action_selection_rules():
            rules.add_rule(rule)
        for rule in create_negotiation_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        self.orchestrator = DemoDialogueOrchestrator(
            agent_id="system",
            rules=rules,
            nlg_engine=self.nlg_engine,
        )
        # Make domain available for action execution fallback
        self.orchestrator.information_state.private.beliefs["domain_model"] = self.domain

    @property
    def state(self) -> InformationState:
        """Convenience accessor for the current InformationState."""
        return self.orchestrator.information_state

    def run(self) -> None:
        """Run the complete scenario.

        Displays:
        1. Banner with scenario metadata
        2. Each dialogue turn with formatting
        3. Final summary and metrics
        """
        self._display_banner()
        self.controller.wait_at_banner()

        for turn in self.scenario.turns:
            self._display_turn(turn)
            self.controller.wait_between_turns()

        self._display_summary()
        self.controller.wait_at_end()
        if self.trace_recorder is not None:
            self.trace_recorder.flush()

    def _display_banner(self) -> None:
        """Display scenario banner with metadata."""
        # Title panel
        title_text = Text(self.scenario.title, style="bold cyan", justify="center")
        self.console.print(Panel(title_text, border_style="cyan"))

        # Metadata
        self.console.print(f"\n[bold]Description:[/bold] {self.scenario.metadata.description}")
        self.console.print(
            f"\n[bold yellow]Business Value:[/bold yellow]\n"
            f"{self.scenario.metadata.business_narrative}"
        )

        # NLG mode indicator
        if self.nlg_mode != "off":
            nlg_emoji = {"compare": "🔄", "replace": "🤖"}.get(self.nlg_mode, "")
            nlg_label = {"compare": "NLG Comparison", "replace": "NLG Alternative (scripted used)"}[
                self.nlg_mode
            ]
            self.console.print(f"\n[bold magenta]{nlg_emoji} {nlg_label}[/bold magenta]")

        # Larsson algorithms
        if self.scenario.metadata.larsson_algorithms:
            self.console.print("\n[bold green]Larsson Algorithms:[/bold green]")
            for algo in self.scenario.metadata.larsson_algorithms:
                self.console.print(f"  • {algo}")

        # Expected outcomes
        if self.scenario.metadata.expected_outcomes:
            self.console.print("\n[bold magenta]Expected Outcomes:[/bold magenta]")
            for key, value in self.scenario.metadata.expected_outcomes.items():
                formatted_key = key.replace("_", " ").title()
                self.console.print(f"  • {formatted_key}: {value}")

        # Execution mode
        mode_text = {
            ExecutionMode.STEP: "⏸️  Manual mode: Press Enter to advance",
            ExecutionMode.AUTO: "▶️  Auto mode: Playing automatically",
            ExecutionMode.REPLAY: "🔄 Replay mode: Playing back scenario",
        }
        self.console.print(f"\n[dim]{mode_text.get(self.controller.mode, '')}[/dim]\n")

    def _display_turn(self, turn: ScenarioTurn) -> None:
        """Display and execute a single dialogue turn through the engine.

        Args:
            turn: Turn to display and execute
        """
        # REAL ENGINE LOGIC: Process through Larsson engine
        if turn.speaker == "user":
            # 1. Mock NLU: Create DialogueMove(s) from JSON
            user_moves = self._create_user_dialogue_move(turn)
            if not isinstance(user_moves, list):
                user_moves = [user_moves]

            # 2-3. Integrate and select via orchestrator (Larsson cycle)
            self.orchestrator.process_user_turn(user_moves)

        elif turn.speaker == "system":
            # Ensure engine has prepared a system move
            engine_move = self.orchestrator.ensure_system_move()
            if engine_move is None:
                # Fall back to the scripted move to keep the dialogue advancing
                fallback_move = DialogueMove(
                    move_type=turn.move_type, content=turn.utterance, speaker="system"
                )
                self.console.print(
                    "[yellow]⚠️  Engine had no system move; using scripted turn[/yellow]"
                )
                engine_move = self.orchestrator.use_scripted_system_move(fallback_move)

        # Determine speaker styling
        if turn.speaker == "user":
            speaker_emoji = "👤"
            speaker_label = "USER"
            speaker_style = "bold blue"
            border_style = "blue"
        else:
            speaker_emoji = "🤖"
            speaker_label = "SYSTEM"
            speaker_style = "bold green"
            border_style = "green"

        # Get actual move type from engine for system turns
        move_type = turn.move_type
        if turn.speaker == "system" and self.orchestrator.pending_system_move:
            move_type = self.orchestrator.pending_system_move.move_type

        # Turn header
        header = Text()
        header.append(f"{speaker_emoji} {speaker_label} ", style=speaker_style)
        header.append(f"[Turn {turn.turn}]", style="dim")
        header.append(f" • {move_type}", style="italic")

        # Build panel content
        content_parts: list[Text] = []

        # Generate utterance for system turns (engine-driven)
        generated_system_text = None
        if turn.speaker == "system":
            engine_move = self.orchestrator.pending_system_move
            if engine_move:
                generated_system_text = self._generate_system_text(engine_move)

        # Display utterances based on speaker and mode
        if turn.speaker == "user":
            # User turns: always show scripted
            utterance_text = Text(f'"{turn.utterance}"', style="white")
            content_parts.append(utterance_text)

        elif self.nlg_mode == "compare":
            # Compare mode: show both scripted and NLG
            content_parts.append(Text("📜 SCRIPTED (Gold Standard):", style="bold yellow"))
            content_parts.append(Text(f'   "{turn.utterance}"', style="yellow"))
            content_parts.append(Text())  # Blank line

            if generated_system_text:
                content_parts.append(Text("🤖 ENGINE OUTPUT:", style="bold green"))
                content_parts.append(Text(f'   "{generated_system_text}"', style="green"))
                content_parts.append(Text())

                # Semantic similarity comparison
                comparison = self._compare_semantic_similarity(
                    turn.utterance, generated_system_text
                )
                similarity = comparison["similarity"]
                confidence = comparison["confidence"]
                explanation = comparison["explanation"]

                # Display comparison result with color coding
                if similarity == "equivalent":
                    icon = "✅"
                    sim_style = "bold green"
                elif similarity == "similar":
                    icon = "✓"
                    sim_style = "bold yellow"
                elif similarity == "different":
                    icon = "⚠️"
                    sim_style = "bold red"
                else:  # error
                    icon = "❌"
                    sim_style = "bold red"

                content_parts.append(
                    Text(
                        f"{icon} SIMILARITY: {similarity.upper()} (confidence: {confidence})",
                        style=sim_style,
                    )
                )
                content_parts.append(Text(f"   {explanation}", style="dim"))
            else:
                content_parts.append(Text("🤖 ENGINE OUTPUT: (generation failed)", style="red"))

        elif self.nlg_mode == "replace":
            # Replace mode: still advance and display with scripted text; show NLG as alternative
            content_parts.append(Text("📜 SCRIPTED (Used for flow):", style="bold yellow"))
            content_parts.append(Text(f'   "{turn.utterance}"', style="yellow"))
            content_parts.append(Text())  # Blank line

            if generated_system_text:
                content_parts.append(Text("🤖 NLG ALTERNATIVE:", style="bold green"))
                content_parts.append(Text(f'   "{generated_system_text}"', style="green"))
            else:
                content_parts.append(Text("🤖 NLG ALTERNATIVE: (generation failed)", style="red"))

        else:  # nlg_mode == "off"
            # Off mode: show scripted text for system, but engine still runs
            utterance_text = Text(f'"{turn.utterance}"', style="white")
            content_parts.append(utterance_text)

        # Business explanation
        if self.show_explanations and turn.business_explanation:
            content_parts.append(Text())  # Blank line
            content_parts.append(Text("💡 Business: ", style="bold yellow"))
            content_parts.append(Text(turn.business_explanation, style="yellow"))

        # Larsson rule
        if self.show_larsson_rules and turn.larsson_rule:
            content_parts.append(Text())
            content_parts.append(Text("📚 Larsson: ", style="bold cyan"))
            content_parts.append(Text(turn.larsson_rule, style="cyan"))

        # State changes (from JSON - not real engine state)
        if self.show_state_changes and turn.state_changes:
            content_parts.append(Text())
            content_parts.append(Text("🔄 Expected State Changes:", style="bold magenta"))
            for key, value in turn.state_changes.items():
                formatted_key = key.replace("_", " ").title()
                content_parts.append(Text(f"  • {formatted_key}: {value}", style="magenta"))

        # Engine state (actual state from running engine)
        if self.show_engine_state:
            content_parts.append(Text())
            content_parts.append(Text("🔍 Real Engine State:", style="bold cyan"))
            top_qud = self.state.shared.top_qud()
            content_parts.append(
                Text(f"  • Top QUD: {top_qud if top_qud else 'None'}", style="cyan")
            )
            content_parts.append(
                Text(f"  • Commitments: {len(self.state.shared.commitments)}", style="cyan")
            )
            if self.state.shared.commitments:
                recent_comms = list(self.state.shared.commitments)[-2:]
                for comm in recent_comms:
                    content_parts.append(Text(f"    - {comm}", style="dim cyan"))
            if self.state.private.plan:
                top_plan = self.state.private.plan[-1]
                agenda_len = len(self.state.private.agenda)
                plan_text = f"{top_plan.plan_type}({top_plan.content})"
                content_parts.append(
                    Text(
                        f"  • Plan: {plan_text} (Agenda: {agenda_len})",
                        style="cyan",
                    )
                )

        # Payoff indicator
        if turn.is_payoff:
            content_parts.append(Text())
            content_parts.append(Text("⭐ High-Value Output", style="bold yellow on black"))

        # Combine content
        panel_content = Text()
        for i, part in enumerate(content_parts):
            if i > 0 and part.plain == "":
                panel_content.append("\n")
            else:
                panel_content.append(part)
                if i < len(content_parts) - 1:
                    panel_content.append("\n")

        # Display panel
        self.console.print(
            Panel(
                panel_content,
                title=header,
                border_style=border_style,
                padding=(1, 2),
            )
        )

        # After presentation, integrate the system move so state reflects the turn
        if turn.speaker == "system":
            self.orchestrator.complete_system_turn()

        self._apply_declared_state_changes(turn)
        self._record_trace(turn)
        if self.show_state_changes:
            self._verify_state_changes(turn)

    def _display_summary(self) -> None:
        """Display scenario summary and metrics."""
        self.console.print("\n" + "═" * 80 + "\n")
        self.console.print("[bold green]✓ Scenario Complete[/bold green]\n")

        # Statistics
        stats_table = Table(show_header=False, box=None, padding=(0, 2))
        stats_table.add_column("Metric", style="bold")
        stats_table.add_column("Value", style="cyan")

        stats_table.add_row("Total Turns", str(self.scenario.total_turns))
        stats_table.add_row("User Turns", str(len(self.scenario.user_turns)))
        stats_table.add_row("System Turns", str(len(self.scenario.system_turns)))
        stats_table.add_row("Payoff Turns", str(len(self.scenario.payoff_turns)))

        self.console.print(stats_table)

        # Quality metrics
        if self.show_metrics and self.scenario.metadata.metrics:
            self.console.print("\n[bold yellow]Quality Metrics:[/bold yellow]")
            for key, value in self.scenario.metadata.metrics.items():
                formatted_key = key.replace("_", " ").title()
                self.console.print(f"  • {formatted_key}: {value}")

        self.console.print()

    def _record_trace(self, turn: ScenarioTurn) -> None:
        """Capture a structured state trace for the current turn."""
        if self.trace_recorder is None:
            return

        self.trace_recorder.record(
            turn=turn.turn,
            speaker=turn.speaker,
            move_type=turn.move_type,
            state=self.state,
            pending_system_move=self.orchestrator.pending_system_move,
            expected_state_changes=turn.state_changes,
        )

    def _apply_declared_state_changes(self, turn: ScenarioTurn) -> None:
        """Apply non-engine side effects declared in scenario state_changes.

        Used for extensions like RAG grounding evidence that Larsson doesn't cover
        but scenarios want to track.
        """
        if not turn.state_changes:
            return

        state_changes = turn.state_changes
        # Capture RAG evidence in private beliefs for grounding transparency
        rag_metadata = state_changes.get("rag_metadata") or state_changes.get("rag_query_executed")
        if rag_metadata is not None:
            self.state.private.beliefs.setdefault("rag_evidence", []).append(rag_metadata)

        # Enqueue referenced actions for execution (doc prep/revision)
        enqueue_actions = state_changes.get("enqueue_actions")
        if enqueue_actions:
            domain_actions = get_doc_actions()
            for action_spec in enqueue_actions:
                name = action_spec.get("name")
                if not name or name not in domain_actions:
                    continue
                template = domain_actions[name]
                action_instance = Action(
                    action_type=template.action_type,
                    name=template.name,
                    parameters={**template.parameters, **action_spec.get("parameters", {})},
                    preconditions=template.preconditions,
                    postconditions=template.postconditions,
                    requires_confirmation=template.requires_confirmation,
                    metadata=action_spec.get("metadata", {}),
                )
                self.state.private.actions.append(action_instance)

    def _verify_state_changes(self, turn: ScenarioTurn) -> None:
        """Compare expected state changes from the scenario with the actual engine state."""
        expected = turn.state_changes or {}
        if not expected:
            return

        qud_stack = [str(q) for q in self.state.shared.qud]
        commitments = self.state.shared.commitments
        warnings: list[str] = []

        expected_commitments = expected.get("commitments_added") or expected.get("commitment_added")
        if expected_commitments:
            if isinstance(expected_commitments, str):
                expected_commitments = [expected_commitments]
            missing = [c for c in expected_commitments if c not in commitments]
            if missing:
                warnings.append(f"Missing commitments: {', '.join(missing)}")

        qud_pushed = expected.get("qud_pushed")
        if qud_pushed and (not qud_stack or qud_stack[-1] != qud_pushed):
            warnings.append(
                f"Expected QUD top '{qud_pushed}', found '{qud_stack[-1] if qud_stack else 'None'}'"
            )

        qud_popped = expected.get("qud_popped")
        if qud_popped and qud_popped in qud_stack:
            warnings.append(f"Expected QUD '{qud_popped}' to be popped but it remains on stack")

        if warnings:
            self.console.print(
                f"[yellow]⚠️ State mismatch (turn {turn.turn}):[/yellow] " + " | ".join(warnings)
            )

    def _create_user_dialogue_move(self, turn: ScenarioTurn) -> DialogueMove | list[DialogueMove]:
        """Create DialogueMove(s) for USER turns (Mocked NLU).

        This converts the JSON turn data into DialogueMove objects that
        the engine can process. This is NOT real NLU - it's mocking the
        interpretation phase for demo purposes.

        Args:
            turn: User turn from scenario JSON

        Returns:
            Single DialogueMove or list of moves (for composite moves)
        """
        from ibdm.core.actions import Proposition
        from ibdm.core.answers import Answer
        from ibdm.core.moves import DialogueMove
        from ibdm.core.questions import WhQuestion

        move_type_str = turn.move_type
        speaker = "user"
        utterance = turn.utterance
        state_changes = turn.state_changes

        moves: list[DialogueMove] = []

        # Handle composite moves (e.g., "request + volunteer_info")
        parts = [p.strip() for p in move_type_str.split("+")]
        primary_type = parts[0]
        has_volunteer = "volunteer_info" in parts

        # 1. Create Primary Move
        if primary_type == "answer":
            top_qud = self.state.shared.top_qud()
            content = Answer(content=utterance, question_ref=top_qud)
            moves.append(DialogueMove(move_type="answer", content=content, speaker=speaker))

        elif primary_type in ["request", "command"]:
            moves.append(DialogueMove(move_type=primary_type, content=utterance, speaker=speaker))

        elif primary_type == "clarification_question":
            predicate = "clarify"
            args = {"utterance": utterance}
            if "mutual" in utterance.lower():
                args["topic"] = "mutual_nda"
            elif "options" in utterance.lower():
                args["topic"] = "jurisdiction_options"
            content = WhQuestion(predicate=predicate, variable="x", constraints=args)
            moves.append(DialogueMove(move_type="ask", content=content, speaker=speaker))

        elif primary_type == "off_topic_question":
            predicate = "non_compete_clause"
            if "long" in utterance.lower():
                predicate = "timeline"
            content = WhQuestion(predicate=predicate, variable="x")
            moves.append(DialogueMove(move_type="ask", content=content, speaker=speaker))

        elif primary_type == "confirm":
            top_qud = self.state.shared.top_qud()
            content = Answer(content="yes", question_ref=top_qud)
            moves.append(DialogueMove(move_type="answer", content=content, speaker=speaker))

        elif primary_type == "acknowledge":
            moves.append(DialogueMove(move_type="ack", content=utterance, speaker=speaker))

        else:
            moves.append(DialogueMove(move_type=primary_type, content=utterance, speaker=speaker))

        # 2. Handle Volunteered Info (Assert moves)
        if has_volunteer:
            commitments = state_changes.get("commitments_added", [])
            for comm_str in commitments:
                if "(" in comm_str and ")" in comm_str:
                    pred = comm_str.split("(")[0]
                    args_str = comm_str.split("(")[1].rstrip(")")
                    # Parse arguments: "key=val" or "key=val1, val2, val3"
                    # Check if it's a simple key=value format
                    if "=" in args_str and args_str.count("=") == 1:
                        # Single key=value pair (value might contain commas)
                        key, val = args_str.split("=", 1)
                        args = {key.strip(): val.strip()}
                    else:
                        # More complex format or just a value - wrap it
                        args = {"value": args_str}
                    prop = Proposition(predicate=pred, arguments=args)
                    moves.append(DialogueMove(move_type="assert", content=prop, speaker=speaker))
                else:
                    moves.append(
                        DialogueMove(move_type="assert", content=comm_str, speaker=speaker)
                    )

        return (
            moves
            if len(moves) > 1
            else (
                moves[0]
                if moves
                else DialogueMove(move_type="unknown", content=utterance, speaker=speaker)
            )
        )

    def _generate_system_text(self, engine_move: DialogueMove) -> str:
        """Produce utterance text for the pending system move.

        Args:
            engine_move: System move from engine

        Returns:
            Generated text (or empty string if generation fails)
        """
        generated_text = ""

        if self.nlg_engine is not None and self.nlg_mode != "off":
            try:
                nlg_result = self.orchestrator.generate_pending_system_utterance()
                if nlg_result:
                    generated_text = nlg_result.utterance_text
            except Exception:
                # Silently fail - error handling in display
                generated_text = ""

        if not generated_text:
            try:
                generated_text = self.orchestrator.generate_from_rules(engine_move)
            except Exception:
                generated_text = ""

        return generated_text or ""

    def _compare_semantic_similarity(self, scripted: str, nlg_generated: str) -> dict[str, Any]:
        """Compare semantic similarity between scripted and NLG-generated utterances.

        Args:
            scripted: Gold standard scripted text
            nlg_generated: NLG-generated text

        Returns:
            Dictionary with similarity, confidence, and explanation
        """
        try:
            import litellm

            prompt = f"""You are evaluating alternative lines for a dialogue agent.
Focus on whether the alternative would push the dialogue off track.
Treat the utterances as equivalent unless the change would materially
alter commitments, reopen/resolve issues differently, or steer to a new plan branch.

SCRIPTED (Gold Standard):
"{scripted}"

ENGINE OUTPUT:
"{nlg_generated}"

Assess conversational similarity and respond in JSON format:
{{
  "similarity": "equivalent|similar|different",
  "confidence": "high|medium|low",
  "explanation": "Brief explanation (1-2 sentences)"
}}

Guidelines (err on "equivalent"/"similar" unless conversation derails):
- "equivalent": Same downstream effect. Differences are style, tone, or minor
  optional details. Default to this unless you see meaningful divergence.
- "similar": Small scope or ordering differences but still keeps the dialogue
  on the intended track.
- "different": Only choose this if the generated text would send the
  conversation off beam (e.g., commits to new facts, drops required info,
  or advances a different plan)."""

            response = litellm.completion(  # type: ignore[reportUnknownMemberType]
                model="claude-haiku-4-5-20251001",
                messages=[{"role": "user", "content": prompt}],
                api_key=os.getenv("IBDM_API_KEY"),
                temperature=0.0,
                max_tokens=200,
            )

            response_text = response.choices[0].message.content  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            if not response_text:
                raise ValueError("Empty response from LLM")

            try:
                result = json.loads(response_text)  # type: ignore[reportUnknownArgumentType]
                if not all(k in result for k in ["similarity", "confidence", "explanation"]):
                    raise ValueError("Missing required fields in LLM response")
                return result
            except json.JSONDecodeError:
                # Fallback: extract from text
                similarity = "similar"
                text_content = str(response_text)  # type: ignore[reportUnknownArgumentType]
                if "equivalent" in text_content.lower():
                    similarity = "equivalent"
                elif "different" in text_content.lower():
                    similarity = "different"
                return {
                    "similarity": similarity,
                    "confidence": "medium",
                    "explanation": text_content[:100],
                }

        except Exception as exc:
            return {
                "similarity": "error",
                "confidence": "low",
                "explanation": f"Comparison failed: {str(exc)[:50]}",
                "error": str(exc),
            }


def run_scenario(
    scenario_id: str,
    mode: ExecutionMode = ExecutionMode.AUTO,
    auto_delay: float = 2.0,
    nlg_mode: str = "off",
    show_explanations: bool = True,
    show_state_changes: bool = True,
    show_larsson_rules: bool = True,
    show_metrics: bool = True,
    show_engine_state: bool = False,
    trace_path: str | None = None,
) -> None:
    """Convenience function to run a scenario by ID.

    Args:
        scenario_id: Scenario identifier
        mode: Execution mode (STEP, AUTO, or REPLAY)
        auto_delay: Delay between turns in AUTO mode (seconds)
        nlg_mode: NLG mode - "off" (scripted), "compare" (both), "replace" (NLG only)
        show_explanations: Show business explanations
        show_state_changes: Show state changes (from JSON)
        show_larsson_rules: Show Larsson rule references
        show_metrics: Show scenario metrics
        show_engine_state: Show actual engine state after each turn
        trace_path: Optional path to write structured state trace (JSONL)

    Examples:
        >>> # Run with defaults (scripted playback)
        >>> run_scenario("nda_basic")

        >>> # Run with NLG comparison
        >>> run_scenario("nda_basic", nlg_mode="compare")

        >>> # Run in step mode with engine state
        >>> run_scenario("nda_basic", mode=ExecutionMode.STEP, show_engine_state=True)

        >>> # Run with NLG only (no scripted text)
        >>> run_scenario("nda_basic", nlg_mode="replace")
    """
    # Use the shared loader helper to keep discovery consistent.
    scenario = load_scenario(scenario_id)

    controller = ExecutionController(
        mode=mode,
        auto_delay=auto_delay,
    )

    trace_recorder = StateTraceRecorder(Path(trace_path)) if trace_path else None

    runner = ScenarioRunner(
        scenario=scenario,
        controller=controller,
        nlg_mode=nlg_mode,
        show_explanations=show_explanations,
        show_state_changes=show_state_changes,
        show_larsson_rules=show_larsson_rules,
        show_metrics=show_metrics,
        show_engine_state=show_engine_state,
        trace_recorder=trace_recorder,
    )

    runner.run()
