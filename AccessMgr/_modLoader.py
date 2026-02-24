"""
permet de lire le fichier de parametrage

"""
from typing import Optional, Final
from AccessMgr._modJsonStructure import Container, MailContainer, MailServerConfig, js, AccessData
from AccessMgr._modConstantes import AccessEnvironment
#import os
from pathlib import Path


# Variable locale pour les tests du choix par défaut
__b__INNER: bool = False

# Constntes : les chemins par défauts!
__DEFAULT_PATH__: Final[str] = '../access/access.json'
__INNER_DEFAULT_PATH__: Final[str] = '../../access/access.json'

def env_key(an_env: AccessEnvironment, st_subname: str) -> str:

    if an_env == AccessEnvironment.PROD:
        return f'{an_env}'

    return f'{an_env}_{st_subname.strip()}'


def load_config(st_path: Optional[str] = None,
                an_environment: AccessEnvironment = AccessEnvironment.PROD,
                st_subname: Optional[str] = None) -> AccessData:
    """
    Lit le fichier de paramétrage

    Args:
        st_path: str: Chemin du fichier JSON (string) par défaut: '../../access/access.json'
        an_environment: un environment. Si prod le subname est ignoré
        st_subname: le sous nom d'un environment

    Returns:
        La partie congrue des droits qui nous interesse.

    Raises:
            FileNotFoundError: Si le fichier n'existe pas
            PermissionError: Si pas de permissions de lecture
            json.JSONDecodeError: Si le JSON est mal formaté
            ValueError: Si le chemin est vide ou invalide; ou si l'environement demandé est mal configuré
            KeyError: si l'envionment x subname n'est pas dans le fichier de configuration
    """

    if an_environment != AccessEnvironment.PROD:
        if st_subname is None or st_subname.strip() == "":
            raise ValueError(f"Pour l'environement: <{an_environment};>, le subname est obligatoire et doit etre non vide!")

    if st_path is None: st_path = [__DEFAULT_PATH__, __INNER_DEFAULT_PATH__][__b__INNER]

    # Validation du chemin
    if not st_path or not isinstance(st_path, str):
        raise ValueError("Le chemin doit être une chaîne non vide")

    # Normalisation du chemin pour tous les OS
    chemin_normalise = Path(st_path).resolve()

    # Vérification de l'existence
    if not chemin_normalise.exists():
        raise FileNotFoundError(f"Le fichier n'existe pas: {chemin_normalise}")

    # Vérification que c'est bien un fichier
    if not chemin_normalise.is_file():
        raise ValueError(f"Le chemin ne pointe pas vers un fichier: {chemin_normalise}")

    # Lecture du fichier
    try:
        with open(chemin_normalise, 'r', encoding='utf-8') as fichier:
            donnees = js.load(fichier)

        st_key: str = env_key(an_env=an_environment, st_subname=st_subname)

        if st_key not in donnees:
            st_msg: str = ""
            if an_environment != AccessEnvironment.PROD:
                st_msg = f";{st_subname!r}"
            raise KeyError(f"L'environment: <{an_environment!s}{st_msg}> n'est pas dans le fichier de configuration!")
        return donnees[st_key]

    except PermissionError:
        raise PermissionError(f"Pas de permission de lecture pour: {chemin_normalise}")

    except js.JSONDecodeError as e:
        raise js.JSONDecodeError(
            f"Erreur de format JSON dans {chemin_normalise}: {e.msg}",
            e.doc,
            e.pos
        )

    except UnicodeDecodeError:
        # Tentative avec un autre encodage
        try:
            with open(chemin_normalise, 'r', encoding='latin-1') as fichier:
                donnees = js.load(fichier)
            return donnees
        except Exception as e:
            raise UnicodeDecodeError(
                'utf-8', b'', 0, 0,
                f"Erreur d'encodage pour {chemin_normalise}")


if __name__ == "__main__":

    __b__INNER = True
    data: AccessData = load_config(an_environment=AccessEnvironment.PROD, st_subname='prod', st_path=__INNER_DEFAULT_PATH__)
    print(data)

    data: AccessData = load_config(an_environment=AccessEnvironment.UAT, st_subname='global', st_path=__INNER_DEFAULT_PATH__)
    print(data)

    try:
        # on s'attend a une erreur car il faut au moins un nom de sous environment
        data: AccessData = load_config(an_environment=AccessEnvironment.UAT, st_path=__INNER_DEFAULT_PATH__)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {e}')


    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: AccessData = load_config(an_environment=AccessEnvironment.UAT, st_subname="toto", st_path=__INNER_DEFAULT_PATH__)
    except KeyError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {e}')


    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: AccessData = load_config(an_environment=AccessEnvironment.PROD, st_path="toto.json")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {type(e)}')

    try:
        # on s'attend a une erreur car le nom de sous environment toto n'existe pas!
        data: AccessData = load_config(an_environment=AccessEnvironment.PROD, st_path=__INNER_DEFAULT_PATH__)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f'unexpected error!: {type(e)}')

    __b__INNER = False