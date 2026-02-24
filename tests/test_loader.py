#from ..modLoader import AccessEnvironment, load_config, AccessData
from typing import Final
import AccessMgr._modLoader as mLoad
#from AccessMgr._modConstantes import AccessEnvironment
import pytest
import json as js

TESTING_PATH: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access.json'
TESTING_PATH_ROTTEN_JSON: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access_rotten_4_test.json'



def test_loader_when_its_ok() -> None:

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_subname='prod',
                                               st_path=TESTING_PATH)

    assert isinstance(data, dict)

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_subname='global',
                                               st_path=TESTING_PATH)
    assert data == {}


def test_load_config_error_cases():
    l_cases: list[tuple] = [
        (mLoad.AccessEnvironment.UAT, None, TESTING_PATH, ValueError),
        (mLoad.AccessEnvironment.UAT, "toto", TESTING_PATH, KeyError),
        (mLoad.AccessEnvironment.PROD, "None", "C:/Users", ValueError),
        (mLoad.AccessEnvironment.PROD, "None", "c:/dummy.json", FileNotFoundError),
        (mLoad.AccessEnvironment.PROD, "None", TESTING_PATH_ROTTEN_JSON, js.JSONDecodeError),
    ]

    for case in l_cases:
        kwargs = {"an_environment": case[0], "st_subname": case[1], "st_path": case[2]}

        with pytest.raises(case[3]) as err_mgr:
            mLoad.load_config(**kwargs)

        assert err_mgr.type == case[3]