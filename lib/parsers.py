import re


def parse_req(str_req):
    pf_str = re.compile('\*')
    if pf_str.match(str_req):
        req = (int(pf_str.sub('', str_req)), True)
    else:
        req = (int(str_req), False)

    return req


class ParsedString(object):

    def __init__(self, attrs):
        for key, value in attrs.iteritems():
            setattr(self, key, value)

    def attribute_names(self):
        return self.__dict__.keys()

    def all_values(self):
        return self.__dict__.values()

    def is_empty(self):
        return not(any(self.all_values()))


def parse_lot(str_lot):
    # TODO: implement parsed lot data object
    pass
