# Checkpoint du 7 novembre 2026 — `2eb813f`

Version `0.10.0` fusionnée dans `main`, sans Release : mise à jour signalée par la barre
d'état et la LED (D045), adresse IP sur la page À propos. Remplace
`CHECKPOINT_2026-11-07_985a150.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `2eb813f`, poussée et vérifiée sur le dépôt distant ; `feature/maj-icone` fusionnée puis supprimée en local et sur le dépôt distant |
| Version | `0.10.0` ; aucune Release `v0.10.0` publiée (choix du propriétaire) |
| Release GitHub « Latest » | `v0.9.0` (`6bd4b90`), inchangée |
| S024C du banc | Binaire de banc privé `0.9.0 (66e0b4e)`, code de `0.10.0` (USB) |
| S028 du banc | Binaire public `0.9.0`, mis à jour depuis HA (L8) ; réadoptée dans HA (supprimée puis rajoutée), « Salle de bain » |
| Module de la cuisine | Binaire public `0.9.0` |
| Module du séjour | Ancienne version, reflash prévu par le propriétaire |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `e61cd38` | Flèche violette clignotante dans la barre d'état, double éclair violet de la LED (D045) ; cahier L |
| `66e0b4e` | Adresse IP sur À propos (capteur interne) ; image du guide régénérée ; cahier M |
| `3366e00` | Binaire S028 écrit par erreur sur la S024C du banc, rétabli ; deux pièges au `09` |
| `2aeb617` | Cahier M1 à M3, L9 OK |
| `9382258` | Cahier L1 à L10 OK, `VERSION` 0.10.0, doc alignée |
| `2eb813f` | Fusion de `feature/maj-icone` |

## Mesures

| Mesure | Valeur |
|---|---|
| Compilation (code 0) | `hapanel.yaml` RAM 31,3 %, flash 63,7 % ; `hapanel_public.yaml` 32,6 %, 75,3 % ; `hapanel_2432s028_public.yaml` 32,6 %, 74,5 % ; bancs S024C et S028 31,3 à 31,4 %, 63,6 à 64,4 % |
| Mémoire libre, plus grand bloc (G6) | S028, binaire public `0.9.0-dev.99` : 149 Ko libres, plus grand bloc **60 Ko** (96 Ko en K10 sur le binaire de banc) : à suivre (cahier, L10) |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Prochaine étape : rang 1 de `docs/TODO.md` (sécurité) ; puis rang 2 (mise à jour depuis
  l'écran, points 2 à 4) et rang 3 (projet publiable).
- Publication de `v0.10.0` : à décider par le propriétaire (`DEPLOIEMENT_PUBLIC.md` § 1).
  L11 se fera à la Release suivante, sur un module déjà en `0.10.0`.
- Tests qui bloquent une fusion : aucun en attente (`docs/CAHIER_DE_TESTS.md`). Port COM,
  adresse IP et carte branchée à redemander au propriétaire (`09_PIEGES.md`).

Reprise : `docs/START_HERE.md`, branche `main`.
