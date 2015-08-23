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
        self.lot_admissions = []
        self.attended = []
        self.total_movs = 0
        self.status = 0

    def _method(self):
        return self.__class__.__name__

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
            # TODO: append to lot_admissions if neccesary
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
        """Meant to be overwritten by subclasses"""
        # TODO: should raise not implemented error.
        return requirements.pop()

    def _final_direction(self):
        try:
            final_dir = (self.attended[-1] - self.attended[-2]) > 0
        except IndexError:
            final_dir = self.simulation.direction

        return ('left', 'right')[final_dir]

    def _result(self):
        return {
            'status': self.status,
            'attended_requirements': self.attended,
            'final_direction': self._final_direction(),
            'method': self._method(),
            'lot_admissions': self.lot_admissions,
            'movements': self.total_movs,
        }
