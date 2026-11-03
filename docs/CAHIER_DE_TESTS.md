# Cahier de tests — HAPanel

Tous les tests lancés et pas encore confirmés, en un seul endroit, pour n'en oublier
aucun. Chaque ligne se coche **OK** ou **KO** ; en cas de KO, noter ce qui a été vu
(et l'heure, pour retrouver les journaux).

- **Module :** `hapanel-a85bfc`, binaire de banc `0.6.0-dev (6ec8bc4)`, flashé le
  3 novembre 2026. Vérifier l'entité « Version » sur la page de l'appareil avant de
  commencer.
- **Ordre :** la partie A bloque la fusion dans `main` ; les parties B à G se font
  quand l'occasion se présente.
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

| Partie | Sujet | Bloque la fusion |
|---|---|---|
| A | Message d'accueil, côté module (D028) | Oui |
| B | Message d'accueil, côté blueprint (D028) | Oui |
| C | Réglages de la LED par module (D027) et bouton Accueil (D025) | Non |
| D | Icônes et couleurs des scénarios (D026) | Non |
| E | LED selon la lumière (D018) et rétroéclairage (D023) | Non |
| F | Cas d'erreur jamais confirmés séparément | Non |
| G | Cas qui demandent une date particulière | Non |

## Préparation (une fois, avant A et B)

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| P1 | Page de l'appareil `hapanel-a85bfc`, rubrique Configuration | Entité **Message d'accueil** présente et activée | |
| P2 | Créer la liste « Messages d'accueil » et exécuter **une fois** le script `docs/exemples/messages_accueil.yaml` (voir `CONFIGURATION.md` § 6) | 27 tâches dans la liste | |
| P3 | Créer la liste « Messages uniques » (vide pour l'instant) | Liste présente | |
| P4 | Importer le blueprint depuis la branche : `https://github.com/cnuma/HAPanel/blob/feature/message-accueil/blueprints/automation/hapanel/message_accueil.yaml` | Blueprint « HAPanel — message d'accueil » listé | |
| P5 | Créer l'automatisation : Panneaux = le module ; Déclencheurs = `binary_sensor.entree_capteur_porte_entree` ; Période sans déclenchement = **1 min** pour les tests ; les deux listes ; Météo = l'entité `weather` | Automatisation enregistrée, sans erreur | |

## A — Message d'accueil, côté module

Sans passer par la porte : **Outils de développement › Actions**, action
`esphome.hapanel_a85bfc_message_accueil`, champs `texte` et `infos`.

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| A1 | Envoyer `texte` = « Test d'accueil », `infos` = « Dehors : 12 °C » | Message plein écran, fond noir, par-dessus la barre de navigation ; croix en haut à droite ; ligne grise d'informations ; « Touchez l'écran pour fermer » en bas | |
| A2 | Pendant A1, regarder la LED | Arc-en-ciel, si la LED est autorisée (entité « LED », D027) | |
| A3 | Toucher la croix | Le message se ferme ; la page d'en dessous revient | |
| A4 | Renvoyer, puis toucher l'écran **à l'endroit d'un bouton** de la page d'en dessous | Le message se ferme ; le bouton n'est **pas** actionné | |
| A5 | Renvoyer, ne rien toucher, chronométrer | Fermeture seule après 3 min (± 1 s) | |
| A6 | Attendre la mise en veille de l'écran (60 s sans toucher), puis envoyer | L'écran se rallume et montre le message | |
| A7 | Envoyer un texte d'environ 150 caractères avec accents | Texte coupé en lignes, centré, lisible ; aucun caractère bizarre | |
| A8 | Envoyer un texte de plus de 240 caractères | Texte tronqué proprement, sans caractère cassé à la fin | |
| A9 | Envoyer `texte` vide | Rien ne s'affiche | |
| A10 | Désactiver l'entité « Message d'accueil », puis envoyer | Rien ne s'affiche | |
| A11 | Message affiché, puis désactiver l'entité « Message d'accueil » | Le message se ferme | |
| A12 | Réactiver l'entité, redémarrer le module (bouton Redémarrer ou coupure) | Entité toujours activée après le redémarrage | |
| A13 | Message affiché, puis couper la liaison avec HA (Paramètres › Appareils et services › ESPHome › `hapanel-a85bfc` › ⋮ › Désactiver ; réactiver ensuite) | Le message se ferme ; l'écran « HA déconnecté » est visible | |

## B — Message d'accueil, côté blueprint

Chaque déclenchement : noter le message affiché. En cas d'absence, ouvrir les
**Traces** de l'automatisation : elles disent quelle condition a bloqué.

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| B1 | Porte fermée et rien touché depuis plus d'1 min, entre 6 h et 23 h : ouvrir la porte | Message tiré de la liste, avec la ligne météo | |
| B2 | Refermer et rouvrir aussitôt | **Pas** de nouveau message (période sans déclenchement) | |
| B3 | Après 1 min de calme, rouvrir | Nouveau message | |
| B4 | Ajouter une tâche « Test unique » dans « Messages uniques », attendre 1 min, ouvrir | « Test unique » s'affiche, puis la tâche est **cochée** dans la liste | |
| B5 | Attendre 1 min, ouvrir | De nouveau un message de la liste ordinaire | |
| B6 | Sur 4 ou 5 déclenchements, comparer les messages aux descriptions de leurs tâches | Seulement des messages sans étiquette, ou étiquetés « automne » et du moment de la journée (« soir » de 18 h à 22 h, « nuit » après 22 h) | |
| B7 | Changer temporairement la plage (« jusqu'à » une heure déjà passée), attendre 1 min, ouvrir | Pas de message ; la trace montre la condition d'horaire | |
| B8 | Remettre la plage ; mettre l'entité « LED » sur éteinte (D027), déclencher | Message affiché, **sans** arc-en-ciel | |
| B9 | **Fin des tests :** remettre la période sans déclenchement à 30 min et la LED à son réglage | Réglages de tous les jours rétablis | |

## C — Réglages de la LED par module (D027) et bouton Accueil (D025)

Binaire `966fb2d` et suivants, jamais rapportés.

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| C1 | Page de l'appareil | Entités « LED », « Intensité LED » et « Alerte LED » présentes | |
| C2 | Changer « Intensité LED », redémarrer le module | Valeur conservée | |
| C3 | Dans le blueprint « module », imposer une valeur LED, enregistrer | La valeur imposée apparaît sur la page de l'appareil | |
| C4 | Choisir « Ne pas imposer », régler à la main sur la page de l'appareil | Le réglage manuel reste | |
| C5 | « Alerte LED » désactivée, puis couper HA (comme A13) | La LED reste muette (pas de rouge clignotant) | |
| C6 | Écran d'accueil | Pas de bouton maison dans la barre | |
| C7 | Aller sur une autre page, attendre le retour automatique à l'accueil | Toujours pas de bouton maison sur l'accueil | |

## D — Icônes et couleurs des scénarios (D026)

Après réimport du blueprint « module » depuis `main`.

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| D1 | Choisir une icône différente pour chaque bouton de scénario | Icônes affichées comme choisies | |
| D2 | Essayer plusieurs des 8 couleurs | Couleurs affichées comme choisies | |
| D3 | Donner un nom long à un scénario | Nom sur 2 lignes, sans débordement | |

## E — LED selon la lumière (D018) et rétroéclairage (D023)

À faire le soir, lumière allumée puis éteinte.

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| E1 | Pièce éclairée : regarder la respiration de la LED | Monte de 0 à environ 5 %, discrète ; couleur du préréglage lisible | |
| E2 | Pièce sombre (attendre 1 min, la mesure est moyennée) | Respiration plus faible (environ 1 %), couleur encore reconnaissable | |
| E3 | Préréglage Confort, puis Éco | Orange et vert bien distincts, de jour comme de nuit | |
| E4 | Boost, ou une alerte | Signal visible, y compris en pièce sombre | |
| E5 | Pièce sombre : lire l'écran | Lisible sans éblouir (niveau `retro_nuit`) | |
| E6 | Allumer puis éteindre la lumière de la pièce | Le rétroéclairage suit après environ 1 min, sans clignoter ni varier sans cesse | |
| E7 | Pièce sombre, écran allumé puis en veille | La luminosité de l'écran ne fausse pas la mesure (pas de va-et-vient) | |

## F — Cas d'erreur jamais confirmés séparément

Méthode pour « indisponible » : **Outils de développement › États**, choisir l'entité,
mettre l'état à `unavailable`, **Définir l'état** (HA remet la vraie valeur à la
mesure suivante).

| N° | Action | Attendu | OK / KO |
|---|---|---|---|
| F1 | Accueil : désactiver l'automatisation « module » 16 min, sans redémarrer | Température « périmée » | |
| F2 | Scénarios : choisir un scénario dont l'entité est mise `unavailable`, l'actionner | « Refusé par HA » | |
| F3 | Scénarios : automatisation « module » désactivée, actionner un scénario | « Pas de réponse de HA » | |
| F4 | Scénarios et menu : HA coupé (comme A13) | Écran « HA déconnecté », aucune commande envoyée | |
| F5 | Scénarios : nom très long | Affiché sans déborder | |
| F6 | Météo : entité `weather` mise `unavailable` | « indisponible » | |
| F7 | Météo et planning : automatisation « module » désactivée 16 min | « périmé » | |
| F8 | Météo et planning : redémarrer le module, automatisation désactivée | « non reçu » | |
| F9 | Planning : regarder en soirée, après le dernier créneau | « Plus rien aujourd'hui », ou « Prochain à » | |
| F10 | Retour à l'accueil (D022) : HA coupé, écran resté allumé sur une autre page | Retour automatique à l'accueil quand même | |
| F11 | Fin : réactiver tout ce qui a été désactivé | Automatisations et intégration actives | |

## G — Cas qui demandent une date particulière

À noter quand l'occasion se présente.

| N° | Quand | Attendu | OK / KO |
|---|---|---|---|
| G1 | Passage à minuit, écran Planning ouvert | Le planning bascule sur le nouveau jour | |
| G2 | Changement d'heure (28 mars 2027) | Planning et heures justes | |
| G3 | 3 ou 4 calendriers dans le blueprint « module » | Tous affichés sur la page Planning | |
| G4 | Message d'accueil en hiver (à partir du 21 décembre) | Messages « hiver » tirés | |
