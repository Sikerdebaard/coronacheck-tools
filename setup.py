from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coronacheck-tools',
    version='1.0.0',
    description='Unofficial tool to dump QR code data from CoronaCheck.nl to RAW, ASN.1 or JSON. Not affiliated with CoronaCheck.nl or Ministry of VWS.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Thomas Phil',
    author_email='thomas@tphil.nl',
    url='https://github.com/Sikerdebaard/coronacheck-tools',
    python_requires=">=3.6",
    packages=find_packages(),  # same as name
    install_requires=[
        'cleo>=0.8.1',
        'base58>=2.1.0',
        'pyzbar>=0.1.8',
        'opencv-python>=4.5.2.54',
        'asn1tools>=0.158.0',
    ],
    entry_points={
        'console_scripts': [
            'coronacheck-tools=coronacheck_tools.cli:main',
        ],
    },
)
