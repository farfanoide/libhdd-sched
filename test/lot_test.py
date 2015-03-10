import unittest
from lib import parsers
from lib.simulation import Lot


class TestLot(unittest.TestCase):

    data = { 'numbers_pfs': '34 *12 456 230 *90' }

    def test_lot_type(self):
        # TODO: rethink basic tests for this class
        lot = parsers.parse_lot(self.data['numbers_pfs'])
        self.assertIsInstance(lot, Lot)

if __name__ == '__main__':
    unittest.main()
