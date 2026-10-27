# 02 — Décisions

Format : contexte, décision, options étudiées, justification, conséquences,
date, statut (proposé, accepté, remplacé, abandonné). Une décision acceptée
ne se modifie pas en silence : elle est remplacée par une nouvelle décision
qui cite la précédente.

## D001 — Socle de règles repris d'AquaLook

- Date : 27 octobre 2026 — Statut : accepté
- Contexte : AquaLook (`cnuma/AquaLook`, mis en pause le 27 octobre 2026)
  dispose d'un corpus de règles ESP32 éprouvé. HAThermostat doit en hériter
  sans dépendre d'AquaLook ni interférer avec lui.
- Décision : les règles génériques sont copiées et versionnées dans ce dépôt
  (`AGENTS.md`, `docs/codex/`, `tools/version_build.py`,
  `include/BuildInfo.h`) ; les règles propres à AquaLook (relais, zones,
  LittleFS, carte SD, LCD, cloud AlwaysData, OTA) sont exclues. L'origine
  exacte est tracée dans `SOCLE_MANIFEST.md`.
- Options écartées : import d'un fichier de règles commun hors dépôt
  (`~/.claude/…`), car il contredit la règle « le dépôt est la seule source
  de vérité » et n'est pas disponible dans une session hors du PC du
  propriétaire ; lecture du dépôt AquaLook à chaque session, car elle crée
  un couplage entre les deux projets.
- Conséquence : une amélioration d'une règle générique dans un projet doit
  être reportée manuellement dans l'autre. À terme, un dépôt modèle
  `esp32-template` peut porter le socle commun.

## D002 — PlatformIO et framework Arduino

- Date : 27 octobre 2026 — Statut : proposé
- Décision proposée : PlatformIO, framework Arduino, plateforme
  `espressif32` à version figée, comme AquaLook.
- Point de remise en cause : si l'intégration Home Assistant retenue est
  ESPHome, le firmware devient majoritairement déclaratif (YAML) et une
  grande partie des règles C++ du socle devient sans objet. À trancher avant
  le premier code.

## D003 — Dépôt de travail hors dossier synchronisé

- Date : 27 octobre 2026 — Statut : accepté
- Décision : la copie de travail est `C:\Users\Emman\00_DevClaude\HAThermostat`,
  hors OneDrive. GitHub assure la sauvegarde.
- Justification : un dossier synchronisé verrouille des fichiers de `.git` et
  `.pio` pendant la compilation et peut créer des conflits qui corrompent
  l'historique.

## D004 — Carte ESP32-2432S024 au lieu d'un ESP32-S3

- Date : 27 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : le projet était prévu sur ESP32-S3 comme AquaLook ; le
  thermostat demande une carte plus petite.
- Décision : carte ESP32-2432S024 (écran tactile 2,4", 240 × 320), à base
  d'ESP32 classique (module WROOM, double cœur), sans PSRAM.
- Conséquences :
  - la cible n'est plus un ESP32-S3 : les règles propres au S3 du socle
    (USB natif, `--dtr 1`, PSRAM OPI) sont retirées ; les environnements
    s'appellent `HAThermostat` et `HAThermostat_banc` ;
  - sans PSRAM, la marge mémoire devient la contrainte de conception
    principale (invariant G6), en particulier pour TLS et l'affichage ;
  - l'expérience AquaLook sur la carte CYD voisine (ESP32-2432S028) est
    directement réutilisable : `board = esp32dev`, bus tactile séparé,
    budget mémoire sans PSRAM ;
  - GPIO libres limités : capteur et étage de sortie se choisissent après
    relevé des connecteurs.
- Points ouverts : variante tactile (`R`, `C` ou `N`), contrôleur d'écran
  (ILI9341 ou ST7789 selon la série), taille de flash.
