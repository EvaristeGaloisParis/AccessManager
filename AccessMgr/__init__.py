"""
Packqage pour gérer les droits des différentes sources sur un projet.

Les sources peuvent être des :

- mail: utilisation de MailContainer pour modéliser dans le fichier, et MailLogin pour l'utilisation dans le code
MailContainer doit avoir les items suivants:
id: str : son nom
type: str == mail impérativement
duration: str: la durée de vie de la connexion. Mettre -1 pour une durée infinie
key: str: la clef api
mail: str: l'adresse mail cible
smtp: MailServerConfig = (host, port): optionnel: config smtp
imap: MailServerConfig = (host, port): optionnel: config imap


- provider: utilisation de ProviderContainer pour modéliser le fichier, l'objet n'est pas encore créé


"""
from typing import Optional

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, MailContainer, ProviderContainer, MailServerConfig
from AccessMgr._modMailLogin import MailLogin
from AccessMgr._modMassiveProvider import ProviderMassiveData

__version__ = "0.1.0"


__all__ = ["AccessEnvironment", "AccessData", "MailContainer", "MailLogin", "MailServerConfig", "get_mail_config",
           "ProviderMassiveData", "get_massive_data_token"]


def get_massive_data_token(st_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None, st_config_path: Optional[str] = None) -> ProviderMassiveData:
    """
    créer un objet MassiveConnexion qui contient toute l'information du compte Massive Data pour récuperer les données!

    Args:
        st_id: str: l'id utiliser dans le gestionnaire de droits!
        an_environment: un environment choisi entre: prod, uat, dev
        st_sub_name: le nom du sous environment (si nous ne sommes pas en prod)
        st_config_path: un chemin qui pointe vers le fichier de configuration json!

    Returns:
        un objet MassiveConnexion qui contient toute l'information du compte Massive Data pour récuperer les données!
        Ne pas logger les informations qu'il contient !!!!

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        PermissionError: Si pas de permissions de lecture
        json.JSONDecodeError: Si le JSON est mal formaté
        ValueError: Si le chemin est vide ou invalide; ou si l'environement demandé est mal configuré
        KeyError: si  la configuration est vide, ou l'envionment x subname n'est pas dans le fichier de config
        TypeError: si la configuration n'est pas de type MassiveProvide!
    """

    return ProviderMassiveData.init_from_config(st_id=st_id, an_environment=an_environment,
                                                st_sub_name=st_sub_name, st_path=st_config_path)


def get_mail_config(mail_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                    st_config_path: Optional[str] = None) -> MailLogin:
    """
    retourne une configuration et des logins mail pour une configuration donnée et un fichier de configuration défini

    Args:
        mail_id: str: l'id du compte mail dans le fichier de configuration
        an_environment: un environment choisi entre: prod, uat, dev
        st_sub_name: le nom du sous environment (si nous ne sommes pas en prod)
        st_config_path: un chemin qui pointe vers le fichier de configuration json!

    Returns:
        un objet MailLoginq qui contient toute l'information du compte mail.
        Ne pas logger les informations qu'il contient !!!!

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        PermissionError: Si pas de permissions de lecture
        json.JSONDecodeError: Si le JSON est mal formaté
        ValueError: Si le chemin est vide ou invalide; ou si l'environement demandé est mal configuré
        KeyError: si  la configuration est vide, ou l'envionment x subname n'est pas dans le fichier de config
        TypeError: si la configuration n'est pas de type Mail!
    """

    return MailLogin.init_from_config(st_mail_id=mail_id,
                                      an_environment=an_environment, st_sub_name=st_sub_name,
                                      st_path=st_config_path)


def set_new_mail_config(config: MailContainer, mail_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                        st_config_path: Optional[str] = None) -> bool:
    pass


def delete_mail_config(mail_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                        st_config_path: Optional[str] = None) -> bool:
    pass