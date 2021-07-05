from coronacheck_tools import decode_qr
from pprint import pprint


# default format = dict, so it decodes everything to a dict
data = decode_qr('test/testdata/qrtest2.png')

pprint(data)
