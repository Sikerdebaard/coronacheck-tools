from pathlib import Path
from cleo import Command, Application

from coronacheck_tools import decode_qr, encode_asn1_der, encode_dict, raw_to_qr
from coronacheck_tools.certificate_versions.v2 import v2_asn1_specs

import pkg_resources  # part of setuptools
import json


AFFILIATE_WARNING = 'This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS'


class Asn1SpecCommand(Command):
    """
    Show ASN.1 spec for a specified version.

    asn1spec
        {version=2 : Currently supported versions: 2}
    """

    def handle(self):
        version = int(self.argument('version'))

        if version == 2:
            print(v2_asn1_specs)


class DumpCommand(Command):
    """
    Dump the QR Code data from image to RAW, ASN.1 or JSON.

    dump
        {format : Output format. RAW, ASN1, JSON.}
        {image : Path to an image file with one or more QR codes.}
        {output : Output directory. Will overwrite existing files.}
    """

    def handle(self):  # noqa: C901
        format = self.argument('format').upper().strip()
        image_path = Path(self.argument('image'))
        output_path = Path(self.argument('output'))

        valid_formats = ('RAW', 'ASN1', 'JSON')
        error = False
        if format not in valid_formats:
            self.line(f'<error>Invalid output format: {format} specify one of {", ".join(valid_formats)}</error>')
            error = True

        if not image_path.is_file():
            self.line(f'<error>Input image file does not exist: {image_path}</error>')
            error = True

        if not output_path.is_dir():
            self.line(f'<error>Output directory does not exist: {output_path}</error>')
            error = True

        if error:
            return

        if format == 'ASN1':
            format = 'ASN1_DER'  # retrieve binary ASN1 DER

        if format == 'JSON':
            format = 'DICT'

        retvals = decode_qr(image_path, format=format)

        mode = 'w'
        if format == 'RAW':
            extension = '.raw'
        elif format == 'ASN1_DER':
            extension = '.asn'
            mode = 'wb'
        elif format == 'DICT':
            retvals = [json.dumps(x) for x in retvals]
            extension = '.json'

        counter = 0
        for data in retvals:
            fname = output_path / f'dhc_data_{counter:03}{extension}'
            print(f'Writing code {counter+1}/{len(retvals)} to {fname}')
            with open(fname, mode) as fh:
                fh.write(data)
            counter += 1


class EncodeCommand(Command):
    """
    Encode RAW, ASN.1 or JSON to QR code

    encode
        {format : Input format. RAW, ASN1, JSON.}
        {input : Input file.}
        {image : Path to an output image file. The QR code will be (over)written to this file.}
    """

    def handle(self):
        format = self.argument('format').upper().strip()
        image_path = Path(self.argument('image'))
        input_path = Path(self.argument('input'))

        valid_formats = ('RAW', 'ASN1', 'JSON')
        error = False
        if format not in valid_formats:
            self.line(f'<error>Invalid output format: {format} specify one of {", ".join(valid_formats)}</error>')
            error = True

        if not image_path.parent.is_dir():
            self.line(f'<error>Output image file directory does not exist: {image_path.parent}</error>')
            error = True

        if not input_path.is_file():
            self.line(f'<error>Input file does not exist: {input_path}</error>')
            error = True

        if error:
            return

        if format == 'ASN1':
            format = 'ASN1_DER'
            with open(input_path, 'rb') as fh:
                data = fh.read()
            retval = encode_asn1_der(data, 'raw')

        if format == 'JSON':
            format = 'DICT'
            with open(input_path, 'r') as fh:
                data = json.load(fh)
            retval = encode_dict(data)

        if format == 'RAW':
            with open(input_path, 'r') as fh:
                retval = fh.read()

        print(f'Writing to {image_path}')
        raw_to_qr(image_path, retval)

        raw_path = image_path.parent / f"{image_path.stem}.raw"
        print(f'Writing to {raw_path}')
        with open(raw_path, 'w') as fh:
            fh.write(retval)


def main():
    application = Application(name="coronacheck-tools", version=pkg_resources.require("coronacheck-tools")[0].version)
    application.add(DumpCommand())
    application.add(EncodeCommand())
    application.add(Asn1SpecCommand())

    print(AFFILIATE_WARNING)

    application.run()


if __name__ == '__main__':
    main()
