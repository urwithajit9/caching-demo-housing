## 1. `docs/architecture.md`

### *Chapter: The Blueprint of a Scalable Housing Portal*

#### 1.1 Introduction

The "Housing Caching Demo" is designed to simulate a high-traffic real estate marketplace. In such systems, the read-to-write ratio is often 100:1. Users spend hours searching and filtering, while property updates happen infrequently. This makes it the perfect candidate for a multi-layered caching strategy.

#### 1.2 The System Components

* **The Persistence Layer (PostgreSQL):** Chosen for its robust support of complex relational queries and indexing. In this project, it acts as the "Single Source of Truth."
* **The Cache Layer (Redis):** An in-memory data store used to alleviate the load on PostgreSQL. We use it for storing expensive API responses and session metadata.
* **The Backend API (Django + DRF):** Handles business logic, authentication, and database abstraction. It is designed to be "stateless" to allow horizontal scaling.
* **The Frontend UI (Next.js):** Utilizes the App Router to implement both Server-Side Rendering (SSR) and Client-Side Rendering (CSR), allowing us to demonstrate edge caching and request memoization.

#### 1.3 Communication Protocol

1. **Client-to-Frontend:** Standard HTTPS.
2. **Frontend-to-Backend:** Internal Docker networking (`http://backend:8000`). This reduces latency and keeps the API internal where possible.
3. **Backend-to-Services:** Django communicates with Postgres (Port 5432) and Redis (Port 6379) over the virtual bridge network created by Docker Compose.

---

