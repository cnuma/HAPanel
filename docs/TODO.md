# TODO — HAPanel

Liste unique du reste à faire, par priorité. On avance écran par écran.

## P0 — Cadrage

- [x] Carte : ESP32-2432S024C (D004).
- [x] Intégration : ESPHome en ligne de commande (D005).
- [x] Nom : HAPanel (D006) ; tout passe par Home Assistant (D007).
- [x] Relever la version de Home Assistant dans `00_CONTEXT.md`.

## P1 — Panneau de banc minimal

- [x] `requirements.txt` (ESPHome figé), `secrets.example.yaml`,
      `tools/build.ps1` (injection de `version` et `git_sha`).
- [x] `hapanel.yaml`, `hapanel_banc.yaml`, `packages/base.yaml`,
      `packages/hardware.yaml`, `packages/lvgl.yaml` (compilés, non testés
      sur la carte).
- [x] Valider sur la carte : brochage publié (R6), écran ILI9341
      (orientation, couleurs, accents), tactile CST820 (R1, D009), Wi-Fi,
      OTA par mot de passe.
- [ ] Adopter le panneau dans Home Assistant ; vérifier « connecté » puis
      « non connecté » à l'écran (P2).
- [ ] Page « À propos » : version, SHA, état de connexion, mémoire libre
      (écrite, à vérifier à l'écran, y compris les accents).
- [ ] Décider : OTA protégée par la clé de l'API au lieu d'un mot de passe
      (recommandation d'ESPHome 2026.10).
- [ ] Mesurer la mémoire libre de référence ; premier checkpoint.

## P2 — Premier écran fonctionnel

- [ ] Définir l'écran d'accueil avec le propriétaire (entités lues, actions).
