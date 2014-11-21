class ParsedString(object):

    """
    Simple dynamic data object to be instatiated based off of a dictionary.
    Any subclass should set a whitelist of permitted attributes in it's class
    variable 'permitted_attributes'


    Keyword arguments
    data (dict) -- Dictionary containing attribute names and it's values
    """

    permitted_attributes = []

    def __init__(self, data={}):
        for key, value in data.iteritems():
            if self._is_valid_attribute(key):
                setattr(self, key, value)

    def attribute_names(self):
        """ Returns a list with all attribute names for the current instance """
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

    def _is_valid_attribute(self, attribute):
        """
        Returns True if a given attribute name is found inside the permitted attributes list
        """

        return attribute in self.permitted_attributes
