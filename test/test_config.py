from coronacheck_tools.verification.verifier import readconfig as verifier_readconfig
from coronacheck_tools.api.denylist import denylist


def test_config_not_empty():
    config = verifier_readconfig()

    assert config


def test_denylist_not_empty():
    assert len(denylist().keys()) > 0

