# Checkpoint du 9 novembre 2026 — `5efef73`

Sécurité (ancien rang 1 du TODO) traitée et fusionnée : actions HA refusées aux modules,
usurpation de `device_id` acceptée (D046). Remplace `CHECKPOINT_2026-11-09_7d81a7d.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `5efef73`, poussée et vérifiée sur le dépôt distant |
| Version | `0.10.0` (inchangée, documentation seule) |
| Modules | Cuisine et séjour (S024C), salle de bain (S028) : binaire public `0.10.0 (99a9a10)`, inchangé ; option « actions HA » décochée sur les trois (cahier N1) |
| Branche `docs/securite-actions-ha` | Fusionnée et supprimée (locale et distante) ; règle de permission locale de l'agent pour les branches `feature/`, `fix/`, `docs/`, `chore/` |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `cd14d12` | D046, R11 au `08`, piège `device_id` au `09`, procédure dans `CONFIGURATION.md` § 1, cahier N |
| `8b7e26c`, `bd74e8a` | Cahier : N1, N2 OK, N3 reporté ; D046 : pas de signalement à HA |
| `2ff8753`, `5efef73` | TODO (P13, rangs remontés d'un cran) ; fusion dans `main` |

## Mesures

| Mesure | Valeur |
|---|---|
| `esphome config` (2026.10.1), binaires publics S024C et S028 | Code 0 ; pas de compilation (firmware inchangé depuis `99a9a10`) |
| Mémoire libre, plus grand bloc (G6) | Non remesurés (firmware inchangé) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Prochaine étape : rang 1 de `docs/TODO.md` (mise à jour depuis l'écran, points 2 à 4) ;
  puis rang 2 (projet publiable) et rang 3 (page d'installation par carte).
- Tests qui bloquent la prochaine fusion : aucun. N4 à faire le 10 novembre 2026, sans
  blocage ; N3 au premier scénario choisi (`docs/CAHIER_DE_TESTS.md`).
- Nouveaux pièges : un, au `09_PIEGES.md` (`device_id` d'un événement non fiable).
  Port COM, adresse IP et carte branchée à redemander au propriétaire.

Reprise : `docs/START_HERE.md`, branche `main`.
