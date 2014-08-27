import re


# Regular Expressions used to parse input into usable lists.


pf_sym = re.compile('\*')       # Page Fault Symbol.
movs_sym = re.compile('#')      # Initialization Movements Symbol.
movs_full = re.compile('#\d+')  # Init Movements including number and symbol.
pf_full = re.compile('\*\d+')   # Full Page Fault, including number and symbol.
num_str = re.compile('\d+')             # Regular Requirement.
whitespace = re.compile('\s+')          # Sequence of whitespaces.
w_extremes = re.compile('^\s+|\s+$')    # Preceding and Trailing whitespaces.
assignment = re.compile('(\w+)=(\w+)')  # Assignment expression.
keyword_title = re.compile('^[A-Z]+\:') # Keyword string title.


class ParsedString(object):

    """
    Data Object to be returned by parsers.

    Keyword arguments
    data (dict) -- Dictionary containing attribute names and it's values
    """

    def __init__(self, data):
        for key, value in data.iteritems():
            setattr(self, key, value)

    def attribute_names(self):
        """ Returns a list of attribute's names for the current instance """
        return self.__dict__.keys()

    def all_values(self):
        """ Returns a list of attribute's values for the current instance """
        return self.__dict__.values()

    def is_empty(self):
        """
        Returns True if all values for the current
        instance are false or None
        """
        return not(any(self.all_values()))


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
    string Initialization Movements are intended to let a Simulation() know how
    many movements of a Lot() it can attend before another Lot() must be taken
    into account.

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
    lot_dict (dict)   -- Dictionary containing basic data tu create a Lot()
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


def _keyword_parser(kw_str=''):
    """
    Receives a string representing variable assignments and returns them
    as a dictionary. Any unused data from kw_str is returned as trash.

    Keyword Arguments
    kw_str (string) -- String representing any assignment.

    Example kw_str = 'HDD: tracks=1024 rpm=5000' would return
    {'tracks':'1024', 'rpm':'5000'}, 'HDD:'
    """
    data = dict(assignment.findall(kw_str))
    trash = _remove_extra_whitespaces(assignment.sub('', kw_str))
    return data, trash


def parse_req(reqs_str=''):
    """
    Returns a ParsedString out of a simple string, ready to
    instatiate a Requirement().

    Keyword Arguments
    reqs_str (string) -- String containing a number and optionally a symbol.
    Example reqs_str '*55' would return
    ParsedString({'requirement': 55, 'is_pf': True})
    """
    if pf_sym.match(reqs_str):
        req = {'requirement': int(pf_sym.sub('', reqs_str)), 'is_pf': True}
    else:
        req = {'requirement': int(reqs_str), 'is_pf': False}

    return ParsedString(req)


def parse_hdd(hdd_str=''):
    hdd_str = keyword_title.sub('', hdd_str)
    hdd, trash = _keyword_parser(hdd_str)
    if trash:
        hdd['trash'] = trash.split(' ')
    return ParsedString(hdd)


def parse_lot(lot_str=''):
    """
    Returns a ParsedString out of a simple string, ready to
    instantiate a Lot().

    Keyword Arguments
    lot_str (string) -- String containing a number and optionally a symbol.

    Example lot_str '*55 45 66 89 #33 some useless strings' would return
    ParsedString({
    'reqs': ['45', '66', '89'],
    'pfs': ['*55'],
    'movs': '33',
    'trash': ['some', 'useless', 'strings']
    })
    """
    lot = {'movs':  None,
           'pfs':   [],
           'trash': [],
           'reqs':  []}
    lot, lot_str = _parse_movs(lot, lot_str)
    lot, lot_str = _parse_pfs(lot, lot_str)
    lot, lot_str = _parse_reqs(lot, lot_str)
    if lot_str:
        lot['trash'] += lot_str.split(' ')

    return ParsedString(lot)
