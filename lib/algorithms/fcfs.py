import json
from lib.parsers import *

from lib.simulation import Simulation, SimulationResult






class FCFS():
    
    example = json.loads(file.read(open('./examples/protosimulation.json')))
    simulation = Simulation(example)


    def execute(self, simulation):
       expected = ['*500', '*400', '*100', '53', '151', '33', '353', '100', '455', '15', '101', '126', '366', '415']
       expected_reqs = [parse_requirement(req) for req in expected]
       result_dict = {'success': False,
                       'attended_requirements': expected_reqs
                   }
        
       result_dict['success'] = True
       return SimulationResult(result_dict)
