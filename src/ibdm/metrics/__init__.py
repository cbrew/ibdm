"""
Larsson Fidelity Metrics Framework.

Comprehensive metrics for measuring IBDM implementation fidelity to Larsson (2002).

Key metrics:
- Architectural compliance (control flow, four-phase architecture)
- Information state structure (IBiS1/3/4 compliance)
- Semantic operations coverage
- Update and selection rules coverage
- Domain independence
- Overall Larsson fidelity score

Visualization:
- Dashboard with all metrics
- Component score charts
- Detailed breakdowns

Reference: docs/LARSSON_ALGORITHMS.md
"""

from .larsson_fidelity import (
    ArchitecturalComplianceMetrics,
    DomainIndependenceMetrics,
    InformationStateMetrics,
    LarsonFidelityScore,
    MetricResult,
    RulesCoverageMetrics,
    SemanticOperationsMetrics,
    evaluate_larsson_fidelity,
)

# Import visualization if matplotlib available
try:
    from .visualization import MetricsVisualizer, create_visualizations

    __all__ = [
        "ArchitecturalComplianceMetrics",
        "InformationStateMetrics",
        "SemanticOperationsMetrics",
        "RulesCoverageMetrics",
        "DomainIndependenceMetrics",
        "LarsonFidelityScore",
        "MetricResult",
        "evaluate_larsson_fidelity",
        "MetricsVisualizer",
        "create_visualizations",
    ]
except ImportError:
    __all__ = [
        "ArchitecturalComplianceMetrics",
        "InformationStateMetrics",
        "SemanticOperationsMetrics",
        "RulesCoverageMetrics",
        "DomainIndependenceMetrics",
        "LarsonFidelityScore",
        "MetricResult",
        "evaluate_larsson_fidelity",
    ]
