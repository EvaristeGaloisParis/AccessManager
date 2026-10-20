from typing import Optional, Final
import os
import datetime as dt

from enum import StrEnum

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, Provider_Kraken
from AccessMgr._modLoader import load_config, env_key


__PROVIDER_TYPE__: Final[str] = 'provider'


class _ProviderElt(StrEnum):
    """Elements sensibles mis en memoire (os.environ) pour Kraken Futures. Ne pas importer."""
    KEY: Final[str] = '__KEY__'
    SECRET: Final[str] = '__SECRET__'


__SUPPORT_SPOT__: Final[str] = 'spot'
__SUPPORT_FUT__: Final[str] = 'fut'


class ProviderKraken:
    """
    Handler vers une connexion Kraken (spot api.kraken.com OU futures futures.kraken.com).

    Porte deux secrets : key (publique) et secret (privee, base64). 'support' indique la
    VENUE de la cle ('spot' par defaut, ou 'fut') : une cle spot ne s'authentifie que sur
    l'API spot, une cle futures que sur l'API futures. Comme les autres providers, on pousse
    les secrets en variable d'environnement et on les expose via key()/secret() avec le meme
    controle de duree de vie. On ne les logge JAMAIS (ni repr ni str).
    """

    @classmethod
    def init_from_config(cls, st_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                         st_path: Optional[str] = None) -> 'ProviderKraken':

        try:
            data: AccessData = load_config(st_path=st_path, an_environment=an_environment, st_subname=st_sub_name)

        except Exception as e:
            raise e

        st_key: str = f"{__PROVIDER_TYPE__}_kraken_{st_id}"

        if st_key not in data:
            raise KeyError(f"no configuration named {st_id} for kraken in {an_environment} in file: {st_path}")

        data_provider: Provider_Kraken = data[st_key]
        if "type" not in data_provider:
            raise KeyError(f"Configuration named {st_id} in {an_environment} in file: {st_path} has no type")

        if data_provider["type"].strip().lower() != __PROVIDER_TYPE__:
            raise TypeError(
                f"Configuration named {st_id} in {an_environment} in file: {st_path} has incorrect type: {data_provider['type']}")

        return cls(provider=data_provider, an_environment=an_environment, st_sub_name=st_sub_name)

    def __init__(self, provider: Provider_Kraken, an_environment: AccessEnvironment, st_sub_name: Optional[str]):
        """
        Args:
            provider: le provider que l'on vise
            an_environment: Prod, Uat, Dev
            st_sub_name: pour les environnements non-prod, donner un sous-nom
        """
        self.__st_inner_id = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{provider["id"].replace(" ", "_")}'
        self.__st_user_name = provider["user_name"].strip()

        # venue de la cle : 'spot' (defaut) ou 'fut' ; non sensible -> pas en os.environ
        st_support = str(provider.get("support", __SUPPORT_SPOT__)).strip().lower()
        if st_support not in (__SUPPORT_SPOT__, __SUPPORT_FUT__):
            raise ValueError(
                f"ProviderKraken : 'support' invalide '{st_support}' "
                f"(attendu '{__SUPPORT_SPOT__}' ou '{__SUPPORT_FUT__}')")
        self.__st_support = st_support

        self.__f_timestamp = dt.datetime.now().timestamp()
        self.__f_end_of_life = self.__f_timestamp + float(provider["duration"])

        # on pousse a l'os les elements sensibles
        os.environ[self.__key(st_element=_ProviderElt.KEY)] = provider["key"]
        os.environ[self.__key(st_element=_ProviderElt.SECRET)] = provider["secret"]

    def __key(self, st_element: _ProviderElt) -> str:
        return f'{self.__st_inner_id}__{str(st_element)}__'

    @property
    def type(self) -> str:
        return __PROVIDER_TYPE__

    @property
    def sub_type(self) -> str:
        return "kraken"

    @property
    def support(self) -> str:
        """Venue de la cle : 'spot' ou 'fut'."""
        return self.__st_support

    @property
    def is_spot(self) -> bool:
        return self.__st_support == __SUPPORT_SPOT__

    @property
    def is_fut(self) -> bool:
        return self.__st_support == __SUPPORT_FUT__

    @property
    def user_name(self) -> str:
        return self.__st_user_name

    @property
    def timestamp(self) -> float:
        return self.__f_timestamp

    @property
    def validity_end(self) -> Optional[float]:
        # validite permanente
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
    data: Provider_Kraken = {"key": ">> a key <<", "id": "test", "duration": -1, "type": "provider",
                             "secret": "a base64 secret", "user_name": "my user name", "support": "spot"}
    prvdr: ProviderKraken = ProviderKraken(provider=data, st_sub_name="", an_environment=AccessEnvironment.PROD)
    print(f'{prvdr.key()}')
    print(f'{prvdr.secret()}')
    print(f'{prvdr.sub_type} / {prvdr.support}')
