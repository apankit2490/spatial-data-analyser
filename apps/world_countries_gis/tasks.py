"""
Module to execute Celery Tasks
"""
import json
import logging
import datapackage
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from apps.world_countries_gis.models import WorldCountry
from spatial_data_analyser.celery import app
from spatial_data_analyser.utils.commons import celery_logger_handler

logger = logging.getLogger('spatial-data-analyser')


@app.task(on_success=celery_logger_handler('Update World Countries Task Successful.', True),
          on_failure=celery_logger_handler('Update World Countries Failed.', False))
def update_world_countries():
    logger.info(f'Inside update_world_countries task. Performing database update using data from '
                f'{settings.DATAHUB_GEOJSON_URL}')
    package = datapackage.Package(settings.DATAHUB_GEOJSON_URL)
    for feature in package.descriptor['features']:
        country_name = feature['properties']['ADMIN'] or feature['properties']['ISO_A3']
        country_code = feature['properties']['ISO_A3']
        geometry_obj = feature['geometry']
        logger.info(f'Persisting/Updating data for name: {country_name}, code: {country_code}')
        logger.debug(f'Geometry object desc for country: {country_name}. \n{geometry_obj}')
        WorldCountry.objects.update_or_create(name=country_name, defaults={
            'name': country_name,
            'code': country_code,
            'geometry': GEOSGeometry(json.dumps(geometry_obj))
        })
