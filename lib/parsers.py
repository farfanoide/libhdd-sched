import re
from simulation import Requirement, Lot, Hdd, Simulation


# Regular Expressions used to parse input into usable lists.
pf_sym = re.compile('\*')       # Page Fault Symbol.
movs_sym = re.compile('#')      # Initialization Movements Symbol.
movs_full = re.compile('#\d+')  # Init Movements including number and symbol.
pf_full = re.compile('\*\d+')   # Full Page Fault, including number and symbol.
num_str = re.compile('\d+')          # Regular Requirement.
whitespace = re.compile('\s+')       # Sequence of whitespaces.
w_extremes = re.compile('^\s+|\s+$')  # Preceding and Trailing whitespaces.
req_regex = re.compile('^\*?\d+$')


def _remove_extra_whitespaces(string):
    """
    Removes preceding and trailing whitespaces from a string and
    turns any sequence of whitespaces into only one.

    Example string '  56    33 #5   ' would return '56 33 #5'
    """
    return whitespace.sub(' ', w_extremes.sub('', string))


def _parse_movs(lot_str):
    """
    Parses Initialization Movements out of a string and returns them as a
    string. Initialization Movements are intended to let a `Simulation()` know
    how many movements of a Lot() it can attend before another Lot() must be
    taken into account.

    Keyword Arguments
    lot_dict (dict)   -- Dictionary containing basic data tu create a Lot()
    lot_str  (string) -- Data string to parse

    Example lot_str input '45 #34' would return '34' inside lot_dict['movs'].
    If lot_str contains more than one match, only the first one will be used
    and any others will be returned inside lot_dict['trash']
    """
    movs = movs_full.findall(lot_str) if movs_full.findall(lot_str) else 0
    if movs:
        movs = movs_sym.sub('', movs.pop(0))
        lot_str = movs_full.sub('', lot_str)
        lot_str = _remove_extra_whitespaces(lot_str)
    return movs, lot_str


def _instantiate_reqs(temp_lot):
    lot = {
        'requirements': [parse_requirement(req) for req in temp_lot['reqs']],
        'page_faults': [parse_requirement(pf) for pf in temp_lot['pfs']],
        'movements': int(temp_lot['movs']) if temp_lot['movs'] else 0
    }
    return lot


def parse_requirement(reqs_str=''):
    """
    Parses and instantiates a Requirement out of a string.

    Keyword Arguments
    reqs_str (string) -- String containing a number and optionally a symbol.
    """

    if pf_sym.match(reqs_str):
        req = {'value': int(pf_sym.sub('', reqs_str)), 'is_pf': True}
    else:
        req = {'value': int(reqs_str), 'is_pf': False}

    return Requirement(req)


def parse_hdd(hdd_dict={}):
    return Hdd(hdd_dict)


def parse_simulation(simulation_dict={}):
    return Simulation(simulation_dict)


def parse_simulations(simulations):
    return [parse_simulation(simulation_str) for simulation_str in simulations]


def generic_parser(stuff):
    """ Do not know how to parse you bitch """
    return None


def parse_int(integer):
    return int(integer)


def parse_str(string):
    return str(string)


def parse_bool(boolean):
    return False if boolean in ['0', 'false', 'False', 0] else True


def parse_list(some_list):
    return some_list


def _matches_req_str(req_str):
    return req_regex.match(req_str)


def _remove_non_reqs(reqs_list):
    sanitized = []
    for req_str in reqs_list:
        if _matches_req_str(req_str):
            sanitized += [req_str]
    return sanitized


def parse_lot(lot_str=''):
    """
    Parses and instantiates a Lot from a string.

    Keyword Arguments
    lot_str (string) -- String containing requirements.
    """
    lot_dict = {'requirements':  []}
    lot_str = _remove_extra_whitespaces(lot_str)
    lot_dict['movements'], lot_str = _parse_movs(lot_str)
    lot_str_list = _remove_non_reqs(lot_str.split(' '))
    lot_dict['requirements'] = [parse_requirement(req_str) for req_str in lot_str_list]
    return Lot(lot_dict)


def parse_lots(lots):
    return [parse_lot(lot_str) for lot_str in lots]
