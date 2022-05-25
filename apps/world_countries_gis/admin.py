"""
Admin module to configure Django admin Interface
"""
from django.contrib.gis import admin

from apps.world_countries_gis.models import WorldCountry
from leaflet.admin import LeafletGeoAdmin


@admin.register(WorldCountry)
class WorldCountryAdmin(LeafletGeoAdmin):
    """
    WorldCountryAdmin deals with WorldCountry model's admin interface
    """
    list_display = ('id', 'name', 'code',)
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    ordering = ('id',)

