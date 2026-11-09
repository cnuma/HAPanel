# Checkpoint du 9 novembre 2026 — `7d81a7d`

Release `v0.10.0` publiée et installée sur les trois modules, cahier L11 OK, état des
modules corrigé (le « banc S024C » était la cuisine). Remplace
`CHECKPOINT_2026-11-07_2eb813f.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `7d81a7d`, poussée et vérifiée sur le dépôt distant |
| Version | `0.10.0` |
| Release GitHub « Latest » | `v0.10.0` (`99a9a10`) ; manifestes d'origine rétablis après L11 (`0.10.0`) |
| Modules | Cuisine et séjour (S024C), salle de bain (S028) : binaire public `0.10.0 (99a9a10)`, mis à jour depuis HA ; aucun module d'atelier à part (`00_CONTEXT.md`) |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `99a9a10` | Checkpoint `2eb813f` : branche `feature/maj-icone` supprimée ; étiquette `v0.10.0` |
| `7d81a7d` | Cahier : publication, état réel des modules, L11 OK ; trois pièges au `09` ; TODO et `00_CONTEXT` |

## Mesures

| Mesure | Valeur |
|---|---|
| Publication `v0.10.0` (GitHub Actions) | Code 0, six fichiers, manifestes en `0.10.0` |
| Mémoire libre, plus grand bloc (G6) | Non remesurés ; plus grand bloc de 60 Ko sur le binaire public à suivre (cahier, L10) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Prochaine étape : rang 1 de `docs/TODO.md` (sécurité) ; puis rang 2 (mise à jour depuis
  l'écran, points 2 à 4) et rang 3 (projet publiable).
- Tests qui bloquent la prochaine fusion : aucun (`docs/CAHIER_DE_TESTS.md`).
- Nouveaux pièges : trois, au `09_PIEGES.md` (pas de module d'atelier ; entité Firmware
  vide ; adoption dans les 15 min). Port COM, adresse IP et carte branchée à
  redemander au propriétaire.

Reprise : `docs/START_HERE.md`, branche `main`.
