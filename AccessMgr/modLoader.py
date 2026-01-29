"""
permet de lire le fichier de parametrage

"""
from typing import Optional
from modJsonStructure import Container, MailContainer, MailServerConfig, js, AccessData
from modConstantes import AccessEnvironment
import os
from pathlib import Path



def __env_key(an_env: AccessEnvironment, st_subname: str) -> str:

    if an_env == AccessEnvironment.PROD:
        return f'{an_env}'

    return f'{an_env}_{st_subname.strip()}'


def load_config(st_path: str = '../../access/access.json',
                an_environment: AccessEnvironment=AccessEnvironment.PROD,
                st_subname: Optional[str] = None ) -> AccessData:
    """
    lit le fichier de paramétrage

    Args:
       st_subname:
       st_path: str: Chemin du fichier JSON (string)
        an_environment: : un environment. Si prod le subname est ignoré

    Returns:

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        PermissionError: Si pas de permissions de lecture
        json.JSONDecodeError: Si le JSON est mal formaté
        ValueError: Si le chemin est vide ou invalide; ou si l'environement demandé est mal configuré
        KeyError: si l'envionment x subname n'est pas dans le fichier de configuration
   """

    if an_environment != AccessEnvironment.PROD:
        if st_subname is None or st_subname.strip() == "":
            raise ValueError(f"Pour l'environement: {an_environment}, le subname est obligatoire et doit etre non vide!")


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


        st_key: str = __env_key(an_env=an_environment, st_subname=st_subname)

        if st_key not in donnees:
            st_msg: str = ""
            if an_environment != AccessEnvironment.PROD:
                st_msg = f"{st_subname!r}"
            raise KeyError(f"L'environment: {an_environment} {st_msg} n'est pas dans le fichier de configuration!")
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

    data: AccessData = load_config(an_environment=AccessEnvironment.PROD, st_subname='prod')
    print(data)

