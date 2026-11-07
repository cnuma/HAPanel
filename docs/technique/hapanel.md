# Configurations de tête : hapanel.yaml, hapanel_banc.yaml, hapanel_public.yaml, hapanel_2432s028_banc.yaml et hapanel_2432s028_public.yaml

## Rôle

Ce sont les points d'entrée qu'on donne à ESPHome. Ils ne contiennent aucune
fonction : ils **assemblent** les packages, choisissent la carte et fixent les
substitutions communes.

| Fichier | Sert à | Flashé sur |
|---|---|---|
| `hapanel.yaml` | Configuration de production | Les modules de la maison |
| `hapanel_banc.yaml` | Production plus outils de mise au point | Le panneau de banc |
| `hapanel_public.yaml` | Mêmes fonctions, sans aucun secret, publiable (D039, maquette) | Les modules installés depuis GitHub |
| `hapanel_2432s028_banc.yaml` | Banc sur carte ESP32-2432S028 | Une carte S028 de l'atelier |
| `hapanel_2432s028_public.yaml` | Binaire public de la carte ESP32-2432S028 (D041) | Les modules S028 installés depuis GitHub |

**Un fichier matériel par carte :** chaque point d'entrée inclut le sien
(`hardware.yaml` pour l'ESP32-2432S024C, `hardware_2432s028.yaml` pour la S028).
`application.yaml` ne contient aucune broche.

Sans `hapanel.yaml`, il n'y a rien à compiler. `hapanel_banc.yaml` n'existe que pour
le banc : il n'est jamais flashé sur un module de la maison.

## Dépendances

- **Utilise :** un fichier matériel, `packages/application.yaml`, qui inclut les 11
  fichiers de fonctions, et un fichier d'accès : `acces_prive.yaml` (lit `secrets.yaml`) pour `hapanel.yaml`,
  `acces_public.yaml` pour `hapanel_public.yaml`.
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

| Package | Fichier | Rôle |
|---|---|---|
| `hardware` | `packages/hardware.yaml` | Carte ESP32-2432S024C (D004) : broches, bus, écran, tactile |
| `application` | `packages/application.yaml` | Toutes les fonctions du panneau, communes au binaire public |
| `acces` | `packages/acces_prive.yaml` | Wi-Fi, clé de l'API et OTA depuis le PC, compilés depuis `secrets.yaml` |

`application.yaml` inclut à son tour chaque fichier de fonction. **L'ordre compte** :

| Ordre | Package | Contrainte d'ordre |
|---|---|---|
| 1 | `base` | |
| 2 | `accueil` | **Première page déclarée : c'est l'écran affiché au démarrage.** Doit rester avant `lvgl`. |
| 3 à 7 | `meteo`, `planning`, `scenarios`, `menu`, `reglages` | Leur ordre est celui des pages dans LVGL. |
| 8 | `lvgl` | Déclare la page À propos et la barre de navigation (`top_layer`). |
| 9 | `liaison_ha` | |
| 10 | `led_veille` | |
| 11 | `message_accueil` | **Après `lvgl`** : son calque est ajouté après la barre de navigation dans `top_layer`, donc dessiné par-dessus. |

## hapanel_public.yaml

Maquette D039, procédure dans `docs/DEPLOIEMENT_PUBLIC.md`.

| Bloc | Contenu | Rôle |
|---|---|---|
| `substitutions` | Celles de `hapanel.yaml`, plus `source_mise_a_jour` | Adresse du manifeste de la dernière Release du dépôt public, lue par l'entité « Firmware ». |
| `packages` | `hardware`, `application`, puis `acces: acces_public.yaml` | Même carte et mêmes fonctions ; accès sans secret. |
| `esphome.build_path` | `build/hapanel_public` | Même nom de nœud que la production : sans dossier propre, les deux compilations s'écraseraient. |

Compilé par GitHub Actions (`.github/workflows/publication.yml`) à l'envoi d'une
étiquette `v<version>` ; localement : `.\tools\build.ps1 compile -Config hapanel_public.yaml`.

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

## hapanel_2432s028_banc.yaml

Banc sur carte ESP32-2432S028 (validé le 7 novembre 2026, cahier K). Il n'inclut pas `hapanel.yaml`, qui
apporte la carte S024C : il reprend ses substitutions et assemble lui-même
`hardware: hardware_2432s028.yaml`, `application` et `acces: acces_prive.yaml`.

| Bloc | Contenu | Rôle |
|---|---|---|
| `substitutions` | Celles de `hapanel.yaml`, `log_level` à `DEBUG` | Comme le banc. |
| `esphome.build_path` | `build/hapanel_2432s028` | Dossier de compilation propre à cette carte. |
| `debug`, `banc_memoire_libre`, `banc_plus_grand_bloc` | Comme `hapanel_banc.yaml` | Mémoire mesurée (G6). |
| `touchscreen` (`!extend tactile`) | Journal `toucher x=… y=… brut x=… y=…` | Les valeurs brutes servent au calibrage du tactile résistif (`hardware_2432s028.md`). |

## hapanel_2432s028_public.yaml

Binaire public de la carte ESP32-2432S028 (D041) : même contenu que
`hapanel_public.yaml`, autre fichier matériel et autre manifeste.

| Bloc | Contenu | Rôle |
|---|---|---|
| `substitutions` | Celles de `hapanel_public.yaml` ; `source_mise_a_jour` vise `manifest-2432s028.json` | Un module S028 ne reçoit jamais le binaire de la S024C. |
| `packages` | `hardware: hardware_2432s028.yaml`, `application`, `acces: acces_public.yaml` | |
| `esphome.build_path` | `build/hapanel_2432s028_public` | Dossier de compilation propre. |

Publié par `.github/workflows/publication.yml` avec la configuration de la S024C.

## Maintenance

| Pour | Faire |
|---|---|
| Ajouter un fichier de fonction | L'ajouter dans `packages:` de `packages/application.yaml`, à la bonne place (voir l'ordre) ; ajouter sa ligne dans `tools/generer_schemas_architecture.py` (matrice) et sa page ici. |
| Ajouter un écran | Package dans `packages/pages/`, inclus **avant** `lvgl`. |
| Changer l'écran de démarrage | Mettre son package en premier parmi les pages. |
| Ajouter un outil de mise au point | Dans `hapanel_banc.yaml` uniquement : la production reste inchangée. |
| Ajouter une carte | Fichier matériel `packages/hardware_<carte>.yaml` avec les mêmes `id`, configurations de banc et publique, ligne dans `publier` de `.github/workflows/publication.yml`, page dans `docs/technique/`, tests au cahier (D041). |
| Changer la version | Modifier le fichier `VERSION`, jamais `version` ici (G5). |

**Pièges :**
- Une compilation sans `tools/build.ps1` affiche `0.0.0-non-injectee` : toujours passer
  par le script.
- Un SHA suivi de `+modif` ne vaut pas validation : committer avant de compiler un
  binaire à tester.
- Deux packages qui déclarent le même `id` font échouer `esphome config`.

**Contrôle après modification :** `.\tools\build.ps1 config`, puis `compile`, pour les
trois fichiers.
