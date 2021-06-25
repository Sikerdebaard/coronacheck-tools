from pathlib import Path
from coronacheck_tools.common.qrreader import read_qr
from coronacheck_tools.common.decoders import raw_decoder
from coronacheck_tools.certificate_versions.v2 import v2_asn1_decoder, v2_dhc_records_to_dict_repr

import asn1tools


supported_versions = (2,)
v2_valid_output_formats = ['RAW', 'ASN1_BLOB', 'ASN1', 'DICT']


def _check_step(format, step, version):
    if version not in supported_versions:
        raise ValueError(f'Version {version} unsupported. Only version(s) {", ".join(supported_versions)} are currently supported.')

    if version == 2:
        valid_output_formats = v2_valid_output_formats

    format = format.upper()
    if format not in valid_output_formats or valid_output_formats.index(format) < valid_output_formats.index(step):
        raise ValueError(f'Invalid format, choose one of {", ".join(valid_output_formats[valid_output_formats.index(format) + 1:])}')

    return format


def decode_qr(image_file, format='dict'):
    format = _check_step(format, 'RAW', 2)  # default to v2, it doesn't really matter for decoding the QR
    image_file = Path(image_file)

    if not image_file.is_file():
        raise ValueError(f'image_file {image_file} does not exist')

    qr_codes = read_qr(str(image_file))

    if format == 'RAW':
        return qr_codes

    qr_codes = [qr for qr in qr_codes if len(qr) > 4 and qr.startswith('NL') and qr[3] == ':']

    return [decode_raw(qr, format=format, version=int(qr[2], 16)) for qr in qr_codes]


def decode_raw(raw, format='dict', version='auto'):
    if not (raw.startswith('NL') and raw[3] == ':'):
        raise ValueError(f'Invalid data. RAW data should start with NL: {raw}')

    if version == 'auto':
        version = int(raw[2], 16)

    format = _check_step(format, 'ASN1_BLOB', version)

    if version == 2:
        data = raw[4:]

    asn1_blob = raw_decoder(data.encode())

    if format == 'ASN1_BLOB':
        return asn1_blob

    return decode_asn1_blob(asn1_blob, format=format, version=version)


def decode_asn1_blob(asn1_blob, format='dict', version=2):
    format = _check_step(format, 'ASN1', version)

    if version == 2:
        dhc_records = v2_asn1_decoder.decode('ProofSerializationV2', asn1_blob)

    if format == 'ASN1':
        return dhc_records

    return decode_to_dict(dhc_records)


def decode_to_dict(dhc_records, format='dict', version=2):
    format = _check_step(format, 'DICT', version)

    if version == 2:
        return v2_dhc_records_to_dict_repr(dhc_records)
