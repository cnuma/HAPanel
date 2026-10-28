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
- [x] Adopter le panneau dans Home Assistant (28 octobre 2026).
- [x] Page « À propos » : version, SHA, mémoire libre et accents vérifiés
      à l'écran.
- [x] Vérifier sur la page « À propos » l'état « connecté » puis
      « non connecté » (désactivation de l'appareil dans Home Assistant)
      (28 octobre 2026 ; redémarrage de Home Assistant non testé, écarté
      par le propriétaire).
- [x] Binaire exécuté = `main` (`33bf440`) après reflash OTA sur bloc
      secteur 1 A ; brownout sur le port USB du PC (R7).
- [x] Décider : OTA protégée par la clé de l'API au lieu d'un mot de passe
      (D010).
- [x] Mesurer la mémoire libre de référence ; premier checkpoint.
- [x] Décider : options d'ESPHome `sram1_as_iram`, `minimum_chip_revision`
      et `flash_chip` (D011 : révision 3.1 ; les deux autres reportées).
- [x] Passer `VERSION` à `0.1.0` une fois P1 entièrement validé.

## Reporté

- [ ] `flash_chip: generic` et `sram1_as_iram` : seulement si l'IRAM vient à
      manquer, après mesure de la mémoire de données (D011).

## P2 — Premier écran fonctionnel

- [ ] Définir l'écran d'accueil avec le propriétaire. Acquis : température
      du séjour ; allumer et couper le chauffage ; consigne au pas de
      0,5 °C ; date, heure et signal Wi-Fi ; barre de navigation en bas,
      « À propos » derrière un bouton. Manque : attributs du thermostat
      (`hvac_modes`, `min_temp`, `max_temp`), bornes de la consigne.
- [ ] Prototype D012 (firmware unique, valeurs poussées par blueprint) :
      réadoption du module renommé, blueprint importé, température affichée,
      cas indisponible, déconnexion, péremption, mémoire.
- [ ] Signal Wi-Fi exposé dans Home Assistant (entité de diagnostic,
      ajoutée avec le prototype, à vérifier).
- [ ] Commandes du panneau par événement : à concevoir avec l'écran
      d'accueil (D012).
