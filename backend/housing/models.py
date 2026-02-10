"""
housing/models.py

The data layer of the Housing Portal.

These models are INTENTIONALLY naive in Part 2. That's not a mistake —
it's the setup. Every missing index, every N+1 trap, every denormalized
field is a slow path that a later part of this series will fix with caching.

Read the comments. They tell you what's wrong and why we're leaving it
wrong on purpose.
"""

from django.db import models
import builtins
from cloudinary.models import CloudinaryField


# =============================================================================
# LOCATION
# A simple geographic unit. Properties belong to locations.
#
# NAIVE ON PURPOSE: No index on city, state, or zip_code.
# The listing page filters by city. Every filter = full table scan.
# Part 3 adds the index. We'll show the query plan before and after.
# =============================================================================
class Location(models.Model):
    city = models.CharField(max_length=100, db_index=False)  # No index. Intentional.
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default="US")

    class Meta:
        ordering = ["city"]
        verbose_name_plural = "locations"

    def __str__(self):
        return f"{self.city}, {self.state}"


# =============================================================================
# OFFICE
# Where an agent works. The second hop in the N+1 chain.
#
# Property → Agent → Office
#
# When the listing page renders 20 properties and shows each agent's office
# name, Django will make 20 separate queries to fetch each office —
# UNLESS we use select_related (which we won't, not yet).
# =============================================================================
class Office(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = "offices"

    def __str__(self):
        return self.name


# =============================================================================
# AGENT
# The first hop in the N+1 chain. Each agent belongs to an office.
#
# NAIVE ON PURPOSE: No index on office_id beyond what Django adds for FKs.
# Actually — Django DOES add an index on ForeignKey fields automatically.
# So office_id IS indexed. That's fine. The N+1 problem isn't about indexes
# here — it's about the NUMBER of queries. 20 properties = 20 agent lookups
# = 20 office lookups. The fix is select_related + caching, not indexes.
# =============================================================================
class Agent(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    office = models.ForeignKey(
        Office,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agents",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "agents"

    def __str__(self):
        return self.name


# =============================================================================
# PROPERTY
# The core model. This is what the listing page displays, what the search
# filters against, and what the cache will eventually serve.
#
# NAIVE ON PURPOSE (multiple things):
#
# 1. No indexes on price, property_type, location, agent, or status.
#    The frontend filters on ALL of these. Every filter query scans the
#    entire table. Part 3 adds indexes and caches the results.
#
# 2. view_count is updated on every page view.
#    That's a DB write on every single request to a listing.
#    Under load, this becomes a write bottleneck. The fix (Part 3+) is
#    cache-aside: increment in Redis, flush to DB on a timer.
#
# 3. status transitions (available → pending → sold) invalidate cached
#    listing pages. We don't handle that yet. We will.
# =============================================================================
class Property(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("pending", "Pending"),
        ("sold", "Sold"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ("apartment", "Apartment"),
        ("house", "House"),
        ("villa", "Villa"),
        ("studio", "Studio"),
        ("condo", "Condo"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        db_index=False,  # No index. Intentional.
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_index=False,  # No index. Intentional.
    )
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="properties",
        db_index=False,  # Override Django's auto-index on FK. Intentional.
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties",
        db_index=False,  # Same. Intentional.
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        db_index=False,  # Cache invalidation target. No index yet.
    )
    view_count = models.IntegerField(
        default=0,
        db_index=False,  # Cache-aside target. Read hot, write rare (eventually).
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Newest first by default
        verbose_name_plural = "properties"

    def __str__(self):
        return f"{self.title} — ${self.price:,.2f}"


# =============================================================================
# PROPERTY IMAGE
# Multiple images per property. This is the image caching surface.
#
# Three URL fields, each representing a different stage of the image pipeline:
#
# original_url  — The raw file as uploaded. Source of truth. Never changes.
# thumbnail_url — A smaller version, generated lazily on first request.
#                 Null until someone actually needs it.
# cdn_url       — The URL after the image has been pushed to a CDN
#                 (Cloudinary, ImageKit, etc.). Null until processed.
#
# The nullable fields are deliberate. They model lazy processing:
# the image exists, but the optimized versions don't — until demand creates them.
# That's the pattern we'll cache in a later part.
#
# display_order = 0 means cover image. The listing page shows the first image
# (order 0) in the card, and loads the rest only when the user clicks through.
# That "load the rest" moment is a cache opportunity.
#
# NAIVE ON PURPOSE: No index on property_id.
# Fetching all images for a property = full table scan on this table.
# =============================================================================
class PropertyImage(models.Model):
    """
    Images for a property listing.

    The image field uses CloudinaryField instead of Django's ImageField.
    This automatically uploads to Cloudinary and stores the Cloudinary URL.
    """
    listing = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        db_index=False,  # No index. Intentional. Full scan on image fetch.
    )
    # original_url = models.URLField(max_length=1024)
    # thumbnail_url = models.URLField(max_length=1024, null=True, blank=True)
    # cdn_url = models.URLField(max_length=1024, null=True, blank=True)
    image = CloudinaryField(
        'image',
        folder='housing/properties',  # Organize in Cloudinary folders
        transformation={
            'quality': 'auto',  # Automatic quality optimization
            'fetch_format': 'auto',  # Automatic format selection (WebP, AVIF, etc.)
        }
    )
    display_order = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name_plural = "property images"

    def __str__(self):
        return f"Image {self.display_order} for {self.listing.title}"

    # @builtins.property
    # def best_url(self):
    #     """
    #     Returns the best available URL for this image.
    #     Priority: cdn_url (fastest) → thumbnail_url → original_url (fallback).
    #     This method becomes the caching decision point in a later part.
    #     """
    #     return self.cdn_url or self.thumbnail_url or self.original_url

    def get_original_url(self):
        """
        Returns the original uploaded image URL.
        """
        if self.image:
            return self.image.url
        return None

    def get_thumbnail_url(self, width=400, height=300):
        """
        Returns a thumbnail URL with Cloudinary transformations.
        Cloudinary generates this on-demand — no separate file is stored.
        """
        if not self.image:
            return None

        # Build transformation string
        # w_400,h_300,c_fill = width 400px, height 300px, fill mode (crop to fit)
        return self.image.build_url(
            transformation=[
                {"width": width, "height": height, "crop": "fill"},
                {"quality": "auto"},
                {"fetch_format": "auto"},
            ]
        )

    def get_webp_url(self):
        """
        Returns a WebP version of the image.
        WebP is 25-35% smaller than JPEG for the same visual quality.
        """
        if not self.image:
            return None

        return self.image.build_url(
            transformation=[
                {"fetch_format": "webp"},
                {"quality": "auto"},
            ]
        )
