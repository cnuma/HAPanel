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
- Révision du 3 novembre 2026 (retour du propriétaire : il faut laisser le doigt
  sur l'écran, contraire aux habitudes des téléphones) : lecture toutes les
  20 ms et bus I²C à 400 kHz (50 kHz par défaut). À valider sur le module.

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
  implémenté en 0.3.0, validé à l'écran le 31 octobre 2026
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

## D016 — Glissière au toucher, température extérieure, icônes en couleur

- Date : 31 octobre 2026 — Statut : accepté (choix du propriétaire),
  implémenté en 0.4.0, validé au banc le 31 octobre 2026 ; complète D014
- Contexte : glissière jugée peu lisible comme curseur ; souhait d'afficher la
  température extérieure avec un capteur modifiable depuis HA ; préréglages à
  distinguer par couleur.
- Décision :
  - **glissière :** toucher le côté inactif envoie l'autre mode ; le
    glissement reste possible. Remplace « un simple toucher ne fait rien » de
    D014 : un frôlement peut changer le mode, risque accepté (visible et
    réversible) ;
  - **température extérieure :** ligne « Extérieur 12,3 °C » sous le séjour ;
    clé `temperature_exterieure`, entrée obligatoire du blueprint
    (`thermometre_exterieur`, D012) ; « indisponible », « périmée », « non
    reçue » et effacement à la déconnexion (P3) ; la ligne du chauffage en
    anomalie prend sa place ;
  - **icônes :** Manuel violet, Hors-gel bleu, Éco vert, Confort orange, Boost
    rouge, en permanence (grises si interdites) ; préréglage réel à bord blanc
    épais, bord gris pendant l'attente de confirmation. Remplace le marquage
    orange de D014.
- Conséquence : après réimport du blueprint, l'entrée doit être renseignée
  dans l'automatisation, sinon le panneau n'est plus alimenté (signalé par P3).

## D017 — LED de face avant et écran éteint par inactivité

- Date : 31 octobre 2026 — Statut : accepté (choix du propriétaire),
  implémenté en 0.5.0, validé au banc le 31 octobre 2026
- Relevé au banc : LED RVB allumée à l'état bas, GPIO4 rouge, GPIO16 vert,
  GPIO17 bleu. Trois canaux à fond : violet, le vert étant dominé ; orange
  obtenu avec rouge 10 % et vert 100 %, blanc avec rouge 10 %, vert 100 %,
  bleu 20 %.
- Décision, LED :
  - chauffage allumé, état normal : couleur du préréglage (D016) ; chauffage
    éteint : éteinte ; préréglage inconnu : blanc ;
  - valeur non reçue, périmée ou indisponible, ou HA déconnecté : rouge
    clignotant (seul le clignotement le distingue de Boost).
- Décision, écran :
  - extinction après 60 s sans toucher, délai réglable à la compilation ;
  - le premier toucher ne fait que rallumer l'écran, sans commande (P4) ;
  - HA déconnecté : l'écran se rallume avec son message (P2).
- Conséquence : écran éteint, la LED porte seule l'état visible (P2).
  Réveil au relâchement du doigt (`resume_on_input: false`) : LVGL en pause
  ignore le toucher.

## D018 — Respiration de la LED selon la lumière de la pièce

- Date : 31 octobre 2026 — Statut : demandé par le propriétaire, implémenté
  en 0.6.0-dev ; respiration, intensité en pièce éclairée et orange de Confort
  validés à l'œil par le propriétaire le 31 octobre 2026 ; **pièce sombre,
  alerte face à Boost et blanc non testés**.
- Décision :
  - état normal, chauffage allumé : respiration de 6 s, de 0 (LED éteinte au
    creux) au plafond ; un même facteur sur les trois canaux conserve les
    mélanges de D017 ;
  - plafond : 25 % pièce éclairée, 5 % pièce sombre, interpolé selon la LDR
    (0,09 à 0,20 V, moyenne sur 5 s depuis le 3 novembre 2026, D023), multiplié par le réglage « Intensité
    LED » (D027, 20 % par défaut : 5 % et 1 %) ; sans mesure, plafond de jour ;
  - révision du 2 novembre 2026 (retour du propriétaire : respiration trop
    haute) : le maximum devient l'ancien niveau bas (20 % de 25 % et de 5 %)
    et le plancher passe de 20 % à 0 ; ce n'est plus la LED qui montre que
    le chauffage est allumé quand elle est au creux, l'alerte reste un
    clignotement franc ;
  - alerte inchangée (D017) : rouge clignotant franc à pleine intensité, qui la
    distingue de Boost, rouge respirant et atténué ;
  - chauffage éteint : LED éteinte, inchangé ;
  - orange de Confort corrigé (retour du propriétaire : trop proche du vert
    d'Éco, qui reste vert) : rouge 10 % → 30 %, vert 100 %, validé à l'œil par le propriétaire le
    31 octobre 2026.
- Limite : d'après le relevé du 31 octobre 2026, la LDR distingue au mieux une
  pièce sombre d'une pièce éclairée, pas les niveaux intermédiaires. La mesure
  n'alimente pas Home Assistant ; elle paraît dans les journaux de banc
  (`hapanel.led`).
- À vérifier au banc : influence du rétroéclairage et de la LED sur la LDR.

## D019 — Écran météo, localisation portée par Home Assistant

- Date : 1er novembre 2026 — Statut : demandé par le propriétaire, implémenté
  et validé par le propriétaire le 1er novembre 2026 (« tout marche ») ; états
  dégradés non confirmés séparément (`docs/TODO.md`).
- Décision :
  - le panneau ne connaît ni la position de la maison ni aucun service météo
    (D007, D012) : le blueprint (`module.yaml`, D021) lit l'entité
    `weather.*` choisie à l'import, qui doit suivre la localisation de Home
    Assistant ;
  - contenu : condition et température actuelles, puis pour 3 jours le jour, la
    condition, la maximale et la minimale ; troisième bouton dans la barre de
    navigation ; aucune commande ;
  - clés `meteo_condition`, `meteo_temperature`, `meteo_jN_jour`,
    `meteo_jN_condition`, `meteo_jN_max`, `meteo_jN_min` (N de 1 à 3). Elles
    sont traitées à part dans `maj_valeur` : une clé inconnue de la liste du
    chauffage y rafraîchirait sinon la date de réception du chauffage (P3) ;
  - « non reçue », « indisponible », « périmée » (15 min, sur tout le groupe)
    et « HA non connecté » affichés sur la page, valeurs effacées (P2, P3) ;
  - une panne de la météo ne déclenche pas l'alerte de la LED, réservée au
    chauffage et aux températures (D017).
- Limite : températures affichées avec « ° » seul, dans l'unité de l'entité.

## D020 — Écran planning d'après les calendriers de Home Assistant

- Date : 1er novembre 2026 — Statut : demandé par le propriétaire, implémenté
  et validé par le propriétaire le 1er novembre 2026 (« tout marche ») ; états
  dégradés non confirmés séparément (`docs/TODO.md`).
- Contexte : le chauffage est programmé par des calendriers HA, un par zone
  (maison, cuisine, baignoire, douche) ; les événements commencent au quart
  d'heure (06:15) et peuvent se chevaucher.
- Décision :
  - le blueprint (`module.yaml`, D021) lit de 1 à 4 entités
    `calendar.*` choisies à l'import ; consultation seule, jour courant ;
  - **disposition « résumé + frise »**, choisie par le propriétaire sur maquette
    le 1er novembre 2026 : pour le premier calendrier, « Prévu jusqu'à 22:00 » ou
    « Prochain à 17:00 » et une frise de 24 h avec repère de l'heure ; pour les
    suivants, une ligne avec le créneau en cours ou le suivant. « Prévu » et non
    « En marche » : le calendrier ne dit pas ce que fait le chauffage ;
  - **précision au quart d'heure**, pas à l'heure : 06:15 à 07:30 serait faux
    sur 24 segments. Un événement qui commence ou finit en cours de quart
    d'heure occupe tout ce quart d'heure ;
  - **marche ou arrêt seulement**, en orange : un calendrier ne porte ni
    préréglage ni consigne, et la variante à la couleur du préréglage est
    abandonnée. Le titre des événements n'est pas affiché ;
  - clés `plan_N_nom` et `plan_N_creneaux` (N de 1 à 4). Créneaux : « h » puis
    24 chiffres hexadécimaux ; le préfixe empêche Home Assistant de lire un
    nombre. `maj_valeur` accepte désormais 31 caractères ;
  - « non reçu », « périmé » (15 min) et « HA non connecté » pour la page,
    « indisponible » par calendrier (P2, P3) ; pas d'alerte de la LED ;
  - barre de navigation à 4 boutons de 55 px, à valider au doigt.
- Limites : la page montre le calendrier, pas l'état réel du chauffage. Jour de
  changement d'heure : bande calculée sur 24 h, décalée après le changement.

## D021 — Un seul blueprint par module

- Date : 1er novembre 2026 — Statut : accepté (choix du propriétaire), validé
  dans Home Assistant par le propriétaire le 1er novembre 2026 ; remplace
  `ecran_accueil.yaml` (D014), retiré du dépôt.
- Contexte : 5 modules prévus ; un blueprint par page imposerait 15
  automatisations.
- Décision : `blueprints/automation/hapanel/module.yaml` alimente toutes les
  pages, avec une automatisation par module. Ajouter une page modifie ce
  blueprint. Les commandes de D014 et D015 sont reprises sans changement.
  Un changement de météo ou de calendrier n'envoie que les valeurs de sa page ;
  l'envoi périodique, le démarrage de HA et la demande du panneau envoient tout.
- Conséquence : l'automatisation créée depuis `ecran_accueil.yaml` doit être
  supprimée dès la création de la nouvelle, sinon chaque commande de chauffage
  s'exécute deux fois.

## D022 — Retour à l'accueil après une minute sans toucher

- Date : 1er novembre 2026 — Statut : accepté (demande du propriétaire), validé
  par lui le 1er novembre 2026, cas sans HA non confirmé.
- Décision : après `veille_delai_ms` (60 s, le délai de D017) sans toucher,
  toute autre page cède la place à l'accueil, juste avant l'extinction. Sans
  HA, l'écran reste allumé (D017) et le retour a lieu quand même.
- Le retour n'envoie aucune commande (P1). Ni écran éteint ni navigation
  n'interrompent la réception des valeurs.

## D023 — Rétroéclairage selon la lumière de la pièce

- Date : 1er novembre 2026 — Statut : demandé par le propriétaire, niveaux
  choisis par l'agent, à ajuster et tester sur le module.
- Décision :
  - la LDR donne une obscurité de 0 à 1 (0,09 à 0,20 V, D018), commune à la LED
    et au rétroéclairage, recalculée toutes les 10 s sur la moyenne de 1 min (2 s et 5 s depuis la
    révision ci-dessous) ;
  - luminosité : 100 % pièce éclairée, 40 % pièce sombre (avant correction
    gamma), interpolée ; transition de 2 s, seulement à partir de 5 points d'écart ;
  - écran éteint : le niveau est appliqué au réveil, sans rallumer l'écran ;
  - sans mesure de la LDR : pleine luminosité, écran lisible. Aucune dépendance
    à Home Assistant.
- Révision du 3 novembre 2026 (retour du propriétaire : l'écran baissait trop
  lentement en éteignant une chambre) : moyenne sur 5 s publiée toutes les 2 s,
  obscurité recalculée toutes les 2 s, transition de 1 s ; l'écart minimal de
  5 points reste le seul rempart contre un écran qui varie sans cesse. Validée par
  le propriétaire (cahier H15) et fusionnée le 4 novembre 2026.
- Limite : si l'écran éclaire la LDR, baisser sa luminosité assombrit la mesure
  et accentue la baisse. Effet borné par `retro_nuit`, à vérifier au banc, comme
  la pièce sombre, jamais testée.

## D024 — Écran scénarios, choisis dans le blueprint du module

- Date : 1er novembre 2026 — Statut : demandé par le propriétaire, validé par lui sur
  le module le 1er novembre 2026, états dégradés non confirmés ; nombre de boutons et disposition choisis par l'agent.
- Décision :
  - jusqu'à 6 scènes, scripts ou automatisations, un champ et un nom facultatif par bouton dans le blueprint
    `module.yaml`. Grille de 2 boutons sur 3 lignes, au nom saisi, sinon à celui de
    l'entité (24 caractères au plus) ;
  - le panneau envoie `scenario` et un numéro par `esphome.hapanel_commande` :
    seul le blueprint connaît les entités et il refuse tout numéro hors liste ou
    entité indisponible ;
  - le panneau affiche ce qui est vrai : « Envoi en cours », puis « Lancé » ou
    « Refusé par HA » selon la clé `scen_resultat`, ou « Pas de réponse de HA »
    après 10 s. Pas de second lancement pendant l'attente. « Lancé » signifie que
    HA a accepté l'action, pas que le scénario a abouti ;
  - HA déconnecté, noms non reçus ou périmés (15 min) : aucune commande (P2, P4) ;
  - accès par la page Menu (D025).
- Limites : les noms et la disponibilité sont renvoyés toutes les 5 min et à la
  connexion, pas à chaque changement. Une automatisation est lancée sans ses
  conditions (`automation.trigger`). Un seul toucher suffit : pas de confirmation.

## D025 — Page Menu et barre de navigation à deux boutons

- Date : 1er novembre 2026 — Statut : choix du propriétaire (option B), validé par lui
  sur le module le 1er novembre 2026 ; remplace la barre à une icône par page (D014, D019, D020).
- Contexte : avec les scénarios, 5 boutons de 43 px, jugés trop petits.
- Décision : barre avec Accueil (68 px) et Menu (160 px). La page Menu donne accès
  à toutes les pages par de grandes tuiles, avec une place libre. L'accueil reste
  à un toucher, les autres pages à deux. Navigation sans HA ni Wi-Fi (P5) ; retour
  à l'accueil après 1 min depuis le Menu aussi (D022).
- Révision du 2 novembre 2026 (retour du propriétaire : les utilisateurs ne
  comprennent pas un bouton qui ne réagit pas) : le bouton Accueil est masqué
  sur la page d'accueil ; seul Menu reste, à sa place.
- Révision du 3 novembre 2026 (demande du propriétaire, même raison) : le bouton
  Menu est masqué sur la page Menu ; seul Accueil reste, à sa place. Après essai,
  la tuile Accueil du Menu, doublon de ce bouton, est retirée ; les cinq tuiles
  restantes remontent. Validée par le propriétaire (cahier H2, H3) et fusionnée le
  4 novembre 2026.
- Révision du 4 novembre 2026 (D036) : le bouton Menu passe dans la barre d'état en
  haut (☰) ; le bouton Accueil est centré en bas, et l'accueil n'a plus de barre du
  bas.

## D026 — Icône et couleur des boutons de scénarios

- Date : 1er novembre 2026 — Statut : choix du propriétaire (couleurs en liste,
  option A), fusionné à sa demande le 1er novembre 2026 ; rendu de chaque icône et couleur non confirmé séparément.
- Décision :
  - chaque scénario du blueprint gagne une liste « Icône » (facultative) et une liste
    « Couleur » (bleu par défaut), clés `scen_N_icone` et `scen_N_couleur` ;
  - 25 icônes compilées (toutes celles de HA ne tiendraient pas en flash, G6) et
    8 couleurs lisibles avec un texte blanc ;
  - icône au-dessus du nom, limité alors à 2 lignes ; bouton inactif en gris quelle
    que soit sa couleur.
- Ajouter une icône ou une couleur modifie le blueprint et
  `packages/pages/scenarios.yaml`, puis demande de reflasher le module.

## D027 — Réglages de la LED par module, dans HA et dans le blueprint

- Date : 2 novembre 2026 — Statut : demandé par le propriétaire (« A et B,
  alignés »), qui a choisi l'alerte réglable, le curseur et la règle
  d'alignement ; validé par le propriétaire (cahier C1 à C7) le 4 novembre 2026.
- Contexte : selon la pièce (une chambre), la LED doit pouvoir être atténuée ou
  éteinte, module par module, alors que le firmware est unique (D012).
- Décision :
  - trois entités de configuration du module, gardées en flash :
    « LED » (Respiration, Éteinte), « Intensité LED » (0 à 100 % par pas de 5,
    100 % = plafonds de D018, 20 % par défaut) et « Alerte LED » (activée par
    défaut) ;
  - alerte désactivée : plus de clignotement rouge, l'écran montre toujours le
    problème (bandeau, « non reçu », « indisponible »). Elle ne dépend pas du
    réglage « LED » ;
  - le blueprint propose les mêmes réglages, « Ne pas imposer » par défaut ; une
    valeur choisie est envoyée (clés `led_*`) à la connexion, au démarrage de HA
    et toutes les 5 min, et le module l'applique à ses entités ;
  - alignement : une valeur imposée par le blueprint l'emporte, un changement
    sur la page de l'appareil est remplacé sous 5 min ; écriture en flash
    seulement si la valeur change (G3).
- Conséquences : nouvelles entités exposées, à ne plus renommer (G10) ; surface
  inscrite au `08`.

## D028 — Message d'accueil à l'arrivée

- Date : 2 novembre 2026 — Statut : demandé par le propriétaire, qui a répondu
  aux questions de cadrage (TODO P4) ; validé par lui sur le module et dans HA le
  3 novembre 2026 (texte blanc et police du projet ajoutés au banc). Le saint du
  jour est reporté (source à choisir). Blueprint de la maison remplacé par une
  section du blueprint du module : D042.
- Contexte : quand quelqu'un arrive après une absence, les panneaux affichent un
  message selon la saison et l'heure, tiré d'une bibliothèque facile à modifier.
- Décision :
  - un blueprint de la maison, `message_accueil.yaml`, distinct de `module.yaml`
    (D021) : l'arrivée concerne toute la maison, un seul tirage pour tous les
    panneaux, un message unique coché une seule fois ;
  - déclencheurs choisis (contact, lumière, interrupteur), passage de « off » à
    « on » ; il faut que le déclencheur et tous les autres soient restés au repos
    pendant la période choisie (30 min par défaut), dans une plage horaire
    (6 h à 23 h par défaut) ;
  - bibliothèque : deux listes de tâches de HA. « Messages uniques » d'abord (la
    première tâche non cochée, cochée après l'envoi), sinon un message au hasard
    de « Messages » dont les mots de la description (saison, moment) conviennent ;
    sinon « Bonjour » ou « Bonsoir, bienvenue à la maison ! » ;
  - ligne de météo composée par HA (« Dehors : 12 °C, nuageux »), entité météo
    facultative ; le saint du jour viendra sur cette même ligne, sans changer le
    firmware ;
  - module : action `message_accueil(texte, infos)` (240 octets au plus par
    texte), plein écran par-dessus la barre de navigation, fermé par la croix
    en haut à droite (demande du propriétaire), par un toucher ailleurs ou après 3 min, écran allumé pendant l'affichage ; fermé à la déconnexion de
    HA pour que l'état de la liaison redevienne visible (P2) ;
  - LED en arc-en-ciel (un tour en 2 s) au plafond de D018 × « Intensité LED » ;
    rien si « LED » est sur Éteinte ; l'alerte rouge reste prioritaire (P2) ;
  - entité de configuration « Message d'accueil » (activée par défaut) : le module
    ignore le message si elle est désactivée, et le blueprint ne vise que les
    panneaux où elle est activée, donc connectés.
- Conséquences : nouvelle entité exposée (G10 : le blueprint la retrouve par son
  nom, `switch.*message_d_accueil`) ; surface inscrite au `08`. Après un
  redémarrage de HA, pas d'accueil avant la période choisie (dernier changement
  remis à zéro).

## D029 — Procédure d'installation versionnée dans chaque dépôt (invariant G11)

- Date : 3 novembre 2026 — Statut : demandé par le propriétaire (« il faut
  systématiquement ajouter dans Git la procédure pour installer les blueprints,
  quel que soit le dépôt ; à ajouter dans les invariants des projets »).
- Contexte : des procédures données seulement dans la conversation (activer
  l'entité « Last seen » de Z-Wave, importer un blueprint, remplir une liste de
  tâches) se perdent avec elle.
- Décision : invariant G11 (`03_INVARIANTS.md`). Tout blueprint ou élément à
  installer dans Home Assistant est livré avec sa procédure complète dans le
  dépôt, dans le même commit ; une explication donnée dans la conversation y est
  reportée. La règle vaut aussi pour les autres dépôts du propriétaire
  (cnuma/HASurveillance : `docs/INSTALLATION.md`).
- Conséquences : pour HAPanel, la procédure est `docs/CONFIGURATION.md` ; toute
  évolution d'un blueprint la met à jour dans le même lot.

## D030 — Moment de la mise à jour documentaire (invariant G12)

- Date : 3 novembre 2026 — Statut : validé par le propriétaire (HAP-R024).
- Contexte : un commit de branche précède les tests du propriétaire (G5 impose
  même de committer avant de compiler) ; l'état stable n'est atteint qu'à la
  validation sur le module et à la fusion dans `main`.
- Décision : invariant G12 (`03_INVARIANTS.md`), en deux temps :
  - documentation de fonctionnement, d'installation et d'utilisation : dans le
    même commit que la modification ; jamais regroupée après plusieurs commits ;
  - statut du projet (`TODO.md` « validé », `VERSION`, checkpoint) : après
    validation par le propriétaire, à la fusion dans `main`, éventuellement pour
    plusieurs fonctions à la fois.
  La règle vaut pour tous les dépôts du propriétaire.
- Conséquences : à tout commit, code et documentation concordent ; une branche
  abandonnée n'emporte que sa propre documentation ; `main` ne déclare stable
  que ce qui a été testé.

## D031 — Réglages à l'écran du module et intensité de l'écran

- Date : 3 novembre 2026 — Statut : choix du propriétaire (1A, 2A, 3A, 4A), validé
  par le propriétaire (cahier H) et fusionné le 4 novembre 2026 ; plancher et bornes
  choisis par l'agent (`retro_plancher` 0,30, intensité de 20 à 100 %).
- Contexte : le propriétaire avait demandé de régler la LED depuis le module ;
  D027 ne l'a fait que dans HA. Nouvelle demande : la luminosité de l'écran,
  réglable des deux côtés, HA et module.
- Décision :
  - page **Réglages**, ouverte par la tuile libre de la page Menu (D025), sans
    protection : « LED », « Intensité LED », « Alerte LED » (D027) et
    « Intensité écran » ; retour à l'accueil après 1 min comme les autres pages
    (D022), sans HA ni Wi-Fi (P5) ;
  - nouvelle entité de configuration « Intensité écran », gardée en flash (G3) :
    multiplie les deux niveaux de D023, l'adaptation à la pièce reste ; plancher à
    fixer au banc pour que l'écran reste lisible ; même réglage dans le
    blueprint « module », « Ne pas imposer » par défaut, comme D027 ;
  - un changement à l'écran met à jour l'entité dans HA, et inversement : une
    seule valeur, écrite en flash seulement si elle change (G3) ;
  - réglage imposé par le blueprint : cadenas devant la commande, qui ne réagit
    pas, et cadenas suivi de « imposé par HA » en bas de la page ; le blueprint
    envoie désormais chaque réglage, avec la valeur `libre` quand il ne l'impose
    pas (clés `led_*` et `ecran_intensite`) ;
  - révision après le premier essai (3 novembre 2026) : le gris seul se confondait
    avec un interrupteur à l'arrêt, d'où le cadenas ; interrupteur à l'arrêt sur
    fond sombre bordé, le bouton blanc sur gris clair étant peu lisible.

## D032 — Cahier de tests codé par fonction (invariant G13)

- Date : 4 novembre 2026 — Statut : demandé par le propriétaire (« toujours
  générer un cahier de tests qui permet un suivi de l'avancement et de ne pas en
  oublier, avec une codification selon les fonctions à tester »).
- Contexte : `docs/CAHIER_DE_TESTS.md`, créé le 3 novembre 2026, a permis de
  répondre par codes (« C1 ok, E1-E7 ok, H1-H9 ok ») et de savoir ce qui bloquait
  la fusion ; auparavant, des tests restaient « non confirmés » dans `TODO.md`.
- Décision : invariant G13 (`03_INVARIANTS.md`). Une partie par fonction, des codes
  stables jamais réattribués, action, attendu et case OK / KO datée, un tableau des
  résultats. Complément du même jour (demande du propriétaire) : une colonne
  « Bloque la fusion de » sur chaque test, avec le nom de la branche en
  référence, « (fusionnée) » après la fusion, « — » si le test ne bloque rien. Les tests d'une
  fonction entrent dans le cahier dans le même commit que son code (comme G12). La
  règle vaut pour tous les dépôts du propriétaire.
- Conséquences : à une fusion, les tests de la fonction sont OK ou explicitement
  reportés ; le checkpoint cite le cahier.

## D033 — Checkpoints courts, TODO priorisé, aucune adresse dans le dépôt (G14, G9)

- Date : 4 novembre 2026 — Statut : demandé par le propriétaire (« nouvelles règles
  pour la rédaction des checkpoints »).
- Contexte : chaque checkpoint recopiait l'identité du matériel, les pièges, la
  procédure de reprise et le reste à faire ; les pièges s'y accumulaient (« pièges des
  checkpoints précédents toujours valables ») et une information se perdait quand elle
  n'était pas recopiée. Les adresses IP de HA et du module y figuraient.
- Décision :
  - invariant **G14** : informations réutilisables d'abord dans leur fichier de
    référence ; nouveau `docs/codex/09_PIEGES.md`, qui rassemble les pièges des
    checkpoints ; procédure de reprise dans `START_HERE.md` ; checkpoint réduit à
    l'état variable, selon le modèle de `docs/checkpoints/README.md` ;
  - `docs/TODO.md` toujours utilisé, avec une colonne **Prio** qui ordonne les
    développements selon leurs dépendances (fusionner avant d'ouvrir un chantier,
    décider avant de coder, matériel avant code) ; les tests n'y figurent plus, ils
    sont dans le cahier (G13) ;
  - **G9** étendu : ni adresse IP, ni port COM, ni mot de passe, ni nom de réseau dans
    un fichier du dépôt ; adresses retirées des checkpoints existants.
  Les règles valent pour tous les dépôts du propriétaire.
- Limite : les adresses restent dans l'historique Git des commits passés. Ce sont des
  adresses de réseau local, non joignables depuis Internet ; réécrire l'historique de
  `main` demanderait l'accord du propriétaire et casserait les SHA cités partout.
- Conséquences : aucune sur le firmware ; méthode de travail seulement.

## D034 — Réglages écrits en flash sous 5 s

- Date : 4 novembre 2026 — Statut : corrige le test C2 (KO : « le module ne garde
  pas les paramètres LED et écran » après redémarrage) ; C2 OK, fusionné le 4 novembre 2026.
- Contexte : les réglages de D027 et D031 sont gardés en flash (`restore_value`),
  mais ESPHome n'écrit la flash qu'à l'intervalle `flash_write_interval`, 60 s par
  défaut. Le module n'a pas de bouton Redémarrer : un redémarrage est une coupure
  d'alimentation, qui perd tout réglage changé depuis moins de 60 s.
- Décision : `preferences: flash_write_interval: 5s` (`packages/base.yaml`).
- G3 respecté : ESPHome n'écrit que les valeurs changées (comparaison avec la
  flash) ; seules les entités réglées par l'utilisateur sont gardées (le
  rétroéclairage, `ALWAYS_ON`, n'écrit rien) ; un curseur déplacé donne au plus une
  écriture toutes les 5 s.
- Limite : une coupure moins de 5 s après le réglage le perd encore ; D035 le montre
  à l'écran.

## D035 — Icône d'enregistrement des réglages

- Date : 4 novembre 2026 — Statut : demandé par le propriétaire (« une petite icône
  juste au-dessus à droite du bouton menu qui s'affiche un temps bref pour confirmer
  l'enregistrement ») ; cahier H16 à H19 OK, fusionné le 4 novembre 2026. La barre
  d'état commune (TODO rang 1) lui donnera une place réservée.
- Décision :
  - disquette (`mdi:content-save`) au-dessus du bouton Menu, à droite, dans la couche
    commune à toutes les pages (`top_layer`, `packages/lvgl.yaml`) ;
  - script `enregistrement_signaler`, appelé à chaque changement d'un réglage gardé
    en flash (« LED », « Intensité LED », « Intensité écran », « Alerte LED »,
    « Message d'accueil »), d'où qu'il vienne : disquette grise, écriture forcée
    (`global_preferences->sync()`) 5 s après le dernier changement, disquette verte
    2 s, puis masquée. L'icône montre donc l'écriture réelle, pas une estimation ;
  - rien au démarrage, quand les entités relisent leur valeur en flash.
- Écartée : un message texte entre les pages et la barre du bas. La page Réglages
  occupe déjà cette bande (« imposé par HA »).
- G3 : au plus une écriture toutes les 5 s pendant une série de gestes, et seulement
  des valeurs changées ; `flash_write_interval: 5s` (D034) reste en secours.
- Révision du 4 novembre 2026 (D036) : la disquette passe dans la barre d'état ; elle
  ne passe plus par-dessus le contenu des pages.

## D036 — Barre d'état commune et navigation en haut

- Date : 4 novembre 2026 — Statut : proposé par le propriétaire (« une barre du haut
  comme sur un portable » ; « le burger de menu en haut dans la barre » ; « le home au
  milieu en bas ») ; choix A aux questions de HAP-R087 et HAP-R090 ; validé par le
  propriétaire (cahier I1 à I12) et fusionné le 4 novembre 2026, version 0.7.0.
- Contexte : seul l'accueil avait un bandeau (date, Wi-Fi, connexion) ; les autres
  pages avaient chacune leur titre, à des places différentes, et le Menu aucun. La
  disquette (D035) passait par-dessus le contenu quand on changeait vite de page.
- Décision :
  - barre de 36 px en haut de toutes les pages (`top_layer`, `packages/lvgl.yaml`) :
    à gauche le bouton Menu ☰ (sans fond, masqué sur le Menu ; zone tactile de 48 × 34 px plus 6 px autour, jugée trop petite à 40 × 32), puis le
    titre de la page (écrit par son `on_load`), ou la date et l'heure sur l'accueil ;
    à droite la disquette, le Wi-Fi et le point de connexion à HA (P2 sur toutes les
    pages, plus seulement l'accueil). Après essai, le ☰ passe de droite à gauche et
    perd son fond bleu, jugé disgracieux (retour du propriétaire) ;
  - barre du bas réduite au bouton Accueil, centré, 68 px ; masquée sur l'accueil,
    qui gagne 44 px ;
  - contenus des pages sous la barre (y ≥ 38) : titres retirés, tuiles du Menu et
    boutons des Scénarios un peu moins hauts, Météo resserrée ;
  - date de l'accueil sans le jour de la semaine (« 4 nov.  17:20 ») : avec, elle
    atteindrait 139 px et toucherait la disquette.
- Conséquences : identifiants internes renommés (`obj_barre_*`, `lbl_barre_date`,
  `ico_barre_enregistrement`) ; aucune entité de HA touchée (G10).
- Bords de l'écran : les 2 rangées de pixels du haut et du bas restent noires (barre
  à y = 2, barre du bas à 2 px du bord). Allumée, la dernière rangée réapparaissait
  par instants sur la première (ligne claire au redessin complet, point dans l'axe
  du bouton maison) ; diagnostic du 4 novembre 2026, idée du propriétaire (I11).
- Limite : sur un panneau mural, le ☰ en haut est un peu moins accessible qu'en bas
  (enfants) ; le Menu sert moins souvent que l'accueil.

## D037 — Mises à jour du parc depuis Home Assistant

- Date : 4 novembre 2026 — Statut : accepté, **révisé le 5 novembre 2026** (voir
  « Révision » en fin de décision) ; option C choisie par le propriétaire (HAP-R096).
- Contexte : le propriétaire prévoit plusieurs modules. Aujourd'hui chaque mise à
  jour part du PC, module par module (`build.ps1 upload`). Le binaire est le même pour
  tous (D012).
- Options étudiées :
  - A. script PC qui compile une fois et envoie l'OTA à chaque `hapanel-xxxxxx.local` :
    rien à changer au firmware, mais le PC est nécessaire et HA ne montre rien ;
  - B. module complémentaire ESPHome de HA : une compilation par module (longue avec
    LVGL sur un petit serveur), dépôt et secrets copiés dans HA, version d'ESPHome
    imposée par HA (R5) ;
  - C. mise à jour tirée par le module : une compilation, un binaire et un manifeste
    déposés sur un serveur local ; chaque module expose une entité de mise à jour
    (« 0.8.0 disponible », bouton Installer).
- Décision : option C.
  - Firmware : composant `http_request`, `ota: platform: http_request` et
    `update: platform: http_request` ; l'OTA native (D010) reste, pour le banc et en
    secours ;
  - adresse du manifeste dans `secrets.yaml` (G9), jamais dans le dépôt ;
  - publication : `build.ps1` produit le binaire de production et son manifeste
    (version, MD5) dans un dossier local ignoré par Git ; le propriétaire les copie
    vers l'hébergement ;
  - après chaque mise à jour, version et SHA relus dans HA (R7), comme aujourd'hui.
- Points à trancher avec le propriétaire avant le code :
  - hébergement : le binaire contient le mot de passe Wi-Fi et la clé de l'API, donc
    jamais de publication sur Internet (GitHub exclu). `/config/www` de HA est servi
    sans authentification sous `/local/` : acceptable seulement si HA n'est pas
    joignable depuis Internet, sinon un autre serveur du réseau local ;
  - installation : bouton seulement, ou automatisation de HA qui met tout le parc à
    jour ; fréquence de vérification du manifeste.
- À mesurer : mémoire libre pendant le téléchargement (G6, R2) ; place en flash (36 %
  libres dans la partition à 0.7.0) ; retour au binaire précédent si le nouveau ne
  démarre pas.
- Conséquences : nouvelle surface au `08` avant fusion : le module ne vérifie que
  l'intégrité (MD5), pas l'auteur ; quiconque peut écrire à l'emplacement du
  manifeste, ou se placer entre le module et le serveur en HTTP, installe son
  firmware (à évaluer avec la sécurité, rang 1 du TODO). Nouvelle partie du cahier
  de tests ; procédure de publication écrite dans le dépôt (G11).
- Compatibilité avec D038 : rien de ce qui est conçu ici ne doit empêcher un binaire
  public sans secret (Wi-Fi saisi à l'installation, mêmes entités de mise à jour).
- **Révision du 5 novembre 2026** (propriétaire, après la maquette D039 : « le
  binaire privé n'est pas la norme que je veux retenir ») : remplace l'hébergement
  local et le binaire de production chiffré décrits plus haut.
  - **Tous les modules de la maison** utilisent le binaire public de D039, publié sur
    GitHub ; mises à jour par Wi-Fi depuis l'entité « Firmware » de HA. Le binaire ne
    contient aucun secret : la publication sur Internet n'est plus un problème.
  - **USB en secours** : première installation, reflash si un module ne se met plus
    à jour.
  - **Configurations privées** (`hapanel.yaml`, `hapanel_banc.yaml`, secrets
    compilés, OTA depuis le PC) : réservées aux modules de test de l'atelier, pour
    essayer un développement avant de le publier ; jamais sur un module de la maison.
  - Passage d'un module de production au binaire public : un reflash par USB, Wi-Fi
    ressaisi par Improv (cahier J14).
  - Points à trancher restants : installation par bouton seulement ou par une
    automatisation de HA qui met tout le parc à jour ; vérification nocturne (TODO,
    mise à jour depuis l'écran).

## D038 — Orientation : un projet publiable

- Date : 4 novembre 2026 — Statut : orientation donnée par le propriétaire (« c'est
  franchement l'orientation que le projet est en train de prendre », après
  HAP-R099) ; cadrage à faire avant tout code.
- Contexte : le binaire de production contient le nom et le mot de passe du Wi-Fi
  et la clé de l'API (vérifié le 4 novembre 2026 sur `a06cdbb`, HAP-R098) ; il ne
  peut donc pas être publié. ESPHome ne permet pas, d'après la recherche du
  4 novembre 2026, de fournir la clé de l'API à un module après compilation.
- Public visé : des utilisateurs de Home Assistant qui veulent réaliser le projet
  chez eux (carte achetée, montage, installation). Le propriétaire développe
  d'abord seul ; la publication vient ensuite. C'est la raison de l'absence de
  secret dans le dépôt (G9).
- Deux chemins pour un utilisateur, le premier possible dès aujourd'hui : cloner le
  dépôt et compiler avec son propre `secrets.yaml` (modèle `secrets.example.yaml`) ;
  ou, plus simple, installer le binaire générique décrit ci-dessous.
- Orientation : HAPanel doit pouvoir être installé par d'autres, sur le modèle des
  projets « Made for ESPHome » :
  - binaire générique sans secret, publié sur GitHub (Releases), installable depuis
    le navigateur (ESP Web Tools) ;
  - Wi-Fi saisi à la première installation (Improv par USB, ou point d'accès du
    module et portail captif), gardé en flash ; Improv par Bluetooth exclu (mémoire,
    R2) ;
  - chaque utilisateur adopte son module (`dashboard_import`) et recompile avec sa
    propre clé ; les modules du propriétaire restent sur D037, binaire chiffré
    hébergé chez lui ;
  - configuration de la maison entièrement dans le blueprint (déjà le cas, D012).
- À cadrer avec le propriétaire : licence (le dépôt est déjà public, constaté le
  4 novembre 2026, mais sans licence : personne n'a légalement le droit de le
  réutiliser ; tranché le 7 novembre 2026 : MIT, D043) ;
  relecture de la documentation pour en retirer ce qui est personnel (pièces,
  nœuds, maison) ; page d'installation ; choix entre « adoption obligatoire » et
  binaire public non chiffré (API et OTA ouvertes sur le réseau local, à refuser
  sauf décision contraire).
- Conséquences immédiates : les nouveaux développements évitent tout réglage propre
  à la maison dans le firmware (tout passe par le blueprint ou les entités de
  configuration) ; le Wi-Fi hors du binaire sert aussi les modules du propriétaire
  (une fuite du binaire ne livre plus le Wi-Fi).

## D039 — Maquette du déploiement public (binaire sans secret, mises à jour depuis HA)

- Date : 4 novembre 2026 — Statut : **accepté le 5 novembre 2026** (cahier J OK,
  J9, J10 et J14 reportés au guide d'installation ; D037 révisée) ; maquette
  demandée par le propriétaire (« valider la faisabilité d'un déploiement de
  nouveaux binaires via une méthode simple depuis HA […] sans avoir à refaire une
  compile en local par l'utilisateur ») ; plusieurs cartes disponibles pour les
  essais.
- Constat dans le code d'ESPHome 2026.10.1 (`.venv`, 4 novembre 2026) :
  - `api: encryption:` sans `key` : le module démarre non provisionné, accepte une
    première clé (`NoiseEncryptionSetKeyRequest`), la garde en flash et refuse
    ensuite toute connexion sans elle ; seule une remise à zéro l'efface ;
  - le Wi-Fi saisi par Improv ou par le portail captif est gardé en flash ;
  - `provisioning:` ferme, passé un délai, le point d'accès, Improv et les
    connexions sans clé, jusqu'au prochain redémarrage ;
  - avec une clé reçue à l'exécution, l'OTA `esphome` (depuis un PC) l'**offre**
    mais accepte aussi un envoi sans clé (« plaintext accepted ») ; ESPHome refuse
    `ota: encryption:` dans ce cas ;
  - `update: platform: http_request` lit un manifeste (version, MD5) et télécharge
    le binaire ; mise à jour proposée si la version diffère de `project.version`.
- Décision (maquette) :
  - les fonctions passent dans `packages/application.yaml`, commun aux deux
    configurations ; l'accès est séparé : `packages/acces_prive.yaml` (Wi-Fi, clé,
    OTA depuis le PC, inchangés pour `hapanel.yaml` et le banc : configuration
    résolue identique, vérifiée) et `packages/acces_public.yaml` ;
  - `hapanel_public.yaml` : aucun secret ; Wi-Fi par Improv (USB) ou point d'accès
    et portail captif ; clé reçue à l'adoption ; fenêtre d'installation de 15 min ;
    **pas d'OTA depuis un PC** (elle accepterait un envoi sans clé) : mises à jour
    par l'entité « Firmware » seulement, reflash par USB sinon ;
  - publication par GitHub Actions (`.github/workflows/publication.yml`) à l'envoi
    d'une étiquette `v<version>` : binaire complet, binaire de mise à jour et
    manifeste dans une Release ; l'entité lit
    `releases/latest/download/manifest.json` ;
  - première installation : binaire complet par USB depuis le navigateur (ESPHome
    Web ou ESP Web Tools), puis Wi-Fi par Improv.
- Mesures (compilation locale, 4 novembre 2026) : binaire public compilé ; flash
  75,2 % (1 379 923 octets, contre 63,6 % pour la production : environ 213 Ko pour
  TLS, `http_request`, portail captif et Improv) ; RAM statique 32,5 % ; aucun des
  trois secrets de `secrets.yaml` dans le binaire (recherche octet par octet). La
  marge de flash tombe à 25 % : à suivre pour l'infrarouge.
- À vérifier par la maquette (cahier J) : HA envoie-t-il la clé à l'adoption ;
  Wi-Fi et clé gardés après une mise à jour ; redirection de GitHub lue
  (`buffer_size_rx` et `buffer_size_tx` portés à 2048 : avec le seul tampon de
  réception, `v0.8.0-dev.1` échoue au démarrage sur « Out of buffer », la requête
  vers l'adresse signée de GitHub ne tenant pas dans 512 octets ; corrigé par
  `v0.8.0-dev.3`, constaté le 5 nov.) ; mémoire libre pendant le téléchargement (G6) ;
  écran pendant la fenêtre d'installation.
- Constaté le 5 novembre 2026 (cahier J1 à J3, J6 à J8, J12) : publication par
  GitHub Actions en 3 min ; carte neuve installée par web.esphome.io, Wi-Fi par
  Improv, adoption sans clé ; mise à jour par Wi-Fi depuis l'entité Firmware de HA,
  téléchargée depuis GitHub en 16 s, Wi-Fi, clé et réglages conservés. Pièges
  (tampons, versions suffixées, vérification au démarrage) : `09_PIEGES.md`. Le
  manifeste désigne le binaire par son étiquette, et non par la dernière Release.
- Avant fusion (faits le 5 novembre 2026) : risques au `08`, schémas d'architecture
  régénérés, procédure G11 validée, D037 révisée.
- Limite : un module public n'a pas d'écran d'installation ; sans Wi-Fi, rien ne
  dit à l'utilisateur de se connecter au point d'accès (à concevoir si la maquette
  est retenue).

## D040 — Nom de la pièce envoyé par le blueprint

- Date : 5 novembre 2026 — Statut : accepté, validé par le propriétaire (cahier
  J12, J13 OK le 5 novembre 2026).
- Contexte : sur le module de la maquette, l'accueil affiche « Séjour » alors que le
  blueprint vise la cuisine (retour du propriétaire, J3). Le mot était écrit dans
  `pages/accueil.yaml` : un réglage propre à la maison dans le firmware, contraire
  à D038.
- Décision : nouvelle clé `piece`, envoyée avec les valeurs de l'accueil. Champ
  facultatif « Nom de la pièce » dans le blueprint ; vide : zone (`area_name`) du
  thermomètre, sinon « Intérieur ». 14 caractères au plus (tampon de 31 octets du
  panneau, accents sur 2 octets) ; à l'écran, 124 px, coupé par « … » au-delà.
  Texte par défaut du firmware : « Intérieur ».
- Conséquences : un ancien blueprint n'envoie pas `piece` : l'accueil affiche
  « Intérieur » jusqu'à la réimportation. L'`id` interne `lbl_acc_sejour` est
  gardé (aucune entité de HA touchée, G10).

## D041 — Un fichier matériel et un binaire public par carte

- Date : 7 novembre 2026 — Statut : accepté par le propriétaire (structure validée
  au banc avec l'ESP32-2432S028, cahier K ; binaire public de la S028 validé en
  `v0.9.0`, cahier K12 à K15).
- Contexte : l'ESP32-2432S024C (D004) semble ne plus être fabriqué ; le propriétaire
  a d'autres cartes en stock, dont l'ESP32-2432S028 à deux prises USB. Flashée avec
  le binaire de la S024C, elle rejoint HA mais l'écran reste noir (rétroéclairage
  sur GPIO21, tactile résistif sur un autre bus). ESPHome fixe pilotes et broches à
  la compilation : un binaire ne peut pas changer de carte une fois installé.
- Décision :
  - un fichier matériel par carte (`packages/hardware.yaml` pour la S024C,
    `packages/hardware_<carte>.yaml` pour les autres), qui déclare tous les mêmes
    `id` ; `packages/application.yaml` ne contient aucun matériel, chaque
    configuration de tête inclut son fichier matériel ;
  - une configuration publique et un jeu de fichiers publiés par carte :
    `hapanel-<carte>-factory.bin`, `hapanel-<carte>-ota.bin` et un manifeste propre ;
    le manifeste de la S024C garde le nom `manifest.json`, compilé dans les modules
    déjà installés ; chaque module ne lit que le manifeste de sa carte ;
  - l'utilisateur choisit sa carte à l'installation parmi les cartes validées
    (« propositions validées », demande du propriétaire du 7 novembre 2026) ; une
    carte hors catalogue demande d'écrire et de compiler son propre fichier matériel.
- Options écartées : réglage des broches et des pilotes depuis HA après
  l'installation (impossible avec ESPHome) ; un binaire unique contenant les pilotes
  de toutes les cartes (broches en conflit, GPIO25, 32 et 33 servent à la fois au
  tactile I²C de la S024C et au tactile SPI de la S028).
- Conséquences : à partir de `v0.9.0-dev.1` (publiée le 7 novembre 2026), la Release
  contient six fichiers ; `hapanel-factory.bin` et `hapanel-ota.bin` deviennent
  `hapanel-2432s024c-factory.bin` et `hapanel-2432s024c-ota.bin` (guide
  d'installation : captures à refaire). Interface encore calée sur 240 × 320 et
  glissière peu adaptée au tactile résistif : TODO rang 5.

## D042 — Message d'accueil réglé dans le blueprint du module

- Date : 7 novembre 2026 — Statut : choisi par le propriétaire (option A, HAP-R001) ;
  validé dans HA sur deux modules le 7 novembre 2026 (cahier B10 à B19). Remplace, dans D028, le
  blueprint de la maison `message_accueil.yaml`.
- Contexte : deux blueprints à configurer ; à chaque nouveau module, le message
  d'accueil est oublié puis cherché (remarque du propriétaire du 7 novembre 2026,
  cahier K).
- Décision :
  - section repliée et facultative « Message d'accueil » dans `module.yaml`
    (déclencheurs, période sans déclenchement, plage horaire, deux listes, météo
    sous le message), remplie dans l'automatisation de chaque module ; sans
    déclencheur, rien ; `message_accueil.yaml` est retiré du dépôt ;
  - chaque module décide seul : les conditions (plage, période sans déclenchement)
    sont évaluées au déclenchement, avant la file d'attente de l'automatisation, et
    le message ne part que vers ce module, s'il a son entité « Message d'accueil »
    activée ;
  - même texte sur tous les modules réglés de la même façon : saison, moment et
    choix du message dépendent de l'instant du déclenchement (millisecondes), et non
    plus d'un tirage au hasard ;
  - météo sous le message prise dans l'entité Météo du module, désactivable ;
  - pas de protection contre deux fois de suite le même message (choix du
    propriétaire).
- Options écartées : un module « pilote » qui sert tous les modules trouvés
  automatiquement (option B, recommandée par l'agent : un seul tirage, messages
  uniques sûrs) ; garder deux blueprints en trouvant les panneaux automatiquement
  (option C).
- Conséquences : réglages à recopier dans chaque module. Un module dont
  l'automatisation est occupée au déclenchement (envoi périodique) peut lire la
  liste des messages uniques après qu'un autre module l'a cochée : il affiche et
  coche alors le message unique suivant, ou un message ordinaire. Migration une
  fois : supprimer l'automatisation et le blueprint « HAPanel — message d'accueil »
  (`CONFIGURATION.md` § 6). Le firmware ne change pas.

## D043 — Licence MIT

- Date : 7 novembre 2026 — Statut : accepté par le propriétaire (HAP-R013).
- Contexte : dépôt public depuis le 4 novembre 2026, sans licence : personne n'avait
  le droit de réutiliser le projet (D038).
- Décision : licence MIT pour tout le dépôt (configuration, blueprints, outils,
  documentation et captures), fichier `LICENSE` à la racine ; titulaire : `cnuma`,
  pseudonyme GitHub, sans nom personnel (D038, relecture du personnel).
- Options écartées : Apache 2.0 (même liberté, texte plus long, clause de brevets sans
  objet ici) ; GPL v3 (empêcherait une reprise fermée, mais freine l'adoption, que
  D038 recherche).
- Justification : licence la plus répandue autour de Home Assistant et d'ESPHome ;
  ESPHome (partie firmware) et LVGL sont eux-mêmes sous MIT.
- Conséquences : chacun peut copier, modifier et vendre le projet, y compris fermé, en
  gardant la mention de copyright. Les composants compilés gardent leur licence
  (ESPHome, LVGL : MIT ; ESP-IDF : Apache 2.0).

## D045 — Mise à jour signalée par la barre d'état et la LED

- Date : 7 novembre 2026 — Statut : choisi par le propriétaire (HAP-R001), implémenté
  sur `feature/maj-icone`, validé sur la S028 le 7 novembre 2026 (cahier L1 à L10), en
  0.10.0. Premier point du
  TODO rang 2 (mise à jour depuis l'écran) ; les points 2 à 4 restent à faire.
- Contexte : une Release publiée n'est visible que dans HA (entité « Firmware ») ; le
  propriétaire veut la voir sur le module, comme dans AquaLook (demande du 5 novembre
  2026, précisée le 6 novembre).
- Décision :
  - **icône :** `mdi:arrow-up-bold-circle`, violette (`#AB47BC`, le violet de Manuel,
    D016), dans la barre d'état à la place de la disquette (x = 160) ; elle clignote
    (500 ms allumée, 500 ms éteinte) ; pendant un enregistrement, la disquette passe
    devant, puis l'icône revient ;
  - **LED :** toutes les 10 s, deux éclairs violets de 150 ms séparés par 150 ms
    d'extinction, puis la respiration du chauffage reprend ; même plafond que la
    respiration (« Intensité LED », lumière de la pièce) : rien avec « LED : Éteinte ».
    Priorités : alerte rouge, puis arc-en-ciel du message d'accueil, puis éclairs de
    mise à jour, puis respiration ;
  - **condition :** entité `maj_firmware` dans l'état « mise à jour disponible » ;
    pendant l'installation, plus rien ; après le redémarrage dans la nouvelle
    version, plus rien. Binaire public seulement : le binaire privé de l'atelier n'a
    pas d'entité de mise à jour et n'affiche jamais rien ;
  - **recherche :** inchangée (au démarrage dès que le Wi-Fi est là, puis toutes les
    6 h, réglage d'ESPHome) : une Release est vue en 6 h au plus. Recherche à 3 h du
    matin et bouton « Rechercher » : TODO rang 2. Remplacée par D047 (recherche au
    démarrage, à 3 h et par le bouton de la page À propos).
- Options écartées : `mdi:package-up` (icône de HA, trop détaillée à 24 px) ; LED en
  clignotement violet continu (la couleur du chauffage disparaîtrait jusqu'à
  l'installation) ; LED à pleine intensité (gênante la nuit, ce n'est pas une alarme).
- Justification : le double éclair ne se confond ni avec Manuel (violet qui respire)
  ni avec l'alerte (rouge, 1 Hz) ; aucune action HA ni surface nouvelle (`08`
  inchangé), le module ne fait que lire l'état de son entité de mise à jour.
- Conséquences : tous les modules publics clignotent dès qu'une Release est publiée,
  y compris une Release de développement marquée « Latest ».

## D046 — Actions Home Assistant refusées aux modules, usurpation de `device_id` acceptée

- Date : 9 novembre 2026 — Statut : choisi par le propriétaire (HAP-R001, option A),
  sur `docs/securite-actions-ha` ; option décochée sur les trois modules (cahier N1).
  TODO rang 1 du 9 novembre 2026 ; validé et fusionné dans `main` le même jour.
- Contexte : l'intégration ESPHome de HA a une option par module, « Autoriser
  l'appareil à effectuer des actions Home Assistant ». Le firmware n'appelle aucune
  action, il n'émet que des événements `esphome.hapanel_*` (testé le 2 novembre
  2026, `08`). Code de l'intégration lu le 9 novembre 2026 (`manager.py`, branche
  `dev`, `async_on_service_call`) :
  - un événement est émis avec `{device_id: <vrai appareil>, **données du module}` :
    un champ `device_id` envoyé par le module **remplace** le vrai ;
  - les modèles (`data_template`) envoyés par le module sont évalués par HA avant
    l'émission : un firmware modifié peut faire calculer par HA l'identifiant d'un
    autre panneau (`integration_entities('esphome')`…), sans le connaître ;
  - ces deux points ne dépendent pas de l'option, qui ne bloque que les actions.
- Décision :
  - l'option reste **décochée** sur chaque module ; les guides le disent à l'ajout et
    pour un module déjà ajouté (`CONFIGURATION.md` § 1) ;
  - l'usurpation de `device_id` est un **risque accepté** (`08`, R11) : elle demande
    un firmware modifié muni de la clé du module, donc en pratique l'accès physique à
    un panneau (flash non chiffrée lisible par USB) ; elle ne donne que les commandes
    que les blueprints autorisent, mais pour tous les panneaux ;
  - toute commande nouvelle (infrarouge) passe par un événement traduit
    par le blueprint, avec bornes et liste fermée, jamais par une action HA appelée
    par le module.
- Options écartées : laisser l'option cochée (un firmware modifié pourrait lancer
  n'importe quelle action de HA : serrures, alarme ; aucun usage par le panneau) ;
  jeton secret par panneau vérifié par le blueprint (lisible par ces mêmes modèles
  s'il est rangé dans une entité, firmware public et blueprint à modifier, pour un
  gain faible) ; chiffrement de la flash et démarrage sécurisé de l'ESP32 (eFuses
  irréversibles, installation par le navigateur à revoir).
- Justification : surface la plus petite sans perte de fonction ; la seule parade
  fiable est dans HA (écrire `device_id` après les données du module), hors du dépôt.
- Conséquences : le blueprint garde son filtre `device_id == panneau`, qui empêche les
  erreurs (deux panneaux, deux automatisations) mais n'est pas une barrière de
  sécurité. Pas de signalement à l'équipe de HA : hors du périmètre de sa politique de
  sécurité (appareil compromis, accès physique), décision du propriétaire du
  9 novembre 2026 (HAP-R005).

## D047 — Mise à jour depuis l'écran : recherche et installation

- Date : 9 novembre 2026 — Statut : choisi par le propriétaire (HAP-R002), implémenté
  sur `feature/maj-ecran`, à valider (cahier O). TODO rang 1, points 2 à 4 ; complète
  D045.
- Contexte : une mise à jour publiée ne s'installait que depuis HA (entité
  « Firmware »), ce qui oblige à se connecter à HA ; le module ne cherchait qu'au
  démarrage, puis toutes les 6 h (demande du propriétaire du 5 novembre 2026).
- Décision (binaire public seulement ; le binaire privé n'a pas d'entité de mise à
  jour, ses boutons restent masqués et ses scripts `maj_rechercher`, `maj_proposer`
  sont vides) :
  - **recherche :** une fois par démarrage, 10 s après la première connexion au
    Wi-Fi ; chaque nuit à 3 h, heure de HA (sans heure reçue, pas de recherche de
    nuit) ; plus de recherche toutes les 6 h (`update_interval: never`) ;
  - **page À propos :** bouton « Rechercher une mise à jour » ; son libellé passe à
    « Recherche… », puis « À jour », « Version X.Y.Z disponible », « Recherche
    impossible » (pas de réponse en 30 s, GitHub inaccessible) ou « Pas de Wi-Fi » ;
    il revient au libellé de départ à chaque ouverture de la page ;
  - **Menu :** tuile violette « Mise à jour » (`#AB47BC`, D045) à la 6e place, visible
    seulement quand une mise à jour attend ; elle ouvre une confirmation « Installer
    la version X.Y.Z ? » (Annuler, Installer), avec en dessous, en gris, le résumé de
    la version (160 octets au plus) ;
  - **résumé (retour du propriétaire, 9 novembre 2026, cahier O5) :** une ligne par
    version dans `NOUVEAUTES.md`, sous `## <version>` (ou la version sans suffixe :
    `0.11.0-dev.1` lit `0.11.0`) ; la publication la copie dans le champ « summary »
    du manifeste, lu par le module et affiché aussi par HA. Sans ligne : rien. Le
    résumé générique « HAPanel X (SHA), carte » disparaît du manifeste ;
  - **bouton de la page À propos violet** quand la recherche trouve une version
    (retour du propriétaire, cahier O2) ; couleur d'origine à la réouverture ;
  - **installation :** « Mise à jour en cours, module indisponible » reste affiché
    jusqu'au redémarrage dans la nouvelle version (le téléchargement bloque la boucle
    principale : l'écran ne bouge plus) ; en cas d'échec, « Échec de la mise à jour.
    Réessayez plus tard. » et un bouton Fermer ; la mise à jour reste proposée ;
  - **sécurité de l'état :** la confirmation et l'installation vérifient que l'entité
    est encore « mise à jour disponible » ; sinon, rien n'est lancé. Sans toucher
    pendant 1 min, la confirmation ou le message d'échec se ferment (comme le retour
    à l'accueil, D022), jamais pendant l'installation.
- Options écartées pour le résumé : message de l'étiquette git (relu seulement à la
  publication, invisible dans les fichiers) ; texte générique actuel (sans intérêt
  pour l'utilisateur).
- Options écartées : tuile toujours visible et grisée (Menu changeant pour rien,
  installation sans objet) ; recherche toutes les 6 h en plus de 3 h (requêtes
  inutiles : la nuit suffit, le bouton couvre l'urgence) ; installation automatique
  la nuit (R10 : une Release compromise s'installerait sans personne).
- Justification : l'installation reste un geste volontaire devant le module, comme
  dans HA ; seule la source déjà utilisée par HA (Release « Latest », MD5 du
  manifeste) est installée ; aucune entité ni action HA nouvelle.
- Conséquences : toute personne devant un module peut installer la version publiée
  (`08`, surfaces) ; une Release publiée est vue au plus tard à 3 h le lendemain, au
  redémarrage, ou par le bouton. HA continue de proposer la mise à jour.

## D048 — Carte Guition JC4827W543 (4,3", ESP32-S3), en portrait provisoire

- Date : 9 novembre 2026 — Statut : choisi par le propriétaire (HAP-R011 : « portrait ce
  soir, paysage ensuite », « sans LED ni LDR »), implémenté sur
  `feature/carte-jc4827w543`, à valider au banc (cahier P). TODO rang 4.
- Contexte : le propriétaire a des cartes Guition JC4827W543C_I, déjà portées et
  validées sur matériel par AquaLook (27 août 2026) : ESP32-S3, 4 Mo de flash, 8 Mo de
  PSRAM, écran NV3041A de 480 × 272 en QSPI, tactile GT911, rétroéclairage GPIO1, ni LED
  RVB ni LDR. Les pages sont dessinées pour 240 × 320 en portrait et ne tiennent pas en
  272 de haut.
- Décision :
  - fichier matériel `packages/hardware_jc4827w543.yaml` et binaire public
    `hapanel_jc4827w543_public.yaml` (D041), manifeste `manifest-jc4827w543.json` ;
  - le bloc `esp32` quitte `base.yaml` pour chaque fichier matériel (la puce dépend de
    la carte) ; contenu inchangé pour la S024C et la S028 ;
  - **portrait provisoire :** rotation de 90° par LVGL, pages de 240 × 320 centrées en
    largeur (marges de 16 px), bande noire de 160 px en bas ; mêmes pages, mêmes
    boutons et mêmes couleurs que les autres cartes ;
  - **sans LED ni LDR :** sorties de LED sans effet (alerte, chauffage et mise à jour
    se lisent à l'écran ; les réglages de la LED restent affichés, sans effet) ;
    capteur de lumière fixé au plein jour : rétroéclairage de jour, réglé par
    « Intensité écran » ;
  - **publication :** la Release porte trois cartes ; le champ `chipFamily` de chaque
    manifeste vaut la puce de la carte (`ESP32` ou `ESP32-S3`), sans quoi ESPHome
    refuse la mise à jour.
- Options écartées : paysage tout de suite (toutes les pages à redessiner, rien de
  testable le 9 novembre) ; portrait définitif ; LED WS2812 externe sur GPIO46 comme
  AquaLook (montage à faire) ; LDR ajoutée sur une broche libre.
- Justification : la carte fonctionne et se met à jour comme les autres dès la
  première version, sans attendre la refonte des pages ; la refonte en paysage
  (TODO rang 4, point 1) se fera page par page avec le propriétaire.
- Conséquences : un module 4,3" ne reçoit jamais un binaire ESP32 (manifeste et puce
  distincts) ; une nouvelle page doit être ajoutée aux marges du fichier matériel tant
  que le portrait provisoire dure ; écran sous-utilisé (bande noire) jusqu'au paysage.
