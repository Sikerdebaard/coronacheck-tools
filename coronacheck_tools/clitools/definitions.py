# cli tool valid input / output formats
VALID_FORMATS = ('QR', 'RAW', 'ASN1', 'JSON')

# Map cli formats to internal tool formats
FORMAT_MAPPINGS = {
    'ASN1': 'ASN1_DER',
    'JSON': 'DICT'
}
