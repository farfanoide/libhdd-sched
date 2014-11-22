from parsed_string import ParsedString


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


