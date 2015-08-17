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
            self._merge_with_previous(lot)

            while self._has_page_faults():
                self._attend_req(page_fault)
                if self._exhausted_movements():
                    break

            if not self._has_page_faults():
                while len(self.unattended) > 0:
                    req = self._next_req(self.unattended)
                    self._attend_req(req)
                    if self._exhausted_movements():
                        break

        return SimulationResult(self._result())

    def _attend_req(self, req):
        self.movements -= req.value
        self.attended.append(req)

    def _merge_with_previous(self, lot):
        self.page_faults += lot.page_faults()
        self.unattended += lot.regular_reqs()
        self.movements = lot.movements

    def _exhausted_movements(self):
        return self.movements <= 0

    def _has_page_faults(self):
        return len(self.page_faults) > 0

    def _next_req(self, requirements):
        """ Meant to be overwritten by subclasses"""
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
