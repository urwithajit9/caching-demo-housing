from rest_framework import serializers
from .models import Location, Office, Agent, Property, PropertyImage


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ["id", "name", "city"]


class AgentSerializer(serializers.ModelSerializer):
    office = OfficeSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ["id", "name", "email", "office"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "city", "state"]


class PropertySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "property_type",
            "price",
            "bedrooms",
            "bathrooms",
            "location",
            "agent",
            "status",
            "view_count",
            "created_at",
        ]
