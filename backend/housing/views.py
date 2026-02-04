"""
housing/views.py

Three views of the same data:
1. Naive — no optimization, triggers N+1 queries
2. Cached — naive view with @cache_page, serves from Redis
3. Optimized — uses select_related to fix N+1 at the database level (Part 4 preview)
"""

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer


class PropertyListView(generics.ListAPIView):
    """
    The naive baseline. No caching. No query optimization.
    This is the "before" picture.
    """
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer
    # Pagination is handled by DRF settings (default 20)


class CachedPropertyListView(PropertyListView):
    """
    The cached version. Same queryset as PropertyListView, but with
    @cache_page(60) applied. This caches the entire HTTP response
    (headers + JSON body) in Redis for 60 seconds.

    First request: cache miss, hits the database, saves to Redis.
    Subsequent requests: cache hit, served from Redis, zero DB queries.
    """

    # Cache this specific view for 60 seconds
    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# class OptimizedPropertyListView(generics.ListAPIView):
#     """
#     The database-optimized version. No cache, but uses select_related
#     to fetch Property + Agent + Office in a single query with JOINs
#     instead of 41 separate queries.

#     This is a preview of Part 4. We're including it here so you can
#     compare "fast cache" vs "fast database" side by side.
#     """

#     queryset = (
#         Property.objects.select_related("agent__office", "location")
#         .all()
#         .order_by("-created_at")
#     )
#     serializer_class = PropertySerializer


class OptimizedPropertyListView(generics.ListAPIView):
    """
    The database-optimized version. Uses select_related to fetch
    Property + Location + Agent + Office in a single query with JOINs.

    This is what "fast without cache" looks like.
    61 queries → 1 query.
    80ms → 15-20ms.
    """

    serializer_class = PropertySerializer

    def get_queryset(self):
        return (
            Property.objects.select_related(
                "location",  # JOIN on property.location_id = location.id
                "agent__office",  # Double underscore: JOIN agent, then JOIN office
            )
            .all()
            .order_by("-created_at")
        )
