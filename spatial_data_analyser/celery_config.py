"""
Celery Beat config Module
"""

from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    # Auto updates the world country data every 10 minutes
    'update_world_countries': {
        'task': 'apps.world_countries_gis.tasks.update_world_countries',
        'schedule': timedelta(minutes=10),
    },
}
