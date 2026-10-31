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
- [x] Accueil, tests du 30 octobre 2026 (binaire `ef223f6`) : préréglages,
      HA déconnecté avec `esphome logs` ouvert (D013, reconnexion et renvoi
      des valeurs en 2 s), centrage des icônes et du « − » / « + » validés
      par le propriétaire ; `VERSION` 0.2.0.
- [x] Accueil, « indisponible » (30 octobre 2026) : invisible en 0.2.0
      (label aligné à droite, créé vide, élargi hors de l'écran) ; corrigé
      en 0.2.1 (`dba8a48`, largeur fixe) et constaté à l'écran. Méthode :
      Outils de développement › États, thermomètre forcé à `unavailable`.
- [ ] Accueil, non vérifié : « périmée » (automatisation désactivée 15 min
      sans redémarrage) ; même label que « indisponible », corrigé en 0.2.1.
- [x] Anomalie du 30 octobre 2026, 18:18 : deux « mode envoye off » et une
      « consigne envoyee 20.5 » non appliqués par HA alors que l'API était
      connectée (le panneau est revenu à l'état réel après 10 s, comme
      prévu). Non reproduite à 21:29 (0.2.0) : coupure et remise du
      chauffage confirmées en moins de 130 ms. Cause probable :
      automatisation en cours de rechargement (réimport du blueprint,
      valeurs renvoyées à 18:17:17). À rouvrir si elle se reproduit.
- [x] HA : blueprint `ecran_accueil.yaml` à jour (`source_url` pointe
      sur `main` depuis sa création ; réimporté le 30 octobre 2026).
- [x] HA : automatisation `temperature` et blueprint `envoyer_valeur`
      supprimés de HA le 30 octobre 2026 (constaté : seul « HAPanel —
      écran d'accueil » reste, utilisé par une automatisation). Le
      blueprint reste dans le dépôt.
- [x] Prototype D012 validé le 29 octobre 2026 (`96227cf`) : module
      réadopté sous `hapanel-a85bfc`, blueprint importé, température
      affichée, effacement à la déconnexion et renvoi immédiat à la
      reconnexion (constatés par le propriétaire). Mémoire inchangée
      (≈ 197 Ko libres, bloc 108 Ko). Non testés : « indisponible »,
      « périmée ».
- [x] D013 : « non connecté » vérifié avec `esphome logs` ouvert
      (30 octobre 2026).
- [x] Signal Wi-Fi exposé dans Home Assistant (entité de diagnostic).
- [x] Commandes du panneau par événement : `esphome.hapanel_commande`
      (D014).

## P3 — Idées du propriétaire (30 octobre 2026), à spécifier avant tout code

- [x] Accueil allégé (D015), version 0.3.0 (`a81d3bb`), validé à l'écran par
      le propriétaire le 31 octobre 2026 : chauffage éteint, préréglages et
      consigne masqués et non réglables ; HA déconnecté, bandeau + message
      selon la cause (« Pas de Wi-Fi » / « Pas de communication avec Home
      Assistant ») + navigation.
- [x] Blueprint D015 : réimporté dans HA (automatisation reconfigurée) et
      refus de `chauffage_consigne` thermostat `off` validé le 31 octobre 2026.
- [x] 0.4.0 (D016), validée par le propriétaire le 31 octobre 2026 : toucher
      sur la glissière, température extérieure
      (`sensor.exterieur_temperature_humidite_temperature` au banc, choisie
      dans le blueprint), icônes de préréglage en couleur.
- [ ] 0.5.0 (D017), à valider à l'écran : LED à la couleur du préréglage,
      rouge clignotant sur anomalie ; écran éteint après 60 s, premier toucher
      sans commande.
- [ ] Bouton de pied de page « Scénarios » : icône Material Design à
      choisir (par exemple `mdi:play-box-multiple` ou
      `mdi:script-text-play`), scénarios et commandes à définir.
- [ ] Icône de pied de page « Météo » : prévisions sur 3 jours, zone
      paramétrable (entité `weather.*` choisie dans un blueprint, D012).
- [ ] LED de face avant, autres informations (alerte météo…), après D017.
- [ ] Photorésistance (LDR) de face avant : baisser la luminosité du
      rétroéclairage (déjà en PWM, `retroeclairage`) selon la lumière de la
      pièce. Relevé le 31 octobre 2026 : GPIO34, atténuation 0 dB, 0,075 V
      (plancher) pièce éclairée et sous torche, 0,13 à 0,26 V capteur couvert,
      signal instable : la tension monte dans le noir et ne distingue pas les
      niveaux de lumière courants. Seuils, courbe, lissage et luminosité
      minimale à définir ; l'écran reste lisible et réactif sans HA (P5).
