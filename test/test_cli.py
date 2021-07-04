import pytest
import itertools

from cleo import Application
from cleo import CommandTester
from coronacheck_tools.cli import ConvertCommand, VerifyCommand
from test.common import TESTQRPATH, TESTQRVALIDPATH, TESTQRINVALIDPATH, filehash, load_validation_data
from pathlib import Path


@pytest.fixture
def validation_data():
    return load_validation_data()


def build_tester(command):
    application = Application()
    application.add(ConvertCommand())
    application.add(VerifyCommand())

    command = application.find(command)
    command_tester = CommandTester(command)

    return command_tester


def _convargs(*args):
    return ' '.join([str(x) for x in args])


def test_cli_convert(tmpdir, validation_data):
    """
    {input_format: Input format.QR, RAW, ASN1, JSON.}
    {input: Input file.}
    {output_format: Output format.QR, RAW, ASN1, JSON.}
    {output: Output directory.Existing files will be overwritten without warning.}
    """

    tester = build_tester('convert')

    test_formats = ('QR', 'RAW', 'ASN1', 'JSON')

    for input_format, output_format in itertools.product(test_formats, test_formats):
        print(f"Testing convert {input_format} -> {output_format}")
        testdir_in = tmpdir.mkdir(f'test_in_{input_format}_{output_format}')
        testdir_out = tmpdir.mkdir(f'test_out_{input_format}_{output_format}')
        testdir_cmp = tmpdir.mkdir(f'test_cmp_{input_format}_{output_format}')

        tester.execute(_convargs('QR', TESTQRPATH, input_format, testdir_in))
        infile = [x for x in Path(testdir_in).iterdir() if x.is_file()][0]

        tester.execute(_convargs(input_format, infile, output_format, testdir_out))
        outfile = [x for x in Path(testdir_out).iterdir() if x.is_file()][0]

        tester.execute(_convargs(output_format, outfile, 'RAW', testdir_cmp))
        cmpfile = [x for x in Path(testdir_cmp).iterdir() if x.is_file()][0]

        assert validation_data['rawfile'] == filehash(cmpfile)


def test_cli_verify_invalid():
    tester = build_tester('verify')

    tester.execute(f"QR {TESTQRINVALIDPATH}")
    output = tester.io.fetch_output()

    assert 'Code is invalid' in output


def test_cli_verify_valid():
    tester = build_tester('verify')

    tester.execute(f"QR {TESTQRVALIDPATH}")
    output = tester.io.fetch_output()

    assert 'Code is valid' in output
