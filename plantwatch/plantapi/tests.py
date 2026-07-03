from django.test import SimpleTestCase


class PlantapiIntegrationTests(SimpleTestCase):
    databases = {'default', 'plantwatch'}

    def test_plants_api_list(self):
        """Test API endpoint listing plants returns HTTP 200."""
        response = self.client.get('/plantapi/plants/')
        self.assertEqual(response.status_code, 200)

    def test_plants_api_detail(self):
        """Test API endpoint for specific plant detail returns HTTP 200."""
        response = self.client.get('/plantapi/plants/SN70015796/')
        self.assertEqual(response.status_code, 200)

    def test_blocks_api_list(self):
        """Test API endpoint listing blocks returns HTTP 200."""
        response = self.client.get('/plantapi/blocks/')
        self.assertEqual(response.status_code, 200)

    def test_blocks_api_detail(self):
        """Test API endpoint for specific block detail returns HTTP 200."""
        response = self.client.get('/plantapi/blocks/SEE985842749525/')
        self.assertEqual(response.status_code, 200)

    def test_pollutions_api_list(self):
        """Test API endpoint listing pollutions returns HTTP 200."""
        response = self.client.get('/plantapi/pollutions/')
        self.assertEqual(response.status_code, 200)

    def test_pollution_by_plantid(self):
        """Test API custom endpoint for pollution by plantid returns HTTP 200."""
        response = self.client.get('/plantapi/pollution/by_plantid/SN70015796/')
        self.assertEqual(response.status_code, 200)

    def test_pollution_by_plantid_st100125(self):
        """Test API endpoint returns multiple pollution records for plant ST100125."""
        response = self.client.get('/plantapi/pollution/by_plantid/ST100125/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)

    def test_pollution_by_year(self):
        """Test API custom endpoint for pollution by year returns HTTP 200."""
        response = self.client.get('/plantapi/pollution/by_year/2020/')
        self.assertEqual(response.status_code, 200)

    def test_plant_blocks_api_matches_blockcount(self):
        """Test API detail endpoint for ST100125 returns nested blocks matching blockcount (3)."""
        response = self.client.get('/plantapi/plants/ST100125/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['blockcount'], 3)
        self.assertEqual(len(data['blocks']), 3)

    def test_plant_st100125_api_all_fields_non_empty(self):
        """Test API detail endpoint for ST100125 returns non-empty values for all plant attributes."""
        response = self.client.get('/plantapi/plants/ST100125/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_fields = [
            'plantid', 'plantname', 'blockcount', 'totalpower', 'energysource',
            'state', 'chp', 'initialop', 'latestexpanded', 'company', 'blocks'
        ]
        for field in expected_fields:
            self.assertIn(field, data)
            self.assertIsNotNone(data[field], f'Field {field} is None')
            self.assertNotEqual(data[field], '', f'Field {field} is empty string')
