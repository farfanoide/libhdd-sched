import unittest
from lib.simulation import ParsedString


class TestParsedString(unittest.TestCase):

    ParsedString.permitted_attributes = ['a', 'b', 'c']

    values = {
        'empty': {'a': '', 'b': '', 'd': ''},
        'with_values': {'a': '4', 'b': '89', 'd': 'should not be used'}
    }

    def _empty_parsed_string(self):
        return ParsedString(self.values['empty'])

    def test_attribute_names(self):
        parsed = self._empty_parsed_string()
        self.assertListEqual(['a', 'b'], parsed.attribute_names())

    def test_all_values(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertListEqual(['4', '89'], parsed.all_values())

    def test_is_empty(self):
        parsed = self._empty_parsed_string()
        self.assertTrue(parsed.is_empty())

    def test_is_not_empty(self):
        parsed = ParsedString(self.values['with_values'])
        self.assertFalse(parsed.is_empty())

    def test_is_valid_attribute(self):
        parsed_string = ParsedString()
        self.assertTrue(parsed_string._is_valid_attribute('a'))
        self.assertFalse(parsed_string._is_valid_attribute('d'))
