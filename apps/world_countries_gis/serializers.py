"""
Serializer for world countries gis app
"""
from rest_framework import serializers

from apps.world_countries_gis.models import WorldCountry


class WorldCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldCountry
        fields = ('__all__',)
