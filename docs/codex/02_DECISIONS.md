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
    (0,09 à 0,20 V, moyenne sur 1 min), multiplié par le réglage « Intensité
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
    et au rétroéclairage, recalculée toutes les 10 s sur la moyenne de 1 min ;
  - luminosité : 100 % pièce éclairée, 40 % pièce sombre (avant correction
    gamma), interpolée ; transition de 2 s, seulement à partir de 5 points d'écart ;
  - écran éteint : le niveau est appliqué au réveil, sans rallumer l'écran ;
  - sans mesure de la LDR : pleine luminosité, écran lisible. Aucune dépendance
    à Home Assistant.
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
  d'alignement ; à valider sur le module.
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
  aux questions de cadrage (TODO P4) ; à valider sur le module et dans HA. Le
  saint du jour est reporté (source à choisir).
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
    texte), plein écran par-dessus la barre de navigation, fermé par un toucher
    ou après 3 min, écran allumé pendant l'affichage ; fermé à la déconnexion de
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
