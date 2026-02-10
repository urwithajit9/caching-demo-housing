"""
housing/management/commands/migrate_images_to_cloudinary.py

Management command to migrate existing PropertyImage records from picsum.photos URLs
to actual Cloudinary uploads.

This is a one-time migration for users who:
1. Ran the seed_data command from Part 2 (which created picsum.photos URLs)
2. Now want to migrate to Cloudinary without losing the seeded images

Usage:
    docker compose exec backend python manage.py migrate_images_to_cloudinary

Options:
    --limit N       Only migrate N images (for testing)
    --dry-run       Show what would happen without actually uploading
    --batch-size N  Process N images at a time (default: 10)
"""

from django.core.management.base import BaseCommand
from housing.models import PropertyImage
import requests
import cloudinary
import cloudinary.uploader
from io import BytesIO
from time import sleep
import sys


class Command(BaseCommand):
    help = "Migrate existing PropertyImage URLs from picsum.photos to Cloudinary"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limit the number of images to migrate (for testing)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be migrated without actually uploading",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=10,
            help="Number of images to process in each batch",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip images that already have Cloudinary URLs",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        dry_run = options["dry_run"]
        batch_size = options["batch_size"]
        skip_existing = options["skip_existing"]

        # Find all PropertyImage records that need migration
        # Old schema had 'original_url' as URLField
        # New schema has 'image' as CloudinaryField
        # Records from seed command have original_url but image=None

        # Query images that need migration
        queryset = PropertyImage.objects.all()

        if skip_existing:
            # Skip images that already have Cloudinary image field populated
            queryset = queryset.filter(image="")

        total_count = queryset.count()

        if limit:
            queryset = queryset[:limit]
            total_count = min(total_count, limit)

        if total_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ No images need migration!"))
            return

        self.stdout.write(self.style.WARNING(f"Found {total_count} images to migrate"))

        if dry_run:
            self.stdout.write(
                self.style.NOTICE("DRY RUN - No actual uploads will occur")
            )
            for img in queryset[:10]:  # Show first 10
                self.stdout.write(
                    f"  Would migrate: Property {img.listing_id} - Image {img.id}"
                )
            if total_count > 10:
                self.stdout.write(f"  ... and {total_count - 10} more")
            return

        # Confirm before proceeding
        confirm = input(
            f"\nThis will upload {total_count} images to Cloudinary. Continue? (y/N): "
        )
        if confirm.lower() != "y":
            self.stdout.write(self.style.ERROR("Migration cancelled"))
            return

        # Process in batches
        success_count = 0
        error_count = 0
        skipped_count = 0

        for i, img in enumerate(queryset.iterator()):
            progress = f"[{i+1}/{total_count}]"

            # If the image field is already populated, skip
            if skip_existing and img.image:
                self.stdout.write(
                    f"{progress} Skipping (already migrated): Image {img.id}"
                )
                skipped_count += 1
                continue

            try:
                # For seed data, we need to generate a picsum URL
                # The seed command created images but didn't populate original_url in the new schema
                # We'll create a new image URL based on the property ID
                property_id = img.listing_id
                image_seed = property_id * 1000 + img.display_order
                picsum_url = f"https://picsum.photos/seed/{image_seed}/800/600"

                self.stdout.write(f"{progress} Downloading: {picsum_url}")

                # Download the image from picsum
                response = requests.get(picsum_url, timeout=30)
                response.raise_for_status()

                # Upload to Cloudinary
                image_file = BytesIO(response.content)

                self.stdout.write(f"{progress} Uploading to Cloudinary...")

                result = cloudinary.uploader.upload(
                    image_file,
                    folder="housing/properties",
                    public_id=f"property_{property_id}_{img.display_order}",
                    overwrite=True,
                    resource_type="image",
                    transformation={
                        "quality": "auto",
                        "fetch_format": "auto",
                    },
                )

                # Update the PropertyImage record
                # The CloudinaryField will handle storing the URL properly
                img.image = result["public_id"]
                img.save()

                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"{progress} ✅ Migrated Image {img.id}")
                )

                # Rate limiting: sleep between requests to avoid overwhelming picsum.photos
                if (i + 1) % batch_size == 0:
                    self.stdout.write(
                        f"Processed {i + 1} images. Pausing for 2 seconds..."
                    )
                    sleep(2)

            except requests.RequestException as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"{progress} ❌ Download failed for Image {img.id}: {e}"
                    )
                )
                continue

            except cloudinary.exceptions.Error as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"{progress} ❌ Cloudinary upload failed for Image {img.id}: {e}"
                    )
                )
                continue

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"{progress} ❌ Unexpected error for Image {img.id}: {e}"
                    )
                )
                continue

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Successfully migrated: {success_count} images")
        )
        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"⏭️  Skipped (already migrated): {skipped_count} images"
                )
            )
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"❌ Failed: {error_count} images"))
        self.stdout.write("=" * 60)

        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    "\nYou can re-run this command to retry failed images."
                )
            )
