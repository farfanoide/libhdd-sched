import unittest
from lib import parsers
from lib.simulation import BaseTemplate


class TestBaseTemplate(unittest.TestCase):

    BaseTemplate.default_attributes = {'a': '', 'b': '', 'c': ''}

    values = {
        'empty': {'a': '', 'b': '', 'd': ''},
        'with_values': {'a': '4', 'b': '89', 'd': 'should not be used'}
    }

    def _empty_parsed_string(self):
        return BaseTemplate(self.values['empty'])

    def test_default_attributes(self):
        parsed = BaseTemplate()
        self.assertListEqual(['a', 'b', 'c'], parsed.attribute_names())

    def test_remove_invalid_attributes(self):
        sanitized = BaseTemplate()._remove_invalid_attributes(
            self.values['with_values'])
        self.assertEquals({'a': '4', 'b': '89'}, sanitized)

    def test_attributes_presedence(self):
        parsed = BaseTemplate(self.values['with_values'])
        self.assertListEqual(['4', '89', ''], [parsed.a, parsed.b, parsed.c])

    def test_attribute_names(self):
        parsed = self._empty_parsed_string()
        self.assertListEqual(['a', 'b', 'c'], parsed.attribute_names())

    def test_all_values(self):
        parsed = BaseTemplate(self.values['with_values'])
        self.assertListEqual(['4', '', '89'], parsed.all_values())

    def test_is_empty(self):
        parsed = self._empty_parsed_string()
        self.assertTrue(parsed.is_empty())

    def test_is_not_empty(self):
        parsed = BaseTemplate(self.values['with_values'])
        self.assertFalse(parsed.is_empty())

    def test_is_valid_attribute(self):
        parsed_string = BaseTemplate()
        self.assertTrue(parsed_string._is_valid_attribute('a'))
        self.assertFalse(parsed_string._is_valid_attribute('d'))

    def test_generic_parser_name(self):
        attr_name = BaseTemplate()._generic_parser_name('a')
        self.assertEquals('parse_str', attr_name)

    def test_object_parser_name(self):
        attr_name = BaseTemplate()._object_parser_name('a')
        self.assertEqual('parse_a', attr_name)

    def test_get_parser(self):
        parser = BaseTemplate()._get_parser('lots')
        self.assertEqual(parser, parsers.parse_lots)

    def test_get_parser_returns_generic_parser(self):
        parser = BaseTemplate()._get_parser('a')
        self.assertEqual(parser, parsers.parse_str)

    def test_equal(self):
        parsed = BaseTemplate({'a': 'a'})
        self.assertEqual(parsed, BaseTemplate({'a': 'a'}))
