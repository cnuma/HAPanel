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

- [x] Définir l'écran d'accueil avec le propriétaire (D014, 29 octobre
      2026) : schéma validé, bornes 15 à 25 °C ; mode par glissière
      (remplace l'appui long après essai au banc).
      Banc : thermostat `climate.entree_thermostat` (Versatile Thermostat),
      thermomètre `sensor.sejour_cheminee_radiateur_ema_temperature`.
- [x] Écran d'accueil et blueprint `ecran_accueil.yaml` (D014), fusionnés
      le 30 octobre 2026 (`ef223f6`) : valeurs reçues, consigne ± avec
      confirmation, glissière Éteint / Chauffage dans les deux sens,
      redémarrage du panneau sans blueprint (« non reçu » jusqu'au retour
      des valeurs) validés au banc. Mémoire ≈ 189 Ko libres, bloc 108 Ko.
- [ ] Accueil, tests restants : préréglages (blueprint réimporté, retour
      du propriétaire non consigné), « indisponible » (thermomètre
      désactivé), « périmée » (automatisation désactivée 15 min sans
      redémarrage), HA déconnecté avec `esphome logs` ouvert, centrage des
      icônes ; puis `VERSION` 0.2.0.
- [ ] HA : réimporter `ecran_accueil.yaml` depuis `main` (URL de
      `source_url`), le blueprint ayant été importé depuis la branche.
- [ ] HA : désactiver l'automatisation `temperature` (blueprint
      `envoyer_valeur`), remplacée par l'automatisation de l'accueil.
- [x] Prototype D012 validé le 29 octobre 2026 (`96227cf`) : module
      réadopté sous `hapanel-a85bfc`, blueprint importé, température
      affichée, effacement à la déconnexion et renvoi immédiat à la
      reconnexion (constatés par le propriétaire). Mémoire inchangée
      (≈ 197 Ko libres, bloc 108 Ko). Non testés : « indisponible »,
      « périmée ».
- [ ] D013 : vérifier « non connecté » avec `esphome logs` ouvert (correctif
      flashé, non testé journaux ouverts).
- [x] Signal Wi-Fi exposé dans Home Assistant (entité de diagnostic).
- [x] Commandes du panneau par événement : `esphome.hapanel_commande`
      (D014).

## P3 — Idées du propriétaire (30 octobre 2026), à spécifier avant tout code

- [ ] Chauffage éteint : masquer ou griser fortement les icônes de
      préréglage et la consigne, pour alléger l'écran (P3 : la consigne
      reste lisible ou explicitement absente, jamais trompeuse).
- [ ] Bouton de pied de page « Scénarios » : icône Material Design à
      choisir (par exemple `mdi:play-box-multiple` ou
      `mdi:script-text-play`), scénarios et commandes à définir.
- [ ] Icône de pied de page « Météo » : prévisions sur 3 jours, zone
      paramétrable (entité `weather.*` choisie dans un blueprint, D012).
- [ ] LED de face avant : état du module (connexion HA, anomalie) puis
      autres informations (alerte météo…) ; broches et nature de la LED à
      relever sur la carte réelle (`packages/hardware.yaml`, R6), jamais
      supposées.
- [ ] Photorésistance (LDR) de face avant : baisser la luminosité du
      rétroéclairage (déjà en PWM, `retroeclairage`) selon la lumière de la
      pièce. Broche à relever sur la carte réelle (R6) ; seuils, courbe,
      lissage et luminosité minimale à définir ; l'écran reste lisible et
      réactif sans HA (P5).
