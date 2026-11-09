# 09 — Pièges connus

Liste unique des pièges rencontrés, valable d'un chat à l'autre (G14). Un piège
découvert s'ajoute ici, dans le même commit que sa correction ; un checkpoint n'en
recopie aucun. Un piège qui ne vaut plus est barré, avec sa date.

## Poste de travail et outils

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash : ESP-IDF refuse MSys/Mingw.
- Activer d'abord l'environnement Python (`.\.venv\Scripts\Activate.ps1`), sinon
  `build.ps1` répond « esphome n'est pas reconnu ».
- Deux cartes (S024C, S028) : avant tout téléversement, demander **quelle carte est sur
  quel port** et choisir le YAML de cette carte. Le 7 novembre 2026, un binaire S028
  écrit sur la S024C de COM6 a laissé l'écran noir (autre pilote, autres broches ;
  GPIO21, rétroéclairage sur S028, est l'interruption du tactile sur S024C) ; reflash
  du banc par USB, tactile retrouvé. Le journal le dit : `cst816` sur S024C, `xpt2046`
  sur S028.
- Il n'y a pas de module d'atelier : les trois modules sont en service (cuisine et
  séjour en S024C, salle de bain en S028). Ne jamais écrire un binaire de banc ou
  privé sur l'un d'eux sans le dire : il perd l'entité Firmware et ne se met plus à
  jour depuis HA. Le 7 novembre 2026, la « S024C du banc » reflashée en privé était la
  cuisine, découverte le 8. Dans HA : entité Firmware = binaire public ; « Mémoire
  libre » sans Firmware = binaire de banc.
- Entité Firmware avec « Version installée » et « Dernière version » vides : la
  dernière lecture du manifeste a échoué (GitHub en `504` le 8 novembre 2026 au
  matin) ; « À jour » n'a alors pas de sens. Le module ne réessaie qu'au démarrage
  ou à 3 h (D047) : bouton « Rechercher une mise à jour » une fois le manifeste lisible
  dans un navigateur.
- Ajouter dans HA un module public réinstallé : dans les 15 min après son démarrage.
  Passé ce délai, HA demande une clé de chiffrement qu'aucune saisie ne satisfait
  (8 novembre 2026) : redémarrer le module, puis ajouter.
- Version de test d'un binaire public : la prendre **plus ancienne** que la Release
  (`0.9.0-dev.99` sous `0.9.0`), sinon HA la juge à jour et refuse d'installer la
  Release, alors que le module signale une mise à jour dès que les versions diffèrent
  (D045).
- `build.ps1 upload` ne compile pas : enchaîner `compile` puis `upload`, ou utiliser
  `run`, avec `-Config hapanel_banc.yaml` pour le banc.
- `build.ps1 logs` exige un YAML présent sur la branche courante et affiche le SHA du
  dépôt local, pas celui du binaire : lire `Project cnuma.hapanel version` et la date de
  compilation.
- Production et banc compilent dans deux dossiers (`.esphome/build/hapanel` et
  `.esphome/build/hapanel_banc`, depuis `d219405`) : avant une fusion, ne compiler que
  la configuration pas encore compilée (`05_BUILD_AND_TEST.md`).
- ~~Production et banc partagent un dossier de compilation (10 min pour changer)~~ :
  corrigé le 3 novembre 2026.
- PowerShell 5.1 : la ligne `NativeCommandError` est sans effet, le code de sortie
  d'ESPHome fait foi. Un journal redirigé (`*>`) sort en UTF-16 ou UTF-8 avec BOM selon
  la commande.
- `git push` et `gh` écrivent sur la sortie d'erreur : PowerShell signale un code 255
  même en cas de réussite ; vérifier avec `git status -sb`.
- Message de commit passé par PowerShell : écrire le fichier en UTF-8 **sans** BOM, sinon
  le BOM entre dans le titre du commit.
- Une capture de journaux lancée en arrière-plan continue jusqu'à son arrêt, et une
  OTA la coupe : se synchroniser avec le propriétaire avant un test matériel.
- `git branch -d` refuse une branche fusionnée dans `main` si sa copie distante n'a pas
  le dernier commit : vérifier `git merge-base --is-ancestor <branche> main`, supprimer
  la branche distante, puis la locale.

## Module

- Ne jamais juger un démarrage alimenté par le port USB du PC (R7) : bloc secteur 1 A.
- Après chaque OTA, relire la version après 60 s (« Boot seems successful »).
  « Bootloader rollback: supported » n'est pas un retour arrière ; seul « OTA rollback
  detected » en est un.
- Les journaux ouverts après le démarrage ne montrent pas les valeurs reçues dans les
  premières secondes.
- `esphome logs` compte comme client abonné aux états : sans D013, il fausserait
  l'indicateur de connexion.
- Perdre `api_encryption_key` interdit toute OTA : flash par USB obligatoire.
- `secrets.yaml` : la ligne `ota_password` est devenue inutile (D010).
- `restore_value` ne suffit pas : ESPHome n'écrit la flash qu'à
  `flash_write_interval` (60 s par défaut, 5 s ici, D034). Pour tester la
  conservation d'un réglage, attendre au moins 10 s avant de couper.
- Ordre de démarrage : un `number` template (priorité `HARDWARE`) est restauré avant
  une `light` (`HARDWARE - 1`). Un `light.turn_on` lancé par son `on_value` au
  démarrage est écrasé par le `restore_mode` de la lumière (`ALWAYS_ON` : 100 %).
  Appliquer un réglage restauré dans l'`on_boot` (priorité -100, après toutes les
  initialisations), et tester son **effet** après redémarrage, pas seulement sa
  valeur (6 novembre 2026).
- Les `esphome: on_boot:` des packages sont fusionnés en **une seule** automatisation :
  la dernière `priority` lue s'applique à toutes les actions. Garder -100 partout ;
  vérifier dans la sortie d'`esphome config` (6 novembre 2026).
- **ESP32-2432S028 (7 novembre 2026) :** rétroéclairage sur GPIO21, pas GPIO27 : avec
  le binaire de la S024C, l'écran reste noir alors que Wi-Fi, HA et LED fonctionnent.
  La variante à deux prises USB a un contrôleur ST7789V (modèle ESPHome
  `ESP32-2432S028-7789`, couleurs justes sans inversion, contrairement au réglage
  TFT_eSPI d'AquaLook). Tactile résistif : x brut décroît de gauche à droite
  (`mirror_x`).
- Téléversement « No serial data received », même avec BOOT tenu, et CH340 bien vu
  par Windows : câble USB de charge seule. Test sans risque : écouter le port et
  appuyer sur RST ; un ESP32 envoie toujours ses lignes de démarrage (7 novembre 2026).
- Guition 4,3" (NV3041A, sans broche de remise à zéro de l'écran) : après un flash par
  USB, l'écran garde l'état du firmware précédent (couleurs inversées, image à 180°)
  jusqu'à une coupure de courant ; ESPHome n'envoie pas de remise à zéro logicielle.
  Juger l'image et le toucher seulement après avoir débranché et rebranché ; déjà vu
  avec AquaLook (9 novembre 2026, cahier Q2). Une OTA garde l'état du même firmware.
- Guition 4,3" : le port USB est celui de l'ESP32-S3 (303A:1001), il disparaît à chaque
  redémarrage : le journal ne montre jamais les premières lignes du démarrage.
- Ouvrir le port série (journaux, script d'écoute) redémarre la carte : la broche EN
  est reliée au port. Un `POWERON_RESET` à ce moment n'est pas une coupure
  d'alimentation (7 novembre 2026).

## LVGL

- Dalle de la carte : quand la dernière rangée de pixels (319) est allumée, elle
  réapparaît par instants sur la première (ligne claire au redessin complet, point
  dans l'axe d'un bouton du bas). Laisser 2 rangées noires en haut et en bas (D036).
  Ce n'est pas un défaut de transmission : à 20 MHz, c'est pire.
- Le `top_layer` n'hérite pas de `text_color` ni de `text_font` posés au niveau de
  `lvgl:` (ils vont aux pages) : un label y est sombre, donc invisible sur fond foncé.
  Les poser sur le conteneur (barre d'état, D036).
- Un label non aligné à gauche dont le texte change porte une largeur fixe
  (`04_DEVELOPMENT_RULES.md`).
- Le curseur natif saute à l'endroit touché (d'où la glissière sur mesure de
  l'accueil) ; `text:` d'un bouton n'est pas centré : utiliser un `label` enfant
  `align: CENTER`.
- Le `top_layer` n'hérite ni de la couleur ni de la police déclarées à la racine de
  `lvgl:` : les fixer sur le conteneur de tout nouveau calque.
- Le thème montre un interrupteur à l'arrêt en gris clair, qui se confond avec un état
  désactivé : fond sombre bordé sur la page Réglages (D031).

## Home Assistant et blueprints

- « Réimporter le blueprint » lit `source_url`, qui pointe sur `main` : pour tester un
  blueprint pas encore fusionné, l'importer par le lien de sa branche. Le cache de
  GitHub peut servir l'ancienne version quelques minutes.
- Une saisie obligatoire ajoutée au blueprint impose de reconfigurer l'automatisation.
- Un changement de clés demande de réimporter le blueprint et de recompiler le module.
- Ajouter une icône ou une couleur de scénario modifie `module.yaml` et `scenarios.yaml`.
- Enregistrer le formulaire n'envoie rien : les valeurs arrivent sous 5 min ou à la
  reconnexion.
- Deux automatisations pour un module exécutent chaque commande deux fois.
- Un modèle Jinja qui produit une liste échoue si elle contient un attribut énuméré
  (`hvac_action`) : écrire la liste en YAML.
- HA ne garde que les 5 dernières traces d'une automatisation : les lire aussitôt après
  l'essai.
- Un réglage imposé par le blueprint (`led_*`, `ecran_intensite`) l'emporte sur l'écran
  et sur la page de l'appareil : vérifier l'automatisation avant de conclure à une panne
  (journaux : `hapanel.liaison: led_alerte on`).
- Mode `queued` : les conditions de l'automatisation sont évaluées au déclenchement,
  les actions peuvent attendre derrière un envoi en cours (D042). Ce qui doit être
  jugé à l'instant de l'arrivée va dans `conditions:`.
- Une date mise dans `variables:` devient du texte : la relire dans chaque modèle
  (`trigger.to_state.last_changed | as_local`).
- « Exécuter les actions » saute le déclencheur : `trigger.id` est absent et la
  branche par défaut s'exécute. Le message d'accueil se teste par l'action
  `esphome.<nœud>_message_accueil`.
- Un déclencheur `state` dont la liste d'entités est vide est accepté et ne surveille
  rien (cahier B11, 7 novembre 2026).
- Le `device_id` d'un événement `esphome.*` n'est pas une preuve d'origine : HA le met
  avant les données du module, qui peuvent le remplacer (D046, R11). Le filtre
  `device_id == panneau` évite les erreurs, il ne protège pas.

## Binaire public et mises à jour (D039)

- `http_request` vers GitHub : `buffer_size_rx` **et** `buffer_size_tx` à 2048. La
  redirection vers l'adresse signée (près de 1 ko) ne tient pas dans 512 octets :
  « HTTP_CLIENT: Out of buffer », puis « Failed to fetch manifest ». Ce message n'est
  écrit qu'au démarrage, vers 20 s : capturer le journal dès le reset.
- L'action « Mettre à jour l'entité » de HA ne fait pas vérifier le module : il ne
  vérifie qu'au démarrage, puis chaque nuit à 3 h (D047). Pour forcer : bouton
  « Rechercher une mise à jour » de la page À propos, ou redémarrer le module.
- Manifeste de mise à jour : `chipFamily` doit valoir la puce du module (`ESP32`,
  `ESP32-S3`) ; ESPHome ne lit que la ligne de sa puce, sinon « Manifest does not
  contain required fields » et aucune mise à jour (D048).
- JC4827W543 (4,3") : GPIO21 est la ligne D0 de l'écran QSPI, pas un rétroéclairage ;
  tout code qui la reprogramme casse l'écran en silence. Avec 8 Mo de PSRAM, parcourir
  le tas (`heap_caps_get_largest_free_block`) a fait redémarrer AquaLook par chien de
  garde : rester sur la mémoire interne (D048, piège repris d'AquaLook).
- `update_interval: never` sur l'`update` `http_request` supprime **aussi** la
  vérification du démarrage (ESPHome ne la programme que si l'intervalle dépasse
  60 s) : elle est relancée par `wifi: on_connect` (D047). Une vérification qui échoue
  ne publie aucun état : la page À propos le détecte par l'absence de réponse en 30 s.
- HA propose la version vue à la **dernière vérification** du module. Juste après une
  publication, il propose encore l'ancienne : l'installer est sans dégât (manifeste lié
  à son étiquette), puis la nouvelle arrive au redémarrage, soit deux mises à jour au
  lieu d'une (6 novembre 2026 : `0.8.0`, puis `0.8.1-dev.1`). Redémarrer le module
  avant d'installer, et vérifier la version proposée.
- HA ne propose une mise à jour que si la version publiée est plus récente : une
  version suffixée (`0.8.0-dev.3-usb`) est incomparable avec `0.8.0-dev.N`, l'entité
  reste « À jour » et `update.install` est refusé. Versions sans suffixe ; le module
  POC, en `0.8.0-dev.4-wifi`, ne verra que des versions suffixées ou `0.8.0`.
- Un binaire public déjà installé qui ne lit pas le manifeste ne peut plus se corriger
  par Wi-Fi : seul l'USB le rattrape. Tester la lecture du manifeste avant de publier.
- Reflasher par USB un module encore connu de HA efface sa clé : HA propose de le
  réassocier en prévenant que **la connexion ne sera plus chiffrée** (7 novembre 2026,
  cahier J14). Refuser (D010) : supprimer l'appareil dans HA, l'adopter de nouveau,
  il reçoit une nouvelle clé. Supprimé puis rajouté, il n'est plus celui que désigne
  « Panneau » dans son automatisation : l'y choisir de nouveau, sinon l'accueil
  n'affiche rien de la maison. Le plus simple : supprimer l'appareil avant le reflash.

## Documentation

- Avant chaque commit qui touche le YAML : mettre à jour la page de `docs/technique/`,
  puis lancer `tools\verifier_doc_technique.py` et `--verifier` (G12).
- La regex des blocs YAML du script de contrôle doit inclure les chiffres
  (`[a-z0-9_]`), sinon `i2c` et `esp32` disparaissent.
- Sur GitHub, la page du dépôt montre `main`, avec quelques minutes de retard après un
  `push` : choisir la branche dans le menu pour voir le travail en cours.
- Libellés d'une interface (web.esphome.io, navigateur, HA) : les relever sur une
  capture réelle, jamais de mémoire. Écrits d'avance, « Install », la case
  d'effacement, « USB-SERIAL CH340 » dans la liste du navigateur (en fait « USB Serial
  (COMx) ») et « Nouveaux appareils découverts » étaient faux (7 novembre 2026).
- Capture d'une page publique (Release GitHub) : Edge sans fenêtre,
  `msedge --headless=new --window-size=1280,1000 --virtual-time-budget=15000
  --screenshot=<fichier> <adresse>`. Sans `--virtual-time-budget`, la liste des
  fichiers n'est pas encore chargée (7 novembre 2026).
- Captures du propriétaire : masquer en entier numéros COM, noms de réseaux (les siens
  et ceux des voisins) et mots de passe (G9) ; un masque partiel laisse lire la
  première et la dernière lettre. Captures de téléphone : trois fois la taille
  d'affichage, les réduire au tiers.

## Échanges avec le propriétaire

- Il lit souvent sur mobile : donner les valeurs à copier en blocs de code.
