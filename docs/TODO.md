# TODO — HAThermostat

Liste unique du reste à faire, par priorité.

## P0 — Cadrage (bloquant pour tout code)

- [ ] Trancher le mode d'intégration Home Assistant : MQTT avec
      auto-découverte (firmware C++) ou ESPHome (YAML) ; confirmer ou
      remplacer D002.
- [ ] Fixer la carte ESP32-S3 exacte (flash, PSRAM) dans `00_CONTEXT.md`.
- [ ] Fixer capteurs, organe commandé et étage de sortie.
- [ ] Valider les invariants T1 à T4.

## P1 — Squelette firmware

- [ ] Créer `platformio.ini` (`HAThermostat_s3`, `HAThermostat_s3_banc`)
      selon `05_BUILD_AND_TEST.md`.
- [ ] `src/main.cpp` minimal : sortie en état sûr, bannière de boot depuis
      `BuildInfo`, bilan de fin de boot.
- [ ] Premier checkpoint après compilation et boot validés sur la carte.
