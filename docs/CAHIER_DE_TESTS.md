# Cahier de tests — HAPanel

Tous les tests lancés et pas encore confirmés, en un seul endroit, pour n'en oublier
aucun. Chaque ligne se coche **OK** ou **KO** ; en cas de KO, noter ce qui a été vu
(et l'heure, pour retrouver les journaux).

- **Module :** `hapanel-a85bfc`, binaire de banc `0.6.0-dev (20dda6e)`, branche
  `feature/reglages-ecran`, flashé le 3 novembre 2026. Vérifier l'entité « Version » sur la page de l'appareil avant de
  commencer.
- **Ordre :** d'abord les tests qui bloquent une fusion (colonne « Bloque la fusion
  de ») ; les autres se font quand l'occasion se présente.
- **Codes (G13) :** une lettre par fonction, puis un numéro. Un code n'est jamais
  réattribué : un test retiré est barré, un test ajouté prend le numéro suivant.
- **Colonne « Bloque la fusion de » (G13) :** la branche que ce test doit valider
  avant sa fusion dans `main` ; « (fusionnée) » une fois fusionnée ; « — » si le
  test ne bloque aucune fusion.
- **Rapport :** donner les numéros KO (par exemple « A7 KO : … ») ; les tests non faits
  restent vides.

## Résultats

| Date | Binaire | Partie | Résultat | Suite |
|---|---|---|---|---|
| 3 novembre 2026 | `6ec8bc4` | A | OK, sauf texte gris sombre sur noir, illisible | Corrigé (`5134e69`) : texte blanc ; à revoir après flash |
| 3 novembre 2026 | `6ec8bc4` | B | OK, même défaut de couleur | Idem |
| 3 novembre 2026 | `6ec8bc4` | C | KO : « pas de menu de réglage sur le module » | À préciser : les réglages D027 sont sur la page de l'appareil dans HA, pas sur l'écran du module |
| 3 novembre 2026 | `6ec8bc4` | D | OK | |
| 3 novembre 2026 | `6ec8bc4` | E | KO, sans détail | Numéros et constats à préciser |
| 3 novembre 2026 | `d67b9c0` | A1 | Couleur OK ; accent de « écran » absent du pied de page | Corrigé (`bade90a`) : police du projet sur tout le message |
| 3 novembre 2026 | `dec159c` | A1 | OK : **A et B validés**, fusion dans `main` | |
| 3 novembre 2026 | `dec159c` | E | KO : aucune variation de la LED ni de l'écran | Journaux à 22 h 30 : `LDR 1.094 V` fixe, plafond de l'ADC en `0db` (relevés du 31 octobre : 0,075 à 0,26 V). Mesure saturée, donc obscurité toujours maximale. Diagnostic : éclairer la LDR à la lampe pendant la lecture des journaux |
| 3 novembre 2026 | `bc6f66e` | H | Page Réglages OK, tactile bien plus réactif, luminosité suit la pièce mais trop lentement ; tuile Accueil du Menu en doublon ; interrupteur à l'arrêt gris confondu avec « grisé = imposé » et peu lisible ; « Alerte LED » bloquée | Corrigé (`20dda6e`) : tuile retirée, cadenas, interrupteur sur fond sombre, LDR moyennée sur 5 s. « Alerte LED » était imposée par l'automatisation (`led_alerte on` dans les journaux) : la mettre sur « Ne pas imposer » |
| 4 novembre 2026 | `20dda6e` | C, E, G, H | OK : C1, C6, C7 ; **E1 à E7** (E levé) ; G3 ; H1 à H9, H15 | Restent : C2 à C5, F, G1, G2, G4, H10 à H14 |
| 4 novembre 2026 | `20dda6e` | P | OK : P1, P2, P4, P5 | P3 (liste « Messages uniques ») non rapporté |
| 4 novembre 2026 | `20dda6e` | A | OK : A1 à A5, cochés un à un (A et B validés en bloc le 3 novembre) | A6 à A13 non rapportés un à un |
| 4 novembre 2026 | `20dda6e` | B | OK : B1, B2. B3 : l'écran se rallume (l'automatisation a bien envoyé) mais le texte est le même qu'en B1 | Tirage au hasard parmi 7 à 10 messages selon l'heure : une répétition est possible (environ 1 fois sur 9). À refaire 3 fois en notant les textes ; toujours le même : message unique non coché (P3) ou défaut du tirage, voir la trace |
| 4 novembre 2026 | `20dda6e` | A, C | OK : A13, C3, C5 ; C4 sauf redémarrage. **KO : C2**, réglages LED et écran perdus au redémarrage | Cause : ESPHome n'écrit la flash que toutes les 60 s, une coupure avant perd le réglage. Corrigé (D034) : écriture sous 5 s ; C2 à refaire après flash, en attendant 10 s avant de couper |

| Partie | Sujet | Bloque la fusion de |
|---|---|---|
| A | Message d'accueil, côté module (D028) | `feature/message-accueil` (fusionnée) |
| B | Message d'accueil, côté blueprint (D028) | `feature/message-accueil` (fusionnée) |
| C | Réglages de la LED par module (D027) et bouton Accueil (D025) | `feature/reglages-ecran` (C2 seulement) |
| D | Icônes et couleurs des scénarios (D026) | — |
| E | LED selon la lumière (D018) et rétroéclairage (D023) | — |
| F | Cas d'erreur jamais confirmés séparément | — |
| G | Cas qui demandent une date particulière | — |
| H | Page Réglages (D031), menu (D025 révisée), tactile (D009 révisée) | `feature/reglages-ecran` |

## Préparation (une fois, avant A et B)

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| P1 | Page de l'appareil `hapanel-a85bfc`, rubrique Configuration | Entité **Message d'accueil** présente et activée | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| P2 | Créer la liste « Messages d'accueil » et exécuter **une fois** le script `docs/exemples/messages_accueil.yaml` (voir `CONFIGURATION.md` § 6) | 27 tâches dans la liste | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| P3 | Créer la liste « Messages uniques » (vide pour l'instant) | Liste présente | `feature/message-accueil` (fusionnée) | |
| P4 | Importer le blueprint (lien de `CONFIGURATION.md` § 6) ; s'il a été importé depuis la branche `feature/message-accueil`, le réimporter depuis `main` | Blueprint « HAPanel — message d'accueil » listé | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| P5 | Créer l'automatisation : Panneaux = le module ; Déclencheurs = `binary_sensor.entree_capteur_porte_entree` ; Période sans déclenchement = **1 min** pour les tests ; les deux listes ; Météo = l'entité `weather` | Automatisation enregistrée, sans erreur | `feature/message-accueil` (fusionnée) | OK 4 nov. |

## A — Message d'accueil, côté module

Sans passer par la porte : **Outils de développement › Actions**, action
`esphome.hapanel_a85bfc_message_accueil`, champs `texte` et `infos`.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| A1 | Envoyer `texte` = « Test d'accueil », `infos` = « Dehors : 12 °C » | Message plein écran, fond noir, par-dessus la barre de navigation ; croix en haut à droite ; ligne grise d'informations ; « Touchez l'écran pour fermer » en bas | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| A2 | Pendant A1, regarder la LED | Arc-en-ciel, si la LED est autorisée (entité « LED », D027) | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| A3 | Toucher la croix | Le message se ferme ; la page d'en dessous revient | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| A4 | Renvoyer, puis toucher l'écran **à l'endroit d'un bouton** de la page d'en dessous | Le message se ferme ; le bouton n'est **pas** actionné | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| A5 | Renvoyer, ne rien toucher, chronométrer | Fermeture seule après 3 min (± 1 s) | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| A6 | Attendre la mise en veille de l'écran (60 s sans toucher), puis envoyer | L'écran se rallume et montre le message | `feature/message-accueil` (fusionnée) | |
| A7 | Envoyer un texte d'environ 150 caractères avec accents | Texte coupé en lignes, centré, lisible ; aucun caractère bizarre | `feature/message-accueil` (fusionnée) | |
| A8 | Envoyer un texte de plus de 240 caractères | Texte tronqué proprement, sans caractère cassé à la fin | `feature/message-accueil` (fusionnée) | |
| A9 | Envoyer `texte` vide | Rien ne s'affiche | `feature/message-accueil` (fusionnée) | |
| A10 | Désactiver l'entité « Message d'accueil », puis envoyer | Rien ne s'affiche | `feature/message-accueil` (fusionnée) | |
| A11 | Message affiché, puis désactiver l'entité « Message d'accueil » | Le message se ferme | `feature/message-accueil` (fusionnée) | |
| A12 | Réactiver l'entité, redémarrer le module (bouton Redémarrer ou coupure) | Entité toujours activée après le redémarrage | `feature/message-accueil` (fusionnée) | |
| A13 | Message affiché, puis couper la liaison avec HA (Paramètres › Appareils et services › ESPHome › `hapanel-a85bfc` › ⋮ › Désactiver ; réactiver ensuite) | Le message se ferme ; l'écran « HA déconnecté » est visible | `feature/message-accueil` (fusionnée) | OK 4 nov. |

## B — Message d'accueil, côté blueprint

Chaque déclenchement : noter le message affiché. En cas d'absence, ouvrir les
**Traces** de l'automatisation : elles disent quelle condition a bloqué.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| B1 | Porte fermée et rien touché depuis plus d'1 min, entre 6 h et 23 h : ouvrir la porte | Message tiré de la liste, avec la ligne météo | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| B2 | Refermer et rouvrir aussitôt | **Pas** de nouveau message (période sans déclenchement) | `feature/message-accueil` (fusionnée) | OK 4 nov. |
| B3 | Après 1 min de calme, rouvrir | Nouveau message | `feature/message-accueil` (fusionnée) | À confirmer 4 nov. : même texte qu'en B1 |
| B4 | Ajouter une tâche « Test unique » dans « Messages uniques », attendre 1 min, ouvrir | « Test unique » s'affiche, puis la tâche est **cochée** dans la liste | `feature/message-accueil` (fusionnée) | |
| B5 | Attendre 1 min, ouvrir | De nouveau un message de la liste ordinaire | `feature/message-accueil` (fusionnée) | |
| B6 | Sur 4 ou 5 déclenchements, comparer les messages aux descriptions de leurs tâches | Seulement des messages sans étiquette, ou étiquetés « automne » et du moment de la journée (« soir » de 18 h à 22 h, « nuit » après 22 h) | `feature/message-accueil` (fusionnée) | |
| B7 | Changer temporairement la plage (« jusqu'à » une heure déjà passée), attendre 1 min, ouvrir | Pas de message ; la trace montre la condition d'horaire | `feature/message-accueil` (fusionnée) | |
| B8 | Remettre la plage ; mettre l'entité « LED » sur éteinte (D027), déclencher | Message affiché, **sans** arc-en-ciel | `feature/message-accueil` (fusionnée) | |
| B9 | **Fin des tests :** remettre la période sans déclenchement à 30 min et la LED à son réglage | Réglages de tous les jours rétablis | `feature/message-accueil` (fusionnée) | |

## C — Réglages de la LED par module (D027) et bouton Accueil (D025)

Binaire `966fb2d` et suivants, jamais rapportés.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| C1 | Page de l'appareil | Entités « LED », « Intensité LED » et « Alerte LED » présentes | — | OK 4 nov. |
| C2 | Changer « Intensité LED » et « Intensité écran », attendre 10 s, couper l'alimentation du module puis la rétablir | Valeurs conservées | `feature/reglages-ecran` | KO 4 nov. (valeurs perdues) ; corrigé (D034), à refaire |
| C3 | Dans le blueprint « module », imposer une valeur LED, enregistrer | La valeur imposée apparaît sur la page de l'appareil | — | OK 4 nov. |
| C4 | Choisir « Ne pas imposer », régler à la main sur la page de l'appareil | Le réglage manuel reste | — | OK 4 nov. (sauf redémarrage, voir C2) |
| C5 | « Alerte LED » désactivée, puis couper HA (comme A13) | La LED reste muette (pas de rouge clignotant) | — | OK 4 nov. |
| C6 | Écran d'accueil | Pas de bouton maison dans la barre | — | OK 4 nov. |
| C7 | Aller sur une autre page, attendre le retour automatique à l'accueil | Toujours pas de bouton maison sur l'accueil | — | OK 4 nov. |

## D — Icônes et couleurs des scénarios (D026)

Après réimport du blueprint « module » depuis `main`.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| D1 | Choisir une icône différente pour chaque bouton de scénario | Icônes affichées comme choisies | — | |
| D2 | Essayer plusieurs des 8 couleurs | Couleurs affichées comme choisies | — | |
| D3 | Donner un nom long à un scénario | Nom sur 2 lignes, sans débordement | — | |

## E — LED selon la lumière (D018) et rétroéclairage (D023)

À faire le soir, lumière allumée puis éteinte.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| E1 | Pièce éclairée : regarder la respiration de la LED | Monte de 0 à environ 5 %, discrète ; couleur du préréglage lisible | — | OK 4 nov. |
| E2 | Pièce sombre (attendre 10 s, la mesure est moyennée) | Respiration plus faible (environ 1 %), couleur encore reconnaissable | — | OK 4 nov. |
| E3 | Préréglage Confort, puis Éco | Orange et vert bien distincts, de jour comme de nuit | — | OK 4 nov. |
| E4 | Boost, ou une alerte | Signal visible, y compris en pièce sombre | — | OK 4 nov. |
| E5 | Pièce sombre : lire l'écran | Lisible sans éblouir (niveau `retro_nuit`) | — | OK 4 nov. |
| E6 | Allumer puis éteindre la lumière de la pièce | Le rétroéclairage suit en moins de 10 s, sans clignoter ni varier sans cesse (binaire `20dda6e` et suivants ; 1 min avant) | — | OK 4 nov. |
| E7 | Pièce sombre, écran allumé puis en veille | La luminosité de l'écran ne fausse pas la mesure (pas de va-et-vient) | — | OK 4 nov. |

## F — Cas d'erreur jamais confirmés séparément

Méthode pour « indisponible » : **Outils de développement › États**, choisir l'entité,
mettre l'état à `unavailable`, **Définir l'état** (HA remet la vraie valeur à la
mesure suivante).

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| F1 | Accueil : désactiver l'automatisation « module » 16 min, sans redémarrer | Température « périmée » | — | |
| F2 | Scénarios : choisir un scénario dont l'entité est mise `unavailable`, l'actionner | « Refusé par HA » | — | |
| F3 | Scénarios : automatisation « module » désactivée, actionner un scénario | « Pas de réponse de HA » | — | |
| F4 | Scénarios et menu : HA coupé (comme A13) | Écran « HA déconnecté », aucune commande envoyée | — | |
| F5 | Scénarios : nom très long | Affiché sans déborder | — | |
| F6 | Météo : entité `weather` mise `unavailable` | « indisponible » | — | |
| F7 | Météo et planning : automatisation « module » désactivée 16 min | « périmé » | — | |
| F8 | Météo et planning : redémarrer le module, automatisation désactivée | « non reçu » | — | |
| F9 | Planning : regarder en soirée, après le dernier créneau | « Plus rien aujourd'hui », ou « Prochain à » | — | |
| F10 | Retour à l'accueil (D022) : HA coupé, écran resté allumé sur une autre page | Retour automatique à l'accueil quand même | — | |
| F11 | Fin : réactiver tout ce qui a été désactivé | Automatisations et intégration actives | — | |

## G — Cas qui demandent une date particulière

À noter quand l'occasion se présente.

| N° | Quand | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| G1 | Passage à minuit, écran Planning ouvert | Le planning bascule sur le nouveau jour | — | |
| G2 | Changement d'heure (28 mars 2027) | Planning et heures justes | — | |
| G3 | 3 ou 4 calendriers dans le blueprint « module » | Tous affichés sur la page Planning | — | OK 4 nov. |
| G4 | Message d'accueil en hiver (à partir du 21 décembre) | Messages « hiver » tirés | — | |

## H — Page Réglages, menu et tactile

Branche `feature/reglages-ecran`. Avant H4 : **importer le blueprint « module »
depuis la branche** (Paramètres › Automatisations et scènes › Blueprints › Importer
un blueprint), en acceptant de remplacer l'existant, avec l'adresse
`https://github.com/cnuma/HAPanel/blob/feature/reglages-ecran/blueprints/automation/hapanel/module.yaml`.
**Pas** « Réimporter le blueprint » : il reprendrait la version de `main`. Rouvrir
ensuite l'automatisation du module et l'enregistrer.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| H1 | Toucher brièvement, comme sur un téléphone, les boutons de la barre et des tuiles | Chaque toucher bref est pris en compte, sans laisser le doigt | `feature/reglages-ecran` | OK 4 nov. |
| H2 | Ouvrir le Menu | Seul le bouton maison reste dans la barre ; pas de tuile Accueil ; tuiles Météo, Planning, Scénarios, **Réglages**, À propos | `feature/reglages-ecran` | OK 4 nov. |
| H3 | Quitter le Menu par une tuile | Le bouton Menu revient sur la nouvelle page | `feature/reglages-ecran` | OK 4 nov. |
| H4 | Ouvrir Réglages, blueprint sur « Ne pas imposer » partout | 4 réglages actifs, mêmes valeurs que la page de l'appareil dans HA ; aucun cadenas ; interrupteur à l'arrêt lisible (fond sombre bordé, bouton blanc) | `feature/reglages-ecran` | OK 4 nov. |
| H5 | Basculer « LED » | La LED s'éteint ou reprend sa respiration ; « LED » change aussi sur la page de l'appareil | `feature/reglages-ecran` | OK 4 nov. |
| H6 | Glisser « Intensité LED », relâcher | Valeur affichée pendant le glissement, par pas de 5 ; LED et page de l'appareil suivent au relâchement | `feature/reglages-ecran` | OK 4 nov. |
| H7 | Basculer « Alerte LED » | Même valeur sur la page de l'appareil | `feature/reglages-ecran` | OK 4 nov. |
| H8 | Glisser « Intensité écran » jusqu'à 20 % | L'écran baisse aussitôt sans devenir illisible (plancher) | `feature/reglages-ecran` | OK 4 nov. |
| H9 | Changer « Intensité écran » sur la page de l'appareil | Le curseur de la page Réglages suit | `feature/reglages-ecran` | OK 4 nov. |
| H10 | Redémarrer le module | Les 4 réglages sont conservés | `feature/reglages-ecran` | |
| H11 | Dans le blueprint, imposer « Alerte LED », enregistrer | Sur l'écran, cadenas devant Alerte LED, qui ne réagit plus ; « imposé par HA » avec un cadenas en bas | `feature/reglages-ecran` | |
| H12 | Remettre « Ne pas imposer », enregistrer | Alerte LED de nouveau modifiable, cadenas et mention disparus | `feature/reglages-ecran` | |
| H13 | Rester 1 min sur Réglages sans toucher | Retour à l'accueil, puis écran éteint | `feature/reglages-ecran` | |
| H14 | HA coupé (comme A13), ouvrir Réglages | La page marche, réglages modifiables | `feature/reglages-ecran` | |
| H15 | Éteindre la lumière d'une pièce éclairée | L'écran baisse en moins de 10 s, sans clignoter ensuite | `feature/reglages-ecran` | OK 4 nov. |
