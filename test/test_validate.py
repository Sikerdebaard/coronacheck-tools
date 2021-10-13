from test.common import TESTQRINVALIDPATH, TESTQRVALIDPATH, TESTQRREVOKEDPATH
from coronacheck_tools import decode_qr
from coronacheck_tools.verification.verifier import validate_raw

def test_revoked_qr():
    with open(TESTQRREVOKEDPATH, 'r') as fh:
        raw = fh.read()

    result = validate_raw(raw)

    assert result[0] == False
    assert 'denylist' in result[1].lower()


def test_validate_invalidqr():
    raw = decode_qr(TESTQRINVALIDPATH, 'RAW')[0]

    assert validate_raw(raw)[0] == False


def test_validate_validqr():
    raw = decode_qr(TESTQRVALIDPATH, 'RAW')[0]

    assert validate_raw(raw)[0] == True
