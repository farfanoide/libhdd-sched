import unittest
import json
from lib.algorithms import FCFS
from lib.simulation import Simulation, SimulationResult
class TestFcfs(unittest.TestCase):

    simulation_dict = json.loads(file.read(open('./examples/protosimulation.json')))
    simulation = Simulation(simulation_dict)

    def test_fcfs_default_behaviour(self):
        results = FCFS.execute(self.simulation)
        self.assertIsInstance(results, SimulationResult)
#        self.assertIsInstance(results.attended_requirements, list)
