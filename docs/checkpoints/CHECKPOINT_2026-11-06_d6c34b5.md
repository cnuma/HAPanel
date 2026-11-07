# Checkpoint du 6 novembre 2026 — `d6c34b5`

Correctif de l'intensité de l'écran au démarrage fusionné et publié en `v0.8.1` ;
guide d'installation pour débutant en cours sur sa branche. Remplace
`CHECKPOINT_2026-11-05_07f5762.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `d6c34b5`, poussée et vérifiée sur le dépôt distant |
| Version | `0.8.1` |
| Release GitHub « Latest » | `v0.8.1` (`d55ed00`), manifeste lié à l'étiquette, MD5 du binaire vérifié |
| Module POC (cuisine), binaire public | `0.8.1-dev.1 (e1ed3f8)` en fin de session ; `0.8.1` proposée par HA |
| Module de banc | inchangé : `0.7.0-dev (7642307)` |
| Branche en cours | `docs/guide-installation` (`a558117`), poussée, pas encore à jour de `main` |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `80dfff3`, `6283585` | « Intensité écran » réappliquée dans l'`on_boot` (priorité -100) : l'écran restait à 100 % jusqu'à la première veille (défaut présent depuis 0.6.0) ; cahier H20 ; deux pièges |
| `5aff2d4`, `e1ed3f8` | `VERSION` 0.8.1-dev ; TODO rang 4 : icône violette qui clignote ; Release de test `v0.8.1-dev.1` |
| `93d4543`, `1a91eaf` | H20 OK ; piège et procédure : HA propose la version vue à la dernière vérification du module |
| `f08a2cf`, `d55ed00` | Statut 0.8.1 ; fusion de `fix/intensite-ecran-demarrage` ; Release `v0.8.1` |
| `d6c34b5` | Proposition d'icône de mise à jour (TODO rang 4) ; liaison USB CH340 (`00_CONTEXT.md`) |
| `docs/guide-installation` : `7c0db67` à `a558117` | `INSTALLATION.md` (brouillon ; captures 01 et 02 réelles, maquettes 10 et 18), `CONFIGURATION.md` réécrit pour débutant, réglages du logiciel déplacés dans `05_BUILD_AND_TEST.md`, avertissement « Chrome ou Edge uniquement », pilote CH340 du fabricant |

## Mesures

| Mesure | Valeur |
|---|---|
| `esphome config` atelier / public | OK sur `main` |
| Compilation banc / public (`6283585`, YAML identiques à `main`) | RAM 31,4 / 32,5 % ; flash 64,3 / 75,2 % |
| Publication `v0.8.1-dev.1`, `v0.8.1` | GitHub Actions OK |
| Mémoire libre, plus grand bloc (G6) | Non relevés cette session (binaire public sans composant `debug`) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Session prévue : test du guide sur le module de la cuisine, flash par le navigateur
  (captures 03 à 07), puis J10, J9 et J14 ; port COM à redemander au propriétaire.
  Capture 19 (mise à jour proposée par HA) avant, si `0.8.1` n'est pas déjà installée.
- Prochaine étape : rang 3 de `docs/TODO.md` (guide d'installation, branche
  `docs/guide-installation`) ; rangs 1 et 2 inchangés.
- Tests qui bloquent la prochaine fusion : J9, J10, J14 (`docs/CAHIER_DE_TESTS.md`).
- Questions ouvertes au propriétaire : test J15 (un débutant suit le guide) à ajouter
  ou non ; icône du rang 4 (proposition au TODO).
- Rappel du checkpoint précédent, non confirmé : réimporter le blueprint depuis `main`
  (`docs/CONFIGURATION.md` § 2).
- Nouveaux pièges : trois, ajoutés à `docs/codex/09_PIEGES.md` (ordre de démarrage
  `number` / `light`, fusion des `on_boot` des packages, version vue à la dernière
  vérification).

Reprise : `docs/START_HERE.md`, branche `main` ; guide : `docs/guide-installation`.
