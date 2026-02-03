"""
management/commands/seed_data.py

Generates realistic test data for the housing portal.
Combines Faker realism with batched bulk_create for performance.

Targets:
    10 locations (real US cities)
    50 offices
    200 agents
    5,000 properties
    ~10,000 images (1-4 per property)

Usage:
    # First run (or any time you want a clean slate):
    docker compose exec backend python manage.py seed_data --flush

    # Add more data on top of what's already there:
    docker compose exec backend python manage.py seed_data

    # Custom property count:
    docker compose exec backend python manage.py seed_data --flush --count 10000
"""

import random
from django.core.management.base import BaseCommand
from faker import Faker
from housing.models import Location, Office, Agent, Property, PropertyImage

fake = Faker()

# How many properties to create per INSERT statement.
# 5000 is the sweet spot: large enough to be fast, small enough
# to not blow memory on a laptop.
BATCH_SIZE = 5000

# Realistic US cities for the locations table.
# We use a fixed list instead of Faker here because we want
# properties distributed across a known, small set of cities.
# That makes the "filter by city" query interesting — each city
# has hundreds of results, not one.
CITIES = [
    ("Seattle", "WA", "98101"),
    ("Portland", "OR", "97201"),
    ("San Francisco", "CA", "94102"),
    ("Los Angeles", "CA", "90001"),
    ("Austin", "TX", "78701"),
    ("Denver", "CO", "80201"),
    ("Chicago", "IL", "60601"),
    ("Miami", "FL", "33101"),
    ("New York", "NY", "10001"),
    ("Boston", "MA", "02101"),
]

PROPERTY_TYPES = ["apartment", "house", "villa", "studio", "condo"]

# Adjectives for property titles. Combined with type and city,
# these produce titles like "Cozy Apartment in Seattle" —
# realistic enough to not look like test data at a glance.
TITLE_ADJECTIVES = [
    "Cozy",
    "Modern",
    "Luxury",
    "Spacious",
    "Charming",
    "Stunning",
    "Elegant",
    "Rustic",
    "Urban",
    "Bright",
    "Quiet",
    "Vibrant",
    "Classic",
    "Contemporary",
    "Peaceful",
]


class Command(BaseCommand):
    help = "Seed the database with realistic housing data. Use --flush to clear first."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing data before seeding. Use this for a clean slate.",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=5000,
            help="Number of properties to create. Default: 5000.",
        )

    def handle(self, *args, **options):
        target_count = options["count"]
        flush = options["flush"]

        # ------------------------------------------------------------------
        # FLUSH — wipe everything if requested.
        # Order matters: delete children before parents, or FK constraints
        # will reject the delete.
        # ------------------------------------------------------------------
        if flush:
            self.stdout.write("Flushing existing data...")
            PropertyImage.objects.all().delete()
            Property.objects.all().delete()
            Agent.objects.all().delete()
            Office.objects.all().delete()
            Location.objects.all().delete()
            self.stdout.write("Done. Database is empty.")

        # ------------------------------------------------------------------
        # LOCATIONS
        # bulk_create returns the created objects WITH their auto-generated
        # IDs — but only on PostgreSQL. SQLite doesn't support this.
        # We're on PostgreSQL, so this works. On SQLite, you'd need to
        # re-fetch: locations = list(Location.objects.all())
        # ------------------------------------------------------------------
        self.stdout.write("Creating locations...")
        locations = Location.objects.bulk_create(
            [
                Location(city=city, state=state, zip_code=zip_code)
                for city, state, zip_code in CITIES
            ]
        )
        self.stdout.write(f"  {len(locations)} locations created.")

        # ------------------------------------------------------------------
        # OFFICES
        # ------------------------------------------------------------------
        self.stdout.write("Creating offices...")
        offices = Office.objects.bulk_create(
            [
                Office(
                    name=f"{fake.last_name()} Realty",
                    address=fake.street_address(),
                    city=random.choice(CITIES)[0],
                    phone=fake.phone_number(),
                )
                for _ in range(50)
            ]
        )
        self.stdout.write(f"  {len(offices)} offices created.")

        # ------------------------------------------------------------------
        # AGENTS
        # Each agent belongs to a random office. This is the first hop
        # in the N+1 chain we'll demonstrate in Part 3.
        # ------------------------------------------------------------------
        self.stdout.write("Creating agents...")
        agents = Agent.objects.bulk_create(
            [
                Agent(
                    name=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    office=random.choice(offices),
                )
                for _ in range(200)
            ]
        )
        self.stdout.write(f"  {len(agents)} agents created.")

        # ------------------------------------------------------------------
        # PROPERTIES — the big one.
        # We batch this into chunks of BATCH_SIZE to avoid loading
        # 5000+ objects into memory at once. Each batch is a single
        # INSERT statement. The loop prints progress so you know it's
        # not hanging.
        # ------------------------------------------------------------------
        self.stdout.write(
            f"Creating {target_count} properties (batch size: {BATCH_SIZE})..."
        )
        created_properties = []

        for batch_start in range(0, target_count, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, target_count)
            batch = []

            for i in range(batch_start, batch_end):
                prop_type = random.choice(PROPERTY_TYPES)
                city = random.choice(locations)

                batch.append(
                    Property(
                        title=f"{random.choice(TITLE_ADJECTIVES)} {prop_type.capitalize()} in {city.city}",
                        description=fake.paragraph(nb_sentences=random.randint(2, 4)),
                        property_type=prop_type,
                        price=round(random.uniform(85000, 3200000), 2),
                        bedrooms=random.randint(1, 6),
                        bathrooms=random.randint(1, 4),
                        location=city,
                        agent=random.choice(agents),
                        status=random.choices(
                            ["available", "pending", "sold"],
                            weights=[70, 20, 10],  # Realistic distribution
                            k=1,
                        )[0],
                        view_count=random.randint(0, 1200),
                        is_published=random.choices(
                            [True, False], weights=[90, 10], k=1
                        )[0],
                    )
                )

            created = Property.objects.bulk_create(batch)
            created_properties.extend(created)
            self.stdout.write(f"  {batch_end}/{target_count} properties created...")

        self.stdout.write(f"  {len(created_properties)} properties total.")

        # ------------------------------------------------------------------
        # PROPERTY IMAGES — every property gets 1-4 images.
        #
        # display_order = 0 is the cover image (shown on listing cards).
        # The rest load when the user clicks into the listing.
        #
        # cdn_url and thumbnail_url are intentionally null. They represent
        # the "not yet processed" state. The image caching section of
        # this series fills them in. This is lazy processing — the
        # optimization doesn't exist until demand creates it.
        #
        # We use picsum.photos with a seed parameter so the URLs are
        # deterministic — same property always gets the same images.
        # That makes debugging easier.
        #
        # Batched at 1000 per INSERT because the image count is
        # roughly 2x the property count.
        # ------------------------------------------------------------------
        self.stdout.write("Creating property images...")
        image_batch = []
        total_images = 0

        for prop in created_properties:
            num_images = random.randint(1, 4)

            for order in range(num_images):
                image_batch.append(
                    PropertyImage(
                        listing=prop,
                        original_url=f"https://picsum.photos/seed/{prop.id}-{order}/800/600",
                        thumbnail_url=None,  # Lazy — filled in during the image caching part
                        cdn_url=None,  # Not pushed to CDN yet — same
                        display_order=order,
                        alt_text=f"{prop.property_type} listing photo {order + 1}",
                    )
                )

            # Flush the batch every 1000 images to avoid memory pressure
            if len(image_batch) >= 1000:
                PropertyImage.objects.bulk_create(image_batch)
                total_images += len(image_batch)
                image_batch = []

        # Flush any remaining images that didn't hit the 1000 threshold
        if image_batch:
            PropertyImage.objects.bulk_create(image_batch)
            total_images += len(image_batch)

        self.stdout.write(f"  {total_images} images created.")

        # ------------------------------------------------------------------
        # DONE — print the summary
        # ------------------------------------------------------------------
        self.stdout.write("─" * 50)
        self.stdout.write(self.style.SUCCESS("Seeding complete. Summary:"))
        self.stdout.write(f"  Locations:  {len(locations)}")
        self.stdout.write(f"  Offices:    {len(offices)}")
        self.stdout.write(f"  Agents:     {len(agents)}")
        self.stdout.write(f"  Properties: {len(created_properties)}")
        self.stdout.write(f"  Images:     {total_images}")
        self.stdout.write("─" * 50)


# Flush the messy mixed data, then re-seed cleanly with 5000 properties
# docker compose exec backend python manage.py seed_data --flush
# docker compose exec backend python manage.py seed_data --flush --count 10000
"""
docker compose exec db psql -U user -d housing_db -c "
    SELECT relname AS table_name, n_live_tup AS row_count
    FROM pg_stat_user_tables
    WHERE schemaname = 'public' AND relname LIKE 'housing_%'
    ORDER BY relname;
"
```

You should see something close to this:
```
        table_name         | row_count
---------------------------+-----------
 housing_agent             |       200
 housing_location          |        10
 housing_office            |        50
 housing_property          |      5000
 housing_propertyimage     |     ~10000
 """
