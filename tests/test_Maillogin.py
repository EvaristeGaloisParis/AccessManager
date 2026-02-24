#from ..modLoader import AccessEnvironment, load_config, AccessData
from typing import Final
from AccessMgr._modMailLogin import MailLogin, AccessEnvironment
#from AccessMgr._modConstantes import AccessEnvironment
import pytest
import json as js

TESTING_PATH: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access.json'
TESTING_PATH_ROTTEN_JSON: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access_rotten_4_test.json'



def test_mail_when_its_ok() -> None:

    a_mailer: MailLogin = MailLogin.init_from_config(st_path=TESTING_PATH, st_sub_name="prod", an_environment=AccessEnvironment.PROD, st_mail_id="prod")

    assert a_mailer is not None
    assert a_mailer.type == "mail"
