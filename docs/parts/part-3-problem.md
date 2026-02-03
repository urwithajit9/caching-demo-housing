# Part 3: The Caching "Quick Win" & The N+1 Problem

In this phase, we moved from a static database to a live API. We deliberately implemented a **"Naive API"** to demonstrate how easily a Django application can become bottlenecked by database I/O, and how Redis can be used as a high-speed "short-circuit."

## 1. The Performance "Villains"

Before applying the fix, we identified two major performance killers in our architecture:

### A. The N+1 Query Trap

Our `PropertySerializer` nests `AgentSerializer`, which in turn nests `OfficeSerializer`.

* **The Request:** 1 Query to fetch 20 Properties.
* **The Fallout:** For *each* property, Django executes a query for the Agent, and another for the Office.
* **Total:** 1 + 20 + 20 = **41 Database Queries** just to render 20 rows of JSON.

### B. The Sequential Scan

With 50,000 records and no indexes on `created_at` or `price`, PostgreSQL is forced to perform a **Sequential Scan**. It reads every single row from the disk into memory to find the latest 20 properties.

---

## 2. Implementation Details

### The "Naive" API Surface

We built a standard REST endpoint at `/api/properties/`.

* **Serializer:** Nested relationships without optimization.
* **View:** Standard `ListAPIView` using the default manager.

### The Redis Plumbing

We integrated `django-redis` to handle our caching layer. This required a specific configuration in `settings.py` to support connection pooling and avoid the `CLIENT_CLASS` mismatch error found in native Django 5.0 Redis backends.

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
    }
}

```

---

## 3. The Solution: Per-View Caching

We applied the `@cache_page(60)` decorator. This captures the **entire HTTP response** and stores it as a binary string in Redis.

* **Cache Miss (Request 1):** Django runs all 41 SQL queries → Serializes to JSON → Saves to Redis → Returns to User.
* **Cache Hit (Request 2-100):** Redis identifies the URL key → Returns the JSON string directly. **The Database is never touched.**

---

## 4. Benchmarking the Difference

| Metric | Baseline (PostgreSQL) | Cached (Redis) |
| --- | --- | --- |
| **Average Latency** | **60ms - 80ms** | **2ms - 5ms** |
| **SQL Queries** | 41 | 0 |
| **Serialization Overhead** | High (Every request) | None (Pre-serialized) |

---

## 5. The "New" Problem: Cache Invalidation

While we achieved a **95%+ speed increase**, we introduced **Data Staleness**.

> **The Problem:** If a Property's price is updated in the database, the API will continue to serve the old price until the 60-second TTL (Time To Live) expires.

This sets the stage for **Part 4**, where we will move away from "Blunt Caching" (caching the whole page) to "Granular Caching" (invalidating specific objects when they change).

---

