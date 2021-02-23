"""Instrumentation for API monitoring.

This module prepares an instrumentator that allows metrics to be exposed to Prometheus
and later displayed in a Grafana dashboard.
"""

from typing import Callable

from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

from app.schemas import Predictions

# this will be imported in api.py to enable instrumentation
instrumentator = Instrumentator()


def product_classifier_output() -> Callable[[Info], None]:
    """Custom metric to count predicted categories"""

    METRIC = Counter(
        "product_classifier_output",
        "Number of times a category has been predicted.",
        labelnames=("category",),
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/v1/categorize":
            if info.response and "X-predictions" in info.response.headers:
                predictions = Predictions.parse_raw(
                    info.response.headers["X-predictions"]
                )
                for category in predictions.categories:
                    METRIC.labels(category).inc()

    return instrumentation


instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
    )
)

instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
    )
)

instrumentator.add(product_classifier_output())

instrumentator.add(metrics.latency(buckets=(1, 2, 3)))
