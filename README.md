# accessmgr

Chargement et distribution **sécurisés** de credentials (mail, Telegram, KuCoin,
Kraken, DataBento, healthcheck) depuis un fichier JSON externe — **sans jamais exposer
de secret en clair dans le code**.

> Le nom de distribution est `accessmgr`, le package importable est `AccessMgr`.

## Principe

1. Tous les secrets vivent dans un **fichier JSON externe** (hors du dépôt), jamais
   dans le code source.
2. Des *factory functions* (`get_kucoin_token`, `get_telegram_config`,
   `get_healthcheck_config`, …) lisent ce fichier et créent des objets credential.
3. Les secrets transitent par les **variables d'environnement** du process et sont
   exposés via des propriétés avec **contrôle de durée de vie** (`duration`, en
   secondes ; `-1` = permanent).

## Installation

```bash
pip install accessmgr
```

Aucune dépendance externe (stdlib uniquement). Python ≥ 3.11.

## Format du fichier de configuration (`access.json`)

Les clés de premier niveau sont des environnements (`prod`, `uat_<nom>`, `dev_<nom>`).
Chaque entrée est préfixée par son type (`telegram_`, `kucoin_`, `healthcheck_`, …).

```json
{
  "prod": {
    "telegram_myBot": {
      "id": "myBot", "type": "telegram", "duration": -1,
      "name": "My Bot", "token": "<telegram-bot-token>", "chat_id": "<chat-id>"
    },
    "healthcheck_nightly": {
      "id": "nightly", "type": "healthcheck", "duration": -1,
      "name": "nightly job", "uuid": "<healthchecks-uuid>"
    },
    "provider_kraken_meanrev": {
      "id": "meanrev", "type": "provider", "support": "spot", "duration": -1,
      "user_name": "Kraken MeanRev", "key": "<api-key>", "secret": "<api-secret-base64>"
    }
  }
}
```

> **Objet Kraken** — remplir une entrée `provider_kraken_<id>` :
> - **clé de l'objet** = `provider_kraken_` suivi de la valeur de `id` (ils doivent concorder) ;
> - `id` : identifiant **technique** passé à `get_kraken_config(st_id=...)` (sensible à la casse) ;
> - `type` : toujours `"provider"` ;
> - `support` : **`"spot"`** (API `api.kraken.com`) ou **`"fut"`** (API `futures.kraken.com`) — une clé
>   spot ne s'authentifie que sur l'API spot, une clé futures que sur l'API futures. Défaut : `"spot"` ;
> - `duration` : durée de vie en secondes (`-1` = permanent) ;
> - `user_name` : libellé humain (affiché dans les logs, **non sensible**) ;
> - `key` : clé **publique** (API Key) ; `secret` : clé **privée** (base64). **Jamais** de clé en clair ailleurs.

> ⚠️ Ce fichier contient vos secrets : gardez-le **hors du dépôt git** et à accès restreint.

## Utilisation

```python
from AccessMgr import (
    get_telegram_config,
    get_healthcheck_config,
    AccessEnvironment,
)

CONFIG = "/chemin/vers/access.json"

# Telegram
tg = get_telegram_config(st_id="myBot", an_environment=AccessEnvironment.PROD,
                         st_config_path=CONFIG)
bot_token = tg.token()
chat_id = tg.chat_id()

# Healthcheck (healthchecks.io ou compatible)
hc = get_healthcheck_config(st_id="nightly", an_environment=AccessEnvironment.PROD,
                            st_config_path=CONFIG)
ping_url = hc.url()          # https://hc-ping.com/<uuid> (base = constante du code)

# Kraken (spot ou futures selon le champ 'support')
from AccessMgr import get_kraken_config
kr = get_kraken_config(st_id="meanrev", an_environment=AccessEnvironment.PROD,
                       st_config_path=CONFIG)
api_key = kr.key()           # clé publique
api_secret = kr.secret()     # clé privée (base64)
venue = kr.support           # 'spot' ou 'fut' -> aiguille le bon connecteur
if kr.is_spot:
    ...                      # api.kraken.com
```

Pour les environnements hors production, un `st_sub_name` est obligatoire :

```python
cfg = get_telegram_config(st_id="myBot", an_environment=AccessEnvironment.UAT,
                          st_sub_name="global", st_config_path=CONFIG)
```

### Chemin de configuration par défaut *(depuis 0.1.2)*

Plutôt que de répéter `st_config_path` à chaque appel, définissez-le **une seule
fois** au démarrage avec `set_default_config_path`. Tous les `get_*()` l'utilisent
ensuite automatiquement :

```python
import AccessMgr
from AccessMgr import get_kucoin_token, get_databendo_config, AccessEnvironment

AccessMgr.set_default_config_path("/chemin/vers/access.json")   # une fois au boot

# plus besoin de st_config_path : le défaut est utilisé
kc = get_kucoin_token(st_id="main", an_environment=AccessEnvironment.PROD)

# l'argument explicite reste prioritaire : surcharge ponctuelle (ex. dev)
db = get_databendo_config(st_id="feed", an_environment=AccessEnvironment.DEV,
                          st_sub_name="test", st_config_path="/autre/access_dev.json")
```

> Passer `set_default_config_path(None)` **réinitialise** explicitement le
> comportement (retour aux chemins par défaut codés en dur). Une chaîne vide lève
> `ValueError`. L'argument `st_config_path` d'un appel prime toujours sur le défaut.

## Providers disponibles

| Factory | Type JSON | Retourne |
|---------|-----------|----------|
| `get_mail_config` | `mail` | `MailLogin` (SMTP/IMAP) |
| `get_telegram_config` | `telegram` | `ProviderTelegram` (`token()`, `chat_id()`) |
| `get_kucoin_token` | `provider` (`provider_kuCoin_<id>`) | `ProviderKucoin` |
| `get_kraken_config` | `provider` (`provider_kraken_<id>`) | `ProviderKraken` (`key()`, `secret()`, `support`, `is_spot`/`is_fut`) |
| `get_massive_data_token` | `massivedata` | `ProviderMassiveData` |
| `get_databendo_config` | `databento` | `ProviderDataBendo` |
| `get_coinalyze_config` | `provider` (`provider_coinalyze_<id>`) | `ProviderCoinalyze` (`api_key()`) |
| `get_healthcheck_config` | `healthcheck` | `ProviderHealthcheck` (`url()`, `uuid()`) |

## Sécurité

- Aucun secret en clair dans le code source.
- Les secrets transitent : JSON externe → `os.environ` → propriétés avec contrôle
  d'expiration.
- Les objets ne *loggent* jamais leurs secrets (absents de `repr`/`str`).

## Licence

MIT — voir [LICENSE](LICENSE).
