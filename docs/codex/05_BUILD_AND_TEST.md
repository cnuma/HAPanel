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
- `hapanel.yaml` et `hapanel_banc.yaml` partagent le répertoire de
  compilation `.esphome/build/hapanel` : alterner entre les deux recompile
  tout (environ 10 minutes).

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

Consigner : configuration flashée, port ou IP, version ESPHome, écrans
testés, cas testés (Home Assistant connecté, déconnecté, entité
indisponible, redémarrages), résultat attendu, résultat observé, mémoire
libre et plus grand bloc libre, tests non effectués.
