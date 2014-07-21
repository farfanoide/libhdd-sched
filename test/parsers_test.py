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


if __name__ == '__main__':
    unittest.main()
