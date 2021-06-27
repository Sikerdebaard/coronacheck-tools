import hashlib
import json
import pickle
import functools


READ_BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
TESTQRPATH = 'test/testdata/qrtest.jpg'
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


#@functools.lru_cache(maxsize=None)
def objecthash(obj, usepickle=True):
    if usepickle:
        barr = pickle.dumps(obj)
    else:
        barr = json.dumps(obj).encode()

    hasher = _get_hash_algo()
    hasher.update(barr)

    return hasher.hexdigest()


@functools.lru_cache(maxsize=None)
def load_validation_data():
    with open(VALIDATIONDATA, 'r') as fh:
        data = json.load(fh)
    return data
