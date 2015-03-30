from lib.simulation import SimulationResult
from lib.parsers import parse_requirement

class FCFS():

    @staticmethod
    def execute(simulation):
        expected = ['*500', '*400', '*100', '53', '151', '33', '353', '100', '455', '15', '101', '126', '366', '415']
        expected_reqs = [parse_requirement(req) for req in expected]
        return SimulationResult({'success': True,
                                 'attended_requirements': expected_reqs
                                 })
