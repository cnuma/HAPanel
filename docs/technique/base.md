# packages/base.yaml

## Rôle

Le socle commun à tous les modules : nom du nœud, type de puce, journaux, écriture
des réglages en flash et identité de build. Il ne contient aucune fonction de l'écran
et **aucun accès au réseau** : le Wi-Fi, la clé de l'API et l'OTA sont dans
`acces_prive.yaml` (secrets compilés, `hapanel.yaml`) ou `acces_public.yaml`
(saisis à l'installation, `hapanel_public.yaml`), D039.

## Dépendances

- **Utilise :** les substitutions de `hapanel.yaml` (`node_name`, `friendly_name`,
  `version`, `git_sha`, `log_level`). Aucun secret (G9).
- **Inclus par :** `application.yaml`, commun à `hapanel.yaml` et `hapanel_public.yaml`.
- **Fournit :**
  - `signal_wifi`, complété par `pages/accueil.yaml` (`!extend`) pour l'icône Wi-Fi ;
  - `identite_build`, l'entité « Version » dans Home Assistant.

## Bloc par bloc

### Bloc `esphome`

| Clé | Valeur | Rôle |
|---|---|---|
| `name` | `${node_name}` | Nom du nœud (`hapanel`). |
| `friendly_name` | `${friendly_name}` | Nom de l'appareil dans Home Assistant. |
| `name_add_mac_suffix` | `true` | Ajoute la fin de l'adresse MAC : `hapanel-a85bfc`. Un seul binaire pour tous les modules, chacun avec un nom unique (D012). |
| `project.name` | `cnuma.hapanel` | Identité du projet, visible dans Home Assistant et dans les journaux. |
| `project.version` | `${version}` | Version du fichier `VERSION`, injectée par `tools/build.ps1` (G5). |

**`on_boot`** (priorité `-100`, c'est-à-dire tard, une fois les composants prêts) :

1. publie `"${version} (${git_sha})"` dans `identite_build` ;
2. écrit `HAPanel <version> (<sha>)` dans les journaux, tag `hapanel.build`, niveau
   `INFO` : c'est la première ligne à chercher pour savoir ce qui tourne sur un module.

`pages/accueil.yaml` ajoute son propre `on_boot` : ESPHome exécute les deux.

### Puce : hors de ce fichier (D048)

Le bloc `esp32` est dans le fichier matériel de chaque carte : ESP32 pour la S024C et la
S028 ([hardware.md](hardware.md)), ESP32-S3 pour la Guition JC4827W543
([hardware_jc4827w543.md](hardware_jc4827w543.md)).

### Wi-Fi, API et OTA : hors de ce fichier (D039)

| Fichier | Wi-Fi | Clé de l'API | OTA |
|---|---|---|---|
| `acces_prive.yaml` | `ssid`, `password` : `!secret` | `encryption.key: !secret api_encryption_key` ; la même clé est saisie dans HA | `esphome` (depuis le PC), `encryption:` **volontairement vide** : reprend la clé de l'API (D010) ; ne pas supprimer |
| `acces_public.yaml` | saisi à l'installation : Improv par USB, ou point d'accès et portail captif | `encryption: {}` sans clé : reçue de HA à l'adoption, gardée en flash | `http_request` seulement, lancée par l'entité « Firmware » ; pas d'OTA depuis un PC (ESPHome l'accepterait sans clé) |

`pages/accueil.yaml` ajoute `on_connect` et `on_disconnect` au bloc `wifi` pour
l'écran « HA déconnecté » (D015).

### Bloc `logger`

| Clé | Valeur | Rôle |
|---|---|---|
| `level` | `${log_level}` | `INFO` en production, `DEBUG` sur le banc (`hapanel_banc.yaml`). |

### Bloc `preferences`

| Clé | Valeur | Rôle |
|---|---|---|
| `flash_write_interval` | `5s` | Délai avant l'écriture en flash des réglages gardés (`restore_value`, `RESTORE_DEFAULT_ON` : « LED », « Intensité LED », « Intensité écran », « Alerte LED », « Message d'accueil »). 60 s par défaut : une coupure d'alimentation avant ce délai perdait le réglage (C2, D034). Seules les valeurs changées sont écrites (G3). |

### Bloc `sensor`

| id | Type | Nom dans HA | Rôle |
|---|---|---|---|
| `signal_wifi` | `wifi_signal` | Signal Wi-Fi (diagnostic) | Force du signal en dBm, mesurée toutes les 60 s (`update_interval`). Lu par `pages/accueil.yaml` (script `accueil_wifi`) pour choisir l'icône Wi-Fi. |

### Bloc `text_sensor`

| id | Type | Nom dans HA | Rôle |
|---|---|---|---|
| `identite_build` | `template` | Version (diagnostic) | Version et SHA du binaire, par exemple `0.6.0-dev (d41de4a)`. Publié une seule fois, au démarrage (`update_interval: never`). |

## Maintenance

| Pour | Faire |
|---|---|
| Changer de réseau Wi-Fi | Module privé : modifier `secrets.yaml`, recompiler, téléverser **par USB** : le module ne joindra plus l'ancien réseau pour une OTA. Module public : `docs/DEPLOIEMENT_PUBLIC.md` § 5. |
| Changer la clé de l'API | Modifier `secrets.yaml`, téléverser, puis ressaisir la clé dans Home Assistant (ESPHome › module › Reconfigurer). L'OTA suivante utilise la nouvelle clé (D010). |
| Changer le délai d'écriture des réglages | `flash_write_interval`. Plus court : moins de perte à la coupure, mais jamais sous 1 s (usure de la flash, G3). |
| Mesurer le Wi-Fi plus souvent | `update_interval` de `signal_wifi`. Plus court : plus de messages vers Home Assistant. |
| Ajouter une entité de diagnostic | Ici si elle concerne le module entier, avec `entity_category: diagnostic`. Son `name` devient stable (G10). |

**Pièges :**
- Changer `name_add_mac_suffix` ou `node_name` change le nom de tous les modules dans
  Home Assistant : tableaux de bord et automatisations perdent leurs entités (G10).
- `minimum_chip_revision: "3.1"` (fichiers matériels des cartes ESP32) : un binaire
  compilé ainsi ne démarre pas sur une puce plus ancienne. Vérifier la révision d'une nouvelle carte dans le premier téléversement
  par USB (ligne `Chip is …`, qui donne la révision).
- Aucun mot de passe ni clé en clair ici, même provisoire (G9).

**Contrôle après modification :** `.\tools\build.ps1 config`, puis `compile` ; après
téléversement, vérifier la ligne `hapanel.build` des journaux et l'entité « Version ».
