# Checkpoint du 10 novembre 2026 — `2f13cf8`

Bouton violet d'À propos : le toucher suivant ouvre la confirmation de mise à jour
(D047, complément), fusionné ; recherche de 3 h et mise à jour depuis l'écran validées
sur tous les modules. Remplace `CHECKPOINT_2026-11-09_5e5f454.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `2f13cf8`, poussée et vérifiée sur le dépôt distant. Branche `feature/maj-bouton-violet` fusionnée, encore présente sur le dépôt distant (suppression à faire) |
| Version | `VERSION` 0.11.1 (Release `v0.11.1` « Latest ») ; `main` contient le bouton violet, non publié. `NOUVEAUTES.md` a déjà la ligne 0.11.2 |
| Page d'installation | `https://cnuma.github.io/HAPanel/`, en 0.11.1 |
| Modules | Tous en 0.11.1, mis à jour depuis l'écran : cuisine et séjour (S024C), salle de bain (S028), Guition 4,3" |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `2913f3b` | Cahier : Q10 et Q12 (S028) OK depuis l'écran |
| `dbd7227` | Bouton violet : global `apropos_maj_trouvee`, script `maj_rechercher` qui ouvre `maj_proposer` si une version a été trouvée, sinon `maj_rechercher_reseau` ; doc d'utilisation, D047, `NOUVEAUTES.md` 0.11.2, O16, O17 |
| `6b7bb7c` | Cahier : O11 OK, Q12 (S024C) OK depuis l'écran ; O16, O17 reportés (accord du propriétaire) |
| `2f13cf8` | Fusion de `feature/maj-bouton-violet` |

## Mesures

| Mesure | Valeur |
|---|---|
| Compilation publique S024C (G6) | RAM 60 232 octets (33,3 %), flash 1 389 183 octets (75,7 %) : +128 octets de RAM, +288 de flash |
| Compilation privée | OK |
| `verifier_doc_technique.py --verifier`, `git diff --check` | OK |

## Suite

- Publier 0.11.2 (bouton violet) avec l'accord du propriétaire : `VERSION`, étiquette
  `v0.11.2`. Puis O15 à la mise à jour (ligne de `NOUVEAUTES.md` sous le titre), O17
  sur un module en 0.11.2, O16 à la Release suivante.
- Résultats attendus du propriétaire : N4 (10 novembre). Puis S6 à la prochaine `-dev`,
  S7, S8 (`docs/CAHIER_DE_TESTS.md`).
- Prochaine étape : place de T18 à fixer (avant la prochaine `-dev`) ; puis T04, T05,
  T06 de `docs/TODO.md`.
- Tests qui bloquent la prochaine fusion : aucun.
- Port COM, adresse IP et carte branchée à redemander au propriétaire.

Reprise : `docs/START_HERE.md`, branche `main`.
