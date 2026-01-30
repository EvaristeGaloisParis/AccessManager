from typing import Optional, Final
import os

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, MailServerConfig, MailContainer
from AccessMgr._modLoader import load_config, env_key


__ELT__MAIL__: Final[str] = 'mail'
__ELT__KEY__: Final[str] = 'key'


class MailLogin:
    """gère les logins / mot de passe et configurations de boites mails pour différents environment dans un projet"""
    __id: str = ""
    __smtp: Optional[MailServerConfig] = None
    __imap: Optional[MailServerConfig] = None

    def __init__(self, st_mail_id: str,
                 an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                 st_path: Optional[str] = None):

        data: AccessData = load_config(st_path=st_path, st_subname=st_sub_name, an_environment=an_environment)
        st_key: str = f"mail_{st_mail_id}"

        if data is None:
            print("errpr")
        else:
            if st_key not in data:
                print("error")
            else:
                data_mail: MailContainer = data[st_key]

                self.__id = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{data_mail["id"]}'
                if "imap" in data_mail: self.__imap = data_mail["imap"]
                if "smtp" in data_mail: self.__smtp = data_mail["smtp"]
                # on pousse a l'os les elements!

                os.environ[self.__key(st_element=__ELT__MAIL__)] = data_mail["mail"]
                os.environ[self.__key(st_element=__ELT__KEY__)] = data_mail["key"]

    def __key(self, st_element: str) -> str:
        return f'{self.__id}__{st_element}__'

    def user_mail(self) -> str:
        return os.getenv(self.__key(st_element=__ELT__MAIL__))

    def api_mail(self) -> str:
        return os.getenv(self.__key(st_element=__ELT__KEY__))

    def server_smtp(self) -> MailServerConfig:
        """
        server d'envoi de mail!

        :return:
        """
        return  self.__smtp

    def server_imap(self) -> MailServerConfig:
        """
        server de lecture!

        :return:
        """
        return self.__imap

    def __repr__(self) -> str:
        return f'Mail: {self.__id} - imap: {["configured", "None"][self.__imap is None]} - smtp: {["configured", "None"][self.__smtp is None]}'

    def __str__(self) -> str:
        return f'{self.__id}'


if __name__ == "__main__":

    mail: MailLogin = MailLogin(st_mail_id="Ze.Bot.4.Teddy.And.Ppr", an_environment=AccessEnvironment.PROD)
    print(f'{mail!r}')
    print(mail.user_mail())
    print(mail.api_mail())