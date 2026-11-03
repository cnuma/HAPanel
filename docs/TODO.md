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
- [ ] Accueil, non vérifié : « périmée » (automatisation désactivée 16 min
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
- [x] 0.5.0 (D017), validée par le propriétaire le 31 octobre 2026 : LED à la
      couleur du préréglage, rouge clignotant sur anomalie ; écran éteint après
      60 s, premier toucher sans commande.
- [ ] LED un peu trop lumineuse (retour du 31 octobre 2026) : respiration selon
      la lumière de la pièce (D018), fusionnée dans `main` (`d441d31`), reste à
      tester au banc : pièce sombre, blanc, Boost / alerte, influence du
      rétroéclairage sur la LDR. Validé à l'œil le 31 octobre 2026 : respiration,
      intensité en pièce éclairée, orange de Confort (rouge 30 %) distinct du
      vert d'Éco. Révisé le 2 novembre 2026 (respiration trop haute) : de 0 à
      l'ancien niveau bas (plafond 5 % de jour, 1 % de nuit), à valider à l'œil,
      y compris la lisibilité des couleurs à ce niveau.
- [ ] Réglages de la LED par module (D027) et bouton Accueil masqué sur l'accueil
      (D025) : fusionnés dans `main` à la demande du propriétaire le 2 novembre
      2026 (binaire de banc `966fb2d` flashé, démarrage sain, 161,7 Ko libres,
      bloc 110,6 Ko) ; résultats des tests sur le module non rapportés. À
      confirmer : entités « LED », « Intensité LED », « Alerte LED » sur la page
      de l'appareil ; conservation après redémarrage ; valeurs imposées par le
      blueprint reflétées sur la page ; alerte désactivée (HA déconnecté, LED
      muette) ; bouton maison absent de l'accueil, y compris après le retour
      automatique.
- [ ] Outillage, reporté par le propriétaire le 31 octobre 2026 (à reprendre
      devant le module) : `hapanel.yaml` et `hapanel_banc.yaml` partagent
      `.esphome/build/hapanel` ; chaque changement de configuration recompile
      environ 1 500 fichiers (environ 10 min). Option recommandée :
      `build_path: build/hapanel_banc` dans `hapanel_banc.yaml` (première
      compilation complète, environ 430 Mo de plus, gain à mesurer).
- [x] Page « Scénarios » (D024) et page « Menu » (D025) : validées par le
      propriétaire le 1er novembre 2026 (« tout marche »), fusionnées dans `main`.
- [ ] Icône et couleur des boutons de scénarios (D026) : fusionnées à la demande du propriétaire ; à confirmer sur le
      module après réimport du blueprint : 25 icônes, 8 couleurs, nom sur 2 lignes.
- [ ] Scénarios et menu, cas non confirmés séparément : « Refusé par HA », « Pas
      de réponse de HA », entité indisponible, HA déconnecté, noms longs.
- [x] Écran « Météo » (D019), écran « Planning » (D020) et blueprint unique
      `module.yaml` (D021) : validés par le propriétaire le 1er novembre 2026
      (« tout marche »), fusionnés dans `main`. Mémoire : 173 Ko libres, plus
      grand bloc 110 Ko.
- [ ] Météo et planning, cas non confirmés séparément : « non reçu »,
      « indisponible », « périmé », HA déconnecté, planning hors créneau
      (« Prochain à », « Plus rien aujourd'hui »), passage à minuit, jour de
      changement d'heure, 3 ou 4 calendriers.
- [ ] Retour à l'accueil (D022) : « tout marche » du propriétaire le 1er novembre
      2026 ; le cas sans HA (écran resté allumé) n'est pas confirmé séparément.
- [ ] LED de face avant, autres informations (alerte météo…), après D017.
- [ ] Rétroéclairage selon la lumière de la pièce (D023) : codé, à tester sur
      le module. Vérifier la lisibilité en pièce sombre (niveau `retro_nuit`),
      l'absence de variations gênantes et l'influence de l'écran sur la LDR.
      Relevé du 31 octobre 2026 : 0,075 V (plancher) pièce éclairée et sous
      torche, 0,13 à 0,26 V capteur couvert, signal instable.
- [x] Autorisation des actions HA : inutile. Testé par le propriétaire le
      2 novembre 2026 (option désactivée, module redémarré, consigne et scénario
      exécutés), puis option réactivée ; version de HA Core non relevée. Documents
      corrigés.
- [ ] Décider : laisser l'autorisation des actions HA activée ou la désactiver
      sur chaque module (surface plus petite, `08`).
- [ ] Usurpation de `device_id`, à évaluer puis à inscrire au `08` : HA écrit son
      `device_id`, puis les données de l'événement, qui peuvent l'écraser. Un firmware
      modifié, avec la clé d'API, pourrait se faire passer pour un autre panneau.

## P4 — Idées du propriétaire (2 novembre 2026), à spécifier avant tout code

- [ ] Message d'accueil (D028), codé sur `feature/message-accueil`, à tester sur le
      module et dans HA : déclenchement après la période sans déclenchement et
      dans la plage horaire, tirage selon saison et moment, message unique coché,
      ligne météo, fermeture au toucher et après 3 min, arc-en-ciel soumis à
      D027, entité « Message d'accueil » désactivée. Saint du jour reporté.
      Tous les tests en attente : `docs/CAHIER_DE_TESTS.md`.
- [ ] Saint du jour : choisir la source (calendrier dans le blueprint, ou service
      en ligne téléchargé par HA) ; il s'affichera sur la ligne de la météo.
- [ ] Spécification d'origine du message d'accueil, quand quelqu'un arrive : écran allumé, LED en arc-en-ciel
      rapide. Déclencheur choisi dans le blueprint (contact de porte, lumière
      d'une pièce…), seulement après une période sans déclenchement réglable.
      Message selon la saison et l'heure, tiré d'une bibliothèque facile à
      modifier ; messages temporaires affichés une seule fois. Éventuellement
      météo du moment et saint du jour. Réponses du propriétaire (2 novembre
      2026) :
      - arc-en-ciel soumis aux réglages « LED » et « Intensité LED » (D027) ;
      - plage horaire réglable dans le blueprint (par exemple rien de 23 h à 6 h) ;
      - message affiché 3 min, fermé par un toucher ;
      - tous les modules, accueil activable par module depuis HA ;
      - message générique, selon la saison et l'heure ;
      - bibliothèque : deux listes de tâches de HA, « messages » (étiquettes de
        saison et de moment dans la description) et « message unique » (coché
        après affichage) ;
      - saint du jour fourni par HA, pas par le firmware : sans HA, pas de saint.
        Proposition de l'agent : calendrier des saints dans le blueprint, sans
        Internet ni configuration en plus.
- [ ] Évolution du message d'accueil : citer la personne qui arrive (présence
      des téléphones dans HA), quand tous les téléphones de la maison seront
      connus.

## P5 — Idées du propriétaire (3 novembre 2026), à spécifier avant tout code

- [ ] Piloter les clims par infrarouge depuis le module : diode émettrice sur une
      broche libre, composant `remote_transmitter` et plateforme `climate` d'ESPHome
      selon la marque (HeatpumpIR exclu : Arduino seulement, D008). Infrarouge à
      vue : seules les clims visibles depuis le panneau. Broches candidates, à
      confirmer sur la carte S024C (inscriptions de P3 et CN1, photo, essai au
      banc) : GPIO22 pour émettre, GPIO35 (entrée seulement) pour un récepteur qui
      apprend les codes. GPIO21 (tactile) et GPIO27 (rétroéclairage) exclus.
      À fournir par le propriétaire : marque et modèle des clims, nombre visibles
      depuis le panneau.
- [ ] Préparer le schéma électronique de la diode infrarouge : diode, transistor
      de commande, résistances de base et de limitation, alimentation, branchement
      sur le connecteur choisi.
- [ ] Référence : le propriétaire a déjà réalisé, dans un autre chat, une solution
      autonome avec un ESP-01 pré-câblé avec une diode infrarouge, qui marche très
      bien. À reprendre (codes, plateforme `climate`, portée) avant de choisir
      entre la diode sur le module et un émetteur autonome par pièce. Extrait
      transmis le 3 novembre 2026 (nœud `clim-parents`, module générique ESP8285,
      `esp8266`, carte `esp01_1m`, cadre Arduino par défaut de l'ESP8266) :
      `remote_transmitter` sur GPIO4, `carrier_duty_percent: 50%` ; climat
      `midea_ir` (« Climatiseur chambre parents ») ; récepteur de test sur
      GPIO14 (`binary_sensor` brut) ; `web_server` version 3. Sur le panneau
      (esp-idf), `remote_transmitter` et `midea_ir` se reprennent tels quels,
      seule la broche change.
- [ ] **À confirmer : modèle exact de la carte.** Le propriétaire pense avoir une
      2,8 pouces capacitive ; le projet suppose l'ESP32-2432S024C, 2,4 pouces
      (D004). Le brochage de `hardware.yaml` est validé au banc quel que soit le
      nom ; le rétroéclairage sur GPIO27 fait plutôt penser à une 2,4 pouces, sans
      certitude. Vérifier la diagonale de l'affichage (environ 6,1 cm pour
      2,4 pouces, 7,1 cm pour 2,8 pouces) et l'inscription au dos de la carte,
      avec une photo des connecteurs (P3, CN1…). Si c'est une 2,8 pouces : corriger
      D004, `docs/technique/hardware.md`, `docs/technique/README.md` dans un même
      commit, et rechercher les broches libres de ce modèle pour la diode.
- [ ] Points en suspens pour l'infrarouge, à fournir par le propriétaire :
      modèle de la carte (point ci-dessus), photo des connecteurs, marque et
      modèle des clims (Midea ou compatible pour la chambre des parents),
      emplacement des panneaux par rapport aux clims.
- [ ] Orientation du propriétaire (3 novembre 2026) : un panneau sera placé en
      vue de chaque clim, diode sur le module. Sinon, une automatisation de HA
      relaiera la commande vers l'émetteur ESP-01 de la pièce.
- [ ] Réglages sur l'écran du module (demande du propriétaire, rappelée le
      3 novembre 2026 ; D027 ne les avait mis que dans HA) : LED (Respiration,
      Éteinte), Intensité LED, Alerte LED, et **nouvelle demande** : luminosité
      de l'écran, réglable des deux côtés, HA et module. Spécifié : D031 (choix
      1A, 2A, 3A, 4A du propriétaire). À coder après la fusion du message
      d'accueil.
- [ ] Bouton Menu masqué sur la page Menu, seul Accueil reste (révision de D025
      du 3 novembre 2026). À coder après la fusion du message d'accueil.
