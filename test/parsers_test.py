import unittest
from lib import parsers
from lib.parsers import ParsedString



class TestReqParser(unittest.TestCase):

    def test_not_pf_and_value(self):
        """ Test regular requirement """
        parsed = parsers.parse_req('4')
        self.assertEquals(parsed.requirement, 4, 'Parsed number error.')
        self.assertFalse(parsed.is_pf, 'Parsed page fault error.')

    def test_pf_and_value(self):
        """ Test page fault requirement """
        parsed = parsers.parse_req('*448')
        self.assertEquals(parsed.requirement, 448, 'Parsed number error.')
        self.assertTrue(parsed.is_pf, 'Parsed page fault error.')


class TestParsers(unittest.TestCase):

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
            'symbols': '#30',
            'all': '34 *12 456 #230 *90',
        }
        self.mixed_data = {
            'numbers_words': '45 09 tres 88 ilegal 456',
            'numbers_words_symbols': '*45  09 tres 88 ilegal 456 #45',
            'two_hashtags': '#35  09 tres 88 ilegal 456 #45',
        }
        self.lot_dict = {
            'movs': None,
            'pfs': [],
            'trash': [],
            'reqs': []
        }

    #  Parser Helpers Tests
    def test_parse_movs_helper(self):
        lot_dict, parsed_str = parsers._parse_movs(
            self.lot_dict, self.valid_data['all'])
        self.assertEqual(lot_dict['movs'], '230')
        self.assertEqual(parsed_str, '34 *12 456 *90')

    def test_remove_extra_whitespaces_helper(self):
        parsed_str = parsers._remove_extra_whitespaces(
            self.invalid_data['multi_whitespace'])
        self.assertEqual(parsed_str, '34 *12 456 230 *90')

    def test_parse_movs_helper_without_movs(self):
        lot_dict, parsed_str = parsers._parse_movs(
            self.lot_dict, self.valid_data['only_numbers'])
        self.assertIsNone(lot_dict['movs'])
        self.assertEqual(parsed_str, self.valid_data['only_numbers'])

    def test_parse_pfs_helper(self):
        lot_dict, parsed_str = parsers._parse_pfs(
            self.lot_dict, self.valid_data['only_pfs'])
        self.assertListEqual(lot_dict['pfs'], ['*34', '*76', '*32', '*342'])
        self.assertEqual(parsed_str, '')

    def test_parse_lot_with_only_numbers(self):
        parsed = parsers.parse_lot(self.valid_data['only_numbers'])
        self.assertListEqual(parsed.reqs, ['5', '90', '34', '88'])
        self.assertIsNone(parsed.movs)
        self.assertListEqual(parsed.pfs, [])
        self.assertListEqual(parsed.trash, [])

    def test_parse_lot_with_only_pfs(self):
        parsed = parsers.parse_lot(self.valid_data['only_pfs'])
        self.assertListEqual(parsed.pfs, ['*34', '*76', '*32', '*342'])
        self.assertIsNone(parsed.movs)
        self.assertListEqual(parsed.reqs, [])
        self.assertListEqual(parsed.trash, [])

    def test_parse_lot_with_numbers_and_pfs(self):
        parsed = parsers.parse_lot(self.valid_data['numbers_pfs'])
        self.assertListEqual(parsed.pfs, ['*12', '*90'])
        self.assertListEqual(parsed.reqs, ['34', '456', '230'])
        self.assertIsNone(parsed.movs)
        self.assertListEqual(parsed.trash, [])

    def test_parse_requirements(self):
        self.lot_dict, parsed_str = parsers._parse_reqs(
            self.lot_dict, self.valid_data['only_numbers'])
        self.assertListEqual(
            self.lot_dict['reqs'], ['5', '90', '34', '88'])
        self.assertEqual(parsed_str, '')

    def test_empty_data(self):
        parsed = parsers.parse_lot(self.invalid_data['empty'])
        self.assertTrue(parsed.is_empty())

    def test_parses_movement(self):
        parsed = parsers.parse_lot(self.valid_data['symbols'])
        self.assertEqual(parsed.movs, '30')
        self.assertListEqual(parsed.pfs, [])
        self.assertListEqual(parsed.reqs, [])
        self.assertListEqual(parsed.trash, [])

    def test_parses_movements(self):
        parsed = parsers.parse_lot(self.mixed_data['two_hashtags'])
        self.assertEqual(parsed.movs, '35')
        self.assertListEqual(parsed.pfs, [])
        self.assertListEqual(parsed.reqs, ['09', '88', '456'])
        self.assertListEqual(parsed.trash, ['#45', 'tres', 'ilegal'])

class TestParsedString(unittest.TestCase):

    def setUp(self):
        self.values = {
            'empty':        {'a': '', 'b': ''},
            'with_values':  {'a': '4', 'b': '89'}
        }

    def _empty_parsed_string(self):
        return ParsedString(self.values['empty'])

    def test_attribute_names(self):
        parsed = self._empty_parsed_string()
        self.assertListEqual(self.values['empty'].keys(),
                             parsed.attribute_names())

    def test_creates_object_with_values(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertListEqual(self.values['with_values'].values(),
                             parsed.all_values())

    def test_all_values(self):
        parsed = self._empty_parsed_string()
        self.assertListEqual(self.values['empty'].values(),
                             parsed.all_values())

    def test_is_empty(self):
        parsed = self._empty_parsed_string()
        self.assertTrue(parsed.is_empty())

    def test_is_not_empty(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertFalse(parsed.is_empty())

#class TestHddParser(unittest.TestCase):

#    def set_up(self):
#        self.data = {
#            valid: 'tracks=512 rpm=5400 seek_time=500 name=protodisk',
#            wo

class TestParserHelpers(unittest.TestCase):

    def setUp(self):
        self.valid_dict = { 'tracks':'512',
                            'rpm':'5400',
                            'seek_time':'500',
                            'name':'protodisk' ,
        }
        self.invalid_data = { 'empty': '',
            'non_kw': 'are you talking to me?',
        }
        self.valid_data = {
            'valid': 'tracks=512 rpm=5400 seek_time=500 name=protodisk',
            'mixed': 'HDD: tracks=512 rpm=5400 seek_time=500 name=protodisk',
        }
    def test_keyword_parser_types(self):
        parsed, trash = parsers._keyword_parser()
        self.assertIsInstance(parsed, dict)
        self.assertIsInstance(trash, str)

    def test_empty_keyword_parser(self):
        parsed, trash = parsers._keyword_parser(self.invalid_data['empty'])
        self.assertDictEqual(parsed, {})
        self.assertEqual(trash, '')

    def test_keyword_parser_valid(self):
        parsed, trash = parsers._keyword_parser(self.valid_data['valid'])
        self.assertDictEqual(parsed, self.valid_dict)
        self.assertEqual(trash, '')

    def test_keyword_parser_trash(self):
        parsed, trash = parsers._keyword_parser(self.invalid_data['non_kw'])
        self.assertEquals(trash, self.invalid_data['non_kw'])
        self.assertDictEqual(parsed, {})

    def test_keyword_parser_mixed(self):
        parsed, trash = parsers._keyword_parser(self.valid_data['mixed'])
        self.assertEquals(trash, 'HDD:')
        self.assertDictEqual(parsed, self.valid_dict)


if __name__ == '__main__':
    unittest.main()
