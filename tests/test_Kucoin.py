from typing import Final
from AccessMgr import get_kucoin_token, ProviderKucoin, AccessEnvironment
TESTING_PATH: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access.json'

def test_loader_when_it_builds_himself() -> None:

    a_mailer: ProviderKucoin = ProviderKucoin.init_from_config(st_path=TESTING_PATH, st_sub_name="prod",
                                                                         an_environment=AccessEnvironment.PROD,
                                                                         st_id="TedAndPpr")

    assert a_mailer is not None
    assert a_mailer.type == "provider"


def test_from_loader_when_its_ok() -> None:

    a_mailer: ProviderKucoin = get_kucoin_token(st_config_path=TESTING_PATH, st_sub_name="prod",
                                                                         an_environment=AccessEnvironment.PROD,
                                                                         st_id="TedAndPpr")

    assert a_mailer is not None
    assert a_mailer.type == "provider"
