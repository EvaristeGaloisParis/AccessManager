"""

"""
from typing import Optional

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData
from AccessMgr._modMailLogin import MailLogin

__version__ = "0.1.0"

__all__ = ["AccessEnvironment", "AccessData", "MailLogin"]


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


