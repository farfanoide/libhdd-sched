import unittest
from lib.lot import Requirement


class TestRequirement(unittest.TestCase):

    def test_value_type(self):
        req = Requirement('4')
        self.assertIsInstance(req.value, int)

    def test_is_not_pf(self):
        req = Requirement('4')
        self.assertFalse(req.is_pf)

    def test_is_pf(self):
        req = Requirement('4', True)
        self.assertTrue(req.is_pf)


if __name__ == '__main__':
    unittest.main()
