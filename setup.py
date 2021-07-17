from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coronacheck-tools',
    version='1.1.3',
    description='Unofficial tool to encode, decode and verify the QR code from CoronaCheck.nl. Not affiliated with CoronaCheck.nl or Ministry of VWS.',  # noqa: E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Thomas Phil',
    author_email='thomas@tphil.nl',
    url='https://github.com/Sikerdebaard/coronacheck-tools',
    python_requires=">=3.6",
    #packages=find_packages(),  # same as name
    packages=['coronacheck_tools'],
    #package_data={'': ['lib/(*.dll|*.so)']},
    include_package_data=True,
    install_requires=[
        'cleo>=0.8.1',
        'base58>=2.1.0',
        'pyzbar>=0.1.8',
        'opencv-python>=4.3.0.38',
        'asn1tools>=0.158.0',
        'qrcode>=6.1',
        'Pillow>=8.2.0',
        'cffi>=1.14.5',
        'numexpr>=2.7.3',
        'appdirs>=1.4.4',
        'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'coronacheck-tools=coronacheck_tools.cli:main',
        ],
    },
)
