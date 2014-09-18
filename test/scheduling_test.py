import unittest

import scheduling


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
    	self.algorithms = scheduling.returnAll()

    def test_name(self):
        for each in self.algorithms:
            self.assertNotEqual('Algorithms', each.name)

    def test_resolve_type(self):
        for each in self.algorithms:
            self.assertIsInstance(each.resolve(), dict)



if __name__ == '__main__':
    unittest.main()
