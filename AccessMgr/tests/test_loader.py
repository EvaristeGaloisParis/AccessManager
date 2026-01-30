#from ..modLoader import AccessEnvironment, load_config, AccessData
import AccessMgr.modLoader as mLoad


def test_loader_when_its_ok() -> None:

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_subname='prod')
    assert data is dict

    data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_subname='global')
    assert data == {}

    try:
        # on s'attend a une erreur car il faut au moins un nom de sous environment
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {e}')


    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.UAT, st_subname="toto")
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
        data: mLoad.AccessData = mLoad.load_config(an_environment=mLoad.AccessEnvironment.PROD, st_path="")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {type(e)}')
