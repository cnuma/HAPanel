# 05 — Compilation et tests

Mis à jour le 27 octobre 2026 (D005). Les fichiers `requirements.txt`,
`hapanel.yaml` et `hapanel_banc.yaml` sont créés au premier palier
(`docs/TODO.md`).

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

```powershell
git -c core.whitespace=cr-at-eol diff --check
esphome config hapanel_banc.yaml
esphome -s version <VERSION> -s git_sha <SHA> run hapanel_banc.yaml --device <PORT_COM ou IP_PANNEAU>
```

- `run` valide, compile, téléverse puis affiche les journaux.
- Sans téléversement prévu : `esphome compile hapanel.yaml`.
- Journaux seuls : `esphome logs hapanel_banc.yaml --device <PORT_COM ou IP_PANNEAU>`.
- L'injection de `version` et `git_sha` depuis `VERSION` et Git (avec le
  suffixe `+modif` si des fichiers ne sont pas commités) sera portée par un
  script `tools/build.ps1`, à créer au premier palier.

## Vérification du binaire exécuté

Les journaux de démarrage, l'entité de diagnostic dans Home Assistant et la
page « À propos » du panneau affichent version et SHA. Un SHA suffixé
`+modif` ne vaut pas validation.

## Compte rendu de test

Consigner : configuration flashée, port ou IP, version ESPHome, écrans
testés, cas testés (Home Assistant connecté, déconnecté, entité
indisponible, redémarrages), résultat attendu, résultat observé, mémoire
libre et plus grand bloc libre, tests non effectués.
