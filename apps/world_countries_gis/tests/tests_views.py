"""
Test Suite Module for World Countries GIS App
"""
from rest_framework import status

from apps.world_countries_gis.models import WorldCountry
from apps.world_countries_gis.tests import utils
from tests.base_test import BaseTest

# Test Constants
WORLD_COUNTRIES_APPLICATION_URL = '/v1/world_countries/'
APPLICATION_JSON = 'application/json'


class TestWorldCountryViewSet(BaseTest):
    """
    Test class for WorldCountryViewSet
    """
    fixtures = [
        'world_countries.json'
    ]

    def setUp(self):
        """
        setUp method is defined to preload data before test method execution
        """
        #  Conditionally perform required action based on current test execution
        if 'test_delete_world_country' in str(self) or 'test_update_world_country' in str(self):
            new_obj = WorldCountry.objects.get(pk=1)
            WorldCountry.objects.create(pk=111, code=new_obj.code, name=new_obj.name, geometry=new_obj.geometry)

    def tearDown(self):
        """
        tearDown method is defined to offload data post test method execution
        """
        #  Conditionally perform required action based on current test execution
        if 'test_update_world_country' in str(self):
            WorldCountry.objects.filter(id=111).delete()

    def test_list_world_countries(self):
        """
        Test case for List World Countries API
        """
        response = self.client.get(WORLD_COUNTRIES_APPLICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        countries = [country['name'] for country in response.data['results']]
        countries.sort()
        self.assertEqual(countries, ['China', 'India', 'Nepal'])

    def test_get_intersecting_countries(self):
        """
        Test case for retrieving intersecting World Countries API. (Spatial Query)
        """
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}intersecting_countries/NPL/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        countries = [country['code'] for country in response.data['results']]
        countries.sort()
        self.assertEqual(countries, ['CHN', 'IND'])

    def test_get_world_countries_search(self):
        """
        Test case for List World Countries API with search functionality
        """
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}?search=Ind')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'India')
        self.assertEqual(response.data['results'][0]['code'], 'IND')

    def test_retrieve_world_country(self):
        """
        Test case for Retrieving World Countries API
        """
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Nepal')
        self.assertEqual(response.data['code'], 'NPL')

    def test_create_world_country(self):
        """
        Test case for Create World Countries object API
        """
        response = self.client.post(WORLD_COUNTRIES_APPLICATION_URL, data=utils.get_world_countries_create_payload(),
                                    content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], utils.get_world_countries_create_payload()['name'])
        self.assertEqual(response.data['code'], utils.get_world_countries_create_payload()['code'])

    def test_update_world_country(self):
        """
        Test case for Updating World Countries API
        """
        response = self.client.put(f'{WORLD_COUNTRIES_APPLICATION_URL}1/',
                                   data=utils.get_world_countries_create_payload(),
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], utils.get_world_countries_create_payload()['name'])
        self.assertEqual(response.data['code'], utils.get_world_countries_create_payload()['code'])

    def test_delete_world_country(self):
        """
        Test case for Deleting World Countries API
        """
        response = self.client.delete(f'{WORLD_COUNTRIES_APPLICATION_URL}111/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_intersecting_countries_invalid_country(self):
        """
        Test case for retrieving intersecting World Countries API when country code is invalid.
        """
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}intersecting_countries/IPL/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data['detail']), "Country with code 'IPL' Not Found")
