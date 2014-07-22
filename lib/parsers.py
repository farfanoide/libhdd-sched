import re


def parse_req(str_req):
    pf_str = re.compile('\*')
    if pf_str.match(str_req):
        req = (int(pf_str.sub('', str_req)), True)
    else:
        req = (int(str_req), False)

    return req


class ParsedString(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def is_empty(self):
        return not(any(self.__dict__.values()))

def parse_lot(str_lot):
    # TODO: implement parsed lot data object
    pass
