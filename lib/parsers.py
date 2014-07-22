import re


class ParsedString(object):
    """
    Data Object to be returned by parers.

    Keyword arguments
    attrs (dict) -- Dictionary containing attribute names and it's values
    """

    def __init__(self, attrs):
        for key, value in attrs.iteritems():
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

# Parsers


def parse_req(str_req):
    pf_str = re.compile('\*')
    if pf_str.match(str_req):
        req = ParsedString({
            'requirement': int(pf_str.sub('', str_req)),
            'is_pf': True
        })
    else:
        req = ParsedString({'requirement': int(str_req), 'is_pf': False})

    return req


def parse_lot(str_lot):
    # TODO: implement parsed lot data object
    pass
