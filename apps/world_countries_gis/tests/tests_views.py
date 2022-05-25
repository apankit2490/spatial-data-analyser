from rest_framework import status

from apps.world_countries_gis.models import WorldCountry
from apps.world_countries_gis.tests import utils
from tests.base_test import BaseTest

WORLD_COUNTRIES_APPLICATION_URL = '/v1/world_countries/'
APPLICATION_JSON = 'application/json'


class TestWorldCountryViewSet(BaseTest):
    fixtures = [
        'world_countries.json'
    ]

    def setUp(self):
        if 'test_delete_world_country' in str(self) or 'test_update_world_country' in str(self):
            new_obj = WorldCountry.objects.get(pk=1)
            WorldCountry.objects.create(pk=111, code=new_obj.code, name=new_obj.name, geometry=new_obj.geometry)

    def tearDown(self):
        if 'test_update_world_country' in str(self):
            WorldCountry.objects.filter(id=111).delete()

    def test_list_world_countries(self):
        response = self.client.get(WORLD_COUNTRIES_APPLICATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        countries = [country['name'] for country in response.data['results']]
        countries.sort()
        self.assertEqual(countries, ['China', 'India', 'Nepal'])

    def test_get_intersecting_countries(self):
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}intersecting_countries/NPL/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        countries = [country['code'] for country in response.data['results']]
        countries.sort()
        self.assertEqual(countries, ['CHN', 'IND'])

    def test_get_world_countries_search(self):
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}?search=Ind')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'India')
        self.assertEqual(response.data['results'][0]['code'], 'IND')

    def test_retrieve_world_country(self):
        response = self.client.get(f'{WORLD_COUNTRIES_APPLICATION_URL}1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Nepal')
        self.assertEqual(response.data['code'], 'NPL')

    def test_create_world_country(self):
        response = self.client.post(WORLD_COUNTRIES_APPLICATION_URL, data=utils.get_world_countries_create_payload(),
                                    content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], utils.get_world_countries_create_payload()['name'])
        self.assertEqual(response.data['code'], utils.get_world_countries_create_payload()['code'])

    def test_update_world_country(self):
        response = self.client.put(f'{WORLD_COUNTRIES_APPLICATION_URL}1/',
                                   data=utils.get_world_countries_create_payload(),
                                   content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], utils.get_world_countries_create_payload()['name'])
        self.assertEqual(response.data['code'], utils.get_world_countries_create_payload()['code'])

    def test_delete_world_country(self):
        response = self.client.delete(f'{WORLD_COUNTRIES_APPLICATION_URL}111/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
