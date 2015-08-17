import unittest
from lib.parsers import parse_lot, parse_requirement
from lib.simulation import Lot


class TestLot(unittest.TestCase):

    data = {'numbers_pfs': '34 *12 456 230 *90'}

    def test_lot_type(self):
        lot = parse_lot(self.data['numbers_pfs'])
        self.assertIsInstance(lot.requirements, list)

    def test_str_representation(self):
        lot = parse_lot(self.data['numbers_pfs'])
        self.assertEquals(str(lot), 'Requirements: 34 *12 456 230 *90, Movements: 0')

    def test_page_faults(self):
        expected_pfs = [parse_requirement(req) for req in ['*12', '*90']]
        lot = parse_lot(self.data['numbers_pfs'])
        self.assertEquals(expected_pfs, lot.page_faults())

    def test_page_faults(self):
        expected_pfs = [parse_requirement(req) for req in ['*12', '*90']]
        lot = parse_lot(self.data['numbers_pfs'])
        self.assertEquals(expected_pfs, lot.page_faults())

if __name__ == '__main__':
    unittest.main()
