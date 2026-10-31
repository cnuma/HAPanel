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

## D010 — OTA authentifiée par la clé de l'API

- Date : 28 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : ESPHome 2026.10 signale à chaque compilation que le mot de
  passe OTA « gaspille flash et RAM » et recommande le chiffrement de l'OTA
  par la clé de l'API (protocole Noise, comme l'API).
- Décision : `ota: encryption:` sans clé propre, qui hérite de
  `api_encryption_key` ; plus de mot de passe OTA. Migration en deux
  installations : la première avec `password` et
  `encryption: allow_plaintext_upload: true` (au cas où le firmware en place
  demanderait encore le mot de passe), la seconde sans les deux, qui prouve
  que l'OTA chiffrée fonctionne. Constaté le 28 octobre 2026 : le firmware
  en place proposait déjà le chiffrement par la clé de l'API, la première
  installation était donc déjà chiffrée.
- Options écartées : garder le mot de passe (avertissement permanent, coût
  mémoire) ; laisser `allow_plaintext_upload` (un tiers sur le réseau pourrait
  forcer une installation en clair).
- Conséquences : un seul secret protège l'API et l'OTA ; `ota_password`
  disparaît de `secrets.example.yaml` ; perdre la clé de l'API impose un
  flash par USB.

## D011 — Options avancées de l'ESP32

- Date : 28 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : au démarrage, ESPHome propose `minimum_chip_revision: "3.1"`,
  `flash_chip: generic` et `sram1_as_iram: true`.
- Décision : `minimum_chip_revision: "3.1"` (puce du panneau en révision
  3.1) ; `flash_chip` et `sram1_as_iram` reportés.
- Justification : la révision réduit le binaire sans contrepartie pour ce
  panneau ; les deux autres options libèrent de l'IRAM (mémoire de code),
  qui ne manque pas, et `sram1_as_iram` prélève probablement de la mémoire
  de données utile à LVGL (G6, R2), sans compter qu'elle exige un chargeur
  compatible que l'OTA ne met pas à jour.
- Conséquences : une carte de rechange de révision inférieure à 3.1 ne
  démarrerait pas ce binaire ; à réévaluer si l'IRAM vient à manquer.

## D012 — Firmware unique, entités choisies dans Home Assistant

- Date : 28 octobre 2026 — Statut : accepté (choix du propriétaire), en
  prototype ; remplace D008 pour le nom du nœud
- Contexte : le propriétaire veut déployer plusieurs modules sans
  recompiler pour chacun ; ESPHome fixe à la compilation les entités lues
  par les plateformes `homeassistant`.
- Décision :
  - un seul binaire pour tous les modules : `name_add_mac_suffix: true`,
    nœud `hapanel-xxxxxx` (suffixe tiré de l'adresse MAC) ;
  - le panneau ne connaît aucune entité : un blueprint de Home Assistant
    (`blueprints/automation/hapanel/`, versionné ici) lui pousse des valeurs
    par clé avec l'action `maj_valeur(cle, valeur)` ; à chaque connexion de
    Home Assistant, le panneau émet l'événement
    `esphome.hapanel_demande_valeurs` et le blueprint renvoie tout ;
  - les commandes du panneau passeront par des événements traités par le
    blueprint (à concevoir avec l'écran d'accueil) ;
  - une clé d'API commune à tous les modules (choix du propriétaire), en
    gardant la possibilité d'une clé par module (R8).
- Options étudiées : paramètres de compilation (une compilation par
  module) ; réglages du module lus par le panneau avec abonnement dynamique
  (`subscribe_home_assistant_state`), qui gardait P2 à P4 sur le panneau
  mais reposait sur du C++ interne à ESPHome.
- Garde-fous côté panneau (P2, P3) : valeur effacée à la déconnexion de
  Home Assistant, « indisponible » si l'état reçu n'est pas un nombre,
  « périmée » sans nouvelle valeur pendant 15 minutes (le blueprint renvoie
  tout toutes les 5 minutes).
- Conséquences :
  - le panneau actuel est renommé et doit être réadopté dans Home Assistant ;
    ses entités changent de nom (G10, aucune n'était utilisée) ;
  - une partie de la logique vit dans Home Assistant : le blueprint est
    une pièce du produit, versionnée et testée avec le firmware ;
  - la règle « lecture par plateformes `homeassistant` » de
    `04_DEVELOPMENT_RULES.md` est remplacée.

## D013 — Connexion à Home Assistant identifiée par le nom du client

- Date : 28 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : l'indicateur de connexion utilisait
  `api.connected: state_subscription_only: true`. Au banc, `esphome logs`
  (2026.10) s'abonne aussi aux états : avec les journaux ouverts, l'écran
  restait « connecté » alors que Home Assistant était déconnecté (P2 violé).
- Décision : seul un client API dont le nom commence par « Home Assistant »
  (nom envoyé par Home Assistant à la connexion, par exemple
  `Home Assistant 2026.9.4`) compte comme connecté ; courte lambda sur
  `api::global_api_server->active_clients()` et `get_name()`.
- Conséquences : dépend de fonctions internes d'ESPHome (R5) : une
  évolution casserait la compilation, sans erreur silencieuse ; si Home
  Assistant changeait de nom de client, l'écran afficherait « non connecté »
  à tort, dans le sens prudent. Le constat « client de journaux non compté
  comme connecté » du checkpoint `6567c6f` ne valait que pour les journaux
  série.

## D014 — Écran d'accueil et commandes par événement

- Date : 29 octobre 2026 — Statut : accepté (choix du propriétaire)
- Contexte : spécification proposée au checkpoint `96227cf` ; trois
  questions ouvertes tranchées par le propriétaire le 29 octobre 2026.
- Décision :
  - disposition : bandeau (date et heure de HA en français, 24 h, `--:--`
    avant synchronisation ; barres Wi-Fi ; point de connexion HA), séjour en
    grand, chauffage (mode et activité, préréglage, « Manuel » si consigne
    libre), consigne − / + au pas de 0,5 °C, bouton Allumer / Couper, barre
    de navigation commune (Accueil, `i` pour « À propos ») ; l'accueil est
    la page de démarrage ;
  - **mode par glissière à deux positions** (« Éteint » à gauche,
    « Chauffage » à droite) : une pastille orange couvre le mode réel ;
    glisser le doigt d'au moins un tiers de la glissière vers l'autre côté,
    depuis n'importe quel point de la glissière, envoie l'autre mode ; un
    simple toucher ne fait rien (protection contre les frôlements d'un
    panneau mural).
    Choix du propriétaire au banc le 29 octobre 2026, qui remplace l'appui
    long d'abord retenu (libellé « Maintenir : couper » jugé peu clair) ;
    widget sur mesure, le curseur LVGL sautant à l'endroit touché ;
  - **préréglages en icônes** (ajout du propriétaire au banc le
    29 octobre 2026) : Manuel, Hors-gel, Éco, Confort, Boost, icônes
    Material Design de Home Assistant ; le préréglage réel est entouré
    d'orange ; appui simple ; **grisés quand le chauffage est éteint** ;
    commande `chauffage_prereglage` (`none`, `frost`, `eco`, `comfort`,
    `boost`) traduite en `climate.set_preset_mode` si le thermostat
    connaît ce préréglage, est allumé et non verrouillé ; la ligne texte
    « Préréglage » disparaît ;
  - ligne « Chauffage : … » supprimée en fonctionnement normal (redondante
    avec la glissière, demande du propriétaire) ; elle n'apparaît, en
    orange, que pour « non reçu », « périmé » ou « indisponible » (P3) ;
    l'activité (chauffe / attente) n'est plus affichée ;
  - barre de navigation en icônes : maison (Material Design) et « i » ;
    boutons − en bleu et + en rouge ;
  - bornes de consigne par défaut **15 à 25 °C**, entrées du blueprint,
    resserrées aux bornes du thermostat ;
  - blueprint dédié `blueprints/automation/hapanel/ecran_accueil.yaml`
    (panneau, thermomètre, thermostat, bornes) ; clés `temperature`,
    `chauffage_mode`, `chauffage_action`, `chauffage_consigne`,
    `chauffage_prereglage`, `chauffage_verrou`, `consigne_min`,
    `consigne_max` ;
  - commandes : événement `esphome.hapanel_commande` (`commande` =
    `chauffage_mode` avec `valeur` heat / off, ou `chauffage_consigne` avec
    une valeur en °C), traduit par le blueprint en `climate.set_hvac_mode` et
    `climate.set_temperature`.
- Garde-fous (P2, P4), contrôlés deux fois :
  - panneau : boutons grisés et aucun envoi si HA déconnecté, chauffage non
    reçu ou périmé, mode inconnu, thermostat verrouillé ou bornes absentes ;
    consigne envoyée 2 s après le dernier appui, affichée en orange jusqu'à
    confirmation, retour à la valeur réelle après 10 s sans confirmation ;
    même attente de 10 s pour le mode (pastille orange atténuée du côté
    demandé) ; pas de pastille si le mode est inconnu, pastille grise si le
    thermostat est verrouillé ;
  - blueprint : commande ignorée si elle ne vient pas de ce panneau, si le
    thermostat n'est pas en `heat` / `off`, s'il est verrouillé ou si la
    consigne sort des bornes ; refus inscrit au journal système de HA.
- Conséquences : l'automatisation `temperature` du blueprint
  `envoyer_valeur` fait doublon et est à désactiver ; une seule clé de
  péremption par groupe (température, chauffage) ; nouvelle surface
  (événement de commande) au registre `08`.

## D015 — Accueil allégé : chauffage éteint et HA déconnecté

- Date : 30 octobre 2026 — Statut : accepté (choix du propriétaire),
  spécifié, non implémenté
- Contexte : idées P3 du propriétaire (30 octobre 2026) et retour du test
  « HA déconnecté » au banc : les valeurs effacées et les commandes grisées
  chargent l'écran sans dire clairement ce qui se passe.
- Décision, chauffage éteint :
  - condition : HA connecté, chauffage reçu, mode réel `off`, ou envoi de
    `off` en attente de confirmation ;
  - **préréglages, −, + et consigne masqués** (pas seulement grisés) ;
    restent la température du séjour, la glissière et la navigation ;
  - **consigne non réglable chauffage éteint** : on la règle après avoir
    rallumé (remplace le comportement D014, où − / + restaient actifs) ;
    le blueprint refuse aussi `chauffage_consigne` si le thermostat est
    `off` (double contrôle, comme les préréglages) ;
  - aucun widget restant ne change de position (la glissière reste sous
    le doigt) ; au rallumage, tout réapparaît avec les valeurs réelles ;
  - un état de chauffage inconnu (« non reçu », « périmé »,
    « indisponible ») garde le comportement D014.
- Décision, HA déconnecté (`ha_connecte_affiche` ≠ 1) :
  - **le bandeau reste** (heure, barres Wi-Fi, point rouge) ainsi que la
    barre de navigation (P5) ; tout le reste de l'accueil est remplacé par
    une icône et un message centrés ;
  - **message selon la cause** : « Pas de Wi-Fi » si le Wi-Fi n'est pas
    connecté, sinon « Pas de communication avec Home Assistant » ;
    icônes Material Design (`mdi:wifi-off`, `mdi:lan-disconnect`, glyphes
    ajoutés à `police_icones`) ;
  - affiché dès la coupure, sans temporisation (P2) ; prioritaire sur
    l'affichage « chauffage éteint » ; au retour de HA, l'écran normal
    revient et les valeurs arrivent par le renvoi existant (D012).
- Garde-fous inchangés : aucune commande sans HA ni sur état inconnu (P2,
  P4) ; les widgets masqués sont aussi désactivés.
- Conséquences : `packages/pages/accueil.yaml` (script
  `accueil_rafraichir`, conteneurs à masquer, message), `packages/lvgl.yaml`
  (deux glyphes), blueprint `ecran_accueil.yaml` (refus de consigne
  chauffage éteint) ; mémoire à mesurer (G6) ; aucun identifiant existant
  renommé (G10).
- Complément du 31 octobre 2026 : refus de `chauffage_consigne` thermostat
  `off` côté blueprint confirmé par le propriétaire. L'écran HA déconnecté
  s'applique dès le démarrage (rafraîchissement à `on_boot`) et le message
  suit les changements de Wi-Fi (`on_connect`, `on_disconnect`).
