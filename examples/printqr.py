from coronacheck_tools import decode_qr
from pprint import pprint

from base64 import b64encode

# default format = dict, so it decodes everything to a dict
data = decode_qr('test/testdata/qrtest2.png', "raw")

#pprint(data)
print(b64encode(data[0].encode()))

