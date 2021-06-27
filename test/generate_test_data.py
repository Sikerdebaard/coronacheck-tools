import json

from common import objecthash, TESTQRPATH, VALIDATIONDATA
from coronacheck_tools import decode_qr, decode_raw, decode_asn1_der, decode_to_dict
from pprint import pprint


validation_data = {
    'qr_raw': objecthash(decode_qr(TESTQRPATH, 'raw')),
    'qr_asn1_der': objecthash(decode_qr(TESTQRPATH, 'ASN1_DER')),
    'qr_asn1': objecthash(decode_qr(TESTQRPATH, 'ASN1')),
    'qr_dict': objecthash(decode_qr(TESTQRPATH, 'DICT')),
}

with open(VALIDATIONDATA, 'w') as fh:
    json.dump(validation_data, fh)

pprint(validation_data)
