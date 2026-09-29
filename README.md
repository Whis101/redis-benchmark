# Redis Cache Benchmark

A small Flask API backed by Redis, built to measure the actual latency and
throughput difference caching makes on a slow endpoint.

## What it does

`GET /product/<id>` simulates a slow database call (`time.sleep(1)`). The
first request for a given `id` is a cache miss: it pays the full 1-second
cost, then stores the result in Redis with a 30-second TTL. Any request for
the same `id` within that window is a cache hit and skips the slow path
entirely (cache-aside pattern).

## Stack

- Flask (API)
- Redis (cache)
- Docker Compose (runs both together)

## Running it

```bash
docker compose up --build
```

The API is then available at `http://localhost:5000/product/<id>`.

## Benchmark results

Measured with `benchmark.py` (50 sequential requests per scenario) against the
app running under `docker compose` on Windows (Docker Desktop), with Redis
flushed before the run. Raw output: [`benchmark_results.txt`](benchmark_results.txt).

| Scenario | p50 | p95 | p99 | Throughput |
|---|---|---|---|---|
| Cached (same id, repeated) | 12.0 ms | 24.0 ms | 59.4 ms | 69.51 req/s |
| Uncached (unique id every request) | 1017.0 ms | 1030.5 ms | 1046.0 ms | 0.98 req/s |

Cached p50 latency is **84.6x faster** than uncached. The uncached scenario
forces a cache miss on every request by hitting a new product id each time,
so every request pays the simulated 1-second database call; the cached
scenario reflects repeated lookups of the same, popular item.

Reproduce it yourself:

```bash
docker compose up --build -d   # start Flask + Redis
python benchmark.py            # in another terminal
```

## Design notes

- **Cache-aside over write-through/read-through:** the app checks Redis
  first and only computes+stores on a miss, keeping Redis fully optional to
  the app's correctness — if Redis is down, `redis_client.get()` would need
  a try/except to fail open to the slow path (not yet added; see below).
- **TTL of 30s:** bounds how stale a cached response can get without needing
  explicit invalidation logic. A real product catalog would tune this per
  how often prices/stock actually change.
- **`REDIS_HOST` env var:** defaults to `localhost` for running the Flask
  app natively, overridden to `redis` (the Compose service name) when run
  via `docker-compose.yml`, so the same code works in both setups.


## Known limitations / next steps

- No fallback if Redis is unreachable (would currently raise instead of
  degrading to the slow path).
- Benchmark is a simple sequential script, not a concurrent load test — it
  measures per-request latency accurately but not behavior under concurrent
  load (a tool like Locust would be the next step for that).
- No cache stampede protection (many simultaneous misses for the same key
  would all hit the slow path at once).
