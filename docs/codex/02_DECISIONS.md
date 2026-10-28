# 02 — Décisions

Format : contexte, décision, options étudiées, justification, conséquences,
date, statut (proposé, accepté, remplacé, abandonné). Une décision acceptée
ne se modifie pas en silence : elle est remplacée par une nouvelle décision
qui cite la précédente.

## D001 — Socle de règles repris d'AquaLook

- Date : 27 octobre 2026 — Statut : accepté
- Contexte : AquaLook (`cnuma/AquaLook`, mis en pause le 27 octobre 2026)
  dispose d'un corpus de règles ESP32 éprouvé. Le projet doit en hériter
  sans dépendre d'AquaLook ni interférer avec lui.
- Décision : les règles de méthode sont copiées et versionnées dans ce dépôt
  (`AGENTS.md`, `docs/codex/`) ; les règles propres à AquaLook (relais,
  zones, LittleFS, carte SD, LCD, cloud AlwaysData, OTA) sont exclues.
  L'origine exacte est tracée dans `SOCLE_MANIFEST.md`.
- Options écartées : import d'un fichier de règles commun hors dépôt
  (`~/.claude/…`), car il contredit la règle « le dépôt est la seule source
  de vérité » et n'est pas disponible dans une session hors du PC du
  propriétaire ; lecture du dépôt AquaLook à chaque session, car elle crée
  un couplage entre les deux projets.
- Conséquence : une amélioration d'une règle de méthode dans un projet doit
  être reportée manuellement dans l'autre.
- Complément du 27 octobre 2026 : avec D005, les règles C++ et l'outillage
  PlatformIO du socle (`tools/version_build.py`, `include/BuildInfo.h`) sont
  retirés ; les règles de méthode restent (gouvernance, anti-régression,
  Git, checkpoint, validation des artefacts, impacts d'abord).

## D002 — PlatformIO et framework Arduino

- Date : 27 octobre 2026 — Statut : **remplacé par D005**
- Décision proposée initialement : PlatformIO, framework Arduino, comme
  AquaLook. Abandonnée avec le choix d'ESPHome.

## D003 — Dépôt de travail hors dossier synchronisé

- Date : 27 octobre 2026 — Statut : accepté
- Décision : la copie de travail est `C:\Users\Emman\00_DevClaude\HAPanel`,
  hors OneDrive. GitHub assure la sauvegarde.
- Justification : un dossier synchronisé verrouille des fichiers de `.git` et
  des répertoires de compilation et peut créer des conflits qui corrompent
  l'historique.

## D004 — Carte ESP32-2432S024C

- Date : 27 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : le projet était prévu sur ESP32-S3 comme AquaLook ; le panneau
  demande une carte plus petite.
- Décision : carte ESP32-2432S024, variante `C` (tactile capacitif CST820),
  écran 2,4" 240 × 320, ESP32 classique (module WROOM, double cœur), sans
  PSRAM.
- Conséquences :
  - sans PSRAM, la mémoire est la contrainte de conception principale
    (invariant G6), en particulier pour le tampon d'affichage LVGL et le
    nombre d'écrans ;
  - le tactile CST820 passe par le composant ESPHome `cst816`, annoncé
    compatible sans garantie : premier essai sur banc avant tout écran.
- Point ouvert : contrôleur d'écran (ILI9341 ou ST7789 selon la série),
  taille de flash.

## D005 — ESPHome en ligne de commande, version figée

- Date : 27 octobre 2026 — Statut : accepté (remplace D002)
- Contexte : HAPanel est un panneau qui lit et commande des entités de Home
  Assistant (D007).
- Décision : configuration ESPHome en YAML, versionnée dans ce dépôt,
  compilée avec la ligne de commande ESPHome installée dans un environnement
  Python du dépôt, à version figée dans `requirements.txt` (2026.10.1 au
  27 octobre 2026). Interface graphique avec le composant LVGL d'ESPHome.
- Options étudiées :
  - firmware C++ avec MQTT : indépendant de Home Assistant, maîtrise totale,
    réutilise le socle C++ d'AquaLook ; écarté car la lecture des entités de
    Home Assistant, les commandes, l'interface, l'OTA et le chiffrement
    seraient à reconstruire ;
  - YAML édités dans l'outil ESPHome de Home Assistant : écarté, les
    fichiers vivraient hors de Git.
- Conséquences :
  - lien fort avec Home Assistant, assumé (D007) ;
  - logique complexe limitée à des lambdas courtes ou, si nécessaire, à un
    composant externe local documenté ;
  - la version ESPHome se change par décision, avec test complet ;
  - identité de build par substitutions (`version`, `git_sha`) depuis
    `VERSION` et Git.

## D006 — Projet renommé HAPanel

- Date : 27 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : le projet n'est plus un thermostat mais un panneau maison
  multi-écrans ; l'ancien nom `HAThermostat` (dépôt `cnuma/HAthermostat`)
  ne décrit plus le produit.
- Décision : produit, dépôt (`cnuma/HAPanel`) et dossier de travail
  renommés `HAPanel` avant toute configuration, quand le coût est nul.
- Conséquence : l'ancien nom n'apparaît plus que dans l'historique Git et
  dans cette décision.

## D007 — Tout passe par Home Assistant

- Date : 27 octobre 2026 — Statut : accepté (choix du propriétaire)
- Décision : le panneau ne pilote jamais directement un appareil ; il lit des
  entités et appelle des actions de Home Assistant.
- Conséquences :
  - aucune sortie de commande sur la carte : les invariants de sécurité
    d'actionneur prévus pour le thermostat sont abandonnés ;
  - sans Home Assistant, le panneau reste navigable mais n'envoie aucune
    commande et l'affiche (invariant P2).

## D008 — Nœud `hapanel` et framework `esp-idf`

- Date : 27 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : le nom du nœud ESPHome est un contrat (G10) et le framework doit
  être fixé explicitement (`04_DEVELOPMENT_RULES.md`).
- Décision : nœud `hapanel` (un seul panneau prévu) ; framework `esp-idf`.
- Options écartées : `hapanel-<pièce>`, utile seulement avec plusieurs
  panneaux ; `arduino`, qu'aucun composant n'exige et qui produit un binaire
  plus gros, alors que la carte n'a pas de PSRAM.
- Conséquences : les entités Home Assistant sont préfixées `hapanel_` ; un
  second panneau imposera une nouvelle décision et un renommage de celui-ci ;
  changer de framework impose un re-flash par USB.

## D009 — Tactile lu périodiquement, sans interruption

- Date : 28 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : au banc, la puce CST820 répond sur le bus I²C mais aucune
  interruption n'arrive sur GPIO21 (broche publiée) ; avec `interrupt_pin`,
  ESPHome n'interroge plus la puce et aucun toucher n'est reçu.
- Décision : `interrupt_pin` n'est pas déclarée ; le tactile est lu toutes
  les 50 ms (`update_interval`).
- Option écartée : rechercher la cause (résistance de rappel, autre broche,
  mode de la puce) : plusieurs flashs pour un gain pratique nul sur un
  panneau alimenté en permanence.
- Conséquences : une transaction I²C toutes les 50 ms, latence de toucher
  d'au plus 50 ms ; dette T1 ; à reprendre si la veille profonde devient
  nécessaire.
