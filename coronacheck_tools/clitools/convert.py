from coronacheck_tools.clitools.definitions import VALID_FORMATS
from coronacheck_tools import (
    cv2img_decode_qr,
    decode_raw,
    decode_asn1_der,
    # decode_to_dict,
    raw_to_qr,
    raw_to_cv2_qr,
    encode_asn1_der,
    # encode_asn1,
    encode_dict
)


def convert(input_format, input_data, output_format):
    """
    CLI convert tool. Converts input_format to output_format.

    :param input_format: one of QR, RAW, ASN1, JSON
    :param input_data: input data as read by coronacheck_tools.clitools.parse_input
    :param output_format: one of QR, RAW, ASN1, JSON
    :param output_path: output directory
    :return:
    """

    if VALID_FORMATS.index(input_format) > VALID_FORMATS.index(output_format):
        # encode
        return _encode(input_format, input_data, output_format)
    elif VALID_FORMATS.index(input_format) < VALID_FORMATS.index(output_format):
        # decode
        return _decode(input_format, input_data, output_format)
    else:
        # clone input to output. Perhaps only useful for cloning qr image -> qr image as it can generate a crisp clean QR from a noisy screenshot of a QR.
        return _clone(input_format, input_data)


def _clone(format, input_data):
    if format != 'QR':
        return input_data

    return [raw_to_cv2_qr(raw) for raw in cv2img_decode_qr(input_data, 'RAW')]


def _encode(input_format, input_data, output_format):
    tmp_output_format = output_format
    to_qr = False
    if output_format == 'QR':
        tmp_output_format = 'RAW'
        to_qr = True
    elif output_format == 'ASN1':
        tmp_output_format = 'ASN1_DER'

    if input_format == 'JSON':
        data = encode_dict(input_data, tmp_output_format)
    elif input_format == 'ASN1':
        data = encode_asn1_der(input_data, tmp_output_format)
    elif input_format == 'RAW':
        data = input_data

    if to_qr:
        data = raw_to_cv2_qr(data)

    return data


def _decode(input_format, input_data, output_format):
    tmp_output_format = output_format
    if output_format == 'JSON':
        tmp_output_format = 'DICT'
    elif output_format == 'ASN1':
        tmp_output_format = 'ASN1_DER'

    if input_format == 'QR':
        data = cv2img_decode_qr(input_data, tmp_output_format)
    elif input_format == 'RAW':
        data = decode_raw(input_data, tmp_output_format)
    elif input_format == 'ASN1':
        data = decode_asn1_der(input_data, tmp_output_format)

    return data
