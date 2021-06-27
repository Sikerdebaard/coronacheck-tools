from test.common import TESTQRPATH, objecthash, load_validation_data
from coronacheck_tools import decode_qr

import pytest


def decode(path, format):
    raw = decode_qr(path, format)
    h = objecthash(raw)

    return h


@pytest.fixture
def validation_data():
    return load_validation_data()


def test_qr_raw(validation_data):
    print(validation_data['qr_raw'])
    print(decode(TESTQRPATH, 'RAW'))
    assert validation_data['qr_raw'] == decode(TESTQRPATH, 'RAW')


def test_qr_asn1_der(validation_data):
    assert validation_data['qr_asn1_der'] == decode(TESTQRPATH, 'ASN1_DER')


def test_qr_asn1(validation_data):
    assert validation_data['qr_asn1'] == decode(TESTQRPATH, 'ASN1')


def test_qr_dict(validation_data):
    assert validation_data['qr_dict'] == decode(TESTQRPATH, 'DICT')
