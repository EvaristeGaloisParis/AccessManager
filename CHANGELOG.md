# Changelog

Toutes les évolutions notables de ce projet sont documentées ici.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et le projet suit le [versionnage sémantique](https://semver.org/lang/fr/).

## [0.1.6] - 2026-11-13

### Ajouté
- **`ProviderCoinalyze`** + factory **`get_coinalyze_config`** : gestion de la clé API Coinalyze
  (donnée dérivée crypto : open interest, long/short, liquidations, funding).
  - Une seule clé (`api_key`). Entrée JSON : clé `provider_coinalyze_<id>`, `type: "provider"`,
    champs `id`, `name`, `user_id`, `duration`, `api_key`.
  - La clé est poussée en variable d'environnement, jamais loggée (absente de `repr`/`str`),
    avec contrôle de durée de vie (`is_alive`, `validity_end`). Propriété d'accès : `api_key()`.
  - Tests auto-contenus (`tests/test_coinalyze.py`), README mis à jour.

## [0.1.5] - 2026-10-20

### Ajouté
- **`ProviderKraken`** + factory **`get_kraken_config`** : gestion des clés API Kraken.
  - Deux secrets : `key` (clé publique) et `secret` (clé privée, base64). Pas de passphrase.
  - Champ **`support`** : `"spot"` (API `api.kraken.com`) ou `"fut"` (API `futures.kraken.com`) —
    une clé spot ne s'authentifie que sur l'API spot, une clé futures que sur l'API futures.
    Défaut `"spot"` ; toute autre valeur lève `ValueError`. Propriétés `support`, `is_spot`, `is_fut`.
  - Entrée JSON : clé `provider_kraken_<id>`, `type: "provider"`. Secrets poussés en variables
    d'environnement, jamais loggés (absents de `repr`/`str`), avec contrôle de durée de vie.
  - README mis à jour (exemple JSON + usage) pour expliquer comment remplir un objet Kraken.

> Note : la 0.1.4 a été publiée manuellement (sans provenance/attestation) — à **yank**.
> La 0.1.5 est publiée via la CI (GitHub Release → Trusted Publishing), provenance signée rétablie.

## [0.1.2] - 2026-10-09

### Ajouté
- **`set_default_config_path(st_path)`** : permet de définir **une seule fois**, au
  démarrage de l'application, le fichier `access.json` utilisé par défaut. Tous les
  `get_*()` (kucoin, telegram, mail, databendo, healthcheck) l'utilisent ensuite
  automatiquement — plus besoin de répéter `st_config_path` à chaque appel.
  - L'argument `st_config_path` d'un appel **reste prioritaire** : on peut garder la
    plupart des accès dans le fichier par défaut et surcharger ponctuellement (ex.
    tester un provider depuis un autre fichier en cours de dev).
  - Passer **`None`** réinitialise explicitement le comportement (retour aux chemins
    codés en dur).
  - Une chaîne vide lève `ValueError`.

### Modifié
- `load_config` résout désormais le chemin selon la priorité :
  **argument explicite > chemin par défaut configuré > constante codée en dur**.
  Comportement strictement rétrocompatible tant que `set_default_config_path` n'est
  pas appelé.

## [0.1.1] - 2026-10-08

### Ajouté
- Provider **healthcheck** (`get_healthcheck_config`, `ProviderHealthcheck`) :
  supervision via healthchecks.io ou compatible. Seul l'`uuid` (partie sensible) est
  stocké dans `access.json` ; la base de l'URL est une constante du code.

## [0.1.0] - 2026-10-08

### Ajouté
- Version initiale : chargement sécurisé de credentials depuis un fichier JSON externe,
  sans secret en clair dans le code.
- Providers : `mail` (SMTP/IMAP), `telegram`, `kucoin`, `massivedata`, `databento`.
- Multi-environnement (`prod`, `uat_<nom>`, `dev_<nom>`) avec contrôle de durée de vie
  des credentials.

[0.1.2]: https://github.com/EvaristeGaloisParis/AccessManager/releases/tag/v0.1.2
[0.1.1]: https://github.com/EvaristeGaloisParis/AccessManager/releases/tag/v0.1.1
[0.1.0]: https://github.com/EvaristeGaloisParis/AccessManager/releases/tag/v0.1.0
