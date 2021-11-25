from appdirs import user_config_dir
from coronacheck_tools.lib import loadlib, listlibs
from pathlib import Path
from datetime import datetime, timedelta

import json
import base64
import requests
import shutil


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

    result = result['Details']

    if result['credentialVersion'] == '1':
        # if this field is set to 1 it is actually a european EHC
        result['isEHC'] = True
        result['isDHC'] = False
    else:
        result['isEHC'] = False
        result['isDHC'] = True

    if result['isEHC'] and not allow_international:
        return False, 'Invalid because the QR Code is an international EHC and allow_international=False'

    return True, result


def readconfig():
    confdir = _ensureconfig()

    conf = {}
    for config_file in confdir.glob('*.json'):
        with open(config_file, 'r') as fh:
            data = fh.read()

        if not data or len(data) == 0:
            conf[f"{config_file.stem}"] = {}
            continue

        conf[f"{config_file.stem}"] = json.loads(data)

    return conf


def clearconfig():
    confdir = _ensureconfig()
    shutil.rmtree(confdir)

def _ensureconfig():
    confversion = 'v6'

    confdir = Path(user_config_dir('coronacheck-tools')) / 'mobilecore'
    confdir.mkdir(parents=True, exist_ok=True)

    timestamp_file = confdir / 'timestamp'

    if timestamp_file.exists():
        with open(timestamp_file, 'r') as fh:
            timestamp = datetime.utcfromtimestamp(0)
            ts = fh.read()
            if len(ts) >= 0 and ts.isdecimal():
                timestamp = datetime.utcfromtimestamp(float(ts))

        now = datetime.utcnow()
        if timestamp >= now - timedelta(hours=24):
            # no need to refresh the config
            return confdir

    config_file = confdir / 'config.json'
    config_url = f"https://verifier-api.coronacheck.nl/{confversion}/verifier/config"
    _getpayload(config_url, config_file)

    public_keys_file = confdir / 'public_keys.json'
    public_keys_url = f"https://verifier-api.coronacheck.nl/{confversion}/verifier/public_keys"
    _getpayload(public_keys_url, public_keys_file)

    with open(timestamp_file, 'w') as fh:
        fh.write(str(int(datetime.utcnow().timestamp())))

    return confdir


def _getpayload(url, outfile):
    req = requests.get(url)
    req.raise_for_status

    req_json = req.json()

    if 'payload' not in req_json:
        # this happens when there's more than 1 response line
        req_json = req_json[0]

    data = base64.b64decode(req_json['payload']).decode()

    with open(outfile, 'w') as fh:
        fh.write(data)
