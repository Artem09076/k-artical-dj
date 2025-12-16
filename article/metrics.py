from prometheus_client import Counter, Histogram

DB_LATENCY = Histogram(
    name="db_latency_seconds",
    documentation="Latency of database operations in seconds",
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],
)

HTTP_REQUESTS_TOTAL = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests",
)

HTTP_RESPONSES_2XX = Counter(
    name="http_responses_2xx_total",
    documentation="Total number of HTTP 2xx responses",
)

HTTP_RESPONSES_4XX = Counter(
    name="http_responses_4xx_total",
    documentation="Total number of HTTP 4xx responses",
)

HTTP_RESPONSES_5XX = Counter(
    name="http_responses_5xx_total",
    documentation="Total number of HTTP 5xx responses",
)