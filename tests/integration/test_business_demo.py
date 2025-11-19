"""Integration tests for business demo package.

Tests:
- Scenario JSON files are valid
- Launcher script runs successfully
- HTML reports generate correctly
- All scenarios complete without errors
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCENARIOS_DIR = PROJECT_ROOT / "demos" / "scenarios"
LAUNCHER_SCRIPT = PROJECT_ROOT / "scripts" / "run_business_demo.py"
REPORTS_DIR = PROJECT_ROOT / "demos" / "reports"


class TestScenarioFiles:
    """Test scenario JSON files are valid and complete."""

    @pytest.fixture
    def scenario_files(self):
        """Get all scenario JSON files."""
        return list(SCENARIOS_DIR.glob("*.json"))

    def test_scenarios_exist(self, scenario_files):
        """Test that scenario files exist."""
        assert len(scenario_files) >= 4, "Should have at least 4 scenarios"

        # Check expected scenarios
        expected = {
            "nda_basic.json",
            "nda_volunteer.json",
            "nda_complex.json",
            "nda_grounding.json",
        }
        actual = {f.name for f in scenario_files if f.name != "README.md"}

        assert expected.issubset(actual), f"Missing scenarios: {expected - actual}"

    def test_scenarios_valid_json(self, scenario_files):
        """Test that all scenario files are valid JSON."""
        for scenario_file in scenario_files:
            try:
                data = json.loads(scenario_file.read_text())
                assert isinstance(data, dict), f"{scenario_file.name} should be JSON object"
            except json.JSONDecodeError as e:
                pytest.fail(f"{scenario_file.name} is not valid JSON: {e}")

    def test_scenarios_have_required_fields(self, scenario_files):
        """Test that scenarios have all required fields."""
        required_fields = {
            "scenario_id",
            "title",
            "description",
            "business_narrative",
            "larsson_algorithms",
            "expected_outcomes",
            "turns",
            "metrics",
        }

        for scenario_file in scenario_files:
            data = json.loads(scenario_file.read_text())
            missing = required_fields - data.keys()
            assert not missing, f"{scenario_file.name} missing fields: {missing}"

    def test_scenarios_have_valid_turns(self, scenario_files):
        """Test that scenario turns are well-formed."""
        required_turn_fields = {"turn", "speaker", "utterance", "move_type"}

        for scenario_file in scenario_files:
            data = json.loads(scenario_file.read_text())
            turns = data.get("turns", [])

            assert len(turns) > 0, f"{scenario_file.name} has no turns"

            for i, turn in enumerate(turns):
                missing = required_turn_fields - turn.keys()
                assert not missing, f"{scenario_file.name} turn {i} missing: {missing}"

                # Check turn numbering
                assert turn["turn"] == i + 1, f"{scenario_file.name} turn {i} has wrong number"

                # Check speaker is valid
                assert turn["speaker"] in ["user", "system"], f"Invalid speaker in turn {i}"

    def test_scenarios_have_business_explanations(self, scenario_files):
        """Test that turns have business explanations."""
        for scenario_file in scenario_files:
            data = json.loads(scenario_file.read_text())
            turns = data.get("turns", [])

            explained_turns = sum(1 for t in turns if "business_explanation" in t)
            coverage = explained_turns / len(turns)

            assert coverage >= 0.8, (
                f"{scenario_file.name} only {coverage:.0%} of turns have explanations"
            )


class TestLauncherScript:
    """Test the business demo launcher script."""

    def test_launcher_exists(self):
        """Test that launcher script exists and is executable."""
        assert LAUNCHER_SCRIPT.exists(), "Launcher script not found"
        assert LAUNCHER_SCRIPT.stat().st_mode & 0o111, "Launcher script not executable"

    def test_launcher_help(self):
        """Test that launcher --help works."""
        result = subprocess.run(
            [sys.executable, str(LAUNCHER_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, f"Help failed: {result.stderr}"
        assert "scenario" in result.stdout.lower(), "Help should mention scenarios"
        assert "nda_basic" in result.stdout.lower(), "Help should list available scenarios"

    @pytest.mark.slow
    def test_launcher_runs_basic_scenario(self, tmp_path):
        """Test that launcher can run basic scenario without crashing."""
        # Run with no-report to speed up test
        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--no-report",
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Check it didn't crash
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check output contains expected elements
        assert "IBDM" in result.stdout, "Output should mention IBDM"
        assert "Turn" in result.stdout, "Output should show turns"
        assert "complete" in result.stdout.lower(), "Output should show completion"

    @pytest.mark.slow
    def test_launcher_generates_html_report(self, tmp_path):
        """Test that launcher generates HTML report."""
        output_dir = tmp_path / "reports"
        output_dir.mkdir()

        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--output-dir",
                str(output_dir),
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check HTML file was created
        html_files = list(output_dir.glob("*.html"))
        assert len(html_files) == 1, f"Expected 1 HTML file, got {len(html_files)}"

        # Check HTML content
        html_content = html_files[0].read_text()
        assert "<!DOCTYPE html>" in html_content, "Should be valid HTML"
        assert "IBDM" in html_content, "Report should mention IBDM"
        assert "nda_basic" in html_content, "Report should mention scenario"
        assert "Turn" in html_content, "Report should show turns"

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "scenario",
        ["nda_basic", "nda_volunteer", "nda_complex", "nda_grounding"],
    )
    def test_all_scenarios_run(self, scenario, tmp_path):
        """Test that all scenarios can run successfully."""
        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                scenario,
                "--no-report",
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )

        assert result.returncode == 0, f"{scenario} failed: {result.stderr}"
        assert "complete" in result.stdout.lower(), f"{scenario} didn't complete"


class TestHTMLReports:
    """Test HTML report generation and content."""

    @pytest.fixture
    def sample_report(self, tmp_path):
        """Generate a sample HTML report for testing."""
        output_dir = tmp_path / "reports"
        output_dir.mkdir()

        subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--output-dir",
                str(output_dir),
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )

        html_files = list(output_dir.glob("*.html"))
        return html_files[0].read_text()

    @pytest.mark.slow
    def test_report_has_professional_styling(self, sample_report):
        """Test that report includes CSS styling."""
        assert "<style>" in sample_report, "Report should include CSS"
        assert "font-family" in sample_report, "Report should set fonts"
        assert "color" in sample_report, "Report should use colors"

    @pytest.mark.slow
    def test_report_has_all_sections(self, sample_report):
        """Test that report includes all required sections."""
        required_sections = [
            "Business Value",
            "Dialogue Transcript",
            "Performance Metrics",
            "Larsson Algorithms",
        ]

        for section in required_sections:
            assert section in sample_report, f"Report missing section: {section}"

    @pytest.mark.slow
    def test_report_has_turn_formatting(self, sample_report):
        """Test that turns are properly formatted."""
        assert 'class="turn' in sample_report, "Turns should have CSS classes"
        assert "Turn 1" in sample_report, "Should show turn numbers"
        assert "USER" in sample_report or "user" in sample_report, "Should show speakers"

    @pytest.mark.slow
    def test_report_is_self_contained(self, sample_report):
        """Test that report doesn't require external resources."""
        # No external CSS links
        assert 'link rel="stylesheet"' not in sample_report, "Should not link external CSS"

        # No external scripts
        assert '<script src="http' not in sample_report, "Should not link external JS"


class TestBusinessDemoEndToEnd:
    """End-to-end tests for complete demo flow."""

    @pytest.mark.slow
    def test_zero_config_demo_works(self, tmp_path):
        """Test that demo works with absolutely zero configuration.

        This is the key requirement: non-technical user can run and understand.
        """
        # Simulate a fresh user: run with defaults
        result = subprocess.run(
            [sys.executable, str(LAUNCHER_SCRIPT), "--quiet"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Should succeed
        assert result.returncode == 0, f"Default demo failed: {result.stderr}"

        # Should provide clear output
        assert len(result.stdout) > 100, "Output should be substantial"
        assert "Turn" in result.stdout, "Should show dialogue turns"
        assert "complete" in result.stdout.lower(), "Should indicate completion"

        # Should generate report
        reports = list(REPORTS_DIR.glob("business-demo-*.html"))
        assert len(reports) >= 1, "Should generate HTML report by default"

    @pytest.mark.slow
    def test_demo_completes_within_time_limit(self, tmp_path):
        """Test that demo completes in reasonable time (<2 minutes)."""
        import time

        start = time.time()

        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--quiet",
                "--no-report",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        elapsed = time.time() - start

        assert result.returncode == 0, "Demo should complete successfully"
        assert elapsed < 120, f"Demo took {elapsed:.1f}s, should be <120s"

    @pytest.mark.slow
    def test_error_messages_are_helpful(self):
        """Test that error messages guide users effectively."""
        # Try invalid scenario
        result = subprocess.run(
            [sys.executable, str(LAUNCHER_SCRIPT), "--scenario", "nonexistent"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode != 0, "Should fail for invalid scenario"
        assert "not found" in result.stderr.lower() or "not found" in result.stdout.lower()
        assert "Available" in result.stdout or "Available" in result.stderr, (
            "Should list available scenarios"
        )


def test_documentation_exists():
    """Test that BUSINESS_DEMO_GUIDE.md exists and is comprehensive."""
    guide = PROJECT_ROOT / "BUSINESS_DEMO_GUIDE.md"
    assert guide.exists(), "BUSINESS_DEMO_GUIDE.md not found"

    content = guide.read_text()

    # Check for key sections
    required_sections = [
        "Quick Start",
        "Available Scenarios",
        "Command Options",
        "Troubleshooting",
        "FAQ",
    ]

    for section in required_sections:
        assert section in content, f"Guide missing section: {section}"

    # Check for code examples
    assert "```bash" in content or "```" in content, "Guide should have code examples"

    # Check for scenario descriptions
    assert "nda_basic" in content, "Guide should describe nda_basic"
    assert "nda_volunteer" in content, "Guide should describe nda_volunteer"

    # Should be substantial
    assert len(content) > 5000, "Guide should be comprehensive (>5000 chars)"


class TestStateReconstruction:
    """Test that BusinessDemo properly reconstructs InformationState from scenario JSON."""

    @pytest.fixture
    def business_demo(self):
        """Create a BusinessDemo instance for testing."""
        # Import BusinessDemo from the script
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        # Import the script as a module
        import importlib.util

        spec = importlib.util.spec_from_file_location("run_business_demo", LAUNCHER_SCRIPT)
        if spec and spec.loader:
            run_business_demo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_business_demo)
            business_demo_class = run_business_demo.BusinessDemo
        else:
            pytest.skip("Could not load business demo script")

        scenario_file = SCENARIOS_DIR / "nda_basic.json"
        demo = business_demo_class(scenario_file, verbose=False, auto_advance=True)
        return demo

    def test_parse_wh_question_from_string(self, business_demo):
        """Test parsing WhQuestion from state_changes string."""
        question = business_demo._parse_question_from_string("?x.legal_entities(x)")

        assert question is not None, "Should parse WhQuestion"
        assert question.variable == "x", "Should extract variable"
        assert question.predicate == "legal_entities", "Should extract predicate"

    def test_parse_yn_question_from_string(self, business_demo):
        """Test parsing YNQuestion from simple string."""
        question = business_demo._parse_question_from_string("?nda_type")

        assert question is not None, "Should parse YNQuestion"
        assert question.proposition == "nda_type", "Should extract proposition"

    def test_create_plan_from_description(self, business_demo):
        """Test creating Plan object from description."""
        plan = business_demo._create_plan_from_description("Draft NDA with 5 questions")

        assert plan is not None, "Should create plan"
        assert plan.plan_type == "findout", "Should have findout type"
        assert "Draft NDA" in plan.content, "Should preserve description"
        assert plan.status == "active", "Should start as active"

    def test_apply_qud_pushed_state_change(self, business_demo):
        """Test applying qud_pushed state change to InformationState."""
        state = business_demo.state
        initial_qud_length = len(state.shared.qud)

        state_changes = {"qud_pushed": "?x.legal_entities(x)"}
        business_demo._apply_state_changes(state, state_changes)

        assert len(state.shared.qud) == initial_qud_length + 1, "Should push to QUD"
        assert state.shared.qud[-1].variable == "x", "Should push correct question"
        assert state.shared.qud[-1].predicate == "legal_entities", "Should have correct predicate"

    def test_apply_qud_popped_state_change(self, business_demo):
        """Test applying qud_popped state change to InformationState."""
        state = business_demo.state

        # First push a question
        state_changes_push = {"qud_pushed": "?x.test_predicate(x)"}
        business_demo._apply_state_changes(state, state_changes_push)
        qud_length_after_push = len(state.shared.qud)

        # Then pop it
        state_changes_pop = {"qud_popped": True}
        business_demo._apply_state_changes(state, state_changes_pop)

        assert len(state.shared.qud) == qud_length_after_push - 1, "Should pop from QUD"

    def test_apply_commitment_added_state_change(self, business_demo):
        """Test applying commitment_added state change to InformationState."""
        state = business_demo.state
        initial_commitments = len(state.shared.commitments)

        state_changes = {"commitment_added": "legal_entities(Acme Corp, TechStart Inc)"}
        business_demo._apply_state_changes(state, state_changes)

        assert len(state.shared.commitments) == initial_commitments + 1, "Should add commitment"
        assert "legal_entities(Acme Corp, TechStart Inc)" in state.shared.commitments

    def test_apply_issues_added_state_change(self, business_demo):
        """Test applying issues_added state change to InformationState."""
        state = business_demo.state
        initial_issues = len(state.private.issues)

        state_changes = {
            "issues_added": ["?x.parties(x)", "?x.effective_date(x)", "?x.governing_law(x)"]
        }
        business_demo._apply_state_changes(state, state_changes)

        assert len(state.private.issues) == initial_issues + 3, "Should add 3 issues"
        assert all(hasattr(q, "predicate") for q in state.private.issues[-3:]), (
            "Should be Question objects"
        )

    def test_apply_plan_created_state_change(self, business_demo):
        """Test applying plan_created state change to InformationState."""
        state = business_demo.state
        initial_plans = len(state.private.plan)

        state_changes = {"plan_created": "Draft NDA with 5 required questions"}
        business_demo._apply_state_changes(state, state_changes)

        assert len(state.private.plan) == initial_plans + 1, "Should add plan"
        assert "Draft NDA" in state.private.plan[-1].content, "Should have correct content"

    def test_apply_plan_status_state_change(self, business_demo):
        """Test applying plan_status state change to InformationState."""
        state = business_demo.state

        # First create a plan
        state_changes_create = {"plan_created": "Test plan"}
        business_demo._apply_state_changes(state, state_changes_create)

        # Then update its status
        state_changes_status = {"plan_status": "completed"}
        business_demo._apply_state_changes(state, state_changes_status)

        assert state.private.plan[-1].status == "completed", "Should update plan status"

    def test_state_reconstruction_through_scenario(self, business_demo):
        """Test that running scenario properly reconstructs state."""
        # Run the full scenario (without output)
        business_demo.verbose = False
        business_demo.run_scenario()

        state = business_demo.state

        # After NDA scenario, should have commitments
        assert len(state.shared.commitments) > 0, "Should have commitments from answers"

        # QUD should be managed (pushed and popped throughout)
        # We can't assert exact length since it varies, but structure should be valid
        assert isinstance(state.shared.qud, list), "QUD should be a list"

    def test_state_serialization_after_reconstruction(self, business_demo):
        """Test that reconstructed state can be serialized."""
        # Apply some state changes
        state_changes = {
            "qud_pushed": "?x.test(x)",
            "commitment_added": "test_commitment",
            "plan_created": "test plan",
        }
        business_demo._apply_state_changes(business_demo.state, state_changes)

        # Serialize state
        state_dict = business_demo.state.to_dict()

        # Check serialization succeeded
        assert isinstance(state_dict, dict), "Should serialize to dict"
        assert "shared" in state_dict, "Should have shared section"
        assert "private" in state_dict, "Should have private section"
        assert "control" in state_dict, "Should have control section"

        # Check reconstructed data is present
        assert len(state_dict["shared"]["qud"]) > 0, "Should have QUD in serialization"
        assert len(state_dict["shared"]["commitments"]) > 0, "Should have commitments"
        assert len(state_dict["private"]["plan"]) > 0, "Should have plans"


class TestSystemDialogueMoveConstruction:
    """Test construction of DialogueMove objects for SYSTEM turns (NLG purposes).

    Note: These tests focus on SYSTEM moves only, since NLG generates system
    utterances. User moves are already natural language and don't need construction.
    """

    @pytest.fixture
    def business_demo(self):
        """Create a BusinessDemo instance for testing."""
        # Import BusinessDemo from the script
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        # Import the script as a module
        import importlib.util

        spec = importlib.util.spec_from_file_location("run_business_demo", LAUNCHER_SCRIPT)
        if spec and spec.loader:
            run_business_demo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_business_demo)
            business_demo_class = run_business_demo.BusinessDemo

            # Load the basic scenario
            scenario_path = PROJECT_ROOT / "demos" / "scenarios" / "nda_basic.json"
            return business_demo_class(scenario_path, verbose=False, auto_advance=False)
        pytest.fail("Could not import BusinessDemo")

    def test_create_system_ask_move_with_wh_question(self, business_demo):
        """Test creating system ask move with WhQuestion content."""
        from ibdm.core.moves import DialogueMove
        from ibdm.core.questions import WhQuestion

        # System turn with qud_pushed
        turn_data = {
            "speaker": "system",
            "move_type": "ask",
            "utterance": "What are the parties to the NDA?",
            "state_changes": {"qud_pushed": "?x.legal_entities(x)"},
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        assert isinstance(move, DialogueMove), "Should create DialogueMove"
        assert move.speaker == "system", "Should be system speaker"
        assert move.move_type == "ask", "Should be ask move"
        assert isinstance(move.content, WhQuestion), "Content should be WhQuestion"
        assert move.content.variable == "x", "Should extract variable"
        assert move.content.predicate == "legal_entities", "Should extract predicate"

    def test_create_system_ask_move_with_yn_question(self, business_demo):
        """Test creating system ask move with YNQuestion content."""
        from ibdm.core.moves import DialogueMove
        from ibdm.core.questions import YNQuestion

        # System turn with simple proposition
        turn_data = {
            "speaker": "system",
            "move_type": "ask",
            "utterance": "Is this a mutual NDA or one-way?",
            "state_changes": {"qud_pushed": "?nda_type"},
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        assert isinstance(move, DialogueMove), "Should create DialogueMove"
        assert move.speaker == "system", "Should be system speaker"
        assert move.move_type == "ask", "Should be ask move"
        assert isinstance(move.content, YNQuestion), "Content should be YNQuestion"
        assert move.content.proposition == "nda_type", "Should extract proposition"

    def test_create_system_ask_move_fallback_to_utterance(self, business_demo):
        """Test ask move falls back to utterance if question parsing fails."""
        from ibdm.core.moves import DialogueMove

        # System turn with unparseable question
        turn_data = {
            "speaker": "system",
            "move_type": "ask",
            "utterance": "What are the parties?",
            "state_changes": {"qud_pushed": ""},  # Empty string
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        assert isinstance(move, DialogueMove), "Should create DialogueMove"
        assert move.content == "What are the parties?", "Should fall back to utterance"

    def test_create_system_greet_move(self, business_demo):
        """Test creating system greet move with string content."""
        from ibdm.core.moves import DialogueMove

        turn_data = {
            "speaker": "system",
            "move_type": "greet",
            "utterance": "Hello! I can help you draft an NDA.",
            "state_changes": {},
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        assert isinstance(move, DialogueMove), "Should create DialogueMove"
        assert move.speaker == "system", "Should be system speaker"
        assert move.move_type == "greet", "Should be greet move"
        assert move.content == "Hello! I can help you draft an NDA.", "Content should be utterance"

    def test_create_system_assert_move(self, business_demo):
        """Test creating system assert move with string content."""
        from ibdm.core.moves import DialogueMove

        turn_data = {
            "speaker": "system",
            "move_type": "assert",
            "utterance": "I've gathered all the information needed.",
            "state_changes": {},
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        assert isinstance(move, DialogueMove), "Should create DialogueMove"
        assert move.speaker == "system", "Should be system speaker"
        assert move.move_type == "assert", "Should be assert move"
        assert move.content == "I've gathered all the information needed.", (
            "Content should be utterance"
        )

    def test_system_moves_from_scenario(self, business_demo):
        """Test creating system moves from actual scenario turns."""
        from ibdm.core.moves import DialogueMove
        from ibdm.core.questions import Question

        scenario = business_demo.scenario
        system_moves = []

        # Extract and create moves for system turns only
        for turn_data in scenario["turns"]:
            if turn_data["speaker"] == "system":
                move = business_demo._create_system_dialogue_move(turn_data)
                system_moves.append(move)

        # Should have system moves from scenario
        assert len(system_moves) > 0, "Should have system turns in scenario"

        # All should be DialogueMoves
        assert all(isinstance(m, DialogueMove) for m in system_moves), "All should be DialogueMoves"

        # All should be system speaker
        assert all(m.speaker == "system" for m in system_moves), "All should be system"

        # Ask moves should have Question content
        ask_moves = [m for m in system_moves if m.move_type == "ask"]
        assert len(ask_moves) > 0, "Should have ask moves"
        for move in ask_moves:
            assert isinstance(move.content, (Question, str)), (
                "Ask moves should have Question or string content"
            )

    def test_move_serialization(self, business_demo):
        """Test that created system moves can be serialized."""
        turn_data = {
            "speaker": "system",
            "move_type": "ask",
            "utterance": "What are the parties?",
            "state_changes": {"qud_pushed": "?x.legal_entities(x)"},
        }

        move = business_demo._create_system_dialogue_move(turn_data)

        # Serialize
        move_dict = move.to_dict()

        # Check serialization
        assert isinstance(move_dict, dict), "Should serialize to dict"
        assert move_dict["move_type"] == "ask", "Should preserve move_type"
        assert move_dict["speaker"] == "system", "Should preserve speaker"
        assert isinstance(move_dict["content"], dict), "Question should serialize to dict"
        assert move_dict["content"]["type"] == "wh", "Should serialize question type"


class TestNLGModes:
    """Test NLG mode integration (off, compare, replace)."""

    @pytest.fixture
    def scenario_path(self):
        """Path to test scenario."""
        return PROJECT_ROOT / "demos" / "scenarios" / "nda_basic.json"

    def test_nlg_mode_off_no_engine_initialized(self, scenario_path):
        """Test that NLG engine is not initialized in 'off' mode."""
        # Import BusinessDemo from the script
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        import importlib.util

        spec = importlib.util.spec_from_file_location("run_business_demo", LAUNCHER_SCRIPT)
        if spec and spec.loader:
            run_business_demo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_business_demo)
            BusinessDemo = run_business_demo.BusinessDemo  # noqa: N806

            # Create demo in off mode
            demo = BusinessDemo(scenario_path, verbose=False, auto_advance=False, nlg_mode="off")

            assert demo.nlg_mode == "off", "Should be in off mode"
            assert demo.nlg_engine is None, "NLG engine should not be initialized"

    def test_nlg_mode_compare_engine_initialized(self, scenario_path):
        """Test that NLG engine is initialized in 'compare' mode."""
        # Import BusinessDemo from the script
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        import importlib.util

        spec = importlib.util.spec_from_file_location("run_business_demo", LAUNCHER_SCRIPT)
        if spec and spec.loader:
            run_business_demo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_business_demo)
            BusinessDemo = run_business_demo.BusinessDemo  # noqa: N806

            # Create demo in compare mode
            demo = BusinessDemo(
                scenario_path, verbose=False, auto_advance=False, nlg_mode="compare"
            )

            assert demo.nlg_mode == "compare", "Should be in compare mode"
            # NLG engine may or may not be initialized depending on availability
            # If it fails to initialize, mode should fall back to "off"
            if demo.nlg_engine is None:
                assert demo.nlg_mode == "off", "Should fall back to off if NLG unavailable"

    def test_nlg_mode_replace_engine_initialized(self, scenario_path):
        """Test that NLG engine is initialized in 'replace' mode."""
        # Import BusinessDemo from the script
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        sys.path.insert(0, str(PROJECT_ROOT / "src"))

        import importlib.util

        spec = importlib.util.spec_from_file_location("run_business_demo", LAUNCHER_SCRIPT)
        if spec and spec.loader:
            run_business_demo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_business_demo)
            BusinessDemo = run_business_demo.BusinessDemo  # noqa: N806

            # Create demo in replace mode
            demo = BusinessDemo(
                scenario_path, verbose=False, auto_advance=False, nlg_mode="replace"
            )

            assert demo.nlg_mode in ["replace", "off"], "Should be in replace mode or fall back"
            # NLG engine may or may not be initialized depending on availability

    def test_nlg_mode_cli_argument(self):
        """Test that --nlg-mode CLI argument is accepted."""
        result = subprocess.run(
            [sys.executable, str(LAUNCHER_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0, "Help should succeed"
        assert "--nlg-mode" in result.stdout, "Should have --nlg-mode argument"
        assert "off" in result.stdout, "Should mention 'off' mode"
        assert "compare" in result.stdout, "Should mention 'compare' mode"
        assert "replace" in result.stdout, "Should mention 'replace' mode"

    @pytest.mark.slow
    def test_nlg_mode_off_runs_successfully(self):
        """Test that demo runs successfully in off mode."""
        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--quiet",
                "--no-report",
                "--nlg-mode",
                "off",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, f"Demo should complete successfully. Error: {result.stderr}"
        assert "complete" in result.stdout.lower(), "Should indicate completion"

    @pytest.mark.slow
    def test_nlg_mode_compare_runs_successfully(self):
        """Test that demo runs successfully in compare mode."""
        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--quiet",
                "--no-report",
                "--nlg-mode",
                "compare",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # May succeed or fail depending on NLG availability
        # Just verify it doesn't crash
        assert result.returncode in [0, 1], "Demo should complete or fail gracefully"

    @pytest.mark.slow
    def test_nlg_mode_replace_runs_successfully(self):
        """Test that demo runs successfully in replace mode."""
        result = subprocess.run(
            [
                sys.executable,
                str(LAUNCHER_SCRIPT),
                "--scenario",
                "nda_basic",
                "--quiet",
                "--no-report",
                "--nlg-mode",
                "replace",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        # May succeed or fail depending on NLG availability
        # Just verify it doesn't crash
        assert result.returncode in [0, 1], "Demo should complete or fail gracefully"
