from pathlib import Path
from cleo import Command, Application

from coronacheck_tools.certificate_versions.v2 import v2_asn1_specs
from coronacheck_tools.clitools import parse_input, write_output,  convert, VALID_FORMATS
from coronacheck_tools.verification.verifier import validate_raw

import pkg_resources  # part of setuptools


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


        error = False
        if format not in VALID_FORMATS:
            self.line(f'<error>Invalid output format: {format} specify one of {", ".join(VALID_FORMATS)}</error>')
            error = True

        if not image_path.is_file():
            self.line(f'<error>Input image file does not exist: {image_path}</error>')
            error = True

        if not output_path.is_dir():
            self.line(f'<error>Output directory does not exist: {output_path}</error>')
            error = True

        if error:
            return

        input_data = parse_input('QR', image_path)
        data = convert('QR', input_data, format)
        write_output(data, format, output_path)


class ConvertCommand(Command):
    """
    Convert between QR image, RAW, ASN.1 der and JSON

    convert
        {input-format : Input format. QR, RAW, ASN1, JSON.}
        {input : Input file.}
        {output-format : Output format. QR, RAW, ASN1, JSON.}
        {output : Output directory. Existing files will be overwritten without warning.}
    """

    def handle(self):
        input_format = self.argument('input-format').upper().strip()
        input_path = Path(self.argument('input'))

        output_format = self.argument('output-format').upper().strip()
        output_path = Path(self.argument('output'))

        error = False
        if input_format not in VALID_FORMATS:
            self.line(f'<error>Invalid input format: {format} specify one of {", ".join(VALID_FORMATS)}</error>')
            error = True

        if output_format not in VALID_FORMATS:
            self.line(f'<error>Invalid output format: {format} specify one of {", ".join(VALID_FORMATS)}</error>')
            error = True

        if not input_path.is_file():
            self.line(f'<error>Input file does not exist: {input_path}</error>')
            error = True

        if not output_path.is_dir():
            self.line(f'<error>Output directory does not exist: {output_path}</error>')
            error = True

        if error:
            return

        input_data = parse_input(input_format, input_path)
        data = convert(input_format, input_data, output_format)
        write_output(data, output_format, output_path)


class VerifyCommand(Command):
    """
    Verify a QR Code from a QR image, RAW, ASN1 DER or JSON.

    verify
        {input-format : Input format. QR, RAW, ASN1, JSON.}
        {input : Input file.}
    """

    def handle(self):
        input_format = self.argument('input-format').upper().strip()
        input_path = Path(self.argument('input'))

        error = False
        if input_format not in VALID_FORMATS:
            self.line(f'<error>Invalid input format: {format} specify one of {", ".join(VALID_FORMATS)}</error>')
            error = True

        if not input_path.is_file():
            self.line(f'<error>Input file does not exist: {input_path}</error>')
            error = True

        if error:
            return

        input_data = parse_input(input_format, input_path)
        data = convert(input_format, input_data, "RAW")

        if isinstance(data, list):
            # if we have multiple QR codes only verify the first one
            data = data[0]

        # Allow international EHC qr codes?
        allow_international = False
        result = validate_raw(data, allow_international=allow_international)

        if result[0]:
            self.line(f"<info>Code is valid</info> {result[1]}")
        else:
            self.line(f"<error>Code is invalid</error> {result[1]}")


def main():
    application = Application(name="coronacheck-tools", version=pkg_resources.require("coronacheck-tools")[0].version)
    application.add(DumpCommand())
    application.add(ConvertCommand())
    application.add(VerifyCommand())
    application.add(Asn1SpecCommand())

    print(AFFILIATE_WARNING)

    application.run()


if __name__ == '__main__':
    main()
