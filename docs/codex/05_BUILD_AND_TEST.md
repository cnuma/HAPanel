# 05 — Compilation et tests

Mis à jour le 27 octobre 2026 (D005).

## Outil

ESPHome en ligne de commande, dans un environnement Python propre au dépôt,
version figée :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
esphome version
```

`requirements.txt` contient une seule ligne `esphome==<version>`. Changer de
version est une décision (`02_DECISIONS.md`) suivie d'un test complet. Le
dossier `.venv/` et le répertoire de compilation `.esphome/` sont ignorés
par Git.

## Configurations

| Fichier | Usage |
|---|---|
| `hapanel.yaml` | production |
| `hapanel_banc.yaml` | banc : production + composant `debug` (mémoire libre, plus grand bloc) et journaux `DEBUG` |
| `hapanel_public.yaml` | binaire public de la S024C, sans secret (D039) |
| `hapanel_2432s028_public.yaml` | binaire public de la S028 (D041) |
| `hapanel_jc4827w543_public.yaml` | binaire public de la Guition JC4827W543, 4,3", ESP32-S3 (D048) ; première installation par USB : `esphome upload … --device <PORT_COM>` |
| `hapanel_2432s028_banc.yaml` | banc sur carte ESP32-2432S028 : `.	oolsuild.ps1 run -Config hapanel_2432s028_banc.yaml -Device <PORT_COM>` |

## Port série et adresse

- Premier flash par USB : `<PORT_COM>`, demandé à chaque session.
  `esphome run` liste les ports si `--device` est omis. Si la carte
  n'apparaît pas, installer le pilote du convertisseur USB-série de la carte.
- Ensuite, mise à jour par le réseau : `<IP_PANNEAU>`.

## Chaîne courante

`tools/build.ps1` lit `VERSION` et le SHA Git (suffixe `+modif` si des
fichiers ne sont pas commités) et les injecte dans ESPHome :

```powershell
git -c core.whitespace=cr-at-eol diff --check
.\tools\build.ps1 config
.\tools\build.ps1 run -Device <PORT_COM ou IP_PANNEAU>
```

- `run` valide, compile, téléverse puis affiche les journaux.
- Sans téléversement prévu : `.\tools\build.ps1 compile -Config hapanel.yaml`.
- Journaux seuls : `.\tools\build.ps1 logs -Device <PORT_COM ou IP_PANNEAU>`.
- `secrets.yaml` est à créer depuis `secrets.example.yaml` avant la
  première commande.
- La première commande télécharge les polices Roboto (Google Fonts) : accès
  Internet requis.
- Lancer ESPHome depuis PowerShell, pas depuis Git Bash : l'installation
  d'ESP-IDF refuse les environnements MSys/Mingw. La première compilation
  télécharge ESP-IDF (plusieurs minutes).
- Dossiers de compilation séparés (3 novembre 2026) : `.esphome/build/hapanel`
  pour la production, `.esphome/build/hapanel_banc` pour le banc
  (`build_path` de `hapanel_banc.yaml`). Alterner entre les deux ne
  recompile plus tout ; la première compilation de chacun reste longue
  (environ 10 minutes).
- Avant une fusion dans `main`, ne compiler que la configuration pas encore
  compilée avec ce YAML (propriétaire, 3 novembre 2026). Si
  `git diff <commit du binaire validé> main -- "*.yaml"` est vide, le
  binaire validé au banc couvre le banc ; seule la production reste à
  compiler.

## Vérification du binaire exécuté

Les journaux de démarrage, l'entité de diagnostic dans Home Assistant et la
page « À propos » du panneau affichent version et SHA. Un SHA suffixé
`+modif` ne vaut pas validation.

« OTA successful » ne prouve pas que le nouveau binaire tourne : s'il
redémarre avant 60 s (`safe_mode`), le chargeur revient seul au binaire
précédent (« OTA rollback detected » dans les journaux). Relire le SHA à
l'écran ou dans les journaux après au moins 60 s, et chercher
« Boot seems successful » (constaté le 28 octobre 2026, R7).

## Alimentation

La carte exige une alimentation qui tient le pic de courant du démarrage du
Wi-Fi, rétroéclairage allumé. Le port USB du PC du propriétaire ne suffit
pas : « Brownout detector was triggered » à chaque démarrage, puis mode sans
échec (R7). Validé sur bloc secteur externe 1 A. Le port USB du PC reste
utilisable pour lire le journal série, pas pour juger un démarrage.

## Compte rendu de test

Les tests à faire par le propriétaire et leurs résultats vivent dans
`docs/CAHIER_DE_TESTS.md`, codés par fonction (G13) : il y répond par codes
(« H4 OK, H11 KO : … »), et rien ne se perd entre deux sessions.

Pour un essai au banc, consigner aussi : configuration flashée, port ou IP, version ESPHome, écrans
testés, cas testés (Home Assistant connecté, déconnecté, entité
indisponible, redémarrages), résultat attendu, résultat observé, mémoire
libre et plus grand bloc libre, tests non effectués.

## Réglages du logiciel

Déplacé de `CONFIGURATION.md` le 6 novembre 2026 (guide pour débutant). Ces valeurs
sont lues à la compilation : après un changement, il faut recompiler et téléverser
le module.

| Réglage | Fichier | Valeur | Effet |
|---|---|---|---|
| `veille_delai_ms` | `packages/led_veille.yaml` | 60000 | Retour à l'accueil et écran éteint sans toucher |
| `retro_jour` | `packages/led_veille.yaml` | 1.0 | Luminosité de l'écran, pièce éclairée |
| `retro_nuit` | `packages/led_veille.yaml` | 0.40 | Luminosité, pièce sombre (après gamma : environ 8 %) |
| `retro_ecart_min` | `packages/led_veille.yaml` | 0.05 | Écart minimal avant de changer la luminosité |
| `retro_plancher` | `packages/led_veille.yaml` | 0.30 | Luminosité minimale de l'écran, quel que soit « Intensité écran » |
| `ecran_intensite_min` / `ecran_intensite_defaut` | `packages/led_veille.yaml` | 20 / 100 | Bornes et valeur d'un module neuf pour « Intensité écran » |
| `led_plafond_jour` / `led_plafond_nuit` | `packages/led_veille.yaml` | 0.25 / 0.05 | Intensité de la LED à 100 % du réglage « Intensité LED » |
| `led_intensite_defaut` | `packages/led_veille.yaml` | 20 | « Intensité LED » d'un module neuf |
| `ldr_tension_jour` / `ldr_tension_nuit` | `packages/led_veille.yaml` | 0.09 / 0.20 | Tensions qui définissent pièce éclairée et pièce sombre |
| `accueil_envoi_consigne` | `packages/pages/accueil.yaml` | 2s | Attente avant l'envoi de la consigne |
| `accueil_attente_confirmation` | `packages/pages/accueil.yaml` | 10s | Attente de la confirmation du chauffage |
| `scenarios_attente_ms` | `packages/pages/scenarios.yaml` | 10000 | Attente de la réponse à un scénario |
| `scenarios_message_ms` | `packages/pages/scenarios.yaml` | 5000 | Durée d'affichage du résultat |
| `liaison_peremption_ms` | `packages/liaison_ha.yaml` | 900000 | Délai avant « périmé » |
| `message_duree_ms` | `packages/message_accueil.yaml` | 180000 | Durée d'affichage du message d'accueil |
| `led_arc_periode_ms` | `packages/led_veille.yaml` | 2000 | Un tour de l'arc-en-ciel |

La lumière de la pièce est lue par un capteur peu précis : attendez-vous plutôt à un
réglage jour / nuit qu'à une variation fine.

### Régénérer les images de la documentation

Après une compilation, qui fournit les polices :

```powershell
.\.venv\Scripts\python tools\generer_images_doc.py
```

### Blueprint importé depuis une branche

Pour un test, le blueprint peut être importé avec un lien contenant `feature/…`.
Après la fusion, l'importer de nouveau avec le lien de `main`
(`CONFIGURATION.md` § 2), en acceptant de remplacer l'existant, puis rouvrir
l'automatisation du module et l'enregistrer. « Réimporter » reprendrait la branche,
qui ne sera plus mise à jour.
