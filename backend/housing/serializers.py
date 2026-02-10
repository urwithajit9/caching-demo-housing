from rest_framework import serializers
from .models import Location, Office, Agent, Property, PropertyImage


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ["id", "name", "city", "phone"]


class AgentSerializer(serializers.ModelSerializer):
    office = OfficeSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ["id", "name", "email", "phone", "office"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "city", "state", "zip_code"]


class PropertyImageSerializer(serializers.ModelSerializer):
    """
    Serializer for property images.
    Returns multiple URL variants for different use cases.
    """

    original_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    webp_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = [
            "id",
            "original_url",
            "thumbnail_url",
            "webp_url",
            "display_order",
            "alt_text",
        ]

    def get_original_url(self, obj):
        """Full-size image URL"""
        return obj.get_original_url()

    def get_thumbnail_url(self, obj):
        """400x300 thumbnail URL"""
        return obj.get_thumbnail_url(width=400, height=300)

    def get_webp_url(self, obj):
        """WebP version URL (smaller file size)"""
        return obj.get_webp_url()


class PropertySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "description",
            "property_type",
            "price",
            "bedrooms",
            "bathrooms",
            "location",
            "agent",
            "status",
            "view_count",
            "created_at",
            "images",
        ]
