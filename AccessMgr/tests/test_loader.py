#from ..modLoader import AccessEnvironment, load_config, AccessData
from typing import Final
import AccessMgr._modLoader as mLoad


TESTING_PATH: Final[str] = r'C:/Users/Evariste Galois/KuCoin.Ted/access/access.json'

def test_loader_when_its_ok() -> None:

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_subname='prod',
                                               st_path=TESTING_PATH)

    assert isinstance(data, dict)

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_subname='global', st_path=TESTING_PATH)
    assert data == {}

    try:
        # on s'attend a une erreur car il faut au moins un nom de sous environment
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_path=TESTING_PATH)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {e}')


    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_subname="toto", st_path=TESTING_PATH)
    except KeyError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {e}')


    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_path="toto.json")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {type(e)}')

    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_path=TESTING_PATH)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {type(e)}')
