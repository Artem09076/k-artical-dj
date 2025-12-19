from prometheus_client import Histogram

DB_LATENCY = Histogram(
    name="db_latency_seconds",
    documentation="Latency of database operations in seconds",
    labelnames=["handler"],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],
)
