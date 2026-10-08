# accessmgr

Chargement et distribution **sécurisés** de credentials (mail, Telegram, KuCoin,
DataBento, healthcheck) depuis un fichier JSON externe — **sans jamais exposer de
secret en clair dans le code**.

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
    }
  }
}
```

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
```

Pour les environnements hors production, un `st_sub_name` est obligatoire :

```python
cfg = get_telegram_config(st_id="myBot", an_environment=AccessEnvironment.UAT,
                          st_sub_name="global", st_config_path=CONFIG)
```

## Providers disponibles

| Factory | Type JSON | Retourne |
|---------|-----------|----------|
| `get_mail_config` | `mail` | `MailLogin` (SMTP/IMAP) |
| `get_telegram_config` | `telegram` | `ProviderTelegram` (`token()`, `chat_id()`) |
| `get_kucoin_token` | `kucoin` | `ProviderKucoin` |
| `get_massive_data_token` | `massivedata` | `ProviderMassiveData` |
| `get_databendo_config` | `databento` | `ProviderDataBendo` |
| `get_healthcheck_config` | `healthcheck` | `ProviderHealthcheck` (`url()`, `uuid()`) |

## Sécurité

- Aucun secret en clair dans le code source.
- Les secrets transitent : JSON externe → `os.environ` → propriétés avec contrôle
  d'expiration.
- Les objets ne *loggent* jamais leurs secrets (absents de `repr`/`str`).

## Licence

MIT — voir [LICENSE](LICENSE).
