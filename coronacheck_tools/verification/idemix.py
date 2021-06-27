import hashlib


def _get_hash_algo():
    return hashlib.sha256()


def _int_to_bytes(i):
    # certainly not the fastest approach but alas, this is python
    # and we just want things to work
    return bytes.fromhex(hex(int(i)).split('x')[1])


def calc_timebased_challenge(timestamp):
    barr = _int_to_bytes(timestamp)
    hasher = _get_hash_algo()
    hasher.update(barr)

    return hasher.hexdigest()

    #challengeByteSize := GabiSystemParameters.Lstatzk / 8
    #return new(big.Int).SetBytes(timeHash[:challengeByteSize])
