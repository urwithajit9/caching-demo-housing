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


class PropertyImageInline(admin.TabularInline):
    """
    Inline admin for uploading multiple images per property.
    Shows as a table below the property form.
    """

    model = PropertyImage
    extra = 3  # Show 3 empty upload slots by default
    fields = ["image", "display_order", "alt_text"]

    # Optional: show thumbnail preview in admin
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        """Display a small thumbnail in the admin list"""
        if obj.image:
            return f'<img src="{obj.get_thumbnail_url(100, 75)}" />'
        return "No image"

    image_preview.allow_tags = True


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
    list_select_related = ["location", "agent"]

    # Add the inline ↓
    inlines = [PropertyImageInline]


# @admin.register(PropertyImage)
# class PropertyImageAdmin(admin.ModelAdmin):
#     list_display = [
#         "listing",
#         "display_order",
#         # "original_url",
#         # "cdn_url",
#         # "thumbnail_url",
#     ]
#     list_select_related = ["listing"]
#     ordering = ["listing", "display_order"]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["listing", "display_order", "alt_text", "created_at"]
    list_select_related = ["listing"]
    ordering = ["listing", "display_order"]
