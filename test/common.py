import hashlib
import json
import pickle
import functools


READ_BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
TESTQRPATH = 'test/testdata/qrtest.png'

TESTQRINVALIDPATH = 'test/testdata/qrtest.png'
TESTQRVALIDPATH = 'test/testdata/qrtest2.png'

VALIDATIONDATA = 'test/testdata/validation.json'


def _get_hash_algo():
    return hashlib.sha256()


@functools.lru_cache(maxsize=None)
def filehash(file):
    hasher = _get_hash_algo()
    with open(file, 'rb') as fh:
        while True:
            data = fh.read(READ_BUF_SIZE)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()


class BytesDump(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.hex()
        return json.JSONEncoder.default(self, obj)

def objecthash(obj, usepickle=False):
    if usepickle:
        barr = pickle.dumps(obj)
    else:
        barr = json.dumps(obj, cls=BytesDump).encode()

    hasher = _get_hash_algo()
    hasher.update(barr)

    return hasher.hexdigest()


@functools.lru_cache(maxsize=None)
def load_validation_data():
    with open(VALIDATIONDATA, 'r') as fh:
        data = json.load(fh)
    return data
