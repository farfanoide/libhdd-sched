import unittest
from lib.simulation import Requirement


class TestRequirement(unittest.TestCase):

    page_fault  = {'value': 4, 'is_pf': True}
    regular_req = {'value': 4, 'is_pf': False}

    def test_value_type(self):
        req = Requirement(self.page_fault)
        self.assertIsInstance(req.value, int)

    def test_is_not_pf(self):
        req = Requirement(self.regular_req)
        self.assertFalse(req.is_pf)

    def test_is_pf(self):
        req = Requirement(self.page_fault)
        self.assertTrue(req.is_pf)


if __name__ == '__main__':
    unittest.main()
