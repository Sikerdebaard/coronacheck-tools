from test.common import TESTQRPATH
from coronacheck_tools import decode_qr
from coronacheck_tools import encode_asn1_der, encode_asn1, encode_dict


def test_asn1_der_raw():
    raw = decode_qr(TESTQRPATH, 'RAW')[0]
    asn1_der = decode_qr(TESTQRPATH, 'ASN1_DER')[0]

    assert encode_asn1_der(asn1_der, 'raw') == raw


def test_asn1_raw():
    raw = decode_qr(TESTQRPATH, 'RAW')[0]
    asn1 = decode_qr(TESTQRPATH, 'ASN1')[0]

    assert encode_asn1(asn1, 'raw') == raw


def test_dict_raw():
    raw = decode_qr(TESTQRPATH, 'RAW')[0]
    dct = decode_qr(TESTQRPATH, 'DICT')[0]

    assert encode_dict(dct, 'raw') == raw


def test_fuzz_dict_raw():
    raw = decode_qr(TESTQRPATH, 'RAW')[0]
    dct = decode_qr(TESTQRPATH, 'DICT')[0]

    dct['aDisclosed']["firstNameInitial"] = 'Z'

    assert encode_dict(dct, 'raw') != raw
