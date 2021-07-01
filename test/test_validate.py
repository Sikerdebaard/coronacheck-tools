from test.common import TESTQRINVALIDPATH, TESTQRVALIDPATH
from coronacheck_tools import decode_qr
from coronacheck_tools.verification.verifier import validate_raw


def test_validate_invalidqr():
    raw = decode_qr(TESTQRINVALIDPATH, 'RAW')[0]

    assert validate_raw(raw)[0] == False


def test_validate_validqr():
    raw = decode_qr(TESTQRVALIDPATH, 'RAW')[0]

    assert validate_raw(raw)[0] == True
