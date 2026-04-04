"""
A pour but principal de regrouper toutes les structures JSON que le logger devra manipuler!


on retrouve:

* le type générique : Container. Ne peut pas etre instancier !

* le type: Mail qui contient:
    :key la clef api !
    :mail le compte mail. il doit detre identique a l'id!
    :imap qui est un json MailServerConfig
    :smtp qui est un json MailServerConfig


* le MailServerConfig qui contient:
    :host
    :port
    :timeout (optionnel)
    : local_hostname (optionnel)

"""
from typing import Any, Optional, TypedDict, NotRequired
import json as js

class Container(TypedDict):
    """
    classe générique de container dont doit hériter un contener pour etre pris en charge !
    """
    id: str         # un id
    type: str       # reprise du type pour le casting
    duration: int   # la durée de vie du logger!

class MailServerConfig(TypedDict):
    """
    Représente les informations pour un appel mail vers le server:
    host ;
    port ;
    timeout ;
    local_hostname
    """
    host: str
    port: int
    timeout: NotRequired[Optional[float]]
    local_hostname: NotRequired[Optional[str]]


class MailContainer(Container):
    mail: str
    key: str
    smtp: NotRequired[MailServerConfig]
    imap: NotRequired[MailServerConfig]


class Provider_MassiveData(Container):
    """modelise nos droits sur le site MassiveDAta pour récuperer les données fines sur le forex et les commos"""
    id: str
    user_id: str
    key: str
    access_key_id: str


class Provider_Telegram(Container):
    """modelise Telegram minimal droits"""
    name: str
    token: str
    chat_id: str

class Provider_Kucoin(Container):
    """modelise nos droits sur le site KuCoin"""
    user_name: str
    trd_pass: str
    key: str
    secret: str
    phrase: str
    uuid: str


class ProviderContainer(Container):
    key: str


class AccessData(TypedDict):
    """
    doit contenir au moins un element de prod
    les environement d'UAT et de DEV doivent etre nommés:
         environment_subname et contenir un dict de container !
    """
    prod: dict[str, Container]