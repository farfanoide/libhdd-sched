from lib.parsers import *
from lib.simulation import Simulation, SimulationResult, Lot


class BaseAlgorithm(object):

    """ An abstract class wich defines basic
        functionality shared among algorithms
    """

    def __init__(self, simulation):
        self.simulation = simulation
        self.page_faults = []
        self.unattended = []
        self.attended = []

    def execute(self):
        for lot in self.simulation.lots:
            self.page_faults += lot.page_faults()
            self.unattended += lot.regular_reqs()
            self.movements = lot.movements
            for pf in self.page_faults:
                self.movements -= pf.value
                self.attended.append(pf)
                if self.movements <= 0:
                    break
            if len(self.page_faults) > 0:
                while len(self.unattended) > 0:
                    req = self._next_req(self.unattended)
                    self.movements -= req.value
                    self.attended.append(req)
                    if self.movements <= 0:
                        break

        return SimulationResult(self._result())

    def _next_req(self, requirements):
        return requirements.pop()

    def _result(self):
        return {}
        # populate dict with everything needed  ['success',
                 # 'error',
                 # 'attended_requirements',
                 # 'final_direction',
                 # 'method',
                 # 'lot_admissions',
                 # 'movements']
