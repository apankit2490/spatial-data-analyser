from django.contrib.gis import admin

from apps.world_countries_gis.models import WorldCountry
from leaflet.admin import LeafletGeoAdmin


@admin.register(WorldCountry)
class WorldCountryAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name', 'code',)
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')

