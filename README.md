# This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS. You have been warned!

### Help requested on validating the QR Code / crypto!
This code seems to use IRMA. Please drop a message in this ticket if you can help out: https://github.com/Sikerdebaard/coronacheck-tools/issues/1

# coronacheck-tools
coronacheck-tools is a python package and cli tool that allows you to dump the contents of the qr code generated at https://coronacheck.nl either through the app or the website. This is useful to get some insight into the data stored in these QR Codes.

# Installation


## Python

```bash
# Install the package through pip
> pip install coronacheck-tools
> coronacheck-tools dump json /path/to/qrcode.jpg /path/to/output/directory
```

## Docker
```bash
# Running the tool through docker is quite easy. Just docker run sikerdebaard/coronacheck-tools:1.0.0
> docker run --rm --user `id -u` -v /path/to/your/data:/data sikerdebaard/coronacheck-tools:latest dump json /data/qrcode.jpg /data
```
#

# Usage

The tool currently has two command built-in. Dump is used for converting an image of a qr code to either raw, ASN.1 or json and the asn1spec command is used to print the ASN.1 specification file.

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

# Python API
The python library allows for a little bit more control over how the qr-code is decoded. Here's an example script on how to dump a qr-code to ASN.1 and then read the ASN.1 and convert it to a dict.

```python3
from coronacheck_tools import decode_qr, decode_raw, decode_asn1_blob, decode_to_dict

# An image can contain multiple QR codes. As such, this function always returns an array with decoded data.
# Format can be the following:
#  RAW = Just grab the raw data from the QR code(s) in the image
#  ASN1_BLOB = Decoded QR Code data. The raw data is confiks and then base45 decoded. This results in a binary blob that contains the ASN.1 data.
#  ASN1 = Uses the ASN.1 specification to decode the ASN1_BLOB data. This is then represented as a dict. Some of the fields in this data
#         are still encoded. Mainly the aDisclosed records still need some decoding. The data is almost usable at this point.
#  DICT = Decode everything, even the records within aDisclosed, and output a dict.


# Let's first convert the qr-code to an ASN1 binary blob.
asn1s = decode_qr('/tmp/test/ecc4.jpg', format='asn1_blob')

# Store the first QR code's ASN.1 blob to disk
with open('/tmp/test/asn1blob.asn', 'wb') as fh:
    fh.write(asn1s[0])


# This ASN1 blob can be read by tools like openssl
# E.g.: openssl asn1parse -in /tmp/test/asn1blob.asn -inform DER


# Let's read the ASN blob data from disk
with open('/tmp/test/asn1blob.asn', 'rb') as fh:
    asn_blob = fh.read()

# Since it's an ASN blob we have to use decode_asn1_blob to decode it.
# Like all of these functions it allows for a desired format parameter.
# Data can always be converted to the next step in the pipeline but 
# never backwards. It always happens in this order:
# RAW -> ASN1_BLOB -> ASN1 -> DICT
#
# Lets convert the blob to a DICT

qrcode_data = decode_asn1_blob(asn_blob, format='dict')
```


# License

The program is licensed under the [MIT License](https://github.com/Sikerdebaard/coronacheck-tools/blob/main/LICENSE).
