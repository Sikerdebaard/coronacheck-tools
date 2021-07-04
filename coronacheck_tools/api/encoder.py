from coronacheck_tools.common.conversion import supported_versions, asn1_der_encoder
from coronacheck_tools.api.decoder import v2_valid_output_formats as v2_decoder_valid_output_formats
from coronacheck_tools.certificate_versions.v2 import v2_asn1, v2_dict_repr_to_dhc_records


v2_valid_output_formats = list(reversed(v2_decoder_valid_output_formats[:-1]))


def _check_step(format, step, version):
    if version not in supported_versions:
        raise ValueError(f'Version {version} unsupported. Only version(s) {", ".join(supported_versions)} are currently supported.')

    if version == 2:
        valid_output_formats = v2_valid_output_formats

    format = format.upper()
    if format not in valid_output_formats or valid_output_formats.index(format) < valid_output_formats.index(step):
        raise ValueError(f'Invalid format, choose one of {", ".join(valid_output_formats[valid_output_formats.index(format) + 1:])}')

    return format


def encode_asn1_der(asn1_der, format='raw', version='auto'):

    if version == 'auto':
        version = supported_versions[-1]  # use latest version

    format = _check_step(format, 'ASN1_DER', version)

    raw = f'NL{version}:' + asn1_der_encoder(asn1_der).decode()

    return raw


def encode_asn1(asn1, format='raw', version='auto'):
    version = supported_versions[-1]  # use latest version
    format = _check_step(format, 'ASN1', version)

    asn1_der = v2_asn1.encode('ProofSerializationV2', asn1)

    if format == 'ASN1_DER':
        return asn1_der

    return encode_asn1_der(asn1_der, format=format, version=version)


def encode_dict(dct, format='raw', version='auto'):
    version = supported_versions[-1]  # use latest version

    asn1 = v2_dict_repr_to_dhc_records(dct)

    if format == 'ASN1':
        return asn1

    return encode_asn1(asn1, format=format, version=version)
