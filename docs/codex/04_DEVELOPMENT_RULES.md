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
- Les broches et réglages matériels vivent uniquement dans
  `packages/hardware.yaml`, sous forme de substitutions, relevés sur la carte
  réelle et jamais supposés.
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

- Lecture d'une entité : plateformes `homeassistant` (sensor, text_sensor,
  binary_sensor) ; mise à jour de l'affichage sur `on_value`, pas par
  interrogation périodique.
- Commande : action `homeassistant.action`, uniquement si l'API est
  connectée et l'état de départ connu (P2, P4).
- L'autorisation « actions Home Assistant » du panneau est activée dans
  l'intégration ESPHome de Home Assistant et consignée comme surface dans
  `08_RISKS_AND_DEBT.md`.
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

## Sécurité

- `api:` avec clé de chiffrement dans `secrets.yaml` ; `ota:` chiffrée par
  la même clé (`encryption:` sans clé propre, D010), sans mot de passe ni
  `allow_plaintext_upload`.
- Pas de `web_server` ni de point d'accès de secours sans décision et ligne
  au registre des risques.

## Journaux

- Niveau `INFO` en production, `DEBUG` sur le banc.
- Tags explicites dans les lambdas (`ESP_LOGI("hapanel.page", …)`) ; messages
  courts et actionnables, sans secret.

## Encodage

- UTF-8 sans BOM ; indentation YAML à deux espaces, sans tabulation.
- Accents et emoji vérifiés à l'écran : une police LVGL ne contient que les
  glyphes déclarés.
