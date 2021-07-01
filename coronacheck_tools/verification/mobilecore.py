from appdirs import user_config_dir
from coronacheck_tools.lib import loadlib, listlibs
from pathlib import Path
from datetime import datetime, timedelta

import json
import base64
import requests


def list_native_libs():
    return listlibs()


def validate(raw: str, lib='auto', allow_international=False):
    confdir = _ensureconfig()
    verifier, ffi = loadlib(lib=lib)

    cstr_raw = ffi.new("char[]", raw.encode())
    cstr_confdir = ffi.new("char[]", str(confdir.absolute()).encode())

    retval = verifier.ffiverify(cstr_raw, cstr_confdir)
    result = ffi.string(retval)

    verifier.freeCString(retval)
    del cstr_raw
    del cstr_confdir

    result = json.loads(result)

    if len(result['Error'].strip()) > 0:
        return False, result['Error']

    result = json.loads(base64.b64decode(result['Value']))

    if result['isNLDCC'] == '1':
        # if this field is set to 1 it is actually a european EHC
        result['isEHC'] = True
        result['isDHC'] = False
    else:
        result['isEHC'] = False
        result['isDHC'] = True
    del result['isNLDCC']

    if result['isEHC'] and not allow_international:
        return False, 'Invalid because the QR Code is an international EHC and allow_international=False'

    return True, result


def _ensureconfig():
    confdir = Path(user_config_dir('coronacheck-tools')) / 'mobilecore'
    confdir.mkdir(parents=True, exist_ok=True)

    timestamp_file = confdir / 'timestamp'

    if timestamp_file.exists():
        with open(timestamp_file, 'r') as fh:
            timestamp = datetime.utcfromtimestamp(int(fh.read()))

        now = datetime.utcnow()
        if timestamp >= now - timedelta(hours=24):
            # no need to refresh the config
            return confdir

    config_file = confdir / 'config.json'
    config_url = "https://verifier-api.coronacheck.nl/v4/verifier/config"
    _getpayload(config_url, config_file)

    public_keys_file = confdir / 'public_keys.json'
    public_keys_url = "https://verifier-api.coronacheck.nl/v4/verifier/public_keys"
    _getpayload(public_keys_url, public_keys_file)

    with open(timestamp_file, 'w') as fh:
        fh.write(datetime.utcnow().strftime('%s'))

    return confdir


def _getpayload(url, outfile):
    req = requests.get(url)
    req.raise_for_status

    data = base64.b64decode(req.json()['payload']).decode()

    with open(outfile, 'w') as fh:
        fh.write(data)
