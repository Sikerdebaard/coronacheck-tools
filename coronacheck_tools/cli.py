from pathlib import Path
from cleo import Command, Application

from coronacheck_tools.certificate_versions.v2 import v2_asn1_specs
from coronacheck_tools.clitools import deep_get, parse_input, write_output,  convert, VALID_FORMATS
from coronacheck_tools.verification.verifier import validate_raw, cconfig, readconfig as verifier_readconfig
from coronacheck_tools.api.denylist import denylist, proof as denylist_proof

import json

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
        {--e|ehc : Allow verification of European Health Certificates}
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

        if not data or len(data) == 0:
            self.line(f"<error>No QR code detected!</error>")
            return

        if isinstance(data, list):
            # if we have multiple QR codes only verify the first one
            data = data[0]

        # Allow international EHC qr codes?
        allow_international = True if self.option('ehc') else False
        result = validate_raw(data, allow_international=allow_international)

        if result[0]:
            self.line(f"<info>Code is valid</info> {result[1]}")
        else:
            self.line(f"<error>Code is invalid</error> {result[1]}")


class ClearConfigCommand(Command):
    """
    Remove the validators config files. Normally you should not need this command.

    clean
    """

    def handle(self):
        cconfig()
        self.line('Config removed')

class ListConfigCommand(Command):
    """
    List the (mobilecore) config.

    config
        {key? : Only show the config starting at <key>}
    """

    def handle(self):
        verifier_config = verifier_readconfig()

        config = {'verifier': verifier_config}

        key = self.argument('key')
        if key:
            config = deep_get(config, key)

        print(json.dumps(config, indent=2, sort_keys=True))


class CheckDenylistCommand(Command):
    """
    Check if a QR code is on the proof identifier denylist or print the denylist if no parameters are given.

    denylist
        {input-format? : Input format}
        {input? : Input QR code data}
    """

    def handle(self):
        input_format = self.argument('input-format')
        input_path = self.argument('input')

        if input_format:
            input_format = input_format.upper().strip()
        if input_path:
            input_path = Path(input_path)

        error = False
        if input_path and input_format not in VALID_FORMATS:
            self.line(f'<error>Invalid input format: {format} specify one of {", ".join(VALID_FORMATS)}</error>')
            error = True

        if input_path and not input_path.is_file():
            self.line(f'<error>Input file does not exist: {input_path}</error>')
            error = True

        if not (input_path and input_format):
            input_path = None
            input_format = None

        if error:
            return

        blacklist = denylist()
        print('Denylist:')
        for k, v in blacklist.items():
            print(f'  {k} -> {v}')
        print()

        if input_path:
            input_data = parse_input(input_format, input_path)
            data = convert(input_format, input_data, 'JSON')

            if isinstance(data, list) and len(data) > 0:
                # only grab the first QR
                data = data[0]

            if not data or len(data) == 0:
                self.line(f'<error>No valid QR code found in {input_path}</error>')
            else:
                proof = denylist_proof(data)
                print(f'QR proof: {proof}')
                if proof in blacklist:
                    self.line(f"<error>QR Code present in proof identifier denylist</error>")
                else:
                    self.line(f"<info>QR Code not present in proof identifier denylist</info>")


def main():
    application = Application(name="coronacheck-tools", version=pkg_resources.require("coronacheck-tools")[0].version)
    application.add(DumpCommand())
    application.add(ConvertCommand())
    application.add(VerifyCommand())
    application.add(Asn1SpecCommand())
    application.add(ClearConfigCommand())
    application.add(ListConfigCommand())
    application.add(CheckDenylistCommand())

    print(AFFILIATE_WARNING)

    application.run()


if __name__ == '__main__':
    main()
