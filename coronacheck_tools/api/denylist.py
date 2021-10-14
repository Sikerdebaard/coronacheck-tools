from coronacheck_tools.clitools import deep_get
from coronacheck_tools.verification.verifier import readconfig

import hashlib
import base64


def _int_to_bytes(int_input):
    h = hex(int_input).split('x')[1]
    if len(h) == 1:
        h = f'0{h}'

    return bytes.fromhex(h)


def denylist():
    config = readconfig()
    denylist = deep_get(config, 'proofIdentifierDenylist')

    return {base64.b64decode(k).hex(): v for k, v in denylist.items()}


def proof(json):
    c = _int_to_bytes(json['c'])

    sha256 = hashlib.sha256()
    sha256.update(c)

    # take the first 128 bits of the sha256 hash
    # https://github.com/minvws/nl-covid19-coronacheck-idemix/blob/21fbb94f41510fe23356c42c4888520dd03b1acb/verifier/verifier.go#L136
    proof = sha256.hexdigest()[:32]

    return proof



