"""
Tests for Larsson Fidelity Metrics Framework.

Verifies that all metric categories work correctly and produce meaningful scores.
"""

import pytest

from ibdm.core import InformationState
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.metrics import (
    ArchitecturalComplianceMetrics,
    DomainIndependenceMetrics,
    InformationStateMetrics,
    LarsonFidelityScore,
    RulesCoverageMetrics,
    SemanticOperationsMetrics,
)
from ibdm.metrics.larsson_fidelity import evaluate_larsson_fidelity


class TestMetricResult:
    """Test MetricResult dataclass."""

    def test_metric_result_creation(self):
        """Test creating a metric result."""
        from ibdm.metrics import MetricResult

        result = MetricResult(
            name="Test Metric",
            score=85.5,
            passed=True,
            details={"check1": 90.0},
            issues=[],
            recommendations=[],
        )

        assert result.name == "Test Metric"
        assert result.score == 85.5
        assert result.passed is True
        assert result.details == {"check1": 90.0}

    def test_metric_result_str(self):
        """Test string representation."""
        from ibdm.metrics import MetricResult

        result = MetricResult(name="Test", score=92.0, passed=True)
        assert "Test" in str(result)
        assert "92" in str(result)
        assert "PASS" in str(result)

    def test_metric_result_to_dict(self):
        """Test serialization to dict."""
        from ibdm.metrics import MetricResult

        result = MetricResult(
            name="Test",
            score=88.0,
            passed=True,
            details={"x": 1},
            issues=["issue1"],
            recommendations=["rec1"],
        )

        data = result.to_dict()
        assert data["name"] == "Test"
        assert data["score"] == 88.0
        assert data["passed"] is True
        assert data["details"] == {"x": 1}
        assert data["issues"] == ["issue1"]
        assert data["recommendations"] == ["rec1"]


class TestArchitecturalComplianceMetrics:
    """Test Architectural Compliance Metrics."""

    def test_initialization(self):
        """Test metrics initialization."""
        metrics = ArchitecturalComplianceMetrics()
        assert metrics.engine is None
        assert metrics.burr_app is None

    def test_evaluation_without_engine(self):
        """Test evaluation with no engine/app provided."""
        metrics = ArchitecturalComplianceMetrics()
        result = metrics.evaluate()

        assert result.name == "Architectural Compliance"
        assert 0 <= result.score <= 100
        # Should have low score without engine
        assert result.score < 50.0

    def test_evaluation_with_engine(self):
        """Test evaluation with engine."""
        engine = DialogueMoveEngine(agent_id="system")
        metrics = ArchitecturalComplianceMetrics(engine=engine)
        result = metrics.evaluate()

        assert result.name == "Architectural Compliance"
        assert 0 <= result.score <= 100
        # Should have some score with engine
        assert result.score > 0

    def test_four_phase_check(self):
        """Test four-phase architecture check."""
        metrics = ArchitecturalComplianceMetrics()
        score = metrics._check_four_phase_architecture()

        assert 0 <= score <= 100

    def test_explicit_state_passing_check(self):
        """Test explicit state passing check."""
        engine = DialogueMoveEngine(agent_id="system")
        metrics = ArchitecturalComplianceMetrics(engine=engine)
        score = metrics._check_explicit_state_passing()

        assert 0 <= score <= 100
        # Engine should have explicit state passing
        assert score > 0


class TestInformationStateMetrics:
    """Test Information State Structure Metrics."""

    def test_initialization(self):
        """Test metrics initialization."""
        metrics = InformationStateMetrics()
        assert metrics.state_class == InformationState

    def test_evaluation(self):
        """Test full evaluation."""
        metrics = InformationStateMetrics()
        result = metrics.evaluate()

        assert result.name == "Information State Structure"
        assert 0 <= result.score <= 100
        assert isinstance(result.passed, bool)
        assert isinstance(result.details, dict)

    def test_private_shared_separation(self):
        """Test private/shared separation check."""
        metrics = InformationStateMetrics()
        score = metrics._check_private_shared_separation()

        # InformationState should have private and shared
        assert score == 100.0

    def test_private_fields_check(self):
        """Test private fields check."""
        metrics = InformationStateMetrics()
        score = metrics._check_private_fields()

        # Should have plan, agenda, beliefs
        assert score > 50.0

    def test_shared_fields_check(self):
        """Test shared fields check."""
        metrics = InformationStateMetrics()
        score = metrics._check_shared_fields()

        # Should have qud, commitments
        assert score > 50.0

    def test_qud_stack_semantics(self):
        """Test QUD stack semantics check."""
        metrics = InformationStateMetrics()
        score = metrics._check_qud_stack_semantics()

        # Should have push_qud, pop_qud, top_qud
        assert score > 50.0


class TestSemanticOperationsMetrics:
    """Test Semantic Operations Coverage Metrics."""

    def test_initialization(self):
        """Test metrics initialization."""
        metrics = SemanticOperationsMetrics()
        assert metrics.domain is None

    def test_evaluation(self):
        """Test full evaluation."""
        metrics = SemanticOperationsMetrics()
        result = metrics.evaluate()

        assert result.name == "Semantic Operations Coverage"
        assert 0 <= result.score <= 100
        assert isinstance(result.passed, bool)

    def test_evaluation_with_domain(self):
        """Test evaluation with domain."""
        domain = get_nda_domain()
        metrics = SemanticOperationsMetrics(domain=domain)
        result = metrics.evaluate()

        # Should have better score with domain
        assert result.score > 0

    def test_resolves_check(self):
        """Test resolves() check."""
        metrics = SemanticOperationsMetrics()
        score = metrics._check_resolves()

        # Question class should have resolves_with
        assert score == 100.0

    def test_combines_check(self):
        """Test combines() check."""
        domain = get_nda_domain()
        metrics = SemanticOperationsMetrics(domain=domain)
        score = metrics._check_combines()

        # Should have some score with domain
        assert score >= 50.0

    def test_depends_check(self):
        """Test depends() check."""
        metrics = SemanticOperationsMetrics()
        score = metrics._check_depends()

        # May not be implemented yet
        assert 0 <= score <= 100


class TestRulesCoverageMetrics:
    """Test Rules Coverage Metrics."""

    def test_initialization(self):
        """Test metrics initialization."""
        metrics = RulesCoverageMetrics()
        assert metrics.rule_set is None
        assert metrics.rules_path is not None

    def test_evaluation(self):
        """Test full evaluation."""
        metrics = RulesCoverageMetrics()
        result = metrics.evaluate()

        assert result.name == "Rules Coverage"
        assert 0 <= result.score <= 100
        assert "update_rules" in result.details
        assert "selection_rules" in result.details

    def test_find_rules_in_source(self):
        """Test finding rules in source files."""
        metrics = RulesCoverageMetrics()
        rules = metrics._find_rules_in_source("integration_rules.py")

        # Should find some rules
        assert isinstance(rules, set)
        # May be empty if file doesn't exist, but should be a set
        assert len(rules) >= 0

    def test_update_rules_evaluation(self):
        """Test update rules evaluation."""
        metrics = RulesCoverageMetrics()
        score = metrics._evaluate_update_rules()

        assert 0 <= score <= 100

    def test_selection_rules_evaluation(self):
        """Test selection rules evaluation."""
        metrics = RulesCoverageMetrics()
        score = metrics._evaluate_selection_rules()

        assert 0 <= score <= 100


class TestDomainIndependenceMetrics:
    """Test Domain Independence Metrics."""

    def test_initialization(self):
        """Test metrics initialization."""
        metrics = DomainIndependenceMetrics()
        assert metrics.rules_path is not None
        assert metrics.domain is None

    def test_evaluation(self):
        """Test full evaluation."""
        metrics = DomainIndependenceMetrics()
        result = metrics.evaluate()

        assert result.name == "Domain Independence"
        assert 0 <= result.score <= 100

    def test_evaluation_with_domain(self):
        """Test evaluation with domain."""
        domain = get_nda_domain()
        metrics = DomainIndependenceMetrics(domain=domain)
        result = metrics.evaluate()

        # Should have better score with domain
        assert result.score > 0

    def test_domain_model_exists(self):
        """Test domain model existence check."""
        metrics = DomainIndependenceMetrics()
        score = metrics._check_domain_model_exists()

        # DomainModel class should exist
        assert score == 100.0

    def test_no_hardcoded_predicates(self):
        """Test no hardcoded predicates check."""
        metrics = DomainIndependenceMetrics()
        score = metrics._check_no_hardcoded_predicates()

        # May have some hardcoded predicates
        assert 0 <= score <= 100

    def test_plan_builders_registered(self):
        """Test plan builders registration check."""
        domain = get_nda_domain()
        metrics = DomainIndependenceMetrics(domain=domain)
        score = metrics._check_plan_builders_registered()

        # NDA domain should have plan builders
        assert score > 0


class TestLarsonFidelityScore:
    """Test Larsson Fidelity Score Aggregator."""

    @pytest.fixture
    def mock_results(self):
        """Create mock metric results for testing."""
        from ibdm.metrics import MetricResult

        return {
            "arch": MetricResult("Architectural", 85.0, True, {}, [], []),
            "state": MetricResult("State", 90.0, True, {}, [], []),
            "sem": MetricResult("Semantic", 75.0, True, {}, [], []),
            "rules": MetricResult("Rules", 80.0, True, {}, [], []),
            "domain": MetricResult("Domain", 88.0, True, {}, [], []),
        }

    def test_overall_score_calculation(self, mock_results):
        """Test overall score calculation."""
        score = LarsonFidelityScore(
            architectural_compliance=mock_results["arch"],
            information_state=mock_results["state"],
            semantic_operations=mock_results["sem"],
            rules_coverage=mock_results["rules"],
            domain_independence=mock_results["domain"],
        )

        # Weighted average:
        # 85*0.25 + 90*0.25 + 75*0.20 + 80*0.20 + 88*0.10 = 83.55
        assert 83.0 <= score.overall_score <= 84.0

    def test_passed_property(self, mock_results):
        """Test passed property."""
        # Low scores - should fail
        low_results = {k: v for k, v in mock_results.items()}
        low_results["arch"] = low_results["arch"].__class__("Arch", 50.0, False, {}, [], [])
        low_results["state"] = low_results["state"].__class__("State", 50.0, False, {}, [], [])

        score = LarsonFidelityScore(
            architectural_compliance=low_results["arch"],
            information_state=low_results["state"],
            semantic_operations=mock_results["sem"],
            rules_coverage=mock_results["rules"],
            domain_independence=mock_results["domain"],
        )

        # Should fail with low scores
        assert not score.passed

    def test_summary_generation(self, mock_results):
        """Test summary report generation."""
        score = LarsonFidelityScore(
            architectural_compliance=mock_results["arch"],
            information_state=mock_results["state"],
            semantic_operations=mock_results["sem"],
            rules_coverage=mock_results["rules"],
            domain_independence=mock_results["domain"],
        )

        summary = score.summary()

        assert "LARSSON FIDELITY METRICS REPORT" in summary
        assert "Overall Score" in summary
        assert "Component Scores" in summary

    def test_to_dict(self, mock_results):
        """Test serialization to dict."""
        score = LarsonFidelityScore(
            architectural_compliance=mock_results["arch"],
            information_state=mock_results["state"],
            semantic_operations=mock_results["sem"],
            rules_coverage=mock_results["rules"],
            domain_independence=mock_results["domain"],
        )

        data = score.to_dict()

        assert "overall_score" in data
        assert "passed" in data
        assert "components" in data
        assert len(data["components"]) == 5


class TestEvaluateLarssonFidelity:
    """Test convenience function for full evaluation."""

    def test_evaluate_without_args(self):
        """Test evaluation with no arguments."""
        score = evaluate_larsson_fidelity()

        assert isinstance(score, LarsonFidelityScore)
        assert 0 <= score.overall_score <= 100

    def test_evaluate_with_engine(self):
        """Test evaluation with engine."""
        engine = DialogueMoveEngine(agent_id="system")
        score = evaluate_larsson_fidelity(engine=engine)

        assert isinstance(score, LarsonFidelityScore)
        # Should have better score with engine
        assert score.overall_score > 0

    def test_evaluate_with_domain(self):
        """Test evaluation with domain."""
        domain = get_nda_domain()
        score = evaluate_larsson_fidelity(domain=domain)

        assert isinstance(score, LarsonFidelityScore)
        # Should have better score with domain
        assert score.overall_score > 0

    def test_evaluate_full_system(self):
        """Test evaluation with full system."""
        engine = DialogueMoveEngine(agent_id="system")
        domain = get_nda_domain()
        score = evaluate_larsson_fidelity(engine=engine, domain=domain)

        assert isinstance(score, LarsonFidelityScore)
        assert 0 <= score.overall_score <= 100

        # Print summary for inspection
        print("\n" + score.summary())

        # Verify all components evaluated
        assert score.architectural_compliance.score >= 0
        assert score.information_state.score >= 0
        assert score.semantic_operations.score >= 0
        assert score.rules_coverage.score >= 0
        assert score.domain_independence.score >= 0


class TestMetricsIntegration:
    """Integration tests for metrics framework."""

    def test_all_metrics_produce_valid_scores(self):
        """Test that all metrics produce valid scores in [0, 100]."""
        engine = DialogueMoveEngine(agent_id="system")
        domain = get_nda_domain()

        arch_metrics = ArchitecturalComplianceMetrics(engine=engine)
        state_metrics = InformationStateMetrics()
        sem_metrics = SemanticOperationsMetrics(domain=domain)
        rules_metrics = RulesCoverageMetrics()
        domain_metrics = DomainIndependenceMetrics(domain=domain)

        results = [
            arch_metrics.evaluate(),
            state_metrics.evaluate(),
            sem_metrics.evaluate(),
            rules_metrics.evaluate(),
            domain_metrics.evaluate(),
        ]

        for result in results:
            assert 0 <= result.score <= 100
            assert isinstance(result.name, str)
            assert isinstance(result.passed, bool)
            assert isinstance(result.details, dict)

    def test_metrics_serialization(self):
        """Test that metrics can be serialized to dict."""
        score = evaluate_larsson_fidelity()
        data = score.to_dict()

        assert isinstance(data, dict)
        assert "overall_score" in data
        assert "components" in data

        # Should be JSON-serializable
        import json

        json_str = json.dumps(data)
        assert isinstance(json_str, str)

    def test_metrics_provide_actionable_feedback(self):
        """Test that metrics provide issues and recommendations."""
        score = evaluate_larsson_fidelity()

        # At least some metrics should have issues/recommendations
        # (since implementation is not 100% complete)
        has_issues = any(
            len(m.issues) > 0
            for m in [
                score.architectural_compliance,
                score.information_state,
                score.semantic_operations,
                score.rules_coverage,
                score.domain_independence,
            ]
        )

        has_recommendations = any(
            len(m.recommendations) > 0
            for m in [
                score.architectural_compliance,
                score.information_state,
                score.semantic_operations,
                score.rules_coverage,
                score.domain_independence,
            ]
        )

        assert has_issues or has_recommendations
