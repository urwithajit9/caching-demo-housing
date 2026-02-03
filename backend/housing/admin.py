"""
housing/admin.py

Register all models with the Django admin panel.
We already verified the admin is running at http://localhost:8000/admin/
in Part 1. This file makes our models show up there.

list_display controls which columns appear in the admin table view.
We keep it minimal — just enough to eyeball the seeded data later
without clicking into every row.
"""

from django.contrib import admin
from .models import Location, Office, Agent, Property, PropertyImage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["city", "state", "zip_code", "country"]
    search_fields = ["city", "state", "zip_code"]
    ordering = ["city"]


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "phone"]
    search_fields = ["name", "city"]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "office"]
    search_fields = ["name", "email"]
    list_select_related = ["office"]  # Prevents N+1 in the admin itself


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "property_type",
        "price",
        "bedrooms",
        "bathrooms",
        "status",
        "location",
        "agent",
        "is_published",
        "view_count",
        "created_at",
    ]
    list_filter = ["property_type", "status", "is_published"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    # Admin uses select_related internally for FK fields in list_display.
    # This is fine — admin is not the performance target. The API is.


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = [
        "property",
        "display_order",
        "original_url",
        "cdn_url",
        "thumbnail_url",
    ]
    list_select_related = ["property"]
    ordering = ["property", "display_order"]
