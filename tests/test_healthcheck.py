from typing import Final

from AccessMgr._modHealthcheck import ProviderHealthcheck
from AccessMgr import get_healthcheck_config, AccessEnvironment

import pytest

TESTING_PATH: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access.json'


def test_healthcheck_when_its_ok() -> None:

    hc: ProviderHealthcheck = get_healthcheck_config(st_id="Research_Pi",
                                                     an_environment=AccessEnvironment.PROD,
                                                     st_config_path=TESTING_PATH)

    assert hc is not None
    assert hc.type == "healthcheck"
    assert hc.is_alive() is True

    # la base de l'url est une constante du code, seul l'uuid vient de la config
    assert hc.base_url == "https://hc-ping.com/"
    assert hc.uuid() is not None and len(hc.uuid()) > 0
    assert hc.url() is not None
    assert hc.url().startswith("https://hc-ping.com/")
    assert hc.url() == f"https://hc-ping.com/{hc.uuid()}"

    # le secret (uuid) ne doit jamais fuiter dans repr / str
    assert hc.uuid() not in repr(hc)
    assert hc.uuid() not in str(hc)


def test_healthcheck_unknown_id_raises() -> None:

    with pytest.raises(KeyError):
        get_healthcheck_config(st_id="ThisIdDoesNotExist",
                               an_environment=AccessEnvironment.PROD,
                               st_config_path=TESTING_PATH)
