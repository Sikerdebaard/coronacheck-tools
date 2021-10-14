from test.common import TESTQRINVALIDPATH, TESTQRVALIDPATH, TESTQRREVOKEDPATH
from coronacheck_tools import decode_qr, decode_raw
from coronacheck_tools.verification.verifier import validate_raw
from coronacheck_tools.api.denylist import proof, denylist


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


def test_proof_not_empty():
    data = decode_qr(TESTQRVALIDPATH, 'DICT')[0]

    assert proof(data)


def test_denylist_present():
    with open(TESTQRREVOKEDPATH, 'r') as fh:
        data = decode_raw(fh.read(), 'DICT')

    blacklist = denylist()
    p = proof(data)

    assert p in blacklist


def test_denylist_not_present():
    data = decode_qr(TESTQRVALIDPATH, 'DICT')[0]

    blacklist = denylist()
    p = proof(data)

    assert p not in blacklist
