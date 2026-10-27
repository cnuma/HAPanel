# Manifeste du socle HAPanel

## Origine

- Dépôt source : `cnuma/AquaLook`
- Branche : `main`
- Commit : `d34ef521feef8e150cdea2347d1f4b5834db2f7d` (27 octobre 2026,
  AquaLook 5.20.0, mise en pause)
- Décisions : D001, complétée par D005 (bascule ESPHome)

## Ce qui est repris

Les règles de **méthode** d'AquaLook, adaptées :

| HAPanel | Source AquaLook | Traitement |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md` | adapté |
| `AGENTS.md` | `AGENTS.md` | checklist de démarrage, numérotation (`HAP-R`), impacts d'abord, périmètre minimal, vérification fonctionnelle, port, versionnement, déclencheur checkpoint, procédure de livraison, validation des artefacts, Git ; transposés à ESPHome |
| `docs/START_HERE.md` | `docs/START_HERE.md`, `docs/engineering/03_DOCUMENTATION_GOVERNANCE.md` | fusionnés et adaptés |
| `docs/codex/03_INVARIANTS.md` | `docs/codex/03_INVARIANTS.md` | invariants génériques transposés au YAML (G1 à G10) ; invariants de panneau P1 à P5 nouveaux |
| `docs/codex/04_DEVELOPMENT_RULES.md` | `docs/codex/04_DEVELOPMENT_RULES.md`, `docs/developer/DEV-005` | principes conservés (mémoire, non-blocage, persistance, sécurité, journaux), réécrits pour ESPHome |
| `docs/codex/05_BUILD_AND_TEST.md` | `docs/codex/05_BUILD_AND_TEST.md` | réécrit pour la ligne de commande ESPHome |
| `docs/codex/06_ANTI_REGRESSION.md` | `docs/codex/06_ANTI_REGRESSION.md` | adapté |
| `docs/codex/07_GIT_WORKFLOW.md` | `docs/codex/07_GIT_WORKFLOW.md` | adapté |
| `docs/codex/08_RISKS_AND_DEBT.md` | `docs/codex/08_RISKS_AND_DEBT.md`, `docs/security/SECURITY_RISK_REGISTER.md` | gabarit adapté |
| `docs/codex/10_TASK_HANDOFF.md` | `docs/codex/10_TASK_HANDOFF.md` | adapté |
| `.gitignore` | `.gitignore` | réécrit pour ESPHome |
| `.vscode/extensions.json` | `.vscode/extensions.json` | PlatformIO remplacé par l'extension YAML |

## Retiré avec la bascule ESPHome (D005)

`tools/version_build.py` et `include/BuildInfo.h` (identité de build
PlatformIO), règles C++ et PlatformIO. Le principe d'identité de build est
conservé et sera porté par `tools/build.ps1` (substitutions ESPHome).

## Volontairement non repris

Protocole de segmentation des chats (seule la règle « chat profond au-delà de
R030 » est conservée), référentiel `docs/engineering/`, ADR et architecture
V4, manuel utilisateur, procédures de release et d'OTA, cloud, bancs
`tools/` d'AquaLook.

## Report des évolutions

Une règle de méthode améliorée dans un des deux projets est reportée à la
main dans l'autre, avec mise à jour de ce manifeste.
