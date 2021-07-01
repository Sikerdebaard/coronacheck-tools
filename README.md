![badge](https://github.com/Sikerdebaard/coronacheck-tools/workflows/Python%20package/badge.svg)

# coronacheck-tools

**This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS. You have been warned!**

coronacheck-tools is a python package and cli tool that allows you to fuzz with the contents of the domestic coronacheck qr code generated at https://coronacheck.nl either through the app or the website. This is useful to get some insight into the data stored in these QR Codes. Currently it supports dumping the QR code data and encoding the dumped data back into a QR code.

# Installation


## Python

```bash
# Install the package through pip
# This package requires python 3.6 or higher
> pip install coronacheck-tools
> coronacheck-tools dump json /path/to/qrcode.jpg /path/to/output/directory
```

## Docker
```bash
# Running the tool through docker is quite easy.
# Just docker run sikerdebaard/coronacheck-tools:latest
> docker run --rm --user `id -u` -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest dump json /data/qrcode.jpg /data
```
#

# Usage

The tool currently has three commands built-in. Dump is used for converting an image of a qr code to either raw, ASN.1 or json and the asn1spec command is used to print the ASN.1 specification file. Finally there's the encode command which allows you to convert the raw, ASN.1 or json files dumped by this tool back into a QR code image. The tool supports most popular image formats as input/output.

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


> coronacheck-tools encode --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
USAGE
  coronacheck-tools encode <format> <input> <image>

ARGUMENTS
  <format>               Input format. RAW, ASN1, JSON.
  <input>                Input file.
  <image>                Path to an output image file. The QR code will be (over)written to this file.

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
from coronacheck_tools import decode_qr, decode_raw, decode_asn1_der, decode_to_dict, encode_dict, raw_to_qr

# An image can contain multiple QR codes. As such, this function always returns an array with decoded data.
# Format can be the following:
#  RAW = Just grab the raw data from the QR code(s) in the image
#  ASN1_DER = Decoded QR Code data. The raw data is confiks and then base45 decoded. This results in a ASN.1 DER blob.
#  ASN1 = Uses the ASN.1 specification to decode the ASN.1 DER data. This is then represented as a dict. Some of the fields in this data
#         are still encoded. Mainly the aDisclosed records still need some decoding. The data is almost usable at this point.
#  DICT = Decode everything, even the records within aDisclosed, and output a dict.


# Let's first convert the qr-code to an ASN1 DER.
asn1s = decode_qr('test/testdata/qrtest.jpg', format='asn1_der')

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
```

# Example scripts
You can find some [example python scripts here](https://github.com/Sikerdebaard/coronacheck-tools/tree/main/examples). E.g. how to fuzz some of the QR code fields or how to read the QR from a webcam.

# License

The program is licensed under the [MIT License](https://github.com/Sikerdebaard/coronacheck-tools/blob/main/LICENSE).
