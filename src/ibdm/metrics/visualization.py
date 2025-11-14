"""
Graphical visualization for Larsson Fidelity Metrics.

Creates charts and graphs for metrics reports, including:
- Overall score gauge
- Component scores radar chart
- Component scores bar chart
- Detailed breakdown heatmap
- Historical trend tracking

Requires matplotlib for chart generation.
"""

from pathlib import Path
from typing import Any

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Circle, Wedge

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from .larsson_fidelity import LarsonFidelityScore


class MetricsVisualizer:
    """
    Visualizer for Larsson fidelity metrics.

    Creates various chart types to present metrics graphically.
    """

    def __init__(self, score: LarsonFidelityScore):
        """
        Initialize visualizer with fidelity score.

        Args:
            score: LarsonFidelityScore instance to visualize

        Raises:
            ImportError: If matplotlib is not available
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError(
                "matplotlib is required for visualization. Install with: pip install matplotlib"
            )

        self.score = score

        # Configure matplotlib style
        plt.style.use("seaborn-v0_8-darkgrid")

    def create_dashboard(self, output_path: str | Path) -> None:
        """
        Create comprehensive dashboard with all visualizations.

        Args:
            output_path: Path to save dashboard image
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Top row: Overall score gauge (larger)
        ax_gauge = fig.add_subplot(gs[0, :])
        self._plot_gauge(ax_gauge)

        # Middle row: Component scores
        ax_bar = fig.add_subplot(gs[1, :2])
        self._plot_component_bars(ax_bar)

        ax_radar = fig.add_subplot(gs[1, 2], projection="polar")
        self._plot_radar(ax_radar)

        # Bottom row: Detailed breakdowns
        ax_arch = fig.add_subplot(gs[2, 0])
        self._plot_detail_bars(
            ax_arch,
            "Architectural",
            self.score.architectural_compliance.details,
        )

        ax_state = fig.add_subplot(gs[2, 1])
        self._plot_detail_bars(
            ax_state,
            "Info State",
            self.score.information_state.details,
        )

        ax_sem = fig.add_subplot(gs[2, 2])
        self._plot_detail_bars(
            ax_sem,
            "Semantic Ops",
            self.score.semantic_operations.details,
        )

        # Overall title
        fig.suptitle(
            "IBDM Larsson Fidelity Metrics Dashboard",
            fontsize=16,
            fontweight="bold",
        )

        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _plot_gauge(self, ax: Any) -> None:
        """
        Plot overall score as a gauge/speedometer.

        Args:
            ax: Matplotlib axes
        """
        score = self.score.overall_score

        # Draw gauge background (semicircle)
        radius = 1.0

        # Color segments for score ranges
        segments = [
            (0, 50, "#d32f2f", "Low"),  # Red
            (50, 70, "#f57c00", "Moderate"),  # Orange
            (70, 80, "#fbc02d", "Good"),  # Yellow
            (80, 90, "#7cb342", "Very Good"),  # Light green
            (90, 100, "#388e3c", "Excellent"),  # Dark green
        ]

        for start, end, color, label in segments:
            start_angle = 180 - (start * 1.8)
            end_angle = 180 - (end * 1.8)
            wedge = Wedge(
                (0, 0),
                radius,
                end_angle,
                start_angle,
                facecolor=color,
                edgecolor="white",
                linewidth=2,
                alpha=0.7,
            )
            ax.add_patch(wedge)

        # Draw needle
        needle_angle = 180 - (score * 1.8)
        needle_rad = np.radians(needle_angle)
        ax.plot(
            [0, radius * 0.9 * np.cos(needle_rad)],
            [0, radius * 0.9 * np.sin(needle_rad)],
            color="black",
            linewidth=3,
            zorder=10,
        )

        # Center circle
        circle = Circle((0, 0), 0.1, facecolor="black", zorder=11)
        ax.add_patch(circle)

        # Score text
        ax.text(
            0,
            -0.3,
            f"{score:.1f}%",
            ha="center",
            va="center",
            fontsize=32,
            fontweight="bold",
        )

        # Target line
        target_angle = 180 - (90 * 1.8)
        target_rad = np.radians(target_angle)
        ax.plot(
            [0, radius * 0.95 * np.cos(target_rad)],
            [0, radius * 0.95 * np.sin(target_rad)],
            color="blue",
            linewidth=2,
            linestyle="--",
            alpha=0.5,
            zorder=5,
        )
        ax.text(
            radius * 1.1 * np.cos(target_rad),
            radius * 1.1 * np.sin(target_rad),
            "Target\n90%",
            ha="center",
            va="center",
            fontsize=10,
            color="blue",
        )

        # Status
        if score >= 90:
            status = "✓ PASS"
            status_color = "#388e3c"
        else:
            status = "✗ FAIL"
            status_color = "#d32f2f"

        ax.text(
            0,
            -0.6,
            status,
            ha="center",
            va="center",
            fontsize=18,
            fontweight="bold",
            color=status_color,
        )

        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-0.8, 1.2)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("Overall Larsson Fidelity", fontsize=14, fontweight="bold")

    def _plot_component_bars(self, ax: Any) -> None:
        """
        Plot component scores as horizontal bar chart.

        Args:
            ax: Matplotlib axes
        """
        components = [
            ("Architectural\nCompliance", self.score.architectural_compliance.score),
            ("Information\nState", self.score.information_state.score),
            ("Semantic\nOperations", self.score.semantic_operations.score),
            ("Rules\nCoverage", self.score.rules_coverage.score),
            ("Domain\nIndependence", self.score.domain_independence.score),
        ]

        names = [c[0] for c in components]
        scores = [c[1] for c in components]

        # Color bars by score
        colors = []
        for score in scores:
            if score >= 90:
                colors.append("#388e3c")  # Dark green
            elif score >= 80:
                colors.append("#7cb342")  # Light green
            elif score >= 70:
                colors.append("#fbc02d")  # Yellow
            elif score >= 50:
                colors.append("#f57c00")  # Orange
            else:
                colors.append("#d32f2f")  # Red

        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, scores, color=colors, alpha=0.8, edgecolor="black")

        # Add score labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(
                score + 2,
                bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}%",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

        # Target line
        ax.axvline(x=90, color="blue", linestyle="--", linewidth=2, alpha=0.5, label="Target (90%)")

        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=10)
        ax.set_xlabel("Score (%)", fontsize=11)
        ax.set_xlim(0, 105)
        ax.set_title("Component Scores", fontsize=12, fontweight="bold")
        ax.legend(loc="lower right")
        ax.grid(axis="x", alpha=0.3)

    def _plot_radar(self, ax: Any) -> None:
        """
        Plot component scores as radar chart.

        Args:
            ax: Matplotlib polar axes
        """
        categories = [
            "Architectural",
            "Info State",
            "Semantic Ops",
            "Rules",
            "Domain Indep.",
        ]

        values = [
            self.score.architectural_compliance.score,
            self.score.information_state.score,
            self.score.semantic_operations.score,
            self.score.rules_coverage.score,
            self.score.domain_independence.score,
        ]

        # Number of variables
        num_vars = len(categories)

        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Complete the circle
        values += values[:1]
        angles += angles[:1]

        # Plot
        ax.plot(angles, values, "o-", linewidth=2, color="#1976d2", label="Current")
        ax.fill(angles, values, alpha=0.25, color="#1976d2")

        # Target circle
        target_values = [90] * (num_vars + 1)
        ax.plot(
            angles, target_values, "--", linewidth=2, color="#388e3c", alpha=0.5, label="Target"
        )

        # Fix axis to go in the right order
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)

        # Y-axis
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(["25", "50", "75", "100"], fontsize=8)
        ax.set_rlabel_position(0)

        ax.set_title("Component Radar", fontsize=12, fontweight="bold", pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)

    def _plot_detail_bars(self, ax: Any, title: str, details: dict[str, float]) -> None:
        """
        Plot detailed breakdown as small bar chart.

        Args:
            ax: Matplotlib axes
            title: Chart title
            details: Dictionary of detail scores
        """
        if not details:
            ax.text(0.5, 0.5, "No details", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(title, fontsize=10, fontweight="bold")
            ax.axis("off")
            return

        # Truncate long labels
        labels = []
        for k in details.keys():
            parts = k.split("_")
            if len(parts) > 2:
                label = "_".join(parts[:2]) + "..."
            else:
                label = k
            labels.append(label)

        scores = list(details.values())

        # Color by score
        colors = []
        for score in scores:
            if score >= 90:
                colors.append("#388e3c")
            elif score >= 70:
                colors.append("#7cb342")
            elif score >= 50:
                colors.append("#fbc02d")
            else:
                colors.append("#f57c00")

        y_pos = np.arange(len(labels))
        ax.barh(y_pos, scores, color=colors, alpha=0.8, edgecolor="black")

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=7)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Score", fontsize=8)
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)

        # Add score labels
        for i, score in enumerate(scores):
            ax.text(
                score + 2,
                i,
                f"{score:.0f}",
                va="center",
                fontsize=7,
            )

    def create_summary_chart(self, output_path: str | Path) -> None:
        """
        Create simple summary chart (just component bars).

        Args:
            output_path: Path to save chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        self._plot_component_bars(ax)

        plt.title(
            f"IBDM Larsson Fidelity: {self.score.overall_score:.1f}%",
            fontsize=14,
            fontweight="bold",
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def create_gauge_chart(self, output_path: str | Path) -> None:
        """
        Create standalone gauge chart.

        Args:
            output_path: Path to save chart
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        self._plot_gauge(ax)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def create_all_charts(self, output_dir: str | Path) -> dict[str, Path]:
        """
        Create all chart types and save to directory.

        Args:
            output_dir: Directory to save charts

        Returns:
            Dictionary mapping chart type to file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        charts = {}

        # Dashboard
        dashboard_path = output_dir / "dashboard.png"
        self.create_dashboard(dashboard_path)
        charts["dashboard"] = dashboard_path

        # Summary
        summary_path = output_dir / "summary.png"
        self.create_summary_chart(summary_path)
        charts["summary"] = summary_path

        # Gauge
        gauge_path = output_dir / "gauge.png"
        self.create_gauge_chart(gauge_path)
        charts["gauge"] = gauge_path

        return charts


def create_visualizations(
    score: LarsonFidelityScore,
    output_dir: str | Path,
) -> dict[str, Path]:
    """
    Convenience function to create all visualizations.

    Args:
        score: LarsonFidelityScore to visualize
        output_dir: Directory to save visualizations

    Returns:
        Dictionary mapping chart type to file path

    Example:
        >>> from ibdm.metrics import evaluate_larsson_fidelity
        >>> score = evaluate_larsson_fidelity()
        >>> charts = create_visualizations(score, "reports/charts")
        >>> print(f"Dashboard: {charts['dashboard']}")
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required for visualization. Install with: pip install matplotlib"
        )

    visualizer = MetricsVisualizer(score)
    return visualizer.create_all_charts(output_dir)
