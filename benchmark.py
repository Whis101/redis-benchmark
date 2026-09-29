"""
Benchmarks the /product/<id> endpoint under two conditions:
  - cached:   repeated requests for the same product id (Redis cache hits)
  - uncached: requests for unique product ids every time (forces cache misses,
              simulating the slow "DB" path on every request)

Reports p50/p95/p99 latency and throughput for each, computed only from
latencies actually measured against a running server -- no estimated numbers.
"""
import time
import statistics
import urllib.request

BASE_URL = "http://127.0.0.1:5000"
N_REQUESTS = 50


def timed_get(url):
    start = time.perf_counter()
    with urllib.request.urlopen(url) as resp:
        resp.read()
    return time.perf_counter() - start


def percentile(data, pct):
    data = sorted(data)
    k = (len(data) - 1) * (pct / 100)
    f = int(k)
    c = min(f + 1, len(data) - 1)
    if f == c:
        return data[f]
    return data[f] + (data[c] - data[f]) * (k - f)


def run_scenario(name, urls):
    latencies = [timed_get(url) for url in urls]
    total_time = sum(latencies)
    throughput = len(urls) / total_time
    print(f"\n--- {name} ({len(urls)} requests) ---")
    print(f"  p50: {percentile(latencies, 50) * 1000:.1f} ms")
    print(f"  p95: {percentile(latencies, 95) * 1000:.1f} ms")
    print(f"  p99: {percentile(latencies, 99) * 1000:.1f} ms")
    print(f"  throughput: {throughput:.2f} req/s")
    return {
        "p50_ms": percentile(latencies, 50) * 1000,
        "p95_ms": percentile(latencies, 95) * 1000,
        "p99_ms": percentile(latencies, 99) * 1000,
        "throughput_rps": throughput,
    }


if __name__ == "__main__":
    # Warm the cache for product id 1
    timed_get(f"{BASE_URL}/product/1")

    cached_results = run_scenario(
        "CACHED (same id, repeated)",
        [f"{BASE_URL}/product/1" for _ in range(N_REQUESTS)],
    )

    uncached_results = run_scenario(
        "UNCACHED (unique id every request -> forced cache miss)",
        [f"{BASE_URL}/product/{2000 + i}" for i in range(N_REQUESTS)],
    )

    speedup = uncached_results["p50_ms"] / cached_results["p50_ms"]
    print(f"\nCached p50 is {speedup:.1f}x faster than uncached p50.")
