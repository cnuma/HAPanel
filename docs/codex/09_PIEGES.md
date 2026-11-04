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

## LVGL

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

## Documentation

- Avant chaque commit qui touche le YAML : mettre à jour la page de `docs/technique/`,
  puis lancer `tools\verifier_doc_technique.py` et `--verifier` (G12).
- La regex des blocs YAML du script de contrôle doit inclure les chiffres
  (`[a-z0-9_]`), sinon `i2c` et `esp32` disparaissent.
- Sur GitHub, la page du dépôt montre `main`, avec quelques minutes de retard après un
  `push` : choisir la branche dans le menu pour voir le travail en cours.

## Échanges avec le propriétaire

- Il lit souvent sur mobile : donner les valeurs à copier en blocs de code.
