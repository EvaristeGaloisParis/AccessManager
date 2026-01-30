"""
encapsule le mécanisme de l'objet MailLogin qui permet de contenir les id, login

pour instancier un MailLogin il faut utiliser la fonction: init_from_config
"""

from typing import Optional, Final
import os
import datetime as dt

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, MailServerConfig, MailContainer
from AccessMgr._modLoader import load_config, env_key


__ELT__MAIL__: Final[str] = 'mail'
__ELT__KEY__: Final[str] = 'key'


class MailLogin:
    """
    gère les logins / mot de passe et configurations de boites mails pour différents environment dans un projet

    instanciation via: init_from_config() se connectera tout seul a la base de données.

    inclut une gestion de durée de vie des identifiants. Ils deviennent inaccessibles une fois la durée de vie passée.
    """

    __id: str = ""                              # l'id dans le fichier de configuration
    __smtp: Optional[MailServerConfig] = None   # les parametrages techniques facultatifs
    __imap: Optional[MailServerConfig] = None   # les parametrages techniques facultatifs
    __f_timestamp: float = 0                    # l'instant de création
    __f_end_of_life: float = 0                  # l'instant de péremption

    @classmethod
    def init_from_config(cls, st_mail_id: str,
                 an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                 st_path: Optional[str] = None) -> 'MailLogin':
        """

        Args:
            st_mail_id: l'id de la configuration a aller chercher
            an_environment: l'environnement a requeter
            st_sub_name: le sous nom dans l'environnement
            st_path: le chemin vers le fichier de configuration

        Returns:
            les informations du compte mail. None en cas de probleme.

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            PermissionError: Si pas de permissions de lecture
            json.JSONDecodeError: Si le JSON est mal formaté
            ValueError: Si le chemin est vide ou invalide; ou si l'environement demandé est mal configuré
            KeyError: si  la configuration est vide, ou l'envionment x subname n'est pas dans le fichier de config
            TypeError: si la configuration n'est pas de type Mail!
        """
        try:
            data: AccessData = load_config(st_path=st_path, st_subname=st_sub_name, an_environment=an_environment)
            if data is None or len(data) == 0:
                raise KeyError(f"no configuration for {an_environment} in file: {st_path}")
        except Exception as e:
            raise e

        st_key: str = f"{__ELT__MAIL__}_{st_mail_id}"

        if st_key not in data:
            raise KeyError(f"no configuration named {st_mail_id} for mail in {an_environment} in file: {st_path}")

        data_mail: MailContainer = data[st_key]
        if "type" not in data_mail:
            raise KeyError(f"Configuration named {st_mail_id} in {an_environment} in file: {st_path} has no type")

        if data_mail["type"].strip().lower() != __ELT__MAIL__:
            raise TypeError(f"Configuration named {st_mail_id} in {an_environment} in file: {st_path} has incorrect type: {data_mail['type']}")

        return cls(data_mail=data_mail, an_environment=an_environment, st_sub_name=st_sub_name)

    def __init__(self, data_mail: MailContainer, an_environment: AccessEnvironment, st_sub_name: str):

        self.__id = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{data_mail["id"].replace(" ", "_")}'
        self.__f_timestamp = dt.datetime.now().timestamp()
        self.__f_end_of_life = self.__f_timestamp + float(data_mail["duration"])

        if "imap" in data_mail: self.__imap = data_mail["imap"]
        if "smtp" in data_mail: self.__smtp = data_mail["smtp"]

        # on pousse a l'os les éléments clefs!
        os.environ[self.__key(st_element=__ELT__MAIL__)] = data_mail["mail"]
        os.environ[self.__key(st_element=__ELT__KEY__)] = data_mail["key"]

    def __key(self, st_element: str) -> str:
        return f'{self.__id}__{st_element}__'

    @property
    def type(self) -> str:
        return __ELT__MAIL__

    @property
    def timestamp(self) -> float:
        return self.__f_timestamp

    @property
    def validity_end(self) -> Optional[float]:
        # validité permanente
        if self.__f_end_of_life <= self.__f_timestamp: return None
        return self.__f_end_of_life

    def is_alive(self) -> bool:
        if self.__f_end_of_life <= self.__f_timestamp: return True
        return dt.datetime.now().timestamp() < self.__f_end_of_life

    def user_mail(self) -> str:
        """
        envoie l'adresse mail du compte

        Returns:
            str qui est une adresse mail
        """
        return os.getenv(self.__key(st_element=__ELT__MAIL__))

    def key(self) -> str:
        """
        la clef du compte mail!

        Returns:
            str qui est la clef du compte
        """

        # si le token est périmé, on renvoie blanc
        if not self.is_alive(): return ""

        return os.getenv(self.__key(st_element=__ELT__KEY__))


    def server_smtp(self) -> MailServerConfig:
        """
        server d'envoi de mail!

        :return:
            le dict type qui modélise la partie smtp du mail
        """
        return  self.__smtp

    def server_imap(self) -> MailServerConfig:
        """
        server de lecture!

        :return:
            le dict type qui modélise la partie imap du mail

        """
        return self.__imap

    def __repr__(self) -> str:
        st_validity_end: str = "Infinity"
        if self.validity_end is not None:
            st_validity_end = f'{dt.datetime.fromtimestamp(self.validity_end):%d-%b-%Y %H:%M:%S}'

        return (f'Mail: {self.__id} - '
                f'imap: {["configured", "None"][self.__imap is None]} - '
                f'smtp: {["configured", "None"][self.__smtp is None]} - '
                f'validity: start: {dt.datetime.fromtimestamp(self.__f_timestamp):%d-%b-%Y %H:%M:%S} -> '
                f'end: {st_validity_end} -> '
                f'alive: {self.is_alive()}')

    def __str__(self) -> str:
        return f'{self.__id}'


if __name__ == "__main__":

    mail: MailLogin = MailLogin(st_mail_id="Ze.Bot.4.Teddy.And.Ppr", an_environment=AccessEnvironment.PROD)
    print(f'{mail!r}')
    print(mail.user_mail())
    print(mail.key())