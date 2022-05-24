"""
Views for  world countries gis app
"""
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from apps.world_countries_gis.models import WorldCountry
from apps.world_countries_gis.serializers import WorldCountrySerializer


class WorldCountryViewSet(viewsets.ModelViewSet):
    queryset = WorldCountry.objects.all()
    serializer_class = WorldCountrySerializer
    ordering_fields = ('id', 'name')
    ordering = ('id',)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('id', 'name', 'code')
    filter_fields = ('id', 'name', 'code')

    @method_decorator(cache_page(settings.WORLD_COUNTRY_LIST_LIFETIME))
    def list(self, request, *args, **kwargs):
        return super(WorldCountryViewSet, self).list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path=r'intersecting_countries/(?P<country_code>[^/.]+)')
    def get_intersecting_countries(self, request, country_code=None):
        world_cntry_obj = WorldCountry.objects.filter(code=country_code).first()
        intersecting_cntry_queryset = WorldCountry.objects.filter(
            geometry__intersects=world_cntry_obj.geometry).exclude(id=world_cntry_obj.id)
        page = self.paginate_queryset(intersecting_cntry_queryset)
        return self.get_paginated_response(
            WorldCountrySerializer(page, many=True).data
        )
