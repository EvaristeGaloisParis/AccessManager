from typing import Optional, Final
import os
import datetime as dt

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, Provider_Telegram
from AccessMgr._modLoader import load_config, env_key


__PROVIDER_TYPE__: Final[str] = 'telegram'
__PROVIDER_ELT_TOKEN__: Final[str] = '__KEY__'
__PROVIDER_ELT_CHAT_ID__: Final[str] = '__ACCESS__KEY__'


class ProviderTelegram:

    @classmethod
    def init_from_config(cls, st_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                         st_path: Optional[str] = None) -> 'ProviderTelegram':

        try:
            data: AccessData = load_config(st_path=st_path, an_environment=an_environment, st_subname=st_sub_name)

        except Exception as e:
            raise e

        st_key: str = f"{__PROVIDER_TYPE__}_{st_id}"

        if st_key not in data:
            raise KeyError(f"no configuration named {st_id} for mail in {an_environment} in file: {st_path}")

        data_provider: Provider_Telegram = data[st_key]
        if "type" not in data_provider:
            raise KeyError(f"Configuration named {st_id} in {an_environment} in file: {st_path} has no type")

        if data_provider["type"].strip().lower() != __PROVIDER_TYPE__:
            raise TypeError(
                f"Configuration named {st_id} in {an_environment} in file: {st_path} has incorrect type: {data_provider['type']}")

        return cls(provider=data_provider, an_environment=an_environment, st_sub_name=st_sub_name)

    def __init__(self, provider: Provider_Telegram, an_environment: AccessEnvironment, st_sub_name: str):
        """
            token: str      --> le token du robot
            chat_id: str   --> le chat où ecrire


        Args:
            provider: le provider que l'on vise
            an_environment: Prod, Uat, Dev
            st_sub_name:  pour les environnements qui ne sont pas de prod, il faut donner un sous nom (car il peut y avoir N env UAT)
        """
        self.__st_inner_id = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{provider["id"].replace(" ", "_")}'
        self.__st_name = provider["name"].strip()  # doit-on le cacher ???

        self.__f_timestamp = dt.datetime.now().timestamp()
        self.__f_end_of_life = self.__f_timestamp + float(provider["duration"])

        # on pousse a l'os les éléments clefs!
        os.environ[self.__key(st_element=__PROVIDER_ELT_TOKEN__)] = provider["token"]
        os.environ[self.__key(st_element=__PROVIDER_ELT_CHAT_ID__)] = provider["chat_id"]

    def __key(self, st_element: str) -> str:
        return f'{self.__st_inner_id}__{st_element}__'

    @property
    def type(self) -> str:
        return __PROVIDER_TYPE__

    @property
    def user_name(self) -> str:
        return self.__st_name

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

    def token(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=__PROVIDER_ELT_TOKEN__))

    def chat_id(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=__PROVIDER_ELT_CHAT_ID__))


    def __repr__(self) -> str:
        st_validity_end: str = "Infinity"
        if self.validity_end is not None:
            st_validity_end = f'{dt.datetime.fromtimestamp(self.validity_end):%d-%b-%Y %H:%M:%S}'

        return (f'inner_id: {self.__st_inner_id} - '
                f'user_id: {self.user_name} - '
                f'validity: start: {dt.datetime.fromtimestamp(self.__f_timestamp):%d-%b-%Y %H:%M:%S} -> '
                f'end: {st_validity_end} -> '
                f'alive: {self.is_alive()}')

    def __str__(self) -> str:
        return f'{self.user_name}'

