from django.urls import path
from .views import (
    PropertyListView,
    CachedPropertyListView,
    OptimizedPropertyListView,
    PropertyDetailView,
)

urlpatterns = [
    path("properties/live/naive/", PropertyListView.as_view(), name="property-naive"),
    path(
        "properties/cached/", CachedPropertyListView.as_view(), name="property-cached"
    ),
    path(
        "properties/live/optimized/",
        OptimizedPropertyListView.as_view(),
        name="property-optimized",
    ),
    path("properties/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
]
