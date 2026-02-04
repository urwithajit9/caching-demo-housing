from rest_framework import serializers
from .models import Location, Office, Agent, Property


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


class PropertySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)

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
        ]
