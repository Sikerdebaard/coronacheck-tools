# This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS. You have been warned!

# coronacheck-tools
coronacheck-tools is a python package and cli tool that allows you to dump the contents of the qr code generated at https://coronacheck.nl either through the app or the website or on paper. This allows others to get some insight into the data stored in these QR Codes.

# Installation


## Pip

```bash
# First install the package through pip
> pip install coronacheck-tools

# Let's check the tools help file
> coronacheck-tools --help

This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS
Coronacheck Tools version 1.0.0

USAGE
  coronacheck-tools [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  asn1spec               Show ASN.1 spec for a specified version.
  dump                   Dump the QR Code data from image to RAW, ASN.1 or JSON.
  help                   Display the manual of a command


# You are now ready to convert a QR code image to either RAW or ASN.1 or JSON.
# The tool supports most popular image formats, e.g. png, jpg etc.
> coronacheck-tools dump json /path/to/qr-code.jpg /path/to/output/directory
```

## Docker

# License

The program is licensed under the [MIT License](https://github.com/Sikerdebaard/coronacheck-tools/blob/main/LICENSE).
