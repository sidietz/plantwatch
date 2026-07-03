import re
from django.test import SimpleTestCase
from plantmaster.helpers import (
    divide_safe,
    calc_workload,
    calc_efficency,
    handle_slider,
    handle_slider_1,
    handle_slider_2,
)


class PlantmasterIntegrationTests(SimpleTestCase):
    databases = {'default', 'plantwatch'}

    def test_plant_detail_status_code(self):
        """Test specific plant detail URL returns HTTP 200."""
        response = self.client.get('/plantwatch/plant/SN70015796/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['plant_id'], 'SN70015796')

    def test_plant_with_two_pollutants_tables(self):
        """Test plant ST100125 returns non-empty pollutants tables for both water and air."""
        response = self.client.get('/plantwatch/plant/ST100125/')
        self.assertEqual(response.status_code, 200)

        # Check context variables for Air (pollutions2) and Water (pollutions3)
        pollutions_air = response.context['pollutions2']
        pollutions_water = response.context['pollutions3']
        self.assertGreater(len(pollutions_air), 0)
        self.assertGreater(len(pollutions_water), 0)

        # Verify rendered HTML contains two non-empty tables and no empty-data placeholders
        content = response.content.decode('utf-8')
        self.assertIn('Schadstoff [Luft]', content)
        self.assertIn('Schadstoff [Wasser]', content)
        self.assertEqual(content.count('Pollutants over time'), 2)
        self.assertNotIn('Keine Schadstoffdaten für Luft vorhaden.', content)
        self.assertNotIn('Keine Schadstoffdaten für Wasser vorhaden.', content)

    def test_plant_with_only_air_pollutants(self):
        """Test plant SN70015796 returns non-empty air table and empty water placeholder."""
        response = self.client.get('/plantwatch/plant/SN70015796/')
        self.assertEqual(response.status_code, 200)

        self.assertGreater(len(response.context['pollutions2']), 0)
        self.assertEqual(len(response.context['pollutions3']), 0)

        content = response.content.decode('utf-8')
        self.assertIn('Schadstoff [Luft]', content)
        self.assertNotIn('Keine Schadstoffdaten für Luft vorhaden.', content)
        self.assertIn('Keine Schadstoffdaten für Wasser vorhaden.', content)

    def test_plant_with_no_pollutants(self):
        """Test plant SD666-16 returns empty placeholders for both water and air tables."""
        response = self.client.get('/plantwatch/plant/SD666-16/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['pollutions2']), 0)
        self.assertEqual(len(response.context['pollutions3']), 0)

        content = response.content.decode('utf-8')
        self.assertIn('Keine Schadstoffdaten für Luft vorhaden.', content)
        self.assertIn('Keine Schadstoffdaten für Wasser vorhaden.', content)

    def test_plant_efficiency_table(self):
        """Test plant ST100125 returns a non-empty efficiency table."""
        response = self.client.get('/plantwatch/plant/ST100125/')
        self.assertEqual(response.status_code, 200)

        elist = response.context['elist']
        self.assertIsNotNone(elist)
        self.assertEqual(len(elist), 2)
        expected_headers = [
            'Jahr',
            'Energie TWh',
            'CO2 [Mio. t.]',
            'g/kWh',
            'Auslastung aktive Blöcke [%]',
            'Auslastung gesamt [%]',
        ]
        self.assertEqual(elist[0], expected_headers)
        self.assertGreater(len(elist[1]), 0)

        content = response.content.decode('utf-8')
        self.assertIn('<caption>Efficiency</caption>', content)
        self.assertIn('id="elistentry0"', content)

    def test_plant4_comparison_efficiency_tables(self):
        """Test comparison view /plant/ST100125/SN70015796 returns two non-empty efficiency tables."""
        response = self.client.get('/plantwatch/plant/ST100125/SN70015796')
        self.assertEqual(response.status_code, 200)

        self.assertGreater(len(response.context['elist']), 0)
        self.assertGreater(len(response.context['elist2']), 0)

        content = response.content.decode('utf-8')
        self.assertEqual(content.count('<caption>Efficiency</caption>'), 2)
        self.assertNotIn('id="nopowerdata"', content)

    def test_plant_blocks_table_matches_blockcount(self):
        """Test plant ST100125 blocks table has exactly as many entries as Blockzahl in Plant table (3)."""
        response = self.client.get('/plantwatch/plant/ST100125/')
        self.assertEqual(response.status_code, 200)

        blocks = response.context['blocks']
        self.assertEqual(len(blocks), 3)

        content = response.content.decode('utf-8')
        self.assertIn('<caption>Blocks</caption>', content)

        # Verify specific block IDs belonging to ST100125 are rendered in the HTML table
        expected_blocks = ['SEE960652233358', 'SEE919134316447', 'SEE947677200282']
        for block_id in expected_blocks:
            self.assertIn(block_id, content)

    def test_multiple_plants_blocks_table_match_blockcount(self):
        """Test several plants (SN70015796, BB45025611, SD666-16) to ensure blocks table count matches Blockzahl."""
        test_cases = [
            ('SN70015796', 4),
            ('BB45025611', 2),
            ('SD666-16', 1),
        ]
        for plant_id, expected_count in test_cases:
            with self.subTest(plant_id=plant_id):
                response = self.client.get(f'/plantwatch/plant/{plant_id}/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.context['blocks']), expected_count)

    def test_plant_detail_root_path(self):
        """Test plant detail URL without /plantwatch prefix returns HTTP 200."""
        response = self.client.get('/plant/SN70015796/')
        self.assertEqual(response.status_code, 200)

    def test_plant_detail_not_found(self):
        """Test non-existent plant ID returns HTTP 404."""
        response = self.client.get('/plantwatch/plant/INVALID_ID_999/')
        self.assertEqual(response.status_code, 404)

    def test_plant2_detail_status_code(self):
        """Test alternative plant view (plant2) returns HTTP 200."""
        response = self.client.get('/plantwatch/plant2/SN70015796/')
        self.assertEqual(response.status_code, 200)

    def test_plant4_comparison_status_code(self):
        """Test plant comparison view (plant4) returns HTTP 200."""
        response = self.client.get('/plantwatch/plant/SN70015796/BB45025564')
        self.assertEqual(response.status_code, 200)

    def test_random_plant_redirect(self):
        """Test random plant view redirects to a specific plant detail page."""
        response = self.client.get('/plantwatch/plant/')
        self.assertEqual(response.status_code, 302)

    def test_block_detail_status_code(self):
        """Test block detail URL returns HTTP 200."""
        response = self.client.get('/plantwatch/block/SEE985842749525/')
        self.assertEqual(response.status_code, 200)

    def test_block_detail_not_found(self):
        """Test non-existent block ID returns HTTP 404."""
        response = self.client.get('/plantwatch/block/INVALID_BLOCK_999/')
        self.assertEqual(response.status_code, 404)

    def test_plants_list_view_get(self):
        """Test plants list view and root index return HTTP 200."""
        response = self.client.get('/plantwatch/plants/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('plants', response.context)

        response_root = self.client.get('/plantwatch/')
        self.assertEqual(response_root.status_code, 200)

    def test_plants_list_tables_and_st100125_cells(self):
        """Test /plantwatch/plants/ renders non-empty summary/plants tables and non-empty cells in ST100125 row."""
        response = self.client.get('/plantwatch/plants/')
        self.assertEqual(response.status_code, 200)

        # Verify summary table and plants table context variables are populated
        self.assertGreater(len(response.context['sources_dict']), 0)
        self.assertGreater(len(response.context['plants']), 0)

        content = response.content.decode('utf-8')
        self.assertIn('<caption>Summary</caption>', content)
        self.assertIn('<caption>Plants</caption>', content)

        # Find ST100125 in the HTML table and extract its HTML row (<tr ...> ... </tr>)
        idx = content.find('ST100125')
        self.assertNotEqual(idx, -1)
        row_start = content.rfind('<tr', 0, idx)
        row_end = content.find('</tr>', idx) + len('</tr>')
        st100125_row_html = content[row_start:row_end]

        # Extract all table cells (<td>...</td>) in the ST100125 row
        cells = re.findall(r'<td[^>]*>(.*?)</td>', st100125_row_html, re.DOTALL)
        self.assertEqual(len(cells), 14)

        # Verify every cell has non-empty visible text/data
        for cell_idx, cell_html in enumerate(cells):
            clean_text = re.sub(r'<.*?>', '', cell_html).strip()
            self.assertNotEqual(clean_text, '', f'Column index {cell_idx} is empty for ST100125')

    def test_plants_list_view_post_filter(self):
        """Test POST filtering on plants list view."""
        response = self.client.post(
            '/plantwatch/plants/',
            {'sort_by': 'totalpower', 'sort_method': '-'},
        )
        self.assertEqual(response.status_code, 200)

    def test_plants_list_power_slider_filtering(self):
        """Test sliding the power slider (slider2) to the right decreases the number of found plants."""
        # Default request (slider2 defaults to 250;4500)
        response_default = self.client.get('/plantwatch/plants/')
        self.assertEqual(response_default.status_code, 200)
        count_default = len(response_default.context['plants'])
        self.assertGreater(count_default, 0)

        # Slide power minimum to 1000 MW
        response_1000 = self.client.post('/plantwatch/plants/', {'slider2': '1000;4500'})
        self.assertEqual(response_1000.status_code, 200)
        count_1000 = len(response_1000.context['plants'])
        self.assertLess(count_1000, count_default)

        # Slide power minimum further to 2000 MW
        response_2000 = self.client.post('/plantwatch/plants/', {'slider2': '2000;4500'})
        self.assertEqual(response_2000.status_code, 200)
        count_2000 = len(response_2000.context['plants'])
        self.assertLess(count_2000, count_1000)

        # Verify HTML table rows also decrease accordingly
        html_default = response_default.content.decode('utf-8')
        html_1000 = response_1000.content.decode('utf-8')
        html_2000 = response_2000.content.decode('utf-8')
        self.assertLess(html_1000.count('/plantwatch/plant/'), html_default.count('/plantwatch/plant/'))
        self.assertLess(html_2000.count('/plantwatch/plant/'), html_1000.count('/plantwatch/plant/'))

    def test_plants_list_energysource_filtering(self):
        """Test filtering by Energieträger reduces found plants, and no checkbox selected equals all selected."""
        response_all = self.client.get('/plantwatch/plants/')
        count_all = len(response_all.context['plants'])
        self.assertGreater(count_all, 0)

        # When no checkbox is selected, initialize_form treats it as all checkboxes selected
        response_none_selected = self.client.post('/plantwatch/plants/', {})
        count_none_selected = len(response_none_selected.context['plants'])
        self.assertEqual(count_none_selected, count_all)

        # Filter specifically by Braunkohle
        response_braunkohle = self.client.post('/plantwatch/plants/', {'select_powersource': ['Braunkohle']})
        count_braunkohle = len(response_braunkohle.context['plants'])
        self.assertGreater(count_braunkohle, 0)
        self.assertLess(count_braunkohle, count_all)
        for plant in response_braunkohle.context['plants']:
            self.assertEqual(plant.energysource, 'Braunkohle')

        # Filter specifically by Steinkohle
        response_steinkohle = self.client.post('/plantwatch/plants/', {'select_powersource': ['Steinkohle']})
        count_steinkohle = len(response_steinkohle.context['plants'])
        self.assertGreater(count_steinkohle, 0)
        self.assertLess(count_steinkohle, count_all)
        for plant in response_steinkohle.context['plants']:
            self.assertEqual(plant.energysource, 'Steinkohle')

    def test_blocks_list_view_get(self):
        """Test blocks list view returns HTTP 200."""
        response = self.client.get('/plantwatch/blocks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('blocks', response.context)

    def test_blocks_list_view_post_filter(self):
        """Test POST filtering on blocks list view."""
        response = self.client.post(
            '/plantwatch/blocks/',
            {'sort_by': 'netpower', 'sort_method': '-'},
        )
        self.assertEqual(response.status_code, 200)

    def test_blocks_list_power_slider_filtering(self):
        """Test sliding the power slider on blocks list view decreases the number of blocks."""
        response_default = self.client.get('/plantwatch/blocks/')
        count_default = len(response_default.context['blocks'])

        response_500 = self.client.post('/plantwatch/blocks/', {'slider2': '500;1500'})
        count_500 = len(response_500.context['blocks'])
        self.assertLess(count_500, count_default)

    def test_blocks_list_energysource_filtering(self):
        """Test filtering blocks by Energieträger reduces found blocks, and no selection equals all selected."""
        response_all = self.client.get('/plantwatch/blocks/')
        count_all = len(response_all.context['blocks'])

        response_none = self.client.post('/plantwatch/blocks/', {})
        self.assertEqual(len(response_none.context['blocks']), count_all)

        response_erdgas = self.client.post('/plantwatch/blocks/', {'select_powersource': ['Erdgas']})
        count_erdgas = len(response_erdgas.context['blocks'])
        self.assertGreater(count_erdgas, 0)
        self.assertLess(count_erdgas, count_all)
        for block in response_erdgas.context['blocks']:
            self.assertEqual(block.energysource, 'Erdgas')

    def test_static_pages(self):
        """Test all static and informational views return HTTP 200."""
        static_urls = [
            '/plantwatch/impressum',
            '/plantwatch/compliance',
            '/plantwatch/widmung',
            '/plantwatch/niemehrrwe',
            '/plantwatch/friends',
            '/plantwatch/Freunde',
            '/plantwatch/calculations',
            '/plantwatch/Berechnungen',
            '/plantwatch/Downloads',
        ]
        for url in static_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)


class PlantmasterUnitTests(SimpleTestCase):
    def test_divide_safe(self):
        self.assertEqual(divide_safe(10, 2), 5.0)
        self.assertEqual(divide_safe(10, 0), 0)

    def test_calc_workload(self):
        workload = calc_workload(100, 1)
        self.assertIsInstance(workload, float)

    def test_calc_efficency(self):
        eff = calc_efficency(50, 10)
        self.assertEqual(eff, 5000.0)
        self.assertEqual(calc_efficency(50, 0), 0)

    def test_handle_slider(self):
        res = handle_slider("1950;2030")
        self.assertEqual(res, [1950, 2030])

    def test_handle_slider_1(self):
        res = handle_slider_1("1950;2030")
        self.assertEqual(res[:2], [1950, 2030])
        self.assertEqual(len(res), 5)

    def test_handle_slider_2(self):
        res_plants = handle_slider_2("300;4500", is_plants=True)
        self.assertEqual(res_plants[:2], [300, 4500])
        self.assertEqual(len(res_plants), 5)

        res_blocks = handle_slider_2("250;1500", is_plants=False)
        self.assertEqual(res_blocks[:2], [250, 1500])
        self.assertEqual(len(res_blocks), 5)
