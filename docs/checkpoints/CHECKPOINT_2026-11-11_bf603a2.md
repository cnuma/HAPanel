# Checkpoint du 11 novembre 2026 — `bf603a2`

Release `v0.13.0` publiée, ménage des branches fait, T20 (LED WS2812 externe) ajouté au
TODO. Remplace `CHECKPOINT_2026-11-11_380945c.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `bf603a2`, poussée et vérifiée sur le dépôt distant ; aucune autre branche, locale ou distante ; dossier `..\HAPanel-t12` supprimé |
| Version | `VERSION` 0.13.0 ; Release `v0.13.0` (`1500d0c`) « Latest », page d'installation en 0.13.0 (cahier, Résultats) |
| Modules | Guition 4,3" : `0.13.0-dev (6405191)` ; cuisine, séjour (S024C) et salle de bain (S028) : 0.12.0 ; mise à jour vers 0.13.0 à faire par le propriétaire. Blueprint du module importé depuis l'ancienne branche T12 : à réimporter depuis `main` (`05_BUILD_AND_TEST.md`, « Blueprint importé depuis une branche ») |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `1500d0c` | Checkpoint précédent ; étiquette `v0.13.0` posée sur ce commit |
| `b939104`, `bf603a2` | TODO : T20, LED WS2812 externe sur tous les modules ; fusion de `docs/t20-led-externe` |

## Mesures

| Mesure | Valeur |
|---|---|
| Compilation | Aucun YAML modifié depuis `380945c` : mesures du checkpoint précédent valables ; les trois binaires publics compilés par la publication (code 0) |
| Mémoire libre, plus grand bloc (G6) | Non relevés |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK, OK |

## Suite

- Premiers sujets de `docs/TODO.md` : T04, T05, T06 ; T20 ajouté en fin de liste, place
  et rapprochement avec T19 et T05 à fixer avec le propriétaire.
- Tests en attente : X10, O15, O17 à la mise à jour des modules en 0.13.0 ; W2, W4 à
  la prochaine étiquette `-dev` (`docs/CAHIER_DE_TESTS.md`).
- Tests qui bloquent la prochaine fusion : aucun.
- Nouveaux pièges : aucun.
- Port COM, adresse IP et carte branchée à redemander au propriétaire.

Reprise : `docs/START_HERE.md`, branche `main`.
