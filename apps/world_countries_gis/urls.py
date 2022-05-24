"""
World Countries GIS app URL routing config
"""

from rest_framework.routers import SimpleRouter

from apps.world_countries_gis import views

router = SimpleRouter()

router.register(f'world_countries', views.WorldCountryViewSet)

urlpatterns = [
]

urlpatterns += router.urls
