import asn1tools


v2_asn1_specs = """
DHC DEFINITIONS ::= BEGIN
    ProofSerializationV2 ::= SEQUENCE {
        disclosureTimeSeconds  INTEGER,
        c                      INTEGER,
        a                      INTEGER,
        eResponse              INTEGER,
        vResponse              INTEGER,
        aResponse              INTEGER,
        aDisclosed             SEQUENCE OF INTEGER
    }
    
    CredentialMetadataSerialization ::= SEQUENCE {
        -- CredentialVersion identifies the credential version, and is always a single byte
        credentialVersion OCTET STRING,

        -- IssuerPkId identifies the public key to use for verification
        issuerPkId PrintableString
    }
END
"""

v2_asn1_decoder = asn1tools.compile_string(v2_asn1_specs)


def v2_dhc_records_to_dict_repr(dhc_records):
    retval = dhc_records.copy()


    retval['aDisclosed'][0] = _decode_metadata_attrs(dhc_records['aDisclosed'][0])

    for i in range(1, len(retval['aDisclosed'])):
        retval['aDisclosed'][i] = _int_to_byte_attrs(dhc_records['aDisclosed'][i]).decode('utf-8')

    retval['aDisclosed'] = _attrs_to_dict(retval['aDisclosed'])
    retval['aDisclosed']['CredentialMetadata']['credentialVersion'] = retval['aDisclosed']['CredentialMetadata']['credentialVersion'].hex()


    return retval


def _attrs_to_dict(lst):
    return {
        "CredentialMetadata": lst[0],
        "isSpecimen": lst[1],
        "isPaperProof": lst[2],
        "validFrom": lst[3],
        "validForHours": lst[4],
        "firstNameInitial": lst[5],
        "lastNameInitial": lst[6],
        "birthDay": lst[7],
        "birthMonth": lst[8],
    }


def _int_to_byte_attrs(int_input):
    if int_input & 1 == 0:
        return []
    else:
        h = hex(int_input >> 1).split('x')[1]
        if len(h) == 1:
            h = f'0{h}'

        # print(h)

        return bytes.fromhex(h)


def _decode_metadata_attrs(record):
    attribute_bytes = _int_to_byte_attrs(record)

    credentials_metadata = v2_asn1_decoder.decode('CredentialMetadataSerialization', attribute_bytes)

    # if credentials_metadata['credentialVersion'] == b'\x02':

    return credentials_metadata
