import base58

supported_versions = (2,)
_qr_charset = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
_confiks_charset = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHI"


def raw_decoder(raw):
    """
    The QR code uses a custom base45 decoder as written by confiks on GitHub:https://github.com/confiks/base45-go/
    This decoder manages to cram a few extra bytes into the QR code compared to a more traditional base45 encoder.

    The confiks decoder works similar to a base58 decoder but with a reduced alphabet.


    :return: ASN.1 DER
    """

    return base58.b58decode(_qr_to_confiks(raw), alphabet=_confiks_charset)


def asn1_der_encoder(asn1_der):
    return _confiks_to_qr(base58.b58encode(asn1_der, alphabet=_confiks_charset))


def _confiks_to_qr(data):
    """
        This converts confiks to the QR code alphabet.
        """
    qr_charset_len = 45

    confiks_qr = {}

    for i in range(0, qr_charset_len):
        confiks_qr[_confiks_charset[i]] = _qr_charset[i]

    input_len = len(data)
    qr_encoded_input = []

    for i in range(0, input_len):
        qr_encoded_input.append(confiks_qr[data[i]])

    return bytes(qr_encoded_input)


def _qr_to_confiks(data):
    """
    This converts the QR code to confiks alphabet.
    """
    qr_charset_len = 45

    qr_confiks = {}

    for i in range(0, qr_charset_len):
        qr_confiks[_qr_charset[i]] = _confiks_charset[i]

    input_len = len(data)
    confiks_encoded_input = []

    for i in range(0, input_len):
        confiks_encoded_input.append(qr_confiks[data[i]])

    return bytes(confiks_encoded_input)
