"""
Metrics and statistics for validation framework.

Tracks success rates, error patterns, and performance metrics.
"""

from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import datetime
from typing import Any

from .parsers import ParseFormat, ParseResult
from .validators import ValidationResult


@dataclass
class ValidationStats:
    """
    Statistics for validation operations.

    Tracks success rates, error patterns, and timing.

    Attributes:
        total_attempts: Total validation attempts
        successful: Number of successful validations
        failed: Number of failed validations
        parse_errors: Number of parsing errors
        validation_errors: Number of validation errors
        warnings: Number of warnings generated
        retries: Number of retry attempts
        formats: Count by parse format
        error_codes: Count by error code
        validator_errors: Count by validator name
        total_time: Total time spent in validation (seconds)
        avg_time: Average time per validation (seconds)
    """

    total_attempts: int = 0
    successful: int = 0
    failed: int = 0
    parse_errors: int = 0
    validation_errors: int = 0
    warnings: int = 0
    retries: int = 0
    formats: dict[str, int] = dataclass_field(default_factory=lambda: defaultdict(int))
    error_codes: dict[str, int] = dataclass_field(default_factory=lambda: defaultdict(int))
    validator_errors: dict[str, int] = dataclass_field(default_factory=lambda: defaultdict(int))
    total_time: float = 0.0
    avg_time: float = 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.successful / self.total_attempts

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        return 1.0 - self.success_rate

    @property
    def retry_rate(self) -> float:
        """Calculate retry rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.retries / self.total_attempts

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "total_attempts": self.total_attempts,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "parse_errors": self.parse_errors,
            "validation_errors": self.validation_errors,
            "warnings": self.warnings,
            "retries": self.retries,
            "retry_rate": self.retry_rate,
            "formats": dict(self.formats),
            "error_codes": dict(self.error_codes),
            "validator_errors": dict(self.validator_errors),
            "total_time": self.total_time,
            "avg_time": self.avg_time,
        }


class ValidationMetrics:
    """
    Metrics tracker for validation operations.

    Collects and aggregates validation statistics.
    """

    def __init__(self):
        """Initialize metrics tracker."""
        self.stats = ValidationStats()
        self._start_times: dict[str, datetime] = {}

    def start_validation(self, validation_id: str | None = None) -> str:
        """
        Start tracking a validation operation.

        Args:
            validation_id: Optional ID for this validation

        Returns:
            Validation ID (generated if not provided)
        """
        if validation_id is None:
            validation_id = f"val_{datetime.now().timestamp()}"

        self._start_times[validation_id] = datetime.now()
        return validation_id

    def record_validation(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        validation_id: str | None = None,
        retry_count: int = 0,
    ) -> None:
        """
        Record a validation attempt.

        Args:
            parse_result: Parse result
            validation_result: Validation result
            validation_id: Optional validation ID
            retry_count: Number of retries attempted
        """
        self.stats.total_attempts += 1

        # Record timing
        if validation_id and validation_id in self._start_times:
            start_time = self._start_times[validation_id]
            elapsed = (datetime.now() - start_time).total_seconds()
            self.stats.total_time += elapsed
            self.stats.avg_time = self.stats.total_time / self.stats.total_attempts
            del self._start_times[validation_id]

        # Record success/failure
        if parse_result.success and validation_result.valid:
            self.stats.successful += 1
        else:
            self.stats.failed += 1

        # Record parse errors
        if parse_result.failed:
            self.stats.parse_errors += 1

        # Record validation errors
        if validation_result.errors:
            self.stats.validation_errors += 1

        # Record warnings
        self.stats.warnings += len(validation_result.warnings)

        # Record retries
        self.stats.retries += retry_count

        # Record format
        if parse_result.format != ParseFormat.UNKNOWN:
            self.stats.formats[parse_result.format.value] += 1

        # Record error codes
        for issue in validation_result.issues:
            if issue.code:
                self.stats.error_codes[issue.code] += 1

        # Record validator errors
        if "validators_run" in validation_result.metadata:
            for validator_name in validation_result.metadata["validators_run"]:
                # Count errors from this validator
                validator_errors = [
                    issue
                    for issue in validation_result.errors
                    if validator_name in str(issue.metadata)
                ]
                if validator_errors:
                    self.stats.validator_errors[validator_name] += len(validator_errors)

    def get_stats(self) -> ValidationStats:
        """Get current statistics."""
        return self.stats

    def reset(self) -> None:
        """Reset all metrics."""
        self.stats = ValidationStats()
        self._start_times.clear()

    def summary(self) -> str:
        """
        Generate a human-readable summary of metrics.

        Returns:
            Formatted summary string
        """
        lines = [
            "=== Validation Metrics Summary ===",
            f"Total Attempts: {self.stats.total_attempts}",
            f"Successful: {self.stats.successful} ({self.stats.success_rate:.1%})",
            f"Failed: {self.stats.failed} ({self.stats.failure_rate:.1%})",
            "",
            "Error Breakdown:",
            f"  Parse Errors: {self.stats.parse_errors}",
            f"  Validation Errors: {self.stats.validation_errors}",
            f"  Warnings: {self.stats.warnings}",
            "",
            f"Retries: {self.stats.retries} ({self.stats.retry_rate:.2f} per attempt)",
            "",
        ]

        # Format breakdown
        if self.stats.formats:
            lines.append("Formats:")
            for fmt, count in sorted(self.stats.formats.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  {fmt}: {count}")
            lines.append("")

        # Top error codes
        if self.stats.error_codes:
            lines.append("Top Error Codes:")
            top_errors = sorted(self.stats.error_codes.items(), key=lambda x: x[1], reverse=True)[
                :5
            ]
            for code, count in top_errors:
                lines.append(f"  {code}: {count}")
            lines.append("")

        # Performance
        if self.stats.total_time > 0:
            lines.append("Performance:")
            lines.append(f"  Total Time: {self.stats.total_time:.2f}s")
            lines.append(f"  Average Time: {self.stats.avg_time:.4f}s")
            lines.append("")

        return "\n".join(lines)

    def get_error_patterns(self) -> dict[str, Any]:
        """
        Analyze error patterns.

        Returns:
            Dictionary of error pattern analysis
        """
        patterns: dict[str, Any] = {
            "most_common_errors": [],
            "problematic_validators": [],
            "format_issues": {},
        }

        # Most common error codes
        if self.stats.error_codes:
            patterns["most_common_errors"] = sorted(
                self.stats.error_codes.items(), key=lambda x: x[1], reverse=True
            )[:10]

        # Validators with most errors
        if self.stats.validator_errors:
            patterns["problematic_validators"] = sorted(
                self.stats.validator_errors.items(), key=lambda x: x[1], reverse=True
            )[:5]

        # Format-specific issues
        for fmt, count in self.stats.formats.items():
            if count > 0:
                error_rate = self.stats.parse_errors / count if fmt in ["json", "xml"] else 0.0
                patterns["format_issues"][fmt] = {
                    "count": count,
                    "error_rate": error_rate,
                }

        return patterns


# Global metrics instance for convenience
_global_metrics = ValidationMetrics()


def get_global_metrics() -> ValidationMetrics:
    """Get the global metrics instance."""
    return _global_metrics


def reset_global_metrics() -> None:
    """Reset the global metrics instance."""
    _global_metrics.reset()
