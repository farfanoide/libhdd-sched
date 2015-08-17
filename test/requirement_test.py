import unittest
from lib import parsers
from lib.simulation import Requirement


class TestRequirement(unittest.TestCase):

    page_fault  = {'value': 4, 'is_pf': True}
    regular_req = {'value': 4, 'is_pf': False}

    def test_requirement_data_types(self):
        req = Requirement(self.page_fault)
        self.assertIsInstance(req.value, int)
        self.assertIsInstance(req.is_pf, bool)

    def test_is_not_pf(self):
        req = Requirement(self.regular_req)
        self.assertFalse(req.is_pf)

    def test_is_pf(self):
        req = Requirement(self.page_fault)
        self.assertTrue(req.is_pf)

    def test_default_requirement(self):
        req = Requirement()
        self.assertIsInstance(req, Requirement)
        self.assertEqual(req.value, 0)
        self.assertFalse(req.is_pf)

    def test_pf_str_representation(self):
        pf = parsers.parse_requirement('*5')
        self.assertEqual('*5', str(pf))

    def test_req_str_representation(self):
        req = parsers.parse_requirement('34')
        self.assertEqual('34', str(req))


if __name__ == '__main__':
    unittest.main()
