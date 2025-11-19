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
