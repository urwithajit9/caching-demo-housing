from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver([post_save, post_delete], sender=Property)
def invalidate_property_cache(sender, instance, **kwargs):
    """
    Automatic cache invalidation.

    Fires whenever a Property is created, updated, or deleted.
    Clears the entire cache to ensure fresh data on the next request.

    In a production system, you'd invalidate specific cache keys
    (e.g., only the listing page, only pages that include this property).
    For this demo, we use cache.clear() for simplicity and guaranteed freshness.
    """
    # In a real app, you'd target specific keys, but for now,
    # we'll clear everything to ensure total freshness.
    cache.clear()
    print("--- Redis Cache Invalidated! ---")
