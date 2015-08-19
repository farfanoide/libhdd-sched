import unittest
from lib import parsers
from lib.simulation import Simulation
from lib.algorithms.base_algorithm import BaseAlgorithm


class TestBaseAlgorithm(unittest.TestCase):

    def setUp(self):
        self.algorithm = BaseAlgorithm(Simulation({}))
        self.origin = parsers.parse_requirement('50')
        self.destination = parsers.parse_requirement('40')

    def test_distance(self):
        self.assertEqual(10, self.algorithm._distance(
            self.origin, self.destination))

    def test_inverse_distance(self):
        self.assertEqual(10, self.algorithm._distance(
            self.destination, self.origin))

    def test_merge_with_previous(self):
        lot = parsers.parse_lot('67 89 *34 0 #23')
        self.assertListEqual([], self.algorithm.page_faults)
        self.algorithm._merge_with_previous(lot)
        self.assertListEqual([parsers.parse_requirement('*34')], self.algorithm.page_faults)

