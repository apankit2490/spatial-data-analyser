"""
Views for  world countries gis app
"""
import logging

from rest_framework import viewsets, exceptions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from apps.world_countries_gis.models import WorldCountry
from apps.world_countries_gis.serializers import WorldCountrySerializer

logger = logging.getLogger('spatial-data-analyser')


class WorldCountryViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet to CRUD WorldCountry objects along with spatial querying.
    """
    queryset = WorldCountry.objects.all()
    serializer_class = WorldCountrySerializer
    ordering_fields = ('id', 'name')
    ordering = ('id',)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('id', 'name', 'code')
    filter_fields = ('id', 'name', 'code')

    @method_decorator(cache_page(settings.WORLD_COUNTRY_LIST_LIFETIME))
    def list(self, request, *args, **kwargs):
        """
        Override list method to enable caching.
        """
        return super(WorldCountryViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.WORLD_INTERSECTING_COUNTRIES_LIFETIME))
    @action(detail=False, methods=['get'], url_path=r'intersecting_countries/(?P<country_code>[^/.]+)')
    def get_intersecting_countries(self, request, country_code: str = None):
        """
        ViewSet Action to obtain countries intersecting with specified country.(spatial query)
        It is cache enabled.
        :param request: Request Object
        :param country_code: Country code in ISO format
        """
        logger.info(f'Received Request to obtain Countries intersecting specified country: {country_code}')
        world_cntry_obj = WorldCountry.objects.filter(code=country_code.upper()).first()
        if not world_cntry_obj:
            logger.error(f"Country with code '{country_code}' Doesn't Exist.")
            raise exceptions.NotFound(detail=f"Country with code '{country_code}' Not Found", code=404)
        intersecting_cntry_queryset = WorldCountry.objects.filter(
            geometry__intersects=world_cntry_obj.geometry).exclude(id=world_cntry_obj.id)
        logger.info(f'Intersecting Countries with {country_code}: {intersecting_cntry_queryset}')
        page = self.paginate_queryset(intersecting_cntry_queryset)
        return self.get_paginated_response(
            WorldCountrySerializer(page, many=True).data
        )
