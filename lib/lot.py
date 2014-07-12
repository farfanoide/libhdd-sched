class Requirement(object):
    """
    Models a single requirement.

    Attributes:
    value (int)     -- Disk track number.
    is_pf (boolean) -- Wether it is a page fault or not.
    """
    def __init__(self, value, is_pf=False):
        self.is_pf = is_pf
        self.value = int(value)

    def value(self):
        return self.value


class Lot(object):
    pass


