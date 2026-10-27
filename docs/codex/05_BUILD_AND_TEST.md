# 05 — Compilation et tests

Créé le 27 octobre 2026. `platformio.ini` n'existe pas encore : il sera créé
après validation de la carte et du mode d'intégration (`00_CONTEXT.md`,
D002).

## Environnements PlatformIO prévus

| Env | Usage |
|---|---|
| `HAThermostat` | binaire de production ; compilation de validation |
| `HAThermostat_banc` | même firmware + routes et traces de développement ; flashé sur le module de banc |
| `test_*` | bancs matériels ciblés (écran, tactile, capteur, sortie, Wi-Fi…) |

Chaque `test_*.cpp` définit son propre `setup()`/`loop()` : il est exclu du
`build_src_filter` des environnements de production.

## Socle commun de chaque environnement

```ini
platform = espressif32 @ <version figée>
board = esp32dev
framework = arduino
extra_scripts = pre:tools/version_build.py
monitor_speed = 115200
monitor_filters = esp32_exception_decoder
```

Les bibliothèques sont déclarées dans `lib_deps` avec une version bornée.
Il n'existe pas de définition PlatformIO dédiée à l'ESP32-2432S024 :
`esp32dev` est la base, comme pour la carte CYD d'AquaLook
(ESP32-2432S028) ; broches écran et tactile dans `include/config.h`.

## Port série

Demander le port COM avant toute commande qui en dépend ; utiliser
`<PORT_COM>` tant qu'il n'est pas confirmé ; `pio device list` pour le
trouver. Le port confirmé vaut pour la session.

## Chaîne courante

```powershell
git -c core.whitespace=cr-at-eol diff --check
pio run -e HAThermostat_banc -t upload --upload-port <PORT_COM>
pio device monitor -p <PORT_COM> -b 115200
```

- `upload` compile avant de téléverser ; en cas d'échec, rien n'est écrit.
- Sans téléversement prévu : `pio run -e HAThermostat`.
- `git diff --check` simple signale à tort les fins de ligne CRLF : utiliser
  `-c core.whitespace=cr-at-eol`.
- Fermer le moniteur avant un téléversement.

## Vérification du binaire exécuté

La bannière série du boot affiche version, environnement, build, SHA et
branche (`BuildInfo`). Un SHA suffixé `+modif` signale un binaire compilé
avec des sources non commitées : il ne vaut pas validation.

## Compte rendu de test

Consigner : profil flashé, port, point d'entrée exécuté, matériel testé,
résultat attendu, résultat observé, tests non effectués.
