import unittest
from lib import parsers
from lib.parsers import ParsedString


class TestReqParser(unittest.TestCase):

    def test_not_pf_and_value(self):
        """ Test regular requirement """
        parsed = parsers.parse_req('4')
        self.assertEquals(parsed.requirement, 4, 'Parsed number error.')
        self.assertFalse(parsed.is_pf, 'Parsed page fault  error.')

    def test_pf_and_value(self):
        """ Test page fault requirement """
        parsed = parsers.parse_req('*448')
        self.assertEquals(parsed.requirement, 448, 'Parsed number error.')
        self.assertTrue(parsed.is_pf, 'Parsed page fault  error.')


class TestLotParser(unittest.TestCase):

    def setUp(self):
        self.invalid_data = {
            'empty': '',
            'only_words': 'no numbers here',
            'symbols': '*yo #mamma so* fat# ** ## ***',
            'multi_whitespace': '    34   *12     456 230 *90  '
        }
        self.valid_data = {
            'only_numbers': '5 90 34 88',
            'only_pfs': '*34 *76 *32 *342',
            'numbers_pfs': '34 *12 456 230 *90',
            'symbols': '#30'
        }
        self.mixed_data = {
            'numbers_words': '45 09 tres 88 ilegal 456',
            'numbers_words_symbols': '*45  09 tres 88 ilegal 456 #45',
            'two_hashtags': '#35  09 tres 88 ilegal 456 #45'
        }
        self.lot_dict = {
            'movs': None, 'pfs': [],
            'trash': [], 'reqs': []
        }

    def test_remove_extra_whitespaces_helper(self):
        parsed_str = parsers._remove_extra_whitespaces(
            self.invalid_data['multi_whitespace'])
        self.assertEqual(parsed_str, '34 *12 456 230 *90')


    def test_parse_movs_helper(self):
        self.lot_dict, parsed_str = parsers._parse_movs(
            self.lot_dict, self.mixed_data['two_hashtags'])
        self.assertEqual(self.lot_dict['movs'], '35')
        self.assertEqual(parsed_str, '09 tres 88 ilegal 456')

    def test_parse_movs_helper_without_movs(self):
        self.lot_dict, parsed_str = parsers._parse_movs(
            self.lot_dict, self.valid_data['only_numbers'])
        self.assertIsNone(self.lot_dict['movs'])
        self.assertEqual(parsed_str, self.valid_data['only_numbers'])

    def test_parse_pfs_helper(self):
        self.lot_dict, parsed_str = parsers._parse_pfs(
            self.lot_dict, self.valid_data['only_pfs'])
        self.assertListEqual(self.lot_dict['pfs'], ['*34', '*76', '*32', '*342'])
        self.assertEqual(parsed_str, '')

    def test_empty_data(self):
        parsed = parsers.parse_lot(self.invalid_data['empty'])
        self.assertTrue(parsed.is_empty())

    def test_parses_movement(self):
        parsed = parsers.parse_lot(self.valid_data['symbols'])
        self.assertEqual(parsed.movs, '30')

    def test_parses_movements(self):
        parsed = parsers.parse_lot(self.mixed_data['two_hashtags'])
        self.assertEqual(parsed.movs, '35')
        self.assertListEqual(parsed.trash, ['#45'])


class TestParsedString(unittest.TestCase):

    def setUp(self):
        self.values = {
            'empty': {'a': '', 'b': ''},
            'with_values': {'a': '4', 'b': '89'}
        }

    def empty_parsed_string(self):
        return ParsedString(self.values['empty'])

    def test_attribute_names(self):
        parsed = self.empty_parsed_string()
        self.assertListEqual(
            self.values['empty'].keys(),
            parsed.attribute_names())

    def test_all_values(self):
        parsed = self.empty_parsed_string()
        self.assertListEqual(
            self.values['empty'].values(),
            parsed.all_values())

    def test_is_empty(self):
        parsed = self.empty_parsed_string()
        self.assertTrue(parsed.is_empty())

    def test_is_not_empty(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertFalse(parsed.is_empty())

    def test_creates_object_with_values(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertListEqual(
            self.values['with_values'].values(),
            parsed.all_values())


if __name__ == '__main__':
    unittest.main()
