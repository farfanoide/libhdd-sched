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
            'symbols': '*yo #mamma so* fat# ** ## ***'
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

    def test_empty_data(self):
        # parsed = parsers.parse_req(invalid_data['empty'])
        # self.assert
        return self.skipTest('not implemented yet')


class TestParsedString(unittest.TestCase):

    def setUp(self):
        self.values = {
            'empty': {'a': '', 'b': ''},
            'with_values': {'a': 'a', 'b': 'b'}
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

    def test_creates_object_with_values(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertListEqual(
            self.values['with_values'].values(),
            parsed.all_values())


if __name__ == '__main__':
    unittest.main()
