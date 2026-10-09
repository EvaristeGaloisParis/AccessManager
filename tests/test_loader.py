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


@pytest.fixture(autouse=True)
def _reset_default_path():
    """Garantit un état propre : pas de défaut configuré avant/après chaque test."""
    mLoad.set_default_config_path(None)
    yield
    mLoad.set_default_config_path(None)


def test_default_path_used_when_no_explicit_path() -> None:
    # une fois le défaut posé, load_config(st_path=None) doit lire ce fichier
    mLoad.set_default_config_path(TESTING_PATH)
    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD,
                                               st_subname='prod')
    assert isinstance(data, dict)


def test_explicit_path_overrides_default() -> None:
    # le défaut pointe vers un fichier valide, mais l'appel explicite vers un
    # fichier inexistant : l'explicite doit primer -> FileNotFoundError
    mLoad.set_default_config_path(TESTING_PATH)
    with pytest.raises(FileNotFoundError):
        mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD,
                          st_subname='prod', st_path="c:/dummy_override.json")


def test_reset_with_none_clears_previous_default() -> None:
    # un défaut invalide est bien consulté (FileNotFoundError), puis None l'efface :
    # après reset + nouveau défaut valide, la lecture repasse. Déterministe (pas de CWD).
    mLoad.set_default_config_path("c:/dummy_default.json")
    with pytest.raises(FileNotFoundError):
        mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_subname='prod')

    mLoad.set_default_config_path(None)
    mLoad.set_default_config_path(TESTING_PATH)
    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD,
                                               st_subname='prod')
    assert isinstance(data, dict)


def test_empty_default_path_raises() -> None:
    with pytest.raises(ValueError):
        mLoad.set_default_config_path("")