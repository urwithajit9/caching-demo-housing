Here is the comprehensive content for your `docs/parts/part-2-db-design.md`. This is written to serve as both an instructional guide for your readers and a professional reference for your project.

---

# Part 2: Database Design & The "Source of Truth"

## 1. Why Design Before Coding?

As an advanced developer, jumping straight into `models.py` is a trap. Database schema changes are "expensive"—they require migrations, data backfilling, and often break frontend API contracts.

**The Benefits of "Design-First":**

* **Source of Truth:** A visual diagram acts as a contract between the Backend (API) and Frontend (Data fetching).
* **Performance Foresight:** You can plan **Indexes** and **Relationships** (Foreign Keys) before the data becomes a bottleneck.
* **Reduced Refactoring:** Identifying a missing 1-to-Many relationship on a diagram takes 10 seconds; doing it after 50,000 rows are inserted takes hours of engineering.

---

## 2. Our Toolchain: DBML & dbdiagram.io

Instead of proprietary binaries, we use **DBML (Database Markup Language)**. It is an open-source DSL (Domain Specific Language) that allows you to define schemas as code.

* **Tool:** [dbdiagram.io](https://dbdiagram.io)
* **Format:** `.dbml` (Stored in `docs/architecture/`)

### Why DBML?

* **Version Control:** You can `git diff` your database structure changes.
* **Agnostic:** It doesn't care if you use Postgres or MySQL; it focuses on the logic.
* **Automation:** Most modern tools can export DBML directly to the `CREATE TABLE` SQL scripts you need for production.

---

## 3. Architecture Implementation Instructions

### Step 1: Create the Design File

Create a new file example `docs/architecture/schema.dbml` or `docs/parts/part-2-data/schema.dbml` and paste the following structure. This represents our Housing Portal's core entities.

```dbml
// =============================================
// PART 2: The Naive Baseline
// Zero indexes (except PKs). No optimizations.
// Everything here is a deliberate slow path.
// =============================================

Table locations {
  id integer [primary key, increment]
  city varchar [not null]
  state varchar(2)
  zip_code varchar(10)
  country varchar [default: 'US']

  // NO indexes. City searches will full-table-scan.
  // We add the index in Part 3 and show the difference.
}

Table offices {
  id integer [primary key, increment]
  name varchar [not null]
  address varchar
  city varchar
  phone varchar

  // Second hop in the N+1 chain: Property → Agent → Office
}

Table agents {
  id integer [primary key, increment]
  name varchar [not null]
  email varchar
  phone varchar
  office_id integer [not null]

  // First hop in the N+1 chain: Property → Agent
  // No index on office_id. Every agent→office lookup is a scan.
}

Ref: agents.office_id > offices.id

Table properties {
  id integer [primary key, increment]
  title varchar [not null]
  description text
  property_type varchar [not null, note: 'Apartment, House, Villa, Studio, Condo']
  price decimal(12,2) [not null]
  bedrooms integer [default: 1]
  bathrooms integer [default: 1]
  location_id integer [not null]
  agent_id integer [not null]
  status varchar [default: 'available', note: 'available, pending, sold — cache invalidation target']
  view_count integer [default: 0, note: 'Cache-aside pattern target. Hot read, rare write.']
  is_published boolean [default: true]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  // NO indexes beyond PK.
  // price, property_type, location_id, agent_id, status —
  // all filtered by the frontend. All full-table-scans right now.
  // That's the point. Part 3 fixes it.
}

Ref: properties.location_id > locations.id
Ref: properties.agent_id > agents.id

// =============================================
// IMAGE LAYER
// This is the surface for image caching,
// CDN integration (Cloudinary / ImageKit),
// and thumbnail/placeholder strategies.
// =============================================

Table property_images {
  id integer [primary key, increment]
  property_id integer [not null]
  original_url varchar [not null, note: 'The raw uploaded image URL']
  thumbnail_url varchar [note: 'Generated thumbnail. Null until first request (lazy).']
  cdn_url varchar [note: 'The CDN-served URL after upload to Cloudinary/ImageKit. Null until processed.']
  display_order integer [default: 0, note: 'Sort order on the listing page. 0 = cover image.']
  alt_text varchar
  created_at timestamp [default: `now()`]

  // No index on property_id.
  // Fetching images for a listing page = full scan on this table.
  // Another thing Part 3 fixes.
}

Ref: property_images.property_id > properties.id

```

### Step 2: Visualizing the Relationships

Upload this code to `dbdiagram.io`. You should see the following relationship:

* **One-to-Many:** One `Location` (e.g., New York) can have many `Properties`.

---

## 4. Troubleshooting & Advanced Tips

### Common Beginner Issue: "Flat Tables"

Many beginners put `city` and `state` directly inside the `Property` table.

* **The Problem:** If you have 50,000 properties in "New York," and you decide to rename it "NYC," you have to update 50,000 rows.
* **The Solution (Normalization):** By using a `Location` table, you update one row, and all 50,000 properties stay consistent.

### Advanced Tip: Composite Indexes

Notice the index `(price, property_type)` in our DBML. This is a **Composite Index**. Since our users will likely search for *"Apartments under $2000"*, this index allows Postgres to find those results in one pass rather than scanning two separate lists.

---

## 5. Next Steps

Now that our "Source of Truth" is documented:

1. Translate the DBML into Django `models.py`.
2. Run `makemigrations`.
3. **Part 2.5:** Write the Seeding Engine to fill these tables with 50,000 listings.

**Would you like me to generate the `seed_data.py` script now to match this new schema?**