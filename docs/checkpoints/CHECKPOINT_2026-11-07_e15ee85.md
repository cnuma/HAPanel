# Checkpoint du 7 novembre 2026 — `e15ee85`

Carte ESP32-2432S028 validée au banc et fusionnée dans `main` ; un fichier matériel par
carte. Remplace `CHECKPOINT_2026-11-07_0052e92.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `e15ee85`, poussée et vérifiée sur le dépôt distant ; `feature/carte-2432s028` fusionnée puis supprimée |
| Version | `0.8.1`, inchangée : configuration fusionnée de la S024C identique ligne à ligne (production, banc, public), aucun binaire publié ne change |
| Release GitHub « Latest » | `v0.8.1` |
| Module de la cuisine, binaire public | `0.8.1`, inchangé |
| Module de banc S024C | inchangé : `0.7.0-dev (7642307)` |
| Carte S028 (deux prises USB) | `hapanel_2432s028_banc.yaml`, `0.8.1 (174aa99)`, flashée par USB ; association à HA avec la clé de `secrets.yaml` à faire |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `b94202b` | `application.yaml` sans matériel ; `hardware_2432s028.yaml`, `hapanel_2432s028_banc.yaml`, doc technique, cahier K |
| `9b78597` | Variante à deux prises USB : modèle d'écran `ESP32-2432S028-7789` (ST7789V) |
| `174aa99` | Calibrage du tactile relevé au banc, `mirror_x` |
| `d9dedb6` | K4 à K11 OK, pièges (`09_PIEGES.md`), demande du propriétaire sur les blueprints (TODO rang 1) |
| `e15ee85` | Fusion dans `main` (accord du propriétaire) |

## Mesures

| Mesure | Valeur |
|---|---|
| `esphome config` production / banc / public | OK, sortie identique à `8c98463` |
| Compilation S028 | OK : RAM 31,3 %, flash 63,5 % ; production et public non recompilés (configuration identique) |
| Mémoire S028 (G6) | Libre 153 Ko, plus grand bloc 96 Ko (K10) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Prochaine étape : rang 1 de `docs/TODO.md` (message d'accueil : B3, et un seul blueprint
  par module, demande du 7 novembre), puis rangs 2 et 3.
- Tests qui bloquent la prochaine fusion : aucun en attente (`docs/CAHIER_DE_TESTS.md`).
  Port COM ou adresse IP à redemander au propriétaire.
- Nouveaux pièges : carte S028, câble de charge seule, redémarrage à l'ouverture du port
  série (`09_PIEGES.md`).

Reprise : `docs/START_HERE.md`, branche `main`.
