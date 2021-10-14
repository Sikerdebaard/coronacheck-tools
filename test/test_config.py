import pytest

from coronacheck_tools.clitools import deep_get, parse_input, write_output,  convert, VALID_FORMATS
from coronacheck_tools.verification.verifier import validate_raw, cconfig, readconfig as verifier_readconfig
from coronacheck_tools.api.denylist import proof, denylist


# def test_config_not_empty():
#     config = verifier_readconfig()
#
#     assert config
#
#
# def test_denylist_not_empty():
#     assert len(denylist().keys()) > 0
#
