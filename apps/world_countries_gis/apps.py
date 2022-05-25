"""
App module for app configs
"""
from django.apps import AppConfig


class WorldCountriesGisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'world_countries_gis'
