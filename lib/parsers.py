import re
# TODO : ver tema modulos en vez de clases.
class ReqParser(object):

    @classmethod
    def parse(cls, str_req):
        pf_str = re.compile('\*')
        if pf_str.match(str_req):
            req = (int(pf_str.sub('', str_req)), True)
        else:
            req = (int(str_req), False)

        return req


