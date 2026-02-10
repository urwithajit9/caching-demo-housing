import random
import time
import requests
from django.core.management.base import BaseCommand
from faker import Faker
import cloudinary.uploader


from housing.models import Location, Office, Agent, Property, PropertyImage

fake = Faker()

BATCH_SIZE = 5000

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
    help = "Seed database with realistic housing data (Cloudinary-enabled)."

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true")
        parser.add_argument("--count", type=int, default=5000)

    def handle(self, *args, **options):
        target_count = options["count"]
        flush = options["flush"]

        if flush:
            self.stdout.write("Flushing existing data...")
            PropertyImage.objects.all().delete()
            Property.objects.all().delete()
            Agent.objects.all().delete()
            Office.objects.all().delete()
            Location.objects.all().delete()
            self.stdout.write("Database cleared.")

        # ------------------------------------------------------------------
        # LOCATIONS
        # ------------------------------------------------------------------
        locations = Location.objects.bulk_create(
            [
                Location(city=city, state=state, zip_code=zip_code)
                for city, state, zip_code in CITIES
            ]
        )

        # ------------------------------------------------------------------
        # OFFICES
        # ------------------------------------------------------------------
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

        # ------------------------------------------------------------------
        # AGENTS
        # ------------------------------------------------------------------
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

        # ------------------------------------------------------------------
        # PROPERTIES (bulk)
        # ------------------------------------------------------------------
        self.stdout.write(f"Creating {target_count} properties...")
        created_properties = []

        for start in range(0, target_count, BATCH_SIZE):
            batch = []
            end = min(start + BATCH_SIZE, target_count)

            for _ in range(start, end):
                city = random.choice(locations)
                prop_type = random.choice(PROPERTY_TYPES)

                batch.append(
                    Property(
                        title=f"{random.choice(TITLE_ADJECTIVES)} {prop_type.capitalize()} in {city.city}",
                        description=fake.paragraph(nb_sentences=random.randint(2, 4)),
                        property_type=prop_type,
                        price=round(random.uniform(85_000, 3_200_000), 2),
                        bedrooms=random.randint(1, 6),
                        bathrooms=random.randint(1, 4),
                        location=city,
                        agent=random.choice(agents),
                        status=random.choices(
                            ["available", "pending", "sold"], weights=[70, 20, 10]
                        )[0],
                        view_count=random.randint(0, 1200),
                        is_published=random.choices([True, False], weights=[90, 10])[0],
                    )
                )

            created = Property.objects.bulk_create(batch)
            created_properties.extend(created)
            self.stdout.write(f"  {len(created_properties)}/{target_count}")

        # ------------------------------------------------------------------
        # PROPERTY IMAGES (Cloudinary uploads)
        # ------------------------------------------------------------------
        self.stdout.write("Uploading property images to Cloudinary...")
        total_images = 0

        for prop in created_properties:
            num_images = random.randint(1, 4)

            for order in range(num_images):
                seed = prop.id * 1000 + order
                source_url = f"https://picsum.photos/seed/{seed}/800/600"

                img = PropertyImage(
                    listing=prop,
                    display_order=order,
                    alt_text=f"{prop.property_type} listing image {order + 1}",
                )

                # # CloudinaryField accepts file-like objects or URLs
                # img.image = source_url

                # # Deterministic public_id for idempotency
                # img.image.public_id = f"property_{prop.id}_{order}"

                # img.save()
                upload_result = cloudinary.uploader.upload(
                source_url,
                public_id=f"property_{prop.id}_{order}",
                overwrite=True,
                folder="properties",
                )

                PropertyImage.objects.create(
                    listing=prop,
                    image=upload_result["public_id"],
                    display_order=order,
                    alt_text=f"{prop.property_type} listing image {order + 1}",
                )
                total_images += 1

                # Light throttling to avoid Cloudinary rate limits
                if total_images % 25 == 0:
                    time.sleep(0.3)

        # ------------------------------------------------------------------
        # SUMMARY
        # ------------------------------------------------------------------
        self.stdout.write("─" * 50)
        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(f"Locations:  {len(locations)}")
        self.stdout.write(f"Offices:    {len(offices)}")
        self.stdout.write(f"Agents:     {len(agents)}")
        self.stdout.write(f"Properties: {len(created_properties)}")
        self.stdout.write(f"Images:     {total_images}")
        self.stdout.write("─" * 50)
