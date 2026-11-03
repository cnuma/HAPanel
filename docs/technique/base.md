# packages/base.yaml

## Rôle

Le socle commun à tous les modules : nom du nœud, type de puce, Wi-Fi, connexion
chiffrée à Home Assistant, mise à jour à distance (OTA), journaux et identité de build.

Sans ce fichier, le module ne démarre pas sur le réseau : pas de Wi-Fi, pas de Home
Assistant, pas de mise à jour à distance. Il ne contient aucune fonction de l'écran.

## Dépendances

- **Utilise :** les substitutions de `hapanel.yaml` (`node_name`, `friendly_name`,
  `version`, `git_sha`, `log_level`) et trois valeurs de `secrets.yaml` (`wifi_ssid`,
  `wifi_password`, `api_encryption_key`), hors de Git (G9).
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

### Bloc `esp32`

| Clé | Valeur | Rôle |
|---|---|---|
| `board` | `esp32dev` | ESP32 classique, sans PSRAM (D004). |
| `flash_size` | `4MB` | Taille de la mémoire flash de la carte. |
| `framework.type` | `esp-idf` | Cadre logiciel d'Espressif, plus léger que celui d'Arduino (D008). |
| `framework.advanced.minimum_chip_revision` | `"3.1"` | La puce du panneau est en révision 3.1 : le compilateur retire le code de contournement des anciennes révisions, le binaire est plus petit (D011). |

### Blocs `wifi`, `api`, `ota`

| Bloc | Clé | Valeur | Rôle |
|---|---|---|---|
| `wifi` | `ssid`, `password` | `!secret` | Réseau Wi-Fi, lu dans `secrets.yaml`. |
| `api` | `encryption.key` | `!secret api_encryption_key` | Connexion à Home Assistant toujours chiffrée. La même clé est saisie dans Home Assistant à l'ajout du module. |
| `ota` | `platform` | `esphome` | Mise à jour par le réseau. |
| `ota` | `encryption:` | vide | **Volontairement vide** : l'OTA reprend la clé de l'API (D010). Ne pas supprimer : sans ce bloc, l'OTA ne serait plus protégée. |

`pages/accueil.yaml` ajoute `on_connect` et `on_disconnect` au bloc `wifi` pour
l'écran « HA déconnecté » (D015).

### Bloc `logger`

| Clé | Valeur | Rôle |
|---|---|---|
| `level` | `${log_level}` | `INFO` en production, `DEBUG` sur le banc (`hapanel_banc.yaml`). |

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
| Changer de réseau Wi-Fi | Modifier `secrets.yaml`, recompiler, téléverser **par USB** : le module ne joindra plus l'ancien réseau pour une OTA. |
| Changer la clé de l'API | Modifier `secrets.yaml`, téléverser, puis ressaisir la clé dans Home Assistant (ESPHome › module › Reconfigurer). L'OTA suivante utilise la nouvelle clé (D010). |
| Mesurer le Wi-Fi plus souvent | `update_interval` de `signal_wifi`. Plus court : plus de messages vers Home Assistant. |
| Ajouter une entité de diagnostic | Ici si elle concerne le module entier, avec `entity_category: diagnostic`. Son `name` devient stable (G10). |

**Pièges :**
- Changer `name_add_mac_suffix` ou `node_name` change le nom de tous les modules dans
  Home Assistant : tableaux de bord et automatisations perdent leurs entités (G10).
- `minimum_chip_revision: "3.1"` : un binaire compilé ainsi ne démarre pas sur une puce
  plus ancienne. Vérifier la révision d'une nouvelle carte dans le premier téléversement
  par USB (ligne `Chip is …`, qui donne la révision).
- Aucun mot de passe ni clé en clair ici, même provisoire (G9).

**Contrôle après modification :** `.\tools\build.ps1 config`, puis `compile` ; après
téléversement, vérifier la ligne `hapanel.build` des journaux et l'entité « Version ».
