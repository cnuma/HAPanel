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
  `esp32-s3-template` peut porter le socle commun.

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
