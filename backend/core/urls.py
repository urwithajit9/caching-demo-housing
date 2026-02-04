"""
core/urls.py

The URL router. Every HTTP request hits this file first.
Django reads the urlpatterns list top-to-bottom and stops at the first match.

Right now we have one route: the admin panel.
The housing API routes come in Part 3 — that's where DRF views enter the picture.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("housing.urls")),  #  added in Part 3 -
    path("__debug__/", include("debug_toolbar.urls")),
]
