# TODO — HAPanel

Liste unique du reste à faire, par priorité. On avance écran par écran.

## P0 — Cadrage

- [x] Carte : ESP32-2432S024C (D004).
- [x] Intégration : ESPHome en ligne de commande (D005).
- [x] Nom : HAPanel (D006) ; tout passe par Home Assistant (D007).
- [ ] Relever la version de Home Assistant dans `00_CONTEXT.md`.

## P1 — Panneau de banc minimal

- [ ] `requirements.txt` (ESPHome figé), `secrets.example.yaml`,
      `tools/build.ps1` (injection de `version` et `git_sha`).
- [ ] `hapanel.yaml`, `hapanel_banc.yaml`, `packages/base.yaml`,
      `packages/hardware.yaml`, `packages/lvgl.yaml`.
- [ ] Valider sur la carte : écran (contrôleur ILI9341 ou ST7789,
      orientation, couleurs), tactile CST820 (risque R1), Wi-Fi, connexion
      chiffrée à Home Assistant, OTA.
- [ ] Page « À propos » : version, SHA, état de connexion, mémoire libre.
- [ ] Mesurer la mémoire libre de référence ; premier checkpoint.

## P2 — Premier écran fonctionnel

- [ ] Définir l'écran d'accueil avec le propriétaire (entités lues, actions).
