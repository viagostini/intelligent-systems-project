import json
from typing import Callable

from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

instrumentator = Instrumentator()


def product_classifier_output() -> Callable[[Info], None]:
    METRIC = Counter(
        "product_classifier_output",
        "Number of times a category has been predicted.",
        labelnames=("category",),
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/v1/categorize":
            if info.response:
                predictions = info.response.headers.get("X-predictions")
                if predictions:
                    for category in json.loads(predictions)["categories"]:
                        METRIC.labels(category).inc()

    return instrumentation


instrumentator.add(metrics.latency(buckets=(1, 2, 3)))

instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
    )
)

instrumentator.add(product_classifier_output())
