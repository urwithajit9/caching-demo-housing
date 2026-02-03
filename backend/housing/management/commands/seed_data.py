import random
from django.core.management.base import BaseCommand
from django.db import transaction
from housing.models import Location, Office, Agent, Property, PropertyImage


class Command(BaseCommand):
    help = "Seeds the database with 50,000 properties and related data."

    def handle(self, *args, **options):
        self.stdout.write("Starting seeding process...")

        # 1. Cleanup existing data (Optional)
        # Location.objects.all().delete()
        # Office.objects.all().delete()

        # 2. Create Locations
        locations = [
            Location(city=f"City_{i}", state="NY", zip_code=f"100{i:02}")
            for i in range(100)
        ]
        Location.objects.bulk_create(locations)
        locations = list(Location.objects.all())

        # 3. Create Offices
        offices = [
            Office(name=f"RealEstate Office {i}", city="New York") for i in range(50)
        ]
        Office.objects.bulk_create(offices)
        offices = list(Office.objects.all())

        # 4. Create Agents
        agents = [
            Agent(name=f"Agent {i}", office=random.choice(offices)) for i in range(200)
        ]
        Agent.objects.bulk_create(agents)
        agents = list(Agent.objects.all())

        # 5. Create 50,000 Properties (The big one)
        self.stdout.write("Creating 50,000 properties...")
        property_types = ["Apartment", "House", "Villa", "Studio", "Condo"]

        # We use a loop to batch create to avoid memory issues
        BATCH_SIZE = 5000
        for i in range(0, 50000, BATCH_SIZE):
            props_to_create = []
            for j in range(BATCH_SIZE):
                props_to_create.append(
                    Property(
                        title=f"Property Listing {i + j}",
                        description="A beautiful home in a naive baseline database.",
                        property_type=random.choice(property_types),
                        price=random.randint(100000, 2000000),
                        location=random.choice(locations),
                        agent=random.choice(agents),
                        status="available",
                        view_count=random.randint(0, 1000),
                    )
                )
            Property.objects.bulk_create(props_to_create)
            self.stdout.write(f"Created {i + BATCH_SIZE} properties...")

        self.stdout.write(self.style.SUCCESS("Successfully seeded 50,000 properties!"))
