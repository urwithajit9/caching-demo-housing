from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all().order_by("-created_at")
    serializer_class = PropertySerializer
    # Pagination is handled by DRF settings (default 20)


    # Cache this specific view for 60 seconds
    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
