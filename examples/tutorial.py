from coronacheck_tools import decode_qr, decode_raw, decode_asn1_der, decode_to_dict, encode_dict, raw_to_qr  # noqa: F401

# An image can contain multiple QR codes. As such, this function always returns an array with decoded data.
# Format can be the following:
#  RAW = Just grab the raw data from the QR code(s) in the image
#  ASN1_DER = Decoded QR Code data. The raw data is confiks and then base45 decoded. This results in a ASN.1 DER blob.
#  ASN1 = Uses the ASN.1 specification to decode the ASN.1 DER data. This is then represented as a dict. Some of the fields in this data
#         are still encoded. Mainly the aDisclosed records still need some decoding. The data is almost usable at this point.
#  DICT = Decode everything, even the records within aDisclosed, and output a dict.


# Let's first convert the qr-code to an ASN1 DER.
asn1s = decode_qr('test/testdata/qrtest.png', format='asn1_der')

# Store the first QR code's ASN.1 DER to disk
with open('/tmp/asn1der.asn', 'wb') as fh:
    fh.write(asn1s[0])


# This ASN1 blob can be read by tools like openssl
# E.g.: openssl asn1parse -in /tmp/test/asn1blob.asn -inform DER


# Let's read the ASN.1 DER data from disk
with open('/tmp/asn1der.asn', 'rb') as fh:
    asn1_der = fh.read()

# Since it's an ASN.1 DER we have to use decode_asn1_der to deserialize it.
# Like all of these functions it allows for a desired format parameter.
# Data can always be converted to the next step in the pipeline but
# never backwards. It always happens in this order:
# RAW -> ASN1_DER -> ASN1 -> DICT
#
# Lets convert the blob to a DICT

data = decode_asn1_der(asn1_der, format='dict')


# Now lets re-encode the dict back to RAW and dump it as a QR code
# As it's a dict, we have to use encode_dict
rawdata = encode_dict(data, 'RAW')


# Now convert RAW to a QR code image
raw_to_qr('/tmp/qrcode.png', rawdata)
