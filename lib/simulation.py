class ParsedString(object):

    """
    Simple dynamic data object to be instatiated based off of a dictionary.
    Any subclass should set a whitelist of permitted attributes in it's class
    variable 'permitted_attributes'


    Keyword arguments
    data (dict) -- Dictionary containing attribute names and it's values
    """

    permitted_attributes = []
    default_attributes = {}

    def __init__(self, data={}):
        data = dict(self.default_attributes.items() + data.items())
        for key, value in data.iteritems():
            if self._is_valid_attribute(key):
                setattr(self, key, value)

    def attribute_names(self):
        """ Returns a list with all attribute names for the current instance """
        return sorted(self.__dict__.keys())

    def all_values(self):
        """ Returns a list of attribute's values for the current instance """
        return self.__dict__.values()

    def is_empty(self):
        """
        Returns True if all values for the current
        instance are false or None
        """
        return not(any(self.all_values()))

    def _is_valid_attribute(self, attribute):
        """
        Returns True if a given attribute name is found inside the permitted
        attributes list
        """

        return attribute in self.permitted_attributes


class Requirement(ParsedString):

    """
    Models a single requirement.

    Attributes:
    value (int)     -- Disk track number.
    is_pf (boolean) -- Wether it is a page fault or not.
    """
    permitted_attributes = ['value', 'is_pf']


class Lot(ParsedString):
    permitted_attributes = ['requirements', 'page_faults', 'movements']
    default_attributes = {
        'requirements': [],
        'page_faultsl': [],
        'movements': 0
    }


class Hdd(ParsedString):
    permitted_attributes = ['name', 'tracks', 'rpm', 'seek_time']
    default_attributes = {
        'name': 'hdd',
        'tracks': 512,
        'rpm': 5400,
        'seek_time': 500
    }


class Simulation(ParsedString):
    permitted_attributes = ['name', 'direction', 'position']
    default_attributes = {
        'name': 'protosimulation',
        'direction': True,
        'position': 0,
        'hdd': Hdd(),
        'lots': []
    }
