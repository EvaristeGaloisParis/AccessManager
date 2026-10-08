from typing import Optional, Final
import os
import datetime as dt

from AccessMgr._modConstantes import AccessEnvironment
from AccessMgr._modJsonStructure import AccessData, Provider_Healthcheck
from AccessMgr._modLoader import load_config, env_key


# base publique des urls de ping ; centralisee ici pour limiter les risques si le domaine change.
# seule la partie variable et sensible (l'uuid) est stockee dans access.json.
__HC_BASE_URL__: Final[str] = 'https://hc-ping.com/'

__PROVIDER_TYPE__: Final[str] = 'healthcheck'
__PROVIDER_ELT_UUID__: Final[str] = '__UUID__'


class ProviderHealthcheck:
    """
    Provider pour un check de supervision type healthchecks.io (ou compatible).

    Ne porte qu'un seul secret : l'uuid de ping (qui agit comme un token). Comme les
    autres providers, on le pousse en variable d'environnement et on l'expose via
    uuid()/url() avec le meme controle de duree de vie. On ne le logge JAMAIS (ni repr ni str).
    """

    @classmethod
    def init_from_config(cls, st_id: str, an_environment: AccessEnvironment, st_sub_name: Optional[str] = None,
                         st_path: Optional[str] = None) -> 'ProviderHealthcheck':

        try:
            data: AccessData = load_config(st_path=st_path, an_environment=an_environment, st_subname=st_sub_name)

        except Exception as e:
            raise e

        st_key: str = f"{__PROVIDER_TYPE__}_{st_id}"

        if st_key not in data:
            raise KeyError(f"no configuration named {st_id} for healthcheck in {an_environment} in file: {st_path}")

        data_provider: Provider_Healthcheck = data[st_key]
        if "type" not in data_provider:
            raise KeyError(f"Configuration named {st_id} in {an_environment} in file: {st_path} has no type")

        if data_provider["type"].strip().lower() != __PROVIDER_TYPE__:
            raise TypeError(
                f"Configuration named {st_id} in {an_environment} in file: {st_path} has incorrect type: {data_provider['type']}")

        return cls(provider=data_provider, an_environment=an_environment, st_sub_name=st_sub_name)

    def __init__(self, provider: Provider_Healthcheck, an_environment: AccessEnvironment, st_sub_name: Optional[str]):
        """
            uuid: str  --> la partie variable de l'url de ping (porte un token, ne pas logger)

        Args:
            provider: le provider que l'on vise
            an_environment: Prod, Uat, Dev
            st_sub_name: pour les environnements qui ne sont pas de prod, il faut donner un sous nom
        """
        self.__st_inner_id: str = f'{env_key(an_env=an_environment, st_subname=st_sub_name)}_{provider["id"].replace(" ", "_")}'
        self.__st_name: str = provider["name"].strip()

        self.__f_timestamp: float = dt.datetime.now().timestamp()
        self.__f_end_of_life: float = self.__f_timestamp + float(provider["duration"])

        # on pousse a l'os l'element sensible (l'uuid porte un token)
        os.environ[self.__key(st_element=__PROVIDER_ELT_UUID__)] = provider["uuid"]

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
        # validite permanente
        if self.__f_end_of_life <= self.__f_timestamp: return None
        return self.__f_end_of_life

    def is_alive(self) -> bool:
        if self.__f_end_of_life <= self.__f_timestamp: return True
        return dt.datetime.now().timestamp() < self.__f_end_of_life

    @property
    def base_url(self) -> str:
        return __HC_BASE_URL__

    def uuid(self) -> Optional[str]:

        if not self.is_alive(): return None

        return os.getenv(self.__key(st_element=__PROVIDER_ELT_UUID__))

    def url(self) -> Optional[str]:

        st_uuid: Optional[str] = self.uuid()
        if st_uuid is None: return None

        return f'{__HC_BASE_URL__}{st_uuid}'

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
