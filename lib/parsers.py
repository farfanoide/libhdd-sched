import re
from simulation import Requirement, Lot, Hdd, Simulation


# Regular Expressions used to parse input into usable lists.
pf_sym = re.compile('\*')       # Page Fault Symbol.
movs_sym = re.compile('#')      # Initialization Movements Symbol.
movs_full = re.compile('#\d+')  # Init Movements including number and symbol.
pf_full = re.compile('\*\d+')   # Full Page Fault, including number and symbol.
num_str = re.compile('\d+')          # Regular Requirement.
whitespace = re.compile('\s+')       # Sequence of whitespaces.
w_extremes = re.compile('^\s+|\s+$') # Preceding and Trailing whitespaces.


def _remove_extra_whitespaces(string):
    """
    Removes preceding and trailing whitespaces from a string and
    turns any sequence of whitespaces into only one.

    Example string '  56    33 #5   ' would return '56 33 #5'
    """
    return whitespace.sub(' ', w_extremes.sub('', string))

def _parse_movs(lot_dict, lot_str):
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
    movs = movs_full.findall(lot_str)
    if movs:
        lot_dict['movs'] = movs_sym.sub('', movs.pop(0))
        lot_dict['trash'] += movs
        lot_str = movs_full.sub('', lot_str)
        lot_str = _remove_extra_whitespaces(lot_str)

    return lot_dict, lot_str

def _parse_pfs(lot_dict, lot_str):
    """
    Parses Page Faults out of a string and returns them as a list

    Keyword Arguments
    lot_dict (dict)   -- Dictionary containing basic data tu create a Lot()
    lot_str  (string) -- Data string to parse

    Example lot_str input '*45 34' would return ['*45'] inside lot_dict['pfs']
    """
    pfs = pf_full.findall(lot_str)
    if pfs:
        lot_dict['pfs'] = pfs
        lot_str = pf_full.sub('', lot_str)

    lot_str = _remove_extra_whitespaces(lot_str)
    return lot_dict, lot_str

def _parse_reqs(lot_dict, lot_str):
    """
    Parses regular requirements out of a string and returns them as a list.
    Regular requirements are basically just numbers, thus it is intended to run
    this method on a string from which all Page Faults and Initialization
    Movements have already been extracted.

    Keyword Arguments
    lot_dict (dict)   -- Dictionary containing basic data to create a Lot()
    lot_str  (string) -- Data string to parse

    Example lot_str input '45 #34' would return ['45', '34']
    inside lot_dict['reqs'].
    """
    reqs = num_str.findall(lot_str)
    if reqs:
        lot_dict['reqs'] = reqs
        lot_str = num_str.sub('', lot_str)

    lot_str = _remove_extra_whitespaces(lot_str)
    return lot_dict, lot_str

def _instantiate_reqs(temp_lot):
    lot = {
        'requirements': [parse_requirement(req) for req in temp_lot['reqs']],
        'page_faults': [parse_requirement(pf) for pf in temp_lot['pfs']],
        'movements': int(temp_lot['movs']) if temp_lot['movs'] else 0
    }
    return lot

def parse_lot(lot_str=''):
    """
    Parses and instantiates a Lot from a string.

    Keyword Arguments
    lot_str (string) -- String containing requirements.
    """
    lot = {'movs':  0,
           'pfs':   [],
           'trash': [],
           'reqs':  []}

    lot, lot_str = _parse_movs(lot, lot_str)
    lot, lot_str = _parse_pfs(lot, lot_str)
    lot, lot_str = _parse_reqs(lot, lot_str)

    if lot_str:
        lot['trash'] += lot_str.split(' ')
    # _log(lot['trash'])

    return Lot(_instantiate_reqs(lot))
def parse_lots(lots):
    return [parse_lot(lot_str) for lot_str in lots]

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
    # TODO: add some regex matching for strings representing False
    return bool(boolean)
def parse_list(some_list):
    return some_list


# thoughts on lots:
#     all ParsedStrings should be able to be re-encoded to json
#     lots don't keep original order when parsed

# def _matches_req_str(req_str):
#     req_regex = re.compile('^\*?\d+$')
#     return req_regex.match(req_str)

# def _remove_non_reqs(reqs_list):
#     print reqs_list
#     sanitized = reqs_list.copy()
#     print sanitized
#     for req_str in reqs_list:
#         if not _matches_req_str(req_str):
#             sanitized.remove(req_str)
#
# def parse_lot(lot_str=''):
#     lot_str = _remove_extra_whitespaces(lot_str)
#     lot_str_list = lot_str.split(' ')
#     lot_str_list = _remove_non_reqs(lot_str_list)
#     return  [parse_req(req_str) for req_str in lot_str_list]
