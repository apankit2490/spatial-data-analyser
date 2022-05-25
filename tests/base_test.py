"""
Base Test class module to globally configure Test Configurations
"""
from os.path import join

from django.conf import settings
from django.test import TestCase
from django.test import override_settings

TEST_MEDIA_ROOT = join(settings.MEDIA_ROOT, 'test_data')


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
)
@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class BaseTest(TestCase):
    pass
