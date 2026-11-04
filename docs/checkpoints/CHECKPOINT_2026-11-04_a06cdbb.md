# Checkpoint du 4 novembre 2026 — `a06cdbb`

Barre d'état commune et navigation en haut (D036) validées par le propriétaire et
fusionnées dans `main` ; version 0.7.0. Remplace `CHECKPOINT_2026-11-04_049e8b7.md`.

## État

| Rubrique | Valeur |
|---|---|
| Branche | `main`, `a06cdbb`, poussée et vérifiée sur le dépôt distant |
| Version | `0.7.0` |
| Binaire sur le module de banc | `0.7.0-dev (7642307)` (banc), même code que la fusion |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|
| `bffcabe` | Fusion de `feature/barre-etat` : barre d'état de 34 px en haut de toutes les pages (☰ à gauche, titre ou date, disquette, Wi-Fi, point HA), maison centrée en bas, pas de barre du bas sur l'accueil (D036, D025 et D035 révisées) ; bords de la dalle laissés noirs ; procédure de réimport d'un blueprint de test (`CONFIGURATION.md` § 2) |
| `a06cdbb` | Statut : cahier I1 à I12 OK ; D036 validée ; TODO renuméroté ; `VERSION` 0.7.0 |

## Mesures

| Mesure | Valeur |
|---|---|
| Compilation production (`hapanel.yaml`, `a06cdbb`) | OK ; RAM 31,2 % (56 472 octets) ; flash 63,6 % (1 166 795 octets), 36 % libres dans la partition |
| Compilation banc (`7642307`) | OK ; RAM 31,3 % ; flash 64,3 % |
| Mémoire libre au démarrage (banc, G6) | 151 636 octets (`2f00f00`) ; plus grand bloc 98 304 octets |
| `verifier_doc_technique.py --verifier`, `git diff --check` | sans écart |

## Suite

- Prochaine étape : rang 1 de `docs/TODO.md` : message d'accueil, B3 et décision sur
  la répétition du même message.
- Tests qui bloquent la prochaine fusion : aucun ouvert. Restent au cahier, sans
  bloquer : B3 à refaire, P3, A6 à A12, B4 à B9, F, G1, G2, G4.
- Nouveaux pièges : bords de la dalle (dernière rangée qui réapparaît sur la
  première), `top_layer` sans texte blanc hérité : ajoutés à
  `docs/codex/09_PIEGES.md` et à `docs/technique/hardware.md`.

Reprise : `docs/START_HERE.md`, branche `main`.
