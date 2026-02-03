"""
management/commands/seed_data_faker.py

Generates realistic test data for the housing portal.
Targets: ~50 offices, ~200 agents, ~3000 properties, ~6000 images.

Run it:
    docker compose exec backend python manage.py seed_data

Run it with a fresh start (clears existing data first):
    docker compose exec backend python manage.py seed_data --flush
"""

import random
from django.core.management.base import BaseCommand
from faker import Faker
from housing.models import Location, Office, Agent, Property, PropertyImage

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with realistic housing data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing data...")
            PropertyImage.objects.all().delete()
            Property.objects.all().delete()
            Agent.objects.all().delete()
            Office.objects.all().delete()
            Location.objects.all().delete()

        # --- Locations ---
        # A fixed set of realistic cities. Properties will be distributed across these.
        cities = [
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
        locations = Location.objects.bulk_create(
            [
                Location(city=city, state=state, zip_code=zip_code)
                for city, state, zip_code in cities
            ]
        )
        self.stdout.write(f"Created {len(locations)} locations.")

        # --- Offices ---
        offices = Office.objects.bulk_create(
            [
                Office(
                    name=f"{fake.last_name()} Realty",
                    address=fake.street_address(),
                    city=random.choice(cities)[0],
                    phone=fake.phone_number(),
                )
                for _ in range(50)
            ]
        )
        self.stdout.write(f"Created {len(offices)} offices.")

        # --- Agents ---
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
        self.stdout.write(f"Created {len(agents)} agents.")

        # --- Properties ---
        # bulk_create sends a single INSERT statement instead of 3000 individual ones.
        # Without it, this loop would take minutes. With it, seconds.
        properties = Property.objects.bulk_create(
            [
                Property(
                    title=f"{random.choice(['Cozy', 'Modern', 'Luxury', 'Spacious', 'Charming', 'Stunning'])} "
                    f"{random.choice(['Apartment', 'House', 'Villa', 'Studio', 'Condo'])} "
                    f"in {random.choice(locations).city}",
                    description=fake.paragraph(nb_sentences=3),
                    property_type=random.choice(
                        ["apartment", "house", "villa", "studio", "condo"]
                    ),
                    price=round(random.uniform(100000, 2500000), 2),
                    bedrooms=random.randint(1, 6),
                    bathrooms=random.randint(1, 4),
                    location=random.choice(locations),
                    agent=random.choice(agents),
                    status=random.choices(
                        ["available", "pending", "sold"],
                        weights=[70, 20, 10],  # 70% available, 20% pending, 10% sold
                        k=1,
                    )[0],
                    view_count=random.randint(0, 500),
                    is_published=random.choices([True, False], weights=[90, 10], k=1)[
                        0
                    ],
                )
                for _ in range(3000)
            ]
        )
        self.stdout.write(f"Created {len(properties)} properties.")

        # --- Property Images ---
        # Each property gets 1-4 images. The first one (display_order=0) is the cover.
        # cdn_url and thumbnail_url are left null — they represent the "not yet processed"
        # state. The image caching section of this series fills them in.
        images = []
        for prop in properties:
            num_images = random.randint(1, 4)
            for order in range(num_images):
                images.append(
                    PropertyImage(
                        listing=prop,
                        original_url=f"https://picsum.photos/seed/{prop.id}-{order}/800/600",
                        thumbnail_url=None,  # Lazy — generated on first request (later)
                        cdn_url=None,  # Not pushed to CDN yet (later)
                        display_order=order,
                        alt_text=f"{prop.property_type} listing image {order + 1}",
                    )
                )

        PropertyImage.objects.bulk_create(images, batch_size=1000)
        self.stdout.write(f"Created {len(images)} property images.")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
