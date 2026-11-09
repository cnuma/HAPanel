# 04 — Règles de développement

Règles ESPHome du projet. Les principes de méthode viennent du socle AquaLook
(`docs/codex/04_DEVELOPMENT_RULES.md` et `docs/developer/DEV-005`), transposés
du C++ au YAML.

## Organisation des fichiers

- `hapanel.yaml` : configuration de production, limitée à l'assemblage des
  packages et aux substitutions.
- `hapanel_banc.yaml` : même configuration plus les outils de mise au point
  (composant `debug`, journaux plus bavards) ; c'est elle qu'on flashe sur
  le panneau de banc.
- `packages/` : un fichier par domaine (`base.yaml` pour Wi-Fi, API, OTA et
  journaux ; `hardware.yaml` pour écran, tactile, bus et broches ;
  `lvgl.yaml` pour le socle graphique ; `pages/<écran>.yaml` pour chaque
  écran).
- Les broches et réglages matériels vivent uniquement dans le fichier
  matériel de la carte (`packages/hardware.yaml` pour l'ESP32-2432S024C,
  `packages/hardware_2432s028.yaml` pour la S028), sous forme de
  substitutions, relevés sur la carte réelle et jamais supposés. Chaque
  configuration de tête inclut un seul fichier matériel ; tous déclarent les
  mêmes `id`.
- `secrets.yaml` (ignoré) et `secrets.example.yaml` (versionné, sans valeur
  réelle).

## YAML

- Une responsabilité par package ; pas de duplication d'un bloc entre
  packages.
- Chaque composant porte un `id` explicite et stable (G10).
- Les noms d'entités exposées sont en français, courts, sans le nom du
  panneau (Home Assistant le préfixe).
- Le framework ESP32 (`esp-idf` ou `arduino`) est fixé explicitement dans le
  YAML, jamais laissé au défaut d'une version d'ESPHome.

## Lambdas et code C++

- Lambdas courtes, sans attente, sans allocation répétée, sans `std::string`
  volumineux dans un chemin fréquent (G1).
- Toujours tester `has_state()` et `isnan()` avant d'utiliser une valeur
  (P3, P4).
- Une logique qui dépasse quelques lignes passe dans un `script` ESPHome ;
  au-delà, dans un composant externe local documenté par une décision.

## Home Assistant

- Aucun `entity_id` dans le firmware (D012) : les valeurs arrivent par
  l'action `maj_valeur(cle, valeur)`, poussée par un blueprint de
  `blueprints/automation/hapanel/` ; chaque clé a un garde-fou
  « indisponible », « périmée » et un effacement à la déconnexion (P3).
- Commande : événement `esphome.hapanel_commande` (D014) traité par le
  blueprint, uniquement si l'API est connectée et l'état de départ connu
  (P2, P4) ; le blueprint refait ces contrôles avant d'agir.
- Un écran redessine ses widgets dans un seul script de rafraîchissement
  (`accueil_rafraichir`), appelé à chaque valeur reçue, changement de
  connexion ou péremption, qui calcule aussi les commandes autorisées.
- Toute clé ou tout événement ajouté est documenté dans le blueprint et dans
  `00_CONTEXT.md`, dans le même lot que le firmware.
- Le panneau ne passe que par des événements (`homeassistant.event`), qui ne
  demandent pas l'autorisation « actions Home Assistant » de l'intégration
  ESPHome (testé le 2 novembre 2026). Toute action HA appelée directement par le
  firmware (`homeassistant.action`) l'exigerait : décision et ligne au `08`.
- Chaque entité lue ou action appelée est inscrite dans le tableau des
  écrans de `00_CONTEXT.md`.

## LVGL et mémoire (carte sans PSRAM)

- `buffer_size` fixé explicitement ; la documentation ESPHome recommande
  25 % sans PSRAM (environ 38 Ko en 240 × 320). Une valeur explicite n'a pas
  de repli : un échec d'allocation met LVGL en échec, à vérifier dans les
  journaux.
- Polices : seulement les tailles et glyphes utilisés ; images
  redimensionnées à leur taille d'affichage.
- Un écran = un package ; mesurer la mémoire libre et le plus grand bloc
  libre avant et après chaque ajout d'écran (G6).
- Mise à jour des widgets sur événement ; pas de rafraîchissement global
  périodique.
- Un `label` dont le texte change et qui n'est pas aligné à gauche porte
  une largeur fixe et un `text_align` : créé vide avec une largeur au
  contenu, il s'élargit sans se recaler, hors de l'écran (constaté le
  30 octobre 2026, corrigé en 0.2.1).

## Sécurité

- `api:` avec clé de chiffrement dans `secrets.yaml` ; `ota:` chiffrée par
  la même clé (`encryption:` sans clé propre, D010), sans mot de passe ni
  `allow_plaintext_upload`.
- Pas de `web_server` ni de point d'accès de secours sans décision et ligne
  au registre des risques.

## Documentation publique

- Pages pour l'utilisateur (README, `INSTALLATION.md`, `CONFIGURATION.md`,
  `UTILISATION.md`, `ARCHITECTURE.md`, `docs/technique/`) : aucun nom réel de
  module, de pièce, de réseau ni de chemin du poste du propriétaire (D052) ;
  nom de module d'exemple : `hapanel-1a2b3c`. Captures : masquer aussi le suffixe
  du nom du module (`09_PIEGES.md`, G9).
- Le journal de développement (`docs/codex/`, cahier, TODO, checkpoints) peut citer
  l'installation réelle ; il ne contient jamais de secret, d'adresse IP ni de port
  COM (G9).
- Documentation en français seulement (D052).

## Journaux

- Niveau `INFO` en production, `DEBUG` sur le banc.
- Tags explicites dans les lambdas (`ESP_LOGI("hapanel.page", …)`) ; messages
  courts et actionnables, sans secret.

## Encodage

- UTF-8 sans BOM ; indentation YAML à deux espaces, sans tabulation.
- Accents et emoji vérifiés à l'écran : une police LVGL ne contient que les
  glyphes déclarés.
