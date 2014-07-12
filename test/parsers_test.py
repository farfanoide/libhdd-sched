import unittest
from lib.parsers import ReqParser

class TestReqParser(unittest.TestCase):

    def test_not_pf_and_value(self):
        """ Test regular requirement """
        req = ReqParser.parse('4')
        self.assertEquals(req[0], 4, 'Parsed number error.')
        self.assertFalse(req[1], 'Parsed page fault  error.')

    def test_pf_and_value(self):
        """ Test page fault requirement """
        req = ReqParser.parse('*448')
        self.assertEquals(req[0], 448, 'Parsed number error.')
        self.assertTrue(req[1], 'Parsed page fault  error.')


if __name__ == '__main__':
    unittest.main()
