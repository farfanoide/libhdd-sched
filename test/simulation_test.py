import unittest
from lib import parsers
from lib.simulation import Simulation, SimulationResult
from lib.algorithms import FCFS


class TestSimulation(unittest.TestCase):

    simulation = Simulation()
    sim_dict = {'direction': False,
                'hdd': {'name': 'protodisk',
                        'rpm': 5400,
                        'seek_time': 500,
                        'tracks': 512},
                'lots': ['53 151 *500 *400 33 353 100 #45',
                         '*100 455 15 #35',
                         '101 126 366 415'],
                'name': 'protosimulation',
                'position': 250}

    def test_can_handle_run_invocation(self):
        try:
            self.simulation.run(FCFS)
        except AttributeError:
            self.fail('Simulation should respond to #run method')

    def test_result_object(self):
        self.assertIsInstance(self.simulation.run(FCFS), SimulationResult)

    def test_default_attributes(self):
        simulation = Simulation(self.sim_dict)
        s = simulation
        self.assertEqual('protosimulation', s.name)


if __name__ == '__main__':
    unittest.main()
