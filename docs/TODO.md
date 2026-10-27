# TODO — HAThermostat

Liste unique du reste à faire, par priorité.

## P0 — Cadrage (bloquant pour tout code)

- [ ] Trancher le mode d'intégration Home Assistant : MQTT avec
      auto-découverte (firmware C++) ou ESPHome (YAML) ; confirmer ou
      remplacer D002.
- [x] Choisir la carte : ESP32-2432S024 (D004).
- [ ] Confirmer sur la carte reçue : variante tactile (R, C ou N), contrôleur
      d'écran, taille de flash ; relever les GPIO libres des connecteurs.
- [ ] Fixer capteurs, organe commandé et étage de sortie.
- [ ] Valider les invariants T1 à T4.

## P1 — Squelette firmware

- [ ] Créer `platformio.ini` (`HAThermostat`, `HAThermostat_banc`)
      selon `05_BUILD_AND_TEST.md`.
- [ ] `src/main.cpp` minimal : sortie en état sûr, bannière de boot depuis
      `BuildInfo`, bilan de fin de boot.
- [ ] Premier checkpoint après compilation et boot validés sur la carte.
