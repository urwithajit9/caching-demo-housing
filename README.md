# 🏠 Housing Caching Demo: Next.js + Django + Redis

A multi-part blog series demonstration on implementing multi-layer caching to scale a real estate portal. This project showcases how to move from a slow, database-heavy baseline to a high-performance system using Redis and Next.js Data Caching.

---

## 🏗 Project Architecture



- **Frontend:** Next.js 14 (App Router)
- **Backend:** Django 5.0 + Django REST Framework
- **Database:** PostgreSQL (Relational data & complex joins)
- **Cache:** Redis (Server-side speed)
- **Tooling:** Docker & Docker Compose

---

## 🚦 How to use this Repository

This project is versioned by **branches** corresponding to each blog post. This allows you to see the code evolve step-by-step.

1. **Part 1: The Baseline** (`branch: part-1-setup`)
   - The "slow" version. Raw DB queries, no caching.
2. **Part 2: Server-Side Caching** (`branch: part-2-drf-caching`)
   - Implementing Redis in Django & handling the "Thundering Herd."
3. **Part 3: Frontend Caching** (`branch: part-3-nextjs-caching`)
   - Leveraging Next.js Data Cache and Request Memoization.

**To jump to a specific part:**
```bash
git checkout part-1-setup

```

---

## 🛠 Setup Instructions (Part 1)

### 1. Prerequisites

* Docker & Docker Compose
* Git

### 2. Clone and Initialize

```bash
git clone [https://github.com/urwithajit9/caching-demo-housing.git](https://github.com/urwithajit9/caching-demo-housing.git)
cd caching-demo-housing
git checkout part-1-setup

```

### 3. Build and Launch

We use Docker to ensure the environment (Postgres/Redis) is identical for everyone.

```bash
docker-compose up --build

```

### 4. Database Seeding

Open a new terminal and generate 50,000 realistic property listings to test performance:

```bash
docker-compose exec backend python manage.py seed_data

```

---

## 🧪 Verification & Testing

| Service | URL | Purpose |
| --- | --- | --- |
| **Frontend** | http://localhost:3000 | Main User Interface |
| **API Root** | http://localhost:8000/api/ | DRF Browsable API |
| **Listings** | http://localhost:8000/api/properties/ | The "Slow" Endpoint |

### Testing the "Baseline" Slowness

In Part 1, visit the listings page. Open your **Browser DevTools > Network Tab**.

* You will notice the API request takes **300ms - 600ms**.
* This is the "Pain Point" we will solve in Part 2.

---

## 📂 Project Structure

```text
.
├── backend/                # Django + DRF
│   ├── core/               # Project settings & configuration
│   ├── housing/            # Real estate logic (models, views, api)
│   ├── manage.py           # Django CLI
│   └── requirements.txt    # Python dependencies (The "shopping list")
├── frontend/               # Next.js (App Router)
│   ├── app/                # UI pages and components
│   ├── public/             # Static assets
│   ├── next.config.ts      # Next.js configuration
│   ├── package.json        # Node.js dependencies
│   └── tsconfig.json       # TypeScript configuration
├── docker-compose.yml      # Orchestrates Postgres, Redis, and Apps
└── README.md               # Documentation

```



---

## 📈 Next Steps for Contributors

To add the next part of the tutorial:

1. Create a new branch from the previous part: `git checkout -b part-2-drf-caching`
2. Implement your caching logic.
3. Update the README locally if specific new environment variables are added.
4. Push to GitHub: `git push origin part-2-drf-caching`

```

---

### One-Click Setup Files
To make the above README work, ensure these two files are also in your root:

**1. `docker-compose.yml`** (Root)
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: housing_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/housing_db
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    depends_on:
      - backend

```

**2. `backend/Dockerfile**`

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

