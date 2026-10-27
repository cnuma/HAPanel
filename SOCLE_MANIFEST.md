# Manifeste du socle HAThermostat

## Origine

- Dépôt source : `cnuma/AquaLook`
- Branche : `main`
- Commit : `d34ef521feef8e150cdea2347d1f4b5834db2f7d` (27 octobre 2026,
  AquaLook 5.20.0, mise en pause)
- Décision : D001 (`docs/codex/02_DECISIONS.md`)

## Correspondance des fichiers

| HAThermostat | Source AquaLook | Traitement |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md` | adapté |
| `AGENTS.md` | `AGENTS.md` | règles génériques conservées ; relais, LittleFS, SD, LCD, Web AlwaysData, soak et OTA retirés ; numérotation `AQL-R` → `HAT-R` |
| `docs/START_HERE.md` | `docs/START_HERE.md`, `docs/engineering/03_DOCUMENTATION_GOVERNANCE.md` | fusionnés et adaptés |
| `docs/codex/00_CONTEXT.md` | — | nouveau, à compléter |
| `docs/codex/02_DECISIONS.md` | — | nouveau (D001 à D003) |
| `docs/codex/03_INVARIANTS.md` | `docs/codex/03_INVARIANTS.md` | invariants génériques G1 à G9 extraits ; T1 à T4 proposés |
| `docs/codex/04_DEVELOPMENT_RULES.md` | `docs/codex/04_DEVELOPMENT_RULES.md`, `docs/developer/DEV-005` | génériques conservées ; section carte ESP32-2432S024 ajoutée (D004) |
| `docs/codex/05_BUILD_AND_TEST.md` | `docs/codex/05_BUILD_AND_TEST.md` | adapté, environnements renommés |
| `docs/codex/06_ANTI_REGRESSION.md` | `docs/codex/06_ANTI_REGRESSION.md` | adapté |
| `docs/codex/07_GIT_WORKFLOW.md` | `docs/codex/07_GIT_WORKFLOW.md` | adapté, checkpoints ZIP retirés |
| `docs/codex/08_RISKS_AND_DEBT.md` | `docs/codex/08_RISKS_AND_DEBT.md`, `docs/security/SECURITY_RISK_REGISTER.md` | gabarit adapté |
| `docs/codex/10_TASK_HANDOFF.md` | `docs/codex/10_TASK_HANDOFF.md` | adapté, règles OTA retirées |
| `tools/version_build.py` | `tools/version_build.py` | préfixe `HAT_`, cible OTA retirée |
| `include/BuildInfo.h` | `src/BuildInfo.h` | adapté, déplacé dans `include/` |
| `.gitignore` | `.gitignore` | entrées propres à AquaLook retirées |
| `.vscode/extensions.json` | `.vscode/extensions.json` | identique |

## Volontairement non repris

Protocole de segmentation des chats (seule la règle « chat profond au-delà de
R030 » est conservée), référentiel `docs/engineering/`, ADR et architecture
V4, manuel utilisateur, procédures de release et d'OTA, cloud, bancs
`tools/` d'AquaLook. À reprendre au cas par cas si le projet en a besoin.

## Report des évolutions

Une règle générique améliorée dans un des deux projets est reportée à la main
dans l'autre, avec mise à jour de ce manifeste.
