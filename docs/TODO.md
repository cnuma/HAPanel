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
| 1 | Message d'accueil : confirmer B3 (même texte deux fois) ; décider s'il faut empêcher deux fois de suite le même message (entrée texte dans HA, procédure G11) | Cahier B3 refait | à créer | Ne touche que le blueprint de la maison ; à trancher avant de l'enrichir (rangs 9 et 11). |
| 2 | Sécurité : décider de laisser ou non l'autorisation des actions HA sur chaque module (surface plus petite, `08`) ; évaluer l'usurpation de `device_id` (un firmware modifié, avec la clé d'API, pourrait se faire passer pour un autre panneau) et l'inscrire au `08` | — | `docs/…` | À décider avant d'ajouter des commandes (infrarouge) et la mise à jour par HA (D039, faite : surface déjà au `08`), sinon elles seraient à reprendre. |
| 3 | Guide d'installation pour débutant (demande du propriétaire du 5 novembre 2026) : remplacer la procédure de technicien par un pas à pas avec une capture d'écran précise à chaque étape (téléchargement, web.esphome.io, Wi-Fi par Improv, adoption dans HA, blueprint, mise à jour) ; captures prises par le propriétaire en reflashant le premier module de production (cahier J14), recadrées sans nom de réseau, adresse ni clé (G9) ; tester aussi le point d'accès (J9, J10) | — | `docs/guide-installation` | Le premier module de production passe au binaire public (D037 révisée) : les captures se prennent à ce moment. Condition de la publication (rang 5). |
| 4 | Mise à jour depuis l'écran (demande du propriétaire du 5 novembre 2026, décision à rédiger) : 1. icône violette **qui clignote** dans la barre d'état quand une mise à jour attend ce module, comme dans AquaLook (précision du 6 novembre 2026 ; icône d'AquaLook à fournir par le propriétaire) ; 2. bouton « Rechercher une mise à jour » sur la page À propos ; 3. recherche chaque nuit à 3 h (au lieu de toutes les 6 h ; heure de HA) ; 4. bouton violet dans le Menu pour lancer la mise à jour, avec confirmation puis message « Mise à jour en cours, module indisponible ». Binaire public seulement (entité `maj_firmware`) : le binaire privé de l'atelier n'affiche rien | D039 (acceptée) | à créer | Complète l'installation sans HA ; place dans la barre à vérifier (entre le titre et la disquette). |
| 5 | Projet publiable (D038) : cadrer avec le propriétaire la licence (dépôt déjà public, sans licence), la relecture de la doc (retirer le personnel), l'adoption par chaque utilisateur ; binaire générique, Wi-Fi saisi à l'installation et publication sur GitHub faits (D039) | Rang 3 (guide d'installation) | à créer | Orientation du projet : à cadrer tôt pour que l'infrarouge et la suite ne mettent rien de propre à la maison dans le firmware. |
| 6 | Indépendance du matériel (demande du propriétaire du 5 novembre 2026, décision à rédiger ; l'ESP32-2432S024C de 2,4 pouces semble ne plus être fabriqué) : 1. interface construite selon la taille de l'écran déclarée dans les paramètres, et non plus calée sur 320 × 240 ; 2. GPIO configurables : écran, tactile, diode infrarouge, LED d'état, LDR ; 3. pilotes d'écran et de tactile configurables ; 4. au total, un firmware indépendant de la carte. Point à trancher : ESPHome fixe pilotes et broches à la compilation, donc « paramètres » veut dire un fichier de carte par modèle (substitutions et package), et un binaire public par modèle de carte | Rang 5 (cadrage du public visé) ; choix des nouvelles cartes par le propriétaire | à créer | Avant l'infrarouge, dont la broche doit déjà être un paramètre ; chaque page écrite d'ici là serait sinon à reprendre. |
| 7 | Infrarouge (P5) : 1. marque et modèle exacts des clims (Midea ou compatible pour la chambre des parents) et emplacement des panneaux ; 2. schéma de la diode sur GPIO22 (transistor, résistances, 3,3 V, connecteur avec GND) ; 3. code (`remote_transmitter`, `midea_ir`, repris de `clim-parents`) | Rang 2 ; rang 6 (broche en paramètre) ; réponses du propriétaire au point 1 | à créer | Plus gros chantier : sur une base stable et des règles de sécurité fixées. Le matériel avant le code. En attendant les réponses, passer au rang 8. |
| 8 | Documentation technique, lots 3 à 6 : `lvgl.md`, `liaison_ha.md` ; `led_veille.md`, `message_accueil.md` ; `pages/` ; blueprints (avec extension du script de contrôle) | Rang 6 (pages reprises) | `docs/…` | Après l'indépendance du matériel, qui modifie toutes les pages. |
| 9 | Saint du jour : choisir la source (calendrier dans le blueprint, sans Internet, proposé ; ou service en ligne lu par HA). Il s'affiche sur la ligne de la météo, sans changer le firmware | Rang 1 | à créer | Blueprint de la maison seulement. |
| 10 | LDR : les seuils (0,09 à 0,20 V) viennent du relevé du 31 octobre ; les journaux du 3 novembre montrent 0,9 à 1,094 V (plafond de l'ADC). Le cahier E est validé à l'œil : relever les tensions jour et nuit dans les journaux pour confirmer ou recaler | — | à créer | Petit et isolé ; à faire à l'occasion d'un flash. |
| 11 | Message d'accueil : citer la personne qui arrive (présence des téléphones dans HA) | Rang 1 ; tous les téléphones de la maison connus dans HA | à créer | Dépend d'un préalable du propriétaire. |
| 12 | LED de face avant : autres informations (alerte météo…), à spécifier | D017, rang 7 | à créer | À spécifier après l'infrarouge, pour ne revoir la logique de la LED qu'une fois. |
| 13 | Outillage : mesurer le gain du dossier de compilation séparé du banc | Prochaine fusion | — | Constat seulement, sans développement. |

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
      (mesure du gain au rang 13).

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
- [x] Orientation : projet publiable (D038, HAP-R099) ; cadrage au rang 5.
- [x] Mise à jour depuis l'écran demandée le 5 novembre 2026 : rang 4.
- [x] Indépendance du matériel demandée le 5 novembre 2026 (2,4 pouces introuvable) :
      rang 6.

### P7 — Déploiement public (5 novembre 2026)

- [x] Binaire public sans secret publié par GitHub Actions, mise à jour par Wi-Fi
      depuis l'entité « Firmware » de HA, nom de la pièce par le blueprint (D039,
      D040) : cahier J OK (J9, J10, J14 au rang 3), fusionné dans `main` le
      5 novembre 2026 ; `VERSION` 0.8.0.
- [x] D037 révisée : binaire public pour tous les modules de la maison, USB en
      secours ; configurations privées pour l'atelier seulement.
