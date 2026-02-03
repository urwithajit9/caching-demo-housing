## 2. `docs/parts/part-1-setup.md`

### *Part 1: Building the Foundation (The Baseline)*

#### 2.1 The Goal

The objective of Part 1 is to establish a "Baseline." A baseline is a version of the application that works correctly but is intentionally unoptimized. We need this to measure the "before and after" performance impact of our caching strategies.

#### 2.2 Containerization Strategy

We use Docker to solve the "Environmental Drift" problem. By containerizing our stack, we ensure that every developer—and eventually our production server—runs the exact same versions of Python, Node, and Postgres.

**Key Docker Patterns Used:**

* **Anonymous Volumes:** Used for `node_modules` to prevent the host machine from overwriting the container's specialized binaries.
* **Multi-Stage Builds (Preview):** Prepared for production to keep image sizes small (see `frontend/Dockerfile`).
* **Service Dependencies:** Using `depends_on` to ensure the database is available before the application attempts to connect.

#### 2.3 Challenges & Troubleshooting

During the setup of Part 1, we identified three critical areas where beginners and experts alike often stumble:

1. **Port Collisions:** The "Address already in use" error (5432/6379). This occurs when local services conflict with Docker services. The solution is to prioritize the Docker environment.
2. **Binary Mismatches:** Next.js SWC compiler issues on Alpine Linux. We resolved this by adding `libc6-compat` to the Alpine image.
3. **The "Hidden Folder" Trap:** How Docker volumes can inadvertently hide `node_modules`. We fixed this using explicit volume definitions in `docker-compose.yml`.

#### 2.4 Verification Checklist

Before moving to Part 2, the following must be true:

* [x] `docker compose ps` shows all 4 containers as "Running."
* [x] Django can connect to Postgres (`python manage.py dbshell`).
* [x] Next.js can resolve the Backend API.
* [x] Redis responds to a `PING` command.

---

### 🚀 Next Step: Transitioning to Part 2

With the foundation laid, we are ready to move from **Infrastructure** to **Data**.

**In the next part, we will:**

1. Design a normalized relational schema for `Properties`.
2. Implement a Python-based Seeding Engine to generate 50,000 realistic listings.
3. Observe the first "bottleneck" as we query the database without an index or a cache.

**Would you like me to start drafting the Django `models.py` for Part 2?**