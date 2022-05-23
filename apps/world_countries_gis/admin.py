from django.contrib.gis import admin

from apps.world_countries_gis.models import WorldCountry
from leaflet.admin import LeafletGeoAdmin


@admin.register(WorldCountry)
class WorldCountryAdmin(LeafletGeoAdmin):
    pass

