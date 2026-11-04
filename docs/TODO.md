# TODO — HAPanel

Liste unique du reste à faire (G14).

- **Priorité :** la colonne « Prio » ordonne les développements : on traite le rang 1
  avant le rang 2. L'ordre suit les dépendances, pour ne pas reprendre un travail
  déjà fait (fusionner avant d'ouvrir un nouveau chantier, décider avant de coder,
  le matériel avant le code). Un changement d'ordre se décide avec le propriétaire.
- **Tests :** ils ne sont pas ici mais dans `docs/CAHIER_DE_TESTS.md` (G13), qui dit
  aussi quels tests bloquent quelle fusion.
- **Fini :** une ligne terminée passe dans l'historique, en bas, avec sa date.

## À faire, par priorité

| Prio | Sujet | Dépend de | Branche | Pourquoi à ce rang |
|---|---|---|---|---|
| 1 | Message d'accueil : confirmer B3 (même texte deux fois) ; décider s'il faut empêcher deux fois de suite le même message (entrée texte dans HA, procédure G11) | Cahier B3 refait | à créer | Ne touche que le blueprint de la maison ; à trancher avant de l'enrichir (rangs 7 et 9). |
| 2 | Sécurité : décider de laisser ou non l'autorisation des actions HA sur chaque module (surface plus petite, `08`) ; évaluer l'usurpation de `device_id` (un firmware modifié, avec la clé d'API, pourrait se faire passer pour un autre panneau) et l'inscrire au `08` | — | `docs/…` | À décider avant d'ajouter des commandes (infrarouge) et la mise à jour par HA (rang 3), sinon elles seraient à reprendre. |
| 3 | Mises à jour du parc depuis HA (D037, option C) : 1. le propriétaire tranche l'hébergement (jamais sur Internet : le binaire contient les secrets) et le mode d'installation (bouton ou automatisation) ; 2. firmware `http_request` et entité de mise à jour, publication par `build.ps1`, procédure (G11) et partie du cahier ; 3. mesure de la mémoire pendant le téléchargement ; compatible avec D038 (rang 4) | Rang 2 (surface de la mise à jour) ; réponses au point 1 | à créer | À installer avant de multiplier les modules : l'infrarouge et la suite se déploieront par ce chemin. |
| 4 | Projet publiable (D038) : cadrer avec le propriétaire la licence, le dépôt public, la relecture de la doc (retirer le personnel), la page d'installation, l'adoption par chaque utilisateur ; puis Wi-Fi saisi à l'installation (Improv par USB, portail captif), binaire générique sans secret publié sur GitHub | Rang 3 (même chemin de mise à jour) | à créer | Orientation du projet : à cadrer tôt pour que l'infrarouge et la suite ne mettent rien de propre à la maison dans le firmware. |
| 5 | Infrarouge (P5) : 1. marque et modèle exacts des clims (Midea ou compatible pour la chambre des parents) et emplacement des panneaux ; 2. schéma de la diode sur GPIO22 (transistor, résistances, 3,3 V, connecteur avec GND) ; 3. code (`remote_transmitter`, `midea_ir`, repris de `clim-parents`) | Rang 2 ; réponses du propriétaire au point 1 | à créer | Plus gros chantier : sur une base stable et des règles de sécurité fixées. Le matériel avant le code. En attendant les réponses, passer au rang 6. |
| 6 | Documentation technique, lots 3 à 6 : `lvgl.md`, `liaison_ha.md` ; `led_veille.md`, `message_accueil.md` ; `pages/` ; blueprints (avec extension du script de contrôle) | — | `docs/…` | La barre d'état est fusionnée : les pages ne bougent plus, la doc n'est pas à refaire. |
| 7 | Saint du jour : choisir la source (calendrier dans le blueprint, sans Internet, proposé ; ou service en ligne lu par HA). Il s'affiche sur la ligne de la météo, sans changer le firmware | Rang 1 | à créer | Blueprint de la maison seulement. |
| 8 | LDR : les seuils (0,09 à 0,20 V) viennent du relevé du 31 octobre ; les journaux du 3 novembre montrent 0,9 à 1,094 V (plafond de l'ADC). Le cahier E est validé à l'œil : relever les tensions jour et nuit dans les journaux pour confirmer ou recaler | — | à créer | Petit et isolé ; à faire à l'occasion d'un flash. |
| 9 | Message d'accueil : citer la personne qui arrive (présence des téléphones dans HA) | Rang 1 ; tous les téléphones de la maison connus dans HA | à créer | Dépend d'un préalable du propriétaire. |
| 10 | LED de face avant : autres informations (alerte météo…), à spécifier | D017, rang 5 | à créer | À spécifier après l'infrarouge, pour ne revoir la logique de la LED qu'une fois. |
| 11 | Outillage : mesurer le gain du dossier de compilation séparé du banc | Prochaine fusion | — | Constat seulement, sans développement. |

## Reporté

- `flash_chip: generic` et `sram1_as_iram` : seulement si l'IRAM vient à manquer, après
  mesure de la mémoire de données (D011).

## Historique

### P0 — Cadrage

- [x] Carte : ESP32-2432S024C (D004).
- [x] Intégration : ESPHome en ligne de commande (D005).
- [x] Nom : HAPanel (D006) ; tout passe par Home Assistant (D007).
- [x] Relever la version de Home Assistant dans `00_CONTEXT.md`.

### P1 — Panneau de banc minimal

- [x] `requirements.txt` (ESPHome figé), `secrets.example.yaml`,
      `tools/build.ps1` (injection de `version` et `git_sha`).
- [x] `hapanel.yaml`, `hapanel_banc.yaml`, `packages/base.yaml`,
      `packages/hardware.yaml`, `packages/lvgl.yaml`.
- [x] Valider sur la carte : brochage publié (R6), écran ILI9341
      (orientation, couleurs, accents), tactile CST820 (R1, D009), Wi-Fi,
      OTA par mot de passe.
- [x] Adopter le panneau dans Home Assistant (28 octobre 2026).
- [x] Page « À propos » : version, SHA, mémoire libre et accents vérifiés
      à l'écran ; états « connecté » et « non connecté » (28 octobre 2026).
- [x] Binaire exécuté = `main` (`33bf440`) après reflash OTA sur bloc
      secteur 1 A ; brownout sur le port USB du PC (R7).
- [x] OTA protégée par la clé de l'API au lieu d'un mot de passe (D010).
- [x] Mémoire libre de référence ; premier checkpoint.
- [x] Options d'ESPHome (D011 : révision 3.1 ; les deux autres reportées).
- [x] `VERSION` à `0.1.0`.

### P2 — Premier écran fonctionnel

- [x] Écran d'accueil défini avec le propriétaire (D014, 29 octobre 2026).
- [x] Écran d'accueil et blueprint `ecran_accueil.yaml` (D014), fusionnés
      le 30 octobre 2026 (`ef223f6`) ; `VERSION` 0.2.0.
- [x] Accueil, « indisponible » corrigé en 0.2.1 (`dba8a48`, largeur fixe).
- [x] Anomalie du 30 octobre 2026, 18:18 (commandes non appliquées par HA) : non
      reproduite ; cause probable : automatisation en cours de rechargement. À
      rouvrir si elle se reproduit.
- [x] Blueprint `ecran_accueil.yaml` réimporté ; automatisation `temperature` et
      blueprint `envoyer_valeur` supprimés de HA le 30 octobre 2026.
- [x] Prototype D012 validé le 29 octobre 2026 (`96227cf`), module `hapanel-a85bfc`.
- [x] D013 : « non connecté » vérifié avec `esphome logs` ouvert.
- [x] Signal Wi-Fi exposé dans Home Assistant ; commandes par
      `esphome.hapanel_commande` (D014).

### P3 — Idées du propriétaire du 30 octobre 2026

- [x] Accueil allégé (D015), 0.3.0 ; toucher sur la glissière, température
      extérieure, icônes en couleur (D016), 0.4.0 ; LED et écran éteint par
      inactivité (D017), 0.5.0 : validés le 31 octobre 2026.
- [x] Respiration de la LED selon la lumière (D018) et rétroéclairage selon la pièce
      (D023) : cahier E1 à E7 OK le 4 novembre 2026.
- [x] Réglages de la LED par module (D027) et bouton Accueil masqué sur l'accueil
      (D025) : fusionnés le 2 novembre 2026 ; cahier C1 à C7 OK le 4 novembre 2026.
- [x] Pages Scénarios (D024) et Menu (D025) ; icônes et couleurs (D026) : validées.
- [x] Écrans Météo (D019), Planning (D020) et blueprint unique `module.yaml` (D021) :
      validés le 1er novembre 2026. États dégradés : cahier F et G.
- [x] Retour à l'accueil (D022) : validé ; cas sans HA au cahier (F10).
- [x] Autorisation des actions HA : inutile, testé le 2 novembre 2026 (option
      réactivée ; décision au rang 2).
- [x] Outillage : dossier de compilation séparé du banc, accepté le 3 novembre 2026
      (mesure du gain au rang 11).

### P4 — Idées du propriétaire du 2 novembre 2026

- [x] Message d'accueil (D028) : validé sur le module et dans HA le 3 novembre 2026,
      fusionné dans `main`. Réponses du propriétaire au cadrage : arc-en-ciel soumis
      aux réglages de la LED ; plage horaire réglable ; message 3 min, fermé par un
      toucher ; tous les modules, activable par module ; deux listes de tâches de HA
      (« messages » étiquetés, « message unique ») ; saint du jour fourni par HA.

### P5 — Idées du propriétaire du 3 novembre 2026

- [x] Modèle de la carte confirmé : ESP32-2432S024C, 2,4 pouces (D004 inchangée).
- [x] Broche de la diode infrarouge choisie : GPIO22, sur un connecteur qui porte
      aussi GND et 3,3 V. Orientation : un panneau en vue de chaque clim, diode sur le
      module ; sinon, une automatisation de HA relaie vers l'émetteur ESP-01 de la
      pièce. Référence existante : nœud `clim-parents` (ESP8285, `remote_transmitter`
      sur GPIO4, `carrier_duty_percent: 50%`, `midea_ir`) ; sur le panneau (esp-idf),
      seule la broche change. Infrarouge à vue ; GPIO35 possible pour un récepteur ;
      GPIO21 et GPIO27 exclus ; HeatpumpIR exclu (Arduino seulement, D008).
- [x] Page Réglages (D031), bouton Menu masqué sur le Menu (D025 révisée), tactile
      plus réactif (D009 révisée) : réglages écrits en flash sous 5 s (D034),
      icône d'enregistrement (D035) : cahier H1 à H19 et C2 OK, fusionnés dans `main`
      le 4 novembre 2026 ; `VERSION` 0.6.0.

### P6 — Idées du propriétaire du 4 novembre 2026

- [x] Barre d'état commune et navigation en haut (D036, D025 révisée) : ☰ à gauche,
      titre ou date, disquette, Wi-Fi, point HA ; maison centrée en bas ; bords de la
      dalle laissés noirs. Cahier I1 à I12 OK, fusionnée dans `main` le 4 novembre
      2026 ; `VERSION` 0.7.0.
- [x] Mises à jour du parc : option C retenue (D037, HAP-R096) ; conception au rang 3.
- [x] Orientation : projet publiable (D038, HAP-R099) ; cadrage au rang 4.
