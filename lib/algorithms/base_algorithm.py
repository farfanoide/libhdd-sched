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
        self.total_movs = 0

    def execute(self):
        for lot in self.simulation.lots:
            self._merge_with_previous(lot)
            self._attend_page_faults()
            self._attend_requirements()

        return SimulationResult(self._result())

    def _attend_page_faults(self):
        # TODO: check this conditional
        while self._has_page_faults():
            page_fault = self.page_faults.pop()
            self._attend_req(page_fault)
            if self._exhausted_movements():
                break


    def _attend_requirements(self):
        # TODO: check this conditional
        if not self._has_page_faults():
            while len(self.unattended) > 0:
                req = self._next_req(self.unattended)
                self._attend_req(req)
                if self._exhausted_movements():
                    break

    def _last_attended(self):
        try:
            return self.attended[-1]
        except IndexError:
            return self.simulation.position

    def _attend_req(self, req):
        distance = self._distance(req, self._last_attended())
        self.total_movs += distance
        self.movements -= distance
        self.attended.append(req)

    def _distance(self, origin, destination):
        return abs(origin - destination)

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
        # raise TypeError
        # TODO: should raise not implemented error.
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
