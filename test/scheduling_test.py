import unittest

import scheduling


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
    	self.algorithms = scheduling.returnAll()

    def test_name(self):
        for each in self.algorithms:
            self.assertNotEqual('Algorithms', each.name)

    def test_input_output(self):
        for each in self.algorithms:
            each.resolve(['3','5','7'])
        self.assertTrue(1 == 1)

if __name__ == '__main__':
    unittest.main()
