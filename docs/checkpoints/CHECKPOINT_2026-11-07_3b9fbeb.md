# Checkpoint du 7 novembre 2026 — `3b9fbeb`

Guide d'installation complété avec les captures réelles du reflash du module de la
cuisine ; J9 et J14 OK, J10 reporté. Remplace `CHECKPOINT_2026-11-06_d6c34b5.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `docs/guide-installation`, `3b9fbeb`, poussée et vérifiée sur le dépôt distant ; `main` inchangée (`9409b16`) |
| Version | `0.8.1` |
| Release GitHub « Latest » | `v0.8.1` |
| Module de la cuisine (`hapanel-583c28`), binaire public | `0.8.1` (Release), reflashé par USB le 7 novembre, réadopté dans HA (nouvelle clé) ; automatisation à rattacher (« Panneau ») |
| Module de banc | inchangé : `0.7.0-dev (7642307)` |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `6621f35` | Fusion de `main` dans la branche du guide (correctif `v0.8.1`, checkpoint `d6c34b5`) |
| `6b97821` | Captures 03 à 05, 08, 09, 13 à 15 et menu du bouton Démarrer ; libellés réels (« USB Serial », flèche « Installer », « Choisir un fichier », « Configure Wi-Fi », « Découvertes ») ; cahier J14, première passe |
| `a625365` | Captures 06, 07, 11, 12 (Wi-Fi par le téléphone) ; plus aucun emplacement de capture dans `INSTALLATION.md` |
| `2e78ea8` | J9 et J14 OK ; reflash d'un module connu de HA : refuser la connexion non chiffrée ; section « Remplacer le logiciel » retirée du guide (demande du propriétaire) |
| `3b9fbeb` | Pièges, modules en service et libellé du port dans le navigateur (`00_CONTEXT.md`), reste du rang 3 (`TODO.md`) |

## Mesures

| Mesure | Valeur |
|---|---|
| `esphome config` production / banc / public | OK |
| Compilation | Non relancée : YAML et `requirements.txt` identiques à `6283585` (RAM banc / public 31,4 / 32,5 %, flash 64,3 / 75,2 %, checkpoint précédent) |
| Mémoire libre, plus grand bloc (G6) | Non relevés (binaire public sans composant `debug`) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Prochaine étape : rang 3 de `docs/TODO.md` (guide) : J10, captures 16 et 17 au
  rattachement de l'automatisation de la cuisine, puis fusion de
  `docs/guide-installation` dans `main` (accord du propriétaire) ; capture 19 à la
  prochaine version publiée. Rangs 1 et 2 inchangés.
- Tests qui bloquent la prochaine fusion : J10 (`docs/CAHIER_DE_TESTS.md`) ; port COM à
  redemander au propriétaire.
- À confirmer par le propriétaire : accueil de la cuisine après rattachement de
  « Panneau » ; réimportation du blueprint depuis `main` (capture 16).
- Questions ouvertes : test J15 (un débutant suit le guide) ; icône du rang 4.
- Nouveaux pièges : trois, ajoutés à `docs/codex/09_PIEGES.md` (reflash d'un module
  connu de HA, libellés d'interface relevés sur capture, masquage des captures).

Reprise : `docs/START_HERE.md`, branche `docs/guide-installation`.
