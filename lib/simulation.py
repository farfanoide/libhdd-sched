import parsers


class ParsedString(object):

    """
    Base class for all simulation objects.
    - Subclasses must define their basic structure in default_attributes.
    - Validations will be performed based off of these attributes and their
    values by the parsers module.

    Keyword arguments
    data (dict) -- Dictionary containing attribute names and it's values
    """

    default_attributes = {}

    def __init__(self, data={}):
        data = self._remove_invalid_attributes(data)
        data = self._instantiate_attributes(data)
        data = self._merge_default_attributes(data)
        self._set_attributes(data)

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

    def permitted_attributes(self):
        return self.default_attributes.keys()

    def attributes(self):
        return self.__dict__

    def _is_valid_attribute(self, attribute):
        """
        Returns True if a given attribute name is found inside the permitted
        attributes list
        """
        return attribute in self.permitted_attributes()

    def _merge_default_attributes(self, attrs_dict):
        """
        Merge default_attributes with initialization dict giving precedence to
        the latter
        """
        return dict(self.default_attributes, **attrs_dict)

    def _remove_invalid_attributes(self, attrs_dict):
        sanitized = attrs_dict.copy()
        permitted_attributes = self.permitted_attributes()
        for attr_name, value in attrs_dict.iteritems():
            if not attr_name in permitted_attributes:
                sanitized.pop(attr_name)
        return sanitized

    def _generic_parser_name(self, attr_name):
        return 'parse_' + str(
            self.default_attributes[attr_name].__class__.__name__)

    def _object_parser_name(self, attr_name):
        return 'parse_' + attr_name

    def _get_parser(self, attr_name):
        """
        Get a parser function based on default_attributes.
        Logic is as follows:
            - Try to get a specific parser for an object
            - Try to get a standard data type parser
            - If no parser was found, return generic_parser
        """
        parser_name = self._object_parser_name(attr_name)
        if not hasattr(parsers, parser_name):
            parser_name = self._generic_parser_name(attr_name)
        parser = getattr(parsers, parser_name, parsers.generic_parser)
        return parser

    def _instantiate_attribute(self, attr):
        # TODO: missing tests
        attr_name, value = attr
        parser = self._get_parser(attr_name)
        return parser(value)

    def _instantiate_attributes(self, attrs_dict):
        # TODO: missing tests
        validated = {}
        for attr, value in attrs_dict.iteritems():
            attribute = self._instantiate_attribute((attr, value))
            if attr:
                validated[attr] = attribute
        return validated

    def _set_attributes(self, attrs_dict):
        for key, value in attrs_dict.iteritems():
            setattr(self, key, value)


class Requirement(ParsedString):

    """
    Models a single requirement.

    Attributes:
    value (int)     -- Disk track number.
    is_pf (boolean) -- Wether it is a page fault or not.
    """
    default_attributes = { 'value': 0, 'is_pf': False }


class Lot(ParsedString):
    default_attributes = {
        'requirements': [],
        'page_faults': [],
        'movements': 0
    }


class Hdd(ParsedString):
    default_attributes = {
        'name': 'hdd',
        'tracks': 512,
        'rpm': 5400,
        'seek_time': 500
    }


class Simulation(ParsedString):
    default_attributes = {
        'name': 'protosimulation',
        'direction': True,
        'position': 0,
        'hdd': Hdd(),
        'lots': []
    }
