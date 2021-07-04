import json

from common import objecthash, TESTQRPATH, VALIDATIONDATA, filehash
from coronacheck_tools import decode_qr
from pprint import pprint


rawfile = '/tmp/testqr.raw'
with open(rawfile, 'w') as fh:
    fh.write(decode_qr(TESTQRPATH, 'raw')[0])

validation_data = {
    'qr_raw': objecthash(decode_qr(TESTQRPATH, 'raw')),
    'qr_asn1_der': objecthash(decode_qr(TESTQRPATH, 'ASN1_DER')),
    'qr_asn1': objecthash(decode_qr(TESTQRPATH, 'ASN1')),
    'qr_dict': objecthash(decode_qr(TESTQRPATH, 'DICT')),
    'rawfile': filehash(rawfile),
}

with open(VALIDATIONDATA, 'w') as fh:
    json.dump(validation_data, fh)

pprint(validation_data)
