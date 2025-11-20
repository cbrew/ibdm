#!/usr/bin/env python3
"""Business Demo Launcher for IBDM.

One-command demo script that runs pre-configured dialogue scenarios
with professional console output (no HTML reports).

ARCHITECTURAL NOTE - Mocked NLU Only:
    This demo injects semantic representations for USER turns from scenario JSON
    and converts them to DialogueMove objects. This is NOT parsing natural language
    text. SYSTEM turns are driven entirely by the Larsson dialogue engine using
    the real rule set.

    What the demo shows:  MEANING → TEXT (NLG)
    Future work:          TEXT → MEANING (NLU)

    Inferring DialogueMoves from natural language utterances would be NLU work,
    which is explicitly out of scope for this demo.

Usage:
    python scripts/run_business_demo.py                    # Run default (nda_basic)
    python scripts/run_business_demo.py --scenario nda_volunteer
    python scripts/run_business_demo.py --all              # Run all scenarios
    python scripts/run_business_demo.py --nlg-mode compare # Show NLG comparison
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Required imports - fail fast if not available
from ibdm.core import DialogueMove, InformationState
from ibdm.demo import ExecutionController, ExecutionMode
from ibdm.demo.orchestrator import DemoDialogueOrchestrator
from ibdm.domains.legal_domain import get_legal_domain
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_selection_rules,
)
from ibdm.services.nda_generator import NDAGenerator, NDAParameters


class BusinessDemo:
    """Run pre-scripted business demonstration scenarios."""

    def __init__(
        self,
        scenario_path: Path,
        verbose: bool = True,
        auto_advance: bool | None = None,
        execution_mode: ExecutionMode | str | None = None,
        nlg_mode: str = "off",
    ):
        """Initialize business demo.

        Args:
            scenario_path: Path to scenario JSON file
            verbose: Whether to print detailed output
            auto_advance: DEPRECATED - use execution_mode instead.
                If True, uses AUTO mode; if False, uses STEP mode
            execution_mode: Execution mode - STEP (manual), AUTO (automatic),
                or REPLAY (playback)
            nlg_mode: NLG mode - "off" (scripted only), "compare" (both),
                or "replace" (NLG only)
        """
        self.scenario_path = scenario_path
        self.verbose = verbose
        self.nlg_mode = nlg_mode

        # Handle backward compatibility: auto_advance -> execution_mode
        if execution_mode is not None:
            # New API: execution_mode parameter
            if isinstance(execution_mode, str):
                self.execution_mode = ExecutionMode(execution_mode)
            else:
                self.execution_mode = execution_mode
        elif auto_advance is not None:
            # Old API: auto_advance parameter (backward compatibility)
            self.execution_mode = ExecutionMode.AUTO if auto_advance else ExecutionMode.STEP
        else:
            # Default: AUTO mode
            self.execution_mode = ExecutionMode.AUTO

        # Create execution controller
        self.controller = ExecutionController(
            mode=self.execution_mode,
            auto_delay=2.0,
            banner_delay=3.0,
        )

        # Load scenario
        self.scenario = json.loads(scenario_path.read_text())

        # Domain model - detect from scenario or default to NDA
        domain_name = self.scenario.get("domain", "nda_drafting")
        if domain_name == "legal_consultation":
            self.domain = get_legal_domain()
        else:
            self.domain = get_nda_domain()

        # Initialize NLG engine conditionally (only if needed)
        self.nlg_engine = None
        if self.nlg_mode != "off":
            from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig

            config = NLGEngineConfig(
                default_strategy="llm",  # Use LLM strategy to verify it's working
                use_plan_awareness=True,
                use_domain_descriptions=True,
                verbose_logging=False,  # Keep logging quiet in demo mode
                use_structured_output=True,  # Enable structured output with user/system separation
            )
            self.nlg_engine = NLGEngine(config)
            if self.verbose:
                print(
                    f"✓ NLG engine initialized "
                    f"(mode: {nlg_mode}, strategy: llm, structured_output: enabled)"
                )

        # Initialize Real Dialogue Engine
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        self.orchestrator = DemoDialogueOrchestrator(
            agent_id="system",
            rules=rules,
            nlg_engine=self.nlg_engine,
        )
        if self.verbose:
            print("✓ Larsson Dialogue Orchestrator initialized (integrate→select→generate)")

    @property
    def state(self) -> InformationState:
        """Convenience accessor for the current InformationState."""

        return self.orchestrator.information_state

    def print_banner(self) -> None:
        """Print demo banner."""
        print("\n" + "=" * 80)
        print("IBDM BUSINESS DEMONSTRATION")
        print("=" * 80)
        print(f"\nScenario: {self.scenario['title']}")
        print(f"Description: {self.scenario['description']}")
        print("\n" + "-" * 80)
        print("BUSINESS VALUE:")
        print(self.scenario["business_narrative"])
        print("-" * 80 + "\n")

        if self.execution_mode == ExecutionMode.AUTO:
            print("⏵ Auto-advance mode: Dialogue will play automatically")
            print("  (Press Ctrl+C to pause)\n")
        elif self.execution_mode == ExecutionMode.STEP:
            print("⏵ Manual mode: Press Enter to advance each turn\n")
        elif self.execution_mode == ExecutionMode.REPLAY:
            print("⏵ Replay mode: Playing back saved scenario\n")

    def print_turn(self, turn_data: dict[str, Any], turn_index: int) -> None:
        """Print a single turn with formatting.

        Args:
            turn_data: Turn data from scenario JSON
            turn_index: Index of turn in scenario
        """
        turn_num = turn_data["turn"]
        speaker = turn_data["speaker"]
        utterance = turn_data["utterance"]
        move_type = turn_data.get("move_type", "")
        if speaker == "system" and self.orchestrator.pending_system_move:
            move_type = self.orchestrator.pending_system_move.move_type

        # REAL ENGINE LOGIC: Update state using Larsson engine
        if speaker == "user":
            # 1. Mock NLU: Create DialogueMove(s) from JSON
            user_moves = self._create_user_dialogue_move(turn_data)
            if not isinstance(user_moves, list):
                user_moves = [user_moves]

            if self.verbose and len(user_moves) > 1:
                for move in user_moves:
                    print(f"   → Integrating sub-move: {move.move_type}")

            # 2-3. Integrate and select via orchestrator (Larsson cycle)
            self.orchestrator.process_user_turn(user_moves)

        elif speaker == "system":
            engine_move = self.orchestrator.ensure_system_move()
            if engine_move is None:
                if self.verbose:
                    print("   ⚠️ No pending system move from engine; skipping scripted system turn")
                return

            if self.verbose:
                print(f"   ✓ Engine predicted: {engine_move.move_type}")

        # Format speaker name
        if speaker == "user":
            speaker_display = "👤 USER"
            color_code = "\033[94m"  # Blue
        else:
            speaker_display = "🤖 SYSTEM"
            color_code = "\033[92m"  # Green

        reset_code = "\033[0m"

        # Print turn header
        print(f"\n{'─' * 80}")
        print(f"{color_code}Turn {turn_num}: {speaker_display} [{move_type}]{reset_code}")
        print(f"{'─' * 80}")

        # Generate utterance for system turns (engine-driven)
        generated_system_text = None
        if speaker == "system":
            engine_move = self.orchestrator.pending_system_move
            if engine_move:
                generated_system_text = self._generate_system_text(engine_move)

        # Display utterances based on mode
        if speaker == "user":
            # User turns: always show scripted
            print(f"{utterance}")

        elif self.nlg_mode == "compare":
            # Compare mode: show both scripted and NLG
            print("\n📜 SCRIPTED (Gold Standard):")
            print(f'   "{utterance}"')

            if generated_system_text:
                print("\n🤖 ENGINE OUTPUT:")
                print(f'   "{generated_system_text}"')

                # Semantic similarity comparison
                comparison = self._compare_semantic_similarity(utterance, generated_system_text)
                similarity = comparison["similarity"]
                confidence = comparison["confidence"]
                explanation = comparison["explanation"]

                # Display comparison result with color coding
                if similarity == "equivalent":
                    icon = "✅"
                    color = "\033[92m"  # Green
                elif similarity == "similar":
                    icon = "✓"
                    color = "\033[93m"  # Yellow
                elif similarity == "different":
                    icon = "⚠️"
                    color = "\033[91m"  # Red
                else:  # error
                    icon = "❌"
                    color = "\033[91m"  # Red

                reset = "\033[0m"
                print(
                    f"\n{color}{icon} SIMILARITY: {similarity.upper()} "
                    f"(confidence: {confidence}){reset}"
                )
                print(f"   {explanation}")
            else:
                print("\n🤖 ENGINE OUTPUT: (generation failed)")

        elif self.nlg_mode == "replace":
            # Replace mode: show NLG only (or fallback to scripted)
            if generated_system_text:
                print(f"{generated_system_text}")
            else:
                print("[No response generated]")

        else:  # speaker == "system" and nlg_mode == "off"
            print(
                f"{generated_system_text}" if generated_system_text else "[No response generated]"
            )

        # After presentation, integrate the system move so state reflects the turn
        if speaker == "system":
            self.orchestrator.complete_system_turn()

        # Print business explanation if verbose
        if self.verbose and "business_explanation" in turn_data:
            print(f"\n💡 {turn_data['business_explanation']}")

        # Print Larsson algorithm reference
        if self.verbose and "larsson_rule" in turn_data:
            print(f"📚 Larsson: {turn_data['larsson_rule']}")

        # VERIFICATION: Check if real engine state matches expectations
        # Print AFTER integration is complete for this turn
        if self.verbose:
            print("\n🔍 Real Engine State:")
            top_qud = self.state.shared.top_qud()
            print(f"   • Top QUD: {top_qud if top_qud else 'None'}")
            print(f"   • Commitments: {len(self.state.shared.commitments)}")
            if self.state.shared.commitments:
                # Show last few commitments for context
                recent_comms = list(self.state.shared.commitments)[-3:]
                for comm in recent_comms:
                    print(f"     - {comm}")
            if self.state.private.plan:
                top_plan = self.state.private.plan[-1]
                agenda_len = len(self.state.private.agenda)
                print(f"   • Plan: {top_plan.plan_type}({top_plan.content}) (Agenda: {agenda_len})")
            else:
                print("   • Plan: None")

    def run_scenario(self) -> dict[str, Any]:
        """Run the scenario and return metrics.

        Returns:
            Dictionary of metrics from the run
        """
        self.print_banner()

        # Wait for user to read banner
        self.controller.wait_at_banner()

        # Run each turn
        for i, turn in enumerate(self.scenario["turns"]):
            self.print_turn(turn, i)

            # Wait between turns (unless it's the last turn)
            if i < len(self.scenario["turns"]) - 1:
                self.controller.wait_between_turns()

        # Final summary
        self.print_summary()

        # Generate NDA if this is the comprehensive scenario
        if self.scenario_path.stem == "nda_comprehensive":
            self.generate_nda_document()

        # Return metrics
        return self.scenario.get("metrics", {})

    def print_summary(self) -> None:
        """Print final summary and metrics."""
        print("\n\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)

        print("\n📊 SCENARIO METRICS:")
        print("-" * 80)

        metrics = self.scenario.get("metrics", {})
        expected = self.scenario.get("expected_outcomes", {})

        # Print expected outcomes
        if expected:
            print("\nExpected Outcomes:")
            for key, value in expected.items():
                key_display = key.replace("_", " ").title()
                print(f"  • {key_display}: {value}")

        # Print metrics
        if metrics:
            print("\nActual Performance:")
            for key, value in metrics.items():
                key_display = key.replace("_", " ").title()
                print(f"  • {key_display}: {value}")

        # Print Larsson algorithms demonstrated
        print("\n📚 LARSSON ALGORITHMS DEMONSTRATED:")
        print("-" * 80)
        for i, algo in enumerate(self.scenario.get("larsson_algorithms", []), 1):
            print(f"{i}. {algo}")

        # Print business value
        if "business_value" in self.scenario:
            print("\n💼 BUSINESS VALUE:")
            print("-" * 80)
            print(self.scenario["business_value"])

        print("\n" + "=" * 80 + "\n")

    def generate_nda_document(self) -> None:
        """Generate NDA document from gathered information.

        This method is called automatically after nda_comprehensive scenario
        to demonstrate the complete workflow: dialogue → document generation.
        """
        print("\n" + "=" * 80)
        print("📝 NDA DOCUMENT GENERATION")
        print("=" * 80)
        print()

        # Extract commitments from final state
        commitments = self.state.shared.commitments

        if not commitments:
            print("⚠️  No commitments found in dialogue state. Skipping generation.")
            return

        print("📋 Extracting NDA parameters from dialogue state...")

        # Parse commitments to extract NDA parameters
        try:
            params = NDAParameters.from_commitments(commitments)
            print(f"   ✓ Parties: {', '.join(params.parties)}")
            print(f"   ✓ Type: {params.nda_type}")
            print(f"   ✓ Effective Date: {params.effective_date}")
            print(f"   ✓ Duration: {params.duration}")
            print(f"   ✓ Jurisdiction: {params.jurisdiction}")
            print()
        except Exception as e:
            print(f"   ✗ Failed to extract parameters: {e}")
            return

        # Initialize generator
        print("🤖 Initializing NDA Generator (Claude Sonnet 4.5)...")
        try:
            generator = NDAGenerator()
            print("   ✓ Generator ready")
            print()
        except ValueError as e:
            print(f"   ✗ Error: {e}")
            print()
            print("   ℹ️  Set IBDM_API_KEY to enable NDA generation")
            print("   ℹ️  Skipping document generation")
            return
        except Exception as e:
            print(f"   ✗ Unexpected error: {e}")
            return

        # Generate NDA
        print("📄 Generating NDA document (this may take 10-30 seconds)...")
        print()

        try:
            nda_text = generator.generate_nda(params)
            print("   ✓ NDA generated successfully!")
            print()
        except Exception as e:
            print(f"   ✗ Generation failed: {e}")
            print()
            print("   ℹ️  Continuing without document generation")
            return

        # Display preview
        print("=" * 80)
        print("GENERATED NDA PREVIEW")
        print("=" * 80)
        print()

        # Show first 30 lines
        lines = nda_text.split("\n")
        preview_lines = lines[:30]
        print("\n".join(preview_lines))

        if len(lines) > 30:
            print()
            print(f"... ({len(lines) - 30} more lines)")
        print()

        # Save to file
        output_dir = Path("demos/generated_documents")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario_name = self.scenario_path.stem
        output_file = output_dir / f"nda_{scenario_name}_{timestamp}.md"

        try:
            with open(output_file, "w") as f:
                f.write(f"# Generated NDA - {params.effective_date}\n\n")
                f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("**Model**: Claude Sonnet 4.5\n")
                f.write(f"**Source**: IBDM {scenario_name} scenario\n")
                f.write(f"**Dialogue Turns**: {len(self.scenario['turns'])}\n")
                f.write("\n---\n\n")
                f.write(nda_text)

            print("=" * 80)
            print("DOCUMENT SAVED")
            print("=" * 80)
            print()
            print(f"📄 Full NDA saved to: {output_file}")
            print(f"📊 Document: {len(lines)} lines, {len(nda_text)} characters")
            print()
            print("=" * 80)
            print()
            print("✓ Complete workflow demonstrated:")
            print("  1. Information gathering via IBDM dialogue")
            print("  2. State management and commitment tracking")
            print("  3. Parameter extraction from dialogue state")
            print("  4. Professional document generation via LLM")
            print()
            print("⚠️  NOTE: AI-generated legal content. Always have a licensed")
            print("   attorney review any legal documents before use.")
            print()

        except Exception as e:
            print(f"⚠️  Failed to save document: {e}")
            print()

    def _create_user_dialogue_move(
        self, turn_data: dict[str, Any]
    ) -> DialogueMove | list[DialogueMove]:
        """Create DialogueMove(s) for USER turns (Mocked NLU)."""
        from ibdm.core.actions import Proposition
        from ibdm.core.answers import Answer
        from ibdm.core.moves import DialogueMove
        from ibdm.core.questions import WhQuestion

        move_type_str = turn_data.get("move_type", "unknown")
        speaker = "user"
        utterance = turn_data.get("utterance", "")
        state_changes = turn_data.get("state_changes", {})

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
                    args = {"value": args_str}
                    prop = Proposition(predicate=pred, arguments=args)
                    moves.append(DialogueMove(move_type="assert", content=prop, speaker=speaker))
                else:
                    moves.append(
                        DialogueMove(move_type="assert", content=comm_str, speaker=speaker)
                    )

        confidence = turn_data.get("confidence")
        if confidence is not None:
            for move in moves:
                move.metadata["confidence"] = confidence

        return moves

    def _generate_system_text(self, engine_move: DialogueMove) -> str:
        """Produce utterance text for the pending system move."""
        generated_text = ""
        tried_llm = False

        if self.nlg_engine is not None and self.nlg_mode != "off":
            tried_llm = True
            try:
                nlg_result = self.orchestrator.generate_pending_system_utterance()
                if nlg_result:
                    generated_text = nlg_result.utterance_text
            except Exception as exc:
                if self.verbose:
                    print(f"\n❌ LLM NLG failed: {exc}")
                generated_text = ""

            if not generated_text and self.verbose:
                print("\n⚠️ LLM NLG unavailable, falling back to rule-based generation.")

        if not generated_text:
            try:
                generated_text = self.orchestrator.generate_from_rules(engine_move)
            except Exception as exc:
                if self.verbose:
                    suffix = " after LLM failure" if tried_llm else ""
                    print(f"\n❌ Generation rules failed{suffix}: {exc}")
                generated_text = ""

        return generated_text or ""

    def _compare_semantic_similarity(self, scripted: str, nlg_generated: str) -> dict[str, Any]:
        """Compare semantic similarity between scripted and NLG-generated utterances."""
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

            response = litellm.completion(
                model="claude-haiku-4-5-20251001",
                messages=[{"role": "user", "content": prompt}],
                api_key=os.getenv("IBDM_API_KEY"),
                temperature=0.0,
                max_tokens=200,
            )

            response_text = response.choices[0].message.content
            if not response_text:
                raise ValueError("Empty response from LLM")

            try:
                result = json.loads(response_text)
                if not all(k in result for k in ["similarity", "confidence", "explanation"]):
                    raise ValueError("Missing required fields in LLM response")
                return result
            except json.JSONDecodeError:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    f"LLM response not valid JSON, using text extraction: {response_text}"
                )
                similarity = "similar"
                if "equivalent" in response_text.lower():
                    similarity = "equivalent"
                elif "different" in response_text.lower():
                    similarity = "different"
                return {
                    "similarity": similarity,
                    "confidence": "medium",
                    "explanation": response_text[:100],
                }

        except Exception as exc:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Semantic similarity comparison failed: {exc}")
            return {
                "similarity": "error",
                "confidence": "low",
                "explanation": f"Comparison failed: {str(exc)[:50]}",
                "error": str(exc),
            }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run IBDM business demonstration scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--scenario",
        default="nda_basic",
        help=(
            "Scenario to run (nda_basic, nda_volunteer, nda_complex, "
            "nda_grounding, nda_comprehensive, legal_rag_basic)"
        ),
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios sequentially",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output (no business explanations)",
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="DEPRECATED: Use --mode step instead. Manual mode (press Enter to advance)",
    )
    parser.add_argument(
        "--mode",
        choices=["step", "auto", "replay"],
        help=(
            "Execution mode: 'step' (manual, press Enter), 'auto' (automatic delays), "
            "'replay' (fast playback). Default: auto (or step if --manual is used)"
        ),
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between turns in auto mode (seconds, default: 2.0)",
    )
    parser.add_argument(
        "--nlg-mode",
        choices=["off", "compare", "replace"],
        default="off",
        help=(
            "NLG mode: 'off' (scripted only, default), 'compare' (show both), 'replace' (NLG only)"
        ),
    )

    args = parser.parse_args()

    # Determine scenarios to run
    scenarios_dir = Path(__file__).parent.parent / "demos" / "scenarios"

    if args.all:
        scenario_files = [
            scenarios_dir / "nda_basic.json",
            scenarios_dir / "nda_volunteer.json",
            scenarios_dir / "nda_complex.json",
            scenarios_dir / "nda_grounding.json",
            scenarios_dir / "nda_comprehensive.json",
        ]
    else:
        scenario_file = scenarios_dir / f"{args.scenario}.json"
        if not scenario_file.exists():
            print(f"Error: Scenario file not found: {scenario_file}")
            print(f"\nAvailable scenarios in {scenarios_dir}:")
            for f in scenarios_dir.glob("*.json"):
                print(f"  - {f.stem}")
            return 1
        scenario_files = [scenario_file]

    # Determine execution mode (handle backward compatibility)
    if args.mode:
        execution_mode = args.mode
    elif args.manual:
        execution_mode = "step"
    else:
        execution_mode = "auto"

    # Run scenarios
    for scenario_file in scenario_files:
        demo = BusinessDemo(
            scenario_file,
            verbose=not args.quiet,
            execution_mode=execution_mode,
            nlg_mode=args.nlg_mode,
        )

        # Configure delay if specified
        if args.delay != 2.0:
            demo.controller.configure(auto_delay=args.delay)

        demo.run_scenario()

    print("\n✓ All demonstrations complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
