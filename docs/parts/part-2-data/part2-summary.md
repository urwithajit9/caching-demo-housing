
# Part 2: Data Architecture (Naive Baseline)

## 1. Design Philosophy: The "Slow Path"

In this phase, we are intentionally building a **Naive Baseline**. We have excluded all non-primary key indexes to create a performance "floor." This allows us to measure the raw impact of large datasets on unoptimized queries before we introduce Redis and PostgreSQL indexing in later parts.

### Key Intentions:

* **Full Table Scans:** Without indexes on fields like `price` or `city`, PostgreSQL must scan every row to find matches.
* **N+1 Demonstration:** We've built a relationship chain (`Property` -> `Agent` -> `Office`) that will trigger dozens of database hits per request if not handled with `select_related`.
* **Cache Invalidation Targets:** Fields like `view_count` and `status` are included to test high-write frequency and cache consistency.

---

## 2. Entity Relationship Diagram (ERD)

The schema was designed using **DBML** to ensure a language-agnostic "Source of Truth" for both Frontend and Backend teams.

---

## 3. Data Models

The implementation in `housing/models.py` follows the normalized structure defined in our DBML.

### Core Tables:

* **Location:** Geographic data (City, State, Zip).
* **Office:** Real estate branch details.
* **Agent:** Contact info linked to an Office.
* **Property:** The main entity containing price, type, and status.
* **PropertyImage:** Associated media with a `best_url` logic for CDN fallbacks.

> **Note:** We use `@builtins.property` for the `best_url` method in the `PropertyImage` model to avoid naming collisions with the `property` ForeignKey.

---

## 4. Environment & Persistence

To ensure data survives container restarts, we use a **Docker Volume** mapped to the PostgreSQL data directory.

### Environment Variables (.env)

We use `django-environ` to keep secrets out of the codebase. Key variables include:

* `DATABASE_URL`: `postgres://user:password@db:5432/housing_db`
* `REDIS_URL`: `redis://redis:6379`

---

## 5. Seeding Strategy

To simulate a real-world production environment, we use a custom management command:
`python manage.py seed_data`

**The Seed Engine generates:**

1. **100** Locations
2. **50** Offices
3. **200** Agents
4. **50,000** Properties (Distributed randomly)
5. **~125,000** Property Images

**Optimization Note:** The seeder uses `bulk_create` in batches of 5,000 to prevent memory exhaustion within the Docker container while maintaining high insertion speeds.

---

## 6. Troubleshooting

* **Permission Denied:** If migrations created inside Docker cannot be edited locally, run: `sudo chown -R $USER:$USER backend/housing/migrations/`
* **Database Connection Refused:** Ensure the `.env` uses `db` as the host when running inside Docker, but `localhost` if running management commands from your host machine.

---

