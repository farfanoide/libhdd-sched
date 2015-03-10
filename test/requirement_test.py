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


if __name__ == '__main__':
    unittest.main()
