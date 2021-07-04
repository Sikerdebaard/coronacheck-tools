![badge](https://github.com/Sikerdebaard/coronacheck-tools/workflows/Python%20package/badge.svg)

# coronacheck-tools

**This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS. You have been warned!**

coronacheck-tools is a python package and cli tool that allows you to validate, convert and dump the contents of the domestic coronacheck qr code generated at https://coronacheck.nl either through the app or the website. This tool is useful to get some insight into the data stored in these QR Codes or to create your own QR validator.

# Installation


## Python

```bash
# Install the package through pip
# This package requires python 3.6 or higher
> pip install coronacheck-tools

# Example: dumping QR code data to JSON
> coronacheck-tools dump json /path/to/qrcode.jpg /path/to/output/directory

# Example: validate QR Code
> coronacheck-tools verify qr /path/to/qrcode.jpg

# Example: convert QR to ASN1 DER
> coronacheck-tools convert qr /path/to/qrcode.jpg asn1 /path/to/output/directory

# Example: convert ASN1 DER to QR
> coronacheck-tools convert asn1 /path/to/asn1.der qr /path/to/output/directory
```

## Docker
```bash
# Running the tool through docker is quite easy.
# Just docker run sikerdebaard/coronacheck-tools:latest
# Optional: add --user `id -u` to change the uid/group of output files to the current user

# Example: dumping QR code data to JSON
> docker run --rm -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest dump json /data/qrcode.jpg /data

# Example: validate QR Code
> docker run --rm -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest verify qr /data/qrcode.jpg

# Example: convert QR to ASN1 DER
> docker run --rm -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest convert qr /data/qrcode.jpg asn1 /data

# Example: convert ASN1 DER to QR
> docker run --rm -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest convert asn1 /data/asn1.der qr /data
```

# Usage

The tool currently has four commands built-in. Dump, convert, verify and asn1spec.

## dump
Dump is for converting and image with a QR code to RAW, ASN1 DER or JSON.

```bash
> coronacheck-tools dump --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
USAGE
  coronacheck-tools dump <format> <image> <output>

ARGUMENTS
  <format>               Output format. RAW, ASN1, JSON.
  <image>                Path to an image file with one or more QR codes.
  <output>               Output directory. Will overwrite existing files.

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal
                         output, "-vv" for more verbose output and "-vvv" for
                         debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```

## convert
The convert command helps in converting one format into another.
Supported formats are QR image, RAW, ASN1 DER and JSON. The tools
can upconvert or downconvert. E.g. QR -> JSON or JSON -> QR, but it can
also be used for cloning QR -> QR. This is usefull for convert a QR in
a fuzzy image to a crisp clean QR.

```bash
> coronacheck-tools convert --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
USAGE
  coronacheck-tools convert <input-format> <input> <output-format> <output>

ARGUMENTS
  <input-format>         Input format. QR, RAW, ASN1, JSON.
  <input>                Input file.
  <output-format>        Output format. QR, RAW, ASN1, JSON.
  <output>               Output directory. Existing files will be overwritten without warning.

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

```

## verify
This command is used for verifying a QR code. It supports a QR image,
RAW, ASN1 DER and JSON as input for verification. This tool uses a thin
wrapper around the official mobilecore verifier as used by the
CoronaCheck.nl app.

```bash
> coronacheck-tools verify --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
USAGE
  coronacheck-tools verify <input-format> <input>

ARGUMENTS
  <input-format>         Input format. QR, RAW, ASN1, JSON.
  <input>                Input file.

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

```

## asn1spec
This tool shows the ASN1 specification as used for
deserializing the QR code data.

```bash
> coronacheck-tools asn1spec --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
USAGE
  coronacheck-tools asn1spec [<version>]

ARGUMENTS
  <version>              Currently supported versions: 2 "2"

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```

# Python API
This package requires python 3.6 or higher

The python library allows for a little bit more control over how the qr-code is decoded. Here's an example script on how to dump a qr-code to ASN.1 and then read the ASN.1 and convert it to a dict. Finally the script wil re-encode the whole thing back to a QR code.

```python3
from coronacheck_tools import decode_qr, decode_raw, decode_asn1_der, decode_to_dict, encode_dict, raw_to_qr, validate_raw

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


# Finally let's validate the QR Code!
validity = validate_raw(rawdata)
```

# Example scripts
You can find some [example python scripts here](https://github.com/Sikerdebaard/coronacheck-tools/tree/main/examples). E.g. how to fuzz some of the QR code fields or how to read (and validate) the QR from a webcam.

# License

The program is licensed under the [MIT License](https://github.com/Sikerdebaard/coronacheck-tools/blob/main/LICENSE).
