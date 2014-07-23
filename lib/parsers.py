import re


# Regex
pf_sym = re.compile('\*')
pf_full = re.compile('\*\d+')
movs_sym = re.compile('#')
movs_full = re.compile('#\d+')
num_str = re.compile('\d+')
whitespace = re.compile('\s+')
w_extremes = re.compile('^\s+|\s+$')


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


def parse_req(reqs_str):
    if pf_sym.match(reqs_str):
        req = {'requirement': int(pf_sym.sub('', reqs_str)), 'is_pf': True}
    else:
        req = {'requirement': int(reqs_str), 'is_pf': False}

    return ParsedString(req)


def parse_hdd(hdd_str):
    pass


def _remove_extra_whitespaces(string):
        return whitespace.sub(' ', w_extremes.sub('', string))


def _parse_movs(lot_dict, lot_str):
    movs = movs_full.findall(lot_str)
    if movs:
        lot_dict['movs'] = movs_sym.sub('', movs.pop(0))
        lot_dict['trash'] += movs
        lot_str = movs_full.sub('', lot_str)
    lot_str = _remove_extra_whitespaces(lot_str)

    return lot_dict, lot_str


def _parse_pfs(lot_dict, lot_str):
    pfs = pf_full.findall(lot_str)
    if pfs:
        lot_dict['pfs'] = pfs
        lot_str = pf_full.sub('', lot_str)

    lot_str = _remove_extra_whitespaces(lot_str)
    return lot_dict, lot_str


def _parse_reqs(lot_dict, lot_str):
    reqs = num_str.findall(lot_str)
    if reqs:
        lot_dict['reqs'] = reqs
        lot_str = num_str.sub('', lot_str)

    lot_str = _remove_extra_whitespaces(lot_str)
    return lot_dict, lot_str


def parse_lot(lot_str):
    lot = {'movs': None,
           'pfs': [],
           'trash': [],
           'reqs': []}
    lot, lot_str = _parse_movs(lot, lot_str)
    lot, lot_str = _parse_pfs(lot, lot_str)
    lot, lot_str = _parse_reqs(lot, lot_str)
    if lot_str:
        lot['trash'] += lot_str.split(' ')

    return ParsedString(lot)
