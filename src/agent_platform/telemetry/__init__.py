"""Observability: metrics, logging, tracing."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass(slots=True)
class Metric:
    name: str
    metric_type: MetricType
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    timestamp_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Telemetry:
    """Observability and SLI/SLO tracking."""

    def __init__(self) -> None:
        self.metrics: list[Metric] = []

    def record_metric(self, name: str, value: float, metric_type: MetricType = MetricType.GAUGE, tags: dict | None = None) -> None:
        """Record a metric."""
        self.metrics.append(
            Metric(
                name=name,
                metric_type=metric_type,
                value=value,
                tags=tags or {},
            )
        )

    def get_sli(self, metric_name: str) -> float:
        """Retrieve SLI (Service Level Indicator)."""
        matching = [m.value for m in self.metrics if m.name == metric_name]
        return sum(matching) / len(matching) if matching else 0.0
