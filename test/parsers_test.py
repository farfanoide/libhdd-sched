import unittest
from lib import parsers
from lib.lot import Requirement, Lot


class TestReqParser(unittest.TestCase):

    def test_not_pf_and_value(self):
        """ Test regular requirement """
        parsed = parsers.parse_req('4')
        self.assertEquals(parsed.value, 4, 'Parsed number error.')
        self.assertFalse(parsed.is_pf, 'Parsed page fault error.')

    def test_pf_and_value(self):
        """ Test page fault requirement """
        parsed = parsers.parse_req('*448')
        self.assertEquals(parsed.value, 448, 'Parsed number error.')
        self.assertTrue(parsed.is_pf, 'Parsed page fault error.')


class TestLotParser(unittest.TestCase):

    invalid_data = {
        'empty': '',
        'only_words': 'no numbers here',
        'symbols': '*yo #mamma so* fat# ** ## ***',
    }
    valid_data = {
        'only_numbers': '5 90 34 88',
        'only_pfs': '*34 *76 *32 *342',
        'numbers_pfs': '34 *12 456 230 *90',
        'symbols': '#30',
    }
    mixed_data = {
        'numbers_words': '45 09 tres 88 ilegal 456',
        'numbers_words_symbols': '*45  09 tres 88 ilegal 456 #45',
        'two_hashtags': '#35  09 tres 88 ilegal 456 #45',
    }
    lot_dict = {'movs': None, 'pfs': [], 'trash': [], 'reqs': []}

    def test_parsed_lot_is_actual_lot(self):
        lot = parsers.parse_lot(self.invalid_data['empty'])
        self.assertIsInstance(lot, Lot)

    def test_parsed_lot_requirements(self):
        lot = parsers.parse_lot(self.valid_data['only_numbers'])
        for req in lot.requirements:
            self.assertIsInstance(req, Requirement)

    def test_parse_lot_amount_of_requirements(self):
        lot = parsers.parse_lot(self.valid_data['numbers_pfs'])
        self.assertEqual(len(lot.requirements), 3)

    def test_parse_lot_with_only_pfs(self):
        # TODO: bdd this shit -> test that req parser is called
        lot = parsers.parse_lot(self.valid_data['only_pfs'])
        self.assertEqual(len(lot.page_faults), 4)

    def test_empty_data(self):
        lot = parsers.parse_lot(self.invalid_data['empty'])
        self.assertTrue(lot.is_empty())

    def test_parses_movement(self):
        lot = parsers.parse_lot(self.valid_data['symbols'])
        self.assertEqual(lot.movements, 30)


    def test_parses_first_movement_symbol(self):
        lot = parsers.parse_lot(self.mixed_data['two_hashtags'])
        self.assertEqual(lot.movements, 35)


    def test_parse_lot_amount_of_requirements(self):
        lot = parsers.parse_lot(self.mixed_data['numbers_words'])
        self.assertEqual(len(lot.requirements), 4)


# class TestHddParser(unittest.TestCase):
#
#     def setUp(self):
#         self.data = {
#             'valid': 'HDD: tracks=512 rpm=5400 seek_time=500 name=protodisk',
#             'invalid': "some sarasa h3r3",
#             'empty': '',
#             'mixed': 'HDD: tracks=512 rpm=5400 seek_time= high  '
#         }
#
#     def test_parse_hdd_type(self):
#         parsed = parsers.parse_hdd()
#         self.assertIsInstance(parsed, ParsedString)
#
#     def test_parse_empty_hdd(self):
#         parsed = parsers.parse_hdd(self.data['empty'])
#         self.assertTrue(parsed.is_empty())
#
#     def test_parse_valid_hdd(self):
#         parsed = parsers.parse_hdd(self.data['valid'])
#         self.assertListEqual(
#             sorted(parsed.all_values()),
#             sorted(['512', '5400', '500', 'protodisk']))
#         self.assertListEqual(
#             sorted(parsed.attribute_names()),
#             sorted(['tracks', 'rpm', 'seek_time', 'name']))
#
#     def test_parse_mixed_hdd(self):
#         parsed = parsers.parse_hdd(self.data['mixed'])
#         self.assertEqual(parsed.trash, ['seek_time=', 'high'])
#         self.assertListEqual(
#             sorted(parsed.all_values()),
#             sorted(['512', '5400', ['seek_time=', 'high']]))
#         self.assertListEqual(
#             sorted(parsed.attribute_names()),
#             sorted(['tracks', 'rpm', 'trash']))
#
#
# class TestParserHelpers(unittest.TestCase):
#
#     def setUp(self):
#         self.lot_dict = {'movs': None, 'pfs': [], 'trash': [], 'reqs': []}
#         self.hdd_dict = {
#             'tracks': '512',
#             'rpm': '5400',
#             'seek_time': '500',
#             'name': 'protodisk'
#         }
#         self.invalid_data = {
#             'empty': '',
#             'non_kw': 'are you talking to me?',
#             'multi_whitespace': '    34   *12     456 230 *90  '
#         }
#         self.valid_data = {
#             'only_pfs': '*34 *76 *32 *342',
#             'only_numbers': '5 90 34 88',
#             'all': '34 *12 456 #230 *90',
#             'valid': 'tracks=512 rpm=5400 seek_time=500 name=protodisk',
#             'mixed': 'HDD: tracks=512 rpm=5400 seek_time=500 name=protodisk',
#         }
#
#     def test_keyword_parser_types(self):
#         parsed, trash = parsers._keyword_parser()
#         self.assertIsInstance(parsed, dict)
#         self.assertIsInstance(trash, str)
#
#     def test_keyword_parser_with_empty_str(self):
#         parsed, trash = parsers._keyword_parser(self.invalid_data['empty'])
#         self.assertDictEqual(parsed, {})
#         self.assertEqual(trash, '')
#
#     def test_keyword_parser_valid(self):
#         parsed, trash = parsers._keyword_parser(self.valid_data['valid'])
#         self.assertDictEqual(parsed, self.hdd_dict)
#         self.assertEqual(trash, '')
#
#     def test_keyword_parser_trash(self):
#         parsed, trash = parsers._keyword_parser(self.invalid_data['non_kw'])
#         self.assertEquals(trash, self.invalid_data['non_kw'])
#         self.assertDictEqual(parsed, {})
#
#     def test_keyword_parser_mixed(self):
#         parsed, trash = parsers._keyword_parser(self.valid_data['mixed'])
#         self.assertEquals(trash, 'HDD:')
#         self.assertDictEqual(parsed, self.hdd_dict)
#
#     def test_remove_extra_whitespaces_helper(self):
#         parsed_str = parsers._remove_extra_whitespaces(
#             self.invalid_data['multi_whitespace'])
#         self.assertEqual(parsed_str, '34 *12 456 230 *90')
#
#     def test_parse_movs_helper(self):
#         lot_dict, parsed_str = parsers._parse_movs(
#             self.lot_dict, self.valid_data['all'])
#         self.assertEqual(lot_dict['movs'], '230')
#         self.assertEqual(parsed_str, '34 *12 456 *90')
#
#     def test_parse_movs_helper_without_movs(self):
#         lot_dict, parsed_str = parsers._parse_movs(
#             self.lot_dict, self.valid_data['only_numbers'])
#         self.assertIsNone(lot_dict['movs'])
#         self.assertEqual(parsed_str, self.valid_data['only_numbers'])
#
#     def test_parse_pfs_helper(self):
#         lot_dict, parsed_str = parsers._parse_pfs(
#             self.lot_dict, self.valid_data['only_pfs'])
#         self.assertListEqual(lot_dict['pfs'], ['*34', '*76', '*32', '*342'])
#         self.assertEqual(parsed_str, '')
#
#     def test_parse_requirements(self):
#         self.lot_dict, parsed_str = parsers._parse_reqs(
#             self.lot_dict, self.valid_data['only_numbers'])
#         self.assertListEqual(
#             self.lot_dict['reqs'], ['5', '90', '34', '88'])
#         self.assertEqual(parsed_str, '')
#

if __name__ == '__main__':
    unittest.main()


# def parse_simulation(json):
# si json.has_key('simulations') parsear varias
# sino
#    parsear una
# orden normal
# json = json.loads(file.open(archivito))
# simulation = parsers.parse_simulation(json)
# Simulation.run('fcfs')
#       -> algorithms.FCFS.resolve(self.lots)
# js = json.loads('{\
    #     "simulations": {\
    #         "simulation_1": {"hdd": "sarasa", "position": 512},\
    #         "simulation_1": {"hdd": "sarasa", "position": 512},\
    #         "simulation_1": {"hdd": "sarasa", "position": 512}\
    #     }\
    # }')
