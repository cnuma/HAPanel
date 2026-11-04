# hapanel.yaml et hapanel_banc.yaml

## Rôle

Ce sont les deux points d'entrée qu'on donne à ESPHome. Ils ne contiennent aucune
fonction : ils **assemblent** les packages et fixent les substitutions communes.

| Fichier | Sert à | Flashé sur |
|---|---|---|
| `hapanel.yaml` | Configuration de production | Les modules de la maison |
| `hapanel_banc.yaml` | Production plus outils de mise au point | Le panneau de banc |

Sans `hapanel.yaml`, il n'y a rien à compiler. `hapanel_banc.yaml` n'existe que pour
le banc : il n'est jamais flashé sur un module de la maison.

## Dépendances

- **Utilise :** les 11 fichiers de `packages/`, et `secrets.yaml` à travers
  `base.yaml`.
- **Fournit :** les substitutions ci-dessous à tous les packages.
- **Outil :** `tools/build.ps1` remplace `version` et `git_sha` au lancement (G5).

## hapanel.yaml

### Bloc `substitutions`

| Substitution | Valeur | Utilisée par | Rôle |
|---|---|---|---|
| `node_name` | `hapanel` | `base.yaml` (`esphome.name`) | Nom du nœud ESPHome. ESPHome y ajoute la fin de l'adresse MAC : `hapanel-a85bfc` (D012). |
| `friendly_name` | `HAPanel` | `base.yaml` | Nom de l'appareil affiché dans Home Assistant. |
| `version` | `0.0.0-non-injectee` | `base.yaml`, `lvgl.yaml` (page À propos) | Version du logiciel. Remplacée par le contenu du fichier `VERSION`. |
| `git_sha` | `inconnu` | `base.yaml`, `lvgl.yaml` | Commit compilé. Remplacé par le SHA court de Git, suivi de `+modif` si des fichiers ne sont pas commités. |
| `log_level` | `INFO` | `base.yaml` (`logger.level`) | Niveau des journaux. |

Les valeurs `0.0.0-non-injectee` et `inconnu` ne doivent jamais apparaître sur un
module : elles signalent une compilation lancée sans `tools/build.ps1`. Une
substitution déclarée ici **prime** sur la même substitution d'un package.

### Bloc `packages`

Chaque ligne fusionne un fichier dans la configuration. **L'ordre compte** :

| Ordre | Package | Contrainte d'ordre |
|---|---|---|
| 1 | `base` | |
| 2 | `hardware` | |
| 3 | `accueil` | **Première page déclarée : c'est l'écran affiché au démarrage.** Doit rester avant `lvgl`. |
| 4 à 8 | `meteo`, `planning`, `scenarios`, `menu`, `reglages` | Leur ordre est celui des pages dans LVGL. |
| 9 | `lvgl` | Déclare la page À propos et la barre de navigation (`top_layer`). |
| 10 | `liaison_ha` | |
| 11 | `led_veille` | |
| 12 | `message_accueil` | **Après `lvgl`** : son calque est ajouté après la barre de navigation dans `top_layer`, donc dessiné par-dessus. |

## hapanel_banc.yaml

### Bloc `substitutions`

| Substitution | Valeur | Rôle |
|---|---|---|
| `log_level` | `DEBUG` | Journaux détaillés sur le banc. Prime sur le `INFO` de `hapanel.yaml`. |

### Bloc `packages`

Un seul package, `production`, qui inclut `hapanel.yaml` entier : le banc exécute
exactement le logiciel de production, avec quelques ajouts.

### Bloc `esphome`

| Clé | Valeur | Rôle |
|---|---|---|
| `build_path` | `build/hapanel_banc` | Dossier de compilation propre au banc, `.esphome/build/hapanel_banc` : ESPHome compte ce chemin depuis `.esphome`. Sans lui, banc et production partagent `.esphome/build/hapanel`, et passer de l'un à l'autre recompile tout (environ 10 min). Coût : environ 430 Mo de plus sur le disque. |

### Bloc `debug` et capteurs de mémoire

Le composant `debug` d'ESPHome mesure la mémoire toutes les 30 s (`update_interval`).

| id | Type | Nom dans HA | Rôle |
|---|---|---|---|
| `banc_memoire_libre` | `sensor` (`debug`, `free`) | Mémoire libre | Mémoire vive libre, en octets. |
| `banc_plus_grand_bloc` | `sensor` (`debug`, `block`) | Plus grand bloc libre | Plus grande zone libre d'un seul tenant : LVGL en a besoin pour ses tampons. |

Ces deux valeurs sont relevées à chaque palier et consignées au checkpoint (G6). La
page À propos les affiche aussi, sur tous les modules, sans le composant `debug`.

### Bloc `touchscreen` (`!extend tactile`)

Complète l'écran tactile `tactile`, déclaré dans `hardware.yaml`, sans modifier ce
fichier : chaque toucher est journalisé (`hapanel.banc`, coordonnées `x` et `y`). Sert
à vérifier que le tactile correspond à l'écran : coin haut gauche vers 0,0, coin bas
droit vers 240,320.

## Maintenance

| Pour | Faire |
|---|---|
| Ajouter un fichier de fonction | L'ajouter dans `packages:` de `hapanel.yaml`, à la bonne place (voir l'ordre) ; ajouter sa ligne dans `tools/generer_schemas_architecture.py` (matrice) et sa page ici. |
| Ajouter un écran | Package dans `packages/pages/`, inclus **avant** `lvgl`. |
| Changer l'écran de démarrage | Mettre son package en premier parmi les pages. |
| Ajouter un outil de mise au point | Dans `hapanel_banc.yaml` uniquement : la production reste inchangée. |
| Changer la version | Modifier le fichier `VERSION`, jamais `version` ici (G5). |

**Pièges :**
- Une compilation sans `tools/build.ps1` affiche `0.0.0-non-injectee` : toujours passer
  par le script.
- Un SHA suivi de `+modif` ne vaut pas validation : committer avant de compiler un
  binaire à tester.
- Deux packages qui déclarent le même `id` font échouer `esphome config`.

**Contrôle après modification :** `.\tools\build.ps1 config`, puis `compile`, pour les
deux fichiers.
