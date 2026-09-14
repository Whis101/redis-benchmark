# Redis Caching Benchmark — Project Brief

Context captured from planning conversation on 2026-09-14, so this project can be picked up cold.

## Who this is for

CS + Math (data science concentration) undergrad, graduating May 2027, building resume/portfolio side-projects.

**Existing skills:** Python, SQL, C++, Java, HTML, Redis, Docker, Flask, pandas, matplotlib, Power BI, Tableau, Git.

**Skill gap being targeted:** comfortable writing code, but a beginner on systems/infra concepts (caching, Docker, performance benchmarking). Goal is not just working code but being able to explain the technology and design decisions out loud in an interview — teaching material matters as much as the code.

## Why this project

Redis/Docker/Flask are listed skills with nothing on the resume demonstrating them. A Redis-backed Flask caching demo with a real benchmark fills that gap.

## Hard constraint

**No fabricated, estimated, or "typical" numbers anywhere** — in code comments, README, study guide, or resume bullets. Only numbers that actually came out of running code on this machine. Every benchmark claim must be reproducible from an actual run.

## What "done" looks like

1. **Working code** — a Flask app backed by Redis caching, plus a Docker Compose setup.
2. **A benchmark script that is actually executed** to produce real measured latency/throughput numbers (not projected ones).
3. **`STUDY_GUIDE.md`** — beginner-friendly, no assumed prior knowledge. Should cover:
   - HTTP request/response cycle
   - What Redis is vs. an in-process dict vs. a CDN cache
   - TTL and staleness trade-offs
   - Docker / Docker Compose rationale
   - p50 / p95 / p99 and why percentiles are used over averages
   - Throughput, cache hit rate
   - Cache stampede
   - Production considerations: cache warming, monitoring
   - **Extra depth requested:** systems-design interview follow-ups — cache stampede mitigation, invalidation strategies, scaling caches — since the user wants to handle follow-up questions confidently, not just describe the base project.
4. **`README.md`** — separate, polished, for repo visitors, with a real-numbers results table from the actual benchmark run.
5. **Resume bullet options** — 2-3 drafts using only real measured numbers.
6. **Interview talking points** — 4-6 points on the actual design decisions made in this build.

## Standing template note

This project follows a repeatable workflow the user wants applied to *any* future "build me a portfolio project" request: present a short menu of quick (~1hr) quantifiable ideas with ATS-worthiness notes → build for real → study guide → README → resume bullets → interview talking points. This Redis project was the first (default) pick from that menu.

## Status as of 2026-09-14

Not yet built. This brief exists so the build can start from here.
