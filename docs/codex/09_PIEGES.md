# 09 — Pièges connus

Liste unique des pièges rencontrés, valable d'un chat à l'autre (G14). Un piège
découvert s'ajoute ici, dans le même commit que sa correction ; un checkpoint n'en
recopie aucun. Un piège qui ne vaut plus est barré, avec sa date.

## Poste de travail et outils

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash : ESP-IDF refuse MSys/Mingw.
- Activer d'abord l'environnement Python (`.\.venv\Scripts\Activate.ps1`), sinon
  `build.ps1` répond « esphome n'est pas reconnu ».
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

## Binaire public et mises à jour (D039)

- `http_request` vers GitHub : `buffer_size_rx` **et** `buffer_size_tx` à 2048. La
  redirection vers l'adresse signée (près de 1 ko) ne tient pas dans 512 octets :
  « HTTP_CLIENT: Out of buffer », puis « Failed to fetch manifest ». Ce message n'est
  écrit qu'au démarrage, vers 20 s : capturer le journal dès le reset.
- L'action « Mettre à jour l'entité » de HA ne fait pas vérifier le module : il ne
  vérifie qu'au démarrage, puis toutes les 6 h. Pour forcer, redémarrer le module.
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
- Captures du propriétaire : masquer en entier numéros COM, noms de réseaux (les siens
  et ceux des voisins) et mots de passe (G9) ; un masque partiel laisse lire la
  première et la dernière lettre. Captures de téléphone : trois fois la taille
  d'affichage, les réduire au tiers.

## Échanges avec le propriétaire

- Il lit souvent sur mobile : donner les valeurs à copier en blocs de code.
