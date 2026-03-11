from typing import Optional, Final
import os
import datetime as dt

from enum import StrEnum

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, Provider_Kucoin
from AccessMgr._modLoader import load_config, env_key


__PROVIDER_TYPE__: Final[str] = 'provider'


class _ProviderElt(StrEnum):
    """modélise tous les élément mis en mémoire pour le provider KuCoin"""
    KEY: Final[str] = '__KEY__'
    SECRET: Final[str] = '__SECRET__'
    PHRASE: Final[str] = '__PHRASE__'
    UUID: Final[str] = '__UUID__'
    TRD_PASS: Final[str] = '__TRD_PASS__'


class ProviderKucoin:
    """
    handler vers une connexion KuCoin
    """

    @classmethod
    def init_from_config(cls, st_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                         st_path: Optional[str] = None) -> 'ProviderKucoin':

        try:
            data: AccessData = load_config(st_path=st_path, an_environment=an_environment, st_subname=st_sub_name)

        except Exception as e:
            raise e

        st_key: str = f"{__PROVIDER_TYPE__}_kuCoin_{st_id}"

        if st_key not in data:
            raise KeyError(f"no configuration named {st_id} for mail in {an_environment} in file: {st_path}")

        data_provider: Provider_Kucoin = data[st_key]
        if "type" not in data_provider:
            raise KeyError(f"Configuration named {st_id} in {an_environment} in file: {st_path} has no type")

        if data_provider["type"].strip().lower() != __PROVIDER_TYPE__:
            raise TypeError(
                f"Configuration named {st_id} in {an_environment} in file: {st_path} has incorrect type: {data_provider['type']}")

        return cls(provider=data_provider, an_environment=an_environment, st_sub_name=st_sub_name)

    def __init__(self, provider: Provider_Kucoin, an_environment: AccessEnvironment, st_sub_name: str):
        """
            st_inner_id: str  --> l'id technique pour récuperer la clef dans l'os
            st_user_name: str   --> le nom de l'utilisateur sur le siet
            f_timestamp: float--> l'isntant de création du jeton
            f_end_of_life: float --> la fin de vie du jeton !

        Args:
            provider: le provider que l'on vise
            an_environment: Prod, Uat, Dev
            st_sub_name:  pour les environnements qui ne sont pas de prod, il faut donner un sous nom (car il peut y avoir N env UAT)
        """
        self.__st_inner_id = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{provider["id"].replace(" ", "_")}'
        self.__st_user_name = provider["user_name"].strip()  # doit-on le cacher ???

        self.__f_timestamp = dt.datetime.now().timestamp()
        self.__f_end_of_life = self.__f_timestamp + float(provider["duration"])

        # on pousse a l'os les éléments clefs!
        for elt in Provider_Kucoin.__annotations__:
            st_to_push: str = f'__{elt.upper()}__'
            if st_to_push  in _ProviderElt:
                os.environ[self.__key(st_element=_ProviderElt(st_to_push))] = provider[elt]

        # il manque le reverse check... mais je ne sais pas comment le faire !

    def __key(self, st_element: _ProviderElt) -> str:
        return f'{self.__st_inner_id}__{str(st_element)}__'

    @property
    def type(self) -> str:
        return __PROVIDER_TYPE__

    @property
    def sub_type(self) -> str:
        return "kucoin"

    @property
    def user_name(self) -> str:
        return self.__st_user_name

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

    def key(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=_ProviderElt.KEY))

    def secret(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=_ProviderElt.SECRET))

    def trd_pass(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=_ProviderElt.TRD_PASS))

    def phrase(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=_ProviderElt.PHRASE))

    def uuid(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=_ProviderElt.UUID))


    def __repr__(self) -> str:
        st_validity_end: str = "Infinity"
        if self.validity_end is not None:
            st_validity_end = f'{dt.datetime.fromtimestamp(self.validity_end):%d-%b-%Y %H:%M:%S}'

        return (f'inner_id: {self.__st_inner_id} - '
                f'user_id: {self.__st_user_name} - '
                f'validity: start: {dt.datetime.fromtimestamp(self.__f_timestamp):%d-%b-%Y %H:%M:%S} -> '
                f'end: {st_validity_end} -> '
                f'alive: {self.is_alive()}')

    def __str__(self) -> str:
        return f'{self.__st_user_name}'





if __name__ == "__main__":
    data: Provider_Kucoin = {"key":">> a key to push here <<", "id": "test", "duration": -1, "type": "provider",
                             "phrase":"a phrase", "uuid":"my uuid","secret":"my secret", "trd_pass":"a trd pass",
                             "user_name": "my user name" }
    prvdr: ProviderKucoin = ProviderKucoin(provider=data, st_sub_name="",an_environment=AccessEnvironment.PROD)
    print('\noutput')
    print(f'{prvdr.phrase()}')
    print(f'{prvdr.secret()}')
    print(f'{prvdr.trd_pass()}')
    print(f'{prvdr.key()}')
    print(f'{prvdr.sub_type}')
    print(f'{prvdr.type}')
    print(f'{prvdr.validity_end}')