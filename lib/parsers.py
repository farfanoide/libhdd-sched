import re

def parse_req(str_req):
    pf_str = re.compile('\*')
    if pf_str.match(str_req):
        req = (int(pf_str.sub('', str_req)), True)
    else:
        req = (int(str_req), False)
    return req



