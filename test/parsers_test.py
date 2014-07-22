import unittest
from lib import parsers


class TestReqParser(unittest.TestCase):

    def test_not_pf_and_value(self):
        """ Test regular requirement """
        req = parsers.parse_req('4')
        self.assertEquals(req[0], 4, 'Parsed number error.')
        self.assertFalse(req[1], 'Parsed page fault  error.')

    def test_pf_and_value(self):
        """ Test page fault requirement """
        req = parsers.parse_req('*448')
        self.assertEquals(req[0], 448, 'Parsed number error.')
        self.assertTrue(req[1], 'Parsed page fault  error.')


class TestLotParser(unittest.TestCase):
    invalid_data = {'empty': '',
                    'only_words': 'no numbers here',
                    'symbols': '*yo #mamma so* fat# ** ## ***'}
    valid_data = {'only_numbers': '5 90 34 88',
                  'only_pfs': '*34 *76 *32 *342',
                  'numbers_pfs': '34 *12 456 230 *90',
                  'symbols': '#30'}
    mixed_data = {'numbers_words': '45 09 tres 88 ilegal 456',
                  'numbers_words_symbols': '*45  09 tres 88 ilegal 456 #45',
                  'two_hashtags': '#35  09 tres 88 ilegal 456 #45'}

    def test_empty_data(self):
        # parsed = parsers.parse_req(invalid_data['empty'])
        # self.assert
        return self.skipTest('not implemented yet')

if __name__ == '__main__':
    unittest.main()
