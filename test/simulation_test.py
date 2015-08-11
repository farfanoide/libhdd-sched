import unittest
from lib import parsers
from lib.simulation import Simulation, SimulationResult
from lib.algorithms import FCFS

class TestSimulation(unittest.TestCase):

    simulation = Simulation()

    def test_can_handle_run_invocation(self):
        try:
            self.simulation.run(FCFS)
        except AttributeError:
            self.fail('Simulation should respond to #run method')

    def test_result_object(self):
        self.assertIsInstance(self.simulation.run(FCFS), SimulationResult)

if __name__ == '__main__':
    unittest.main()
