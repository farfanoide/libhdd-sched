import unittest
import json
from lib.algorithms import FCFS
from lib.simulation import Simulation, SimulationResult
from lib.parsers import parse_lot


class TestFcfs(unittest.TestCase):

    simulation_dict = json.loads(file.read(open('./examples/protosimulation.json')))
    simulation = Simulation(simulation_dict)
    expected = '*500 *400 *100 53 151 33 353 100 455 15 101 126 366 415'
    expected_reqs = parse_lot(expected).requirements

    def setUp(self):
        self.results = FCFS.execute(self.simulation)

    def test_fcfs_returns_correct_object(self):
        self.assertIsInstance(self.results, SimulationResult)

    def test_fcfs_attended_requirements_order(self):
        self.assertEquals(
            self.results.attended_requirements,
            self.expected_reqs)

    def test_fcfs_default_behaviour(self):
        self.assertTrue(self.results.success)
