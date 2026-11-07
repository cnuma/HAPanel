# Cahier de tests — HAPanel

Tous les tests lancés et pas encore confirmés, en un seul endroit, pour n'en oublier
aucun. Chaque ligne se coche **OK** ou **KO** ; en cas de KO, noter ce qui a été vu
(et l'heure, pour retrouver les journaux).

- **Module :** `hapanel-a85bfc`, binaire de banc `0.7.0-dev (7642307)`, branche
  `feature/barre-etat` (fusionnée dans `main` le 4 novembre 2026), flashé le 4 novembre 2026. Vérifier l'entité « Version » sur la page de l'appareil avant de
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
| 4 novembre 2026 | `420fdbe` | H | OK : H16 à H19 (disquette). Interfaces non uniformes : barre du haut sur l'Accueil seulement, titres différents d'une page à l'autre ; la disquette verte s'affiche par-dessus le contenu de la page quand on change vite de page | Proposition du propriétaire : barre d'état commune (titre, Wi-Fi, HA, disquette) ; TODO rang 2 |
| 4 novembre 2026 | `7642307` | I | **I12 OK** : partie I validée | **Fusion de `feature/barre-etat` dans `main`**, accord du propriétaire |
| 4 novembre 2026 | `c95f6b8` | I | **I1 à I11 OK**. ☰ « un peu capricieux à attraper », trop petit | Zone tactile agrandie : bouton de toute la hauteur de la barre, 48 px de large, plus 6 px autour (I12) |
| 4 novembre 2026 | `8d21d4e` | I | **I11 OK** : « plus de point blanc, plus de ligne blanche » | Diagnostic provisoire retiré du binaire de banc |
| 5 novembre 2026 | `67a2674` (public, `v0.8.0-dev.1`) | J | **J1 à J3 OK** : Release publiée par GitHub Actions en 2 min 35 ; carte neuve installée par web.esphome.io, Wi-Fi par Improv, adoption sans clé demandée. L'accueil affiche « Séjour » alors que le blueprint vise la cuisine (calendrier correct) | « Séjour » était écrit dans le firmware : clé `piece` envoyée par le blueprint (D040), à tester avec `v0.8.0-dev.2` (J6, J12, J13) |
| 5 novembre 2026 | `v0.8.0-dev.1`, puis local `0.8.0-dev.3-usb` | J6 | **J6 KO avec dev.1** : entité Firmware « À jour », versions vides ; au démarrage « HTTP_CLIENT: Out of buffer » puis « Failed to fetch manifest » ; « Mettre à jour l'entité » de HA ne relance pas la vérification | `buffer_size_tx: 2048` ; binaire local flashé par USB : démarrage sans erreur. Publication `v0.8.0-dev.3`, J6 à refaire |
| 7 novembre 2026 | `v0.8.1` (Release), module de la cuisine | J10, J14 | **J14** : accueil de la cuisine rétabli après choix du module dans « Panneau » ; blueprint réimporté depuis `main`. **J10 clôturé sans essai** par le propriétaire (point mineur) : la fermeture du point d'accès après 15 min reste non vérifiée sur le module | **Fusion de `docs/guide-installation` dans `main`**, accord du propriétaire |
| 7 novembre 2026 | `v0.8.1` (Release), module de la cuisine | J9, J14 | **J9 OK** : le module rejoint le Wi-Fi saisi depuis le téléphone. **J14 OK** : sans suppression préalable, HA propose de réassocier le module en prévenant que la connexion ne sera plus chiffrée (clé effacée par l'écriture) ; non accepté : appareil supprimé, module de nouveau dans « Découvertes », ajouté comme une première association | Piège ajouté au 09 ; `DEPLOIEMENT_PUBLIC.md` § 5 et dépannage de `CONFIGURATION.md` : refuser, supprimer puis rajouter l'appareil, le choisir de nouveau dans « Panneau ». Section « Remplacer le logiciel » retirée du guide : seul le propriétaire avait un module compilé sur son ordinateur. Accueil à confirmer après réassociation de l'automatisation (captures 16, 17). J10 reporté à une prochaine séance (propriétaire) |
| 7 novembre 2026 | `v0.8.1` (Release), module de la cuisine | J9, J14 | **Seconde passe, sans rien supprimer dans HA** : écriture par web.esphome.io, « Chip erase completed » puis « Installation finie » ; Wi-Fi par un iPhone : réseau `hapanel-583c28` sans mot de passe, page « Wi-Fi captif » ouverte seule, liste des réseaux, SSID et mot de passe, **Save** : « Saved. Connecting... » (6 h 43) | J9 : connexion du module au Wi-Fi à confirmer. J14 : comportement de HA à noter. J10 non fait (Wi-Fi saisi avant les 15 min). Captures 06, 07, 11, 12 dans le guide (noms des réseaux masqués) |
| 7 novembre 2026 | `v0.8.1` (Release), module de la cuisine | J14 | **Première passe, appareil supprimé d'abord dans HA par le propriétaire** : `hapanel-factory.bin` (empreinte de la Release vérifiée) écrit par web.esphome.io, Edge (petite flèche « Installer », fenêtre « Choisir un fichier », aucune case d'effacement) ; Wi-Fi saisi après l'écriture dans « Configure Wi-Fi » (« Provisioned! », version 0.8.1). HA : module dans « Découvertes », **aucune clé demandée**, nom de l'ancien appareil repris tout seul, pièce choisie à la main. L'accueil ne s'affiche pas correctement : l'automatisation désigne encore l'appareil supprimé | Réassocier « Panneau » dans l'automatisation (captures 16, 17). J14 à refaire **sans supprimer l'appareil dans HA**, avec la reprise de J10 puis J9 (module de nouveau effacé, Wi-Fi par le téléphone). Captures 03 à 05, 08, 09, 13 à 15 dans le guide |
| 6 novembre 2026 | `v0.8.1-dev.1` (`e1ed3f8`) | H20 | Accord du propriétaire | **Fusion de `fix/intensite-ecran-demarrage` dans `main`**, publication `v0.8.1` |
| 6 novembre 2026 | `v0.8.1-dev.1` (`e1ed3f8`), mise à jour depuis HA | H20 | **H20 OK** : réglage appliqué dès la fin du démarrage | Mise à jour depuis HA en deux temps : HA proposait encore `0.8.0`, vue à la dernière vérification du module ; installée sans erreur (manifeste lié à son étiquette), puis `0.8.1-dev.1` proposée au redémarrage. Piège ajouté au 09 et procédure (`DEPLOIEMENT_PUBLIC.md` § 4). Fusion de `fix/intensite-ecran-demarrage` à soumettre au propriétaire |
| 6 novembre 2026 | `0.8.0` et antérieurs | H | **KO, constaté par le propriétaire** : après un redémarrage, « Intensité écran » est conservée dans les réglages, mais l'écran reste à 100 % ou presque ; le réglage ne s'applique qu'après une mise en veille. H10 vérifiait la valeur, pas son effet | Cause : « Intensité écran » est restaurée avant le rétroéclairage, dont le démarrage à 100 % (`ALWAYS_ON`) écrase le réglage ; l'intervalle de la LDR ne corrige pas, sa valeur étant déjà jugée appliquée. Corrigé sur `fix/intensite-ecran-demarrage` ; test H20 |
| 5 novembre 2026 | `0.8.0-dev.3-usb` → `v0.8.0-dev.4-wifi` (`670e30e`) | J6, J7, J8 | **J6 OK** : HA juge `0.8.0-dev.3-usb` et `0.8.0-dev.3` incomparables (« À jour », `update.install` refusé) ; avec `0.8.0-dev.4-wifi`, « Mise à jour disponible », **Mettre à jour** : téléchargement par Wi-Fi depuis GitHub en 16 s, « Update complete », redémarrage, Wi-Fi et HA retrouvés sans rien ressaisir, À propos en `0.8.0-dev.4-wifi`. Aucune erreur au journal. Accueil « Intérieur » : blueprint de `main`, sans la clé `piece` | Versions sans suffixe (§ 1 de `DEPLOIEMENT_PUBLIC.md`). Le binaire est lu par `releases/latest/…` : une Release publiée entre la vérification et l'installation ferait échouer le MD5 (sans dégât) ; lien vers l'étiquette dans le manifeste, corrigé dans `publication.yml` (effet à la prochaine Release). J7 et J8 OK, constatés par le propriétaire |
| 5 novembre 2026 | `v0.8.0-dev.4-wifi`, blueprint de la branche | J12 | **J12 OK** : blueprint importé depuis la branche, « Nom de la pièce » vide : l'accueil affiche « Cuisine » | — |
| 5 novembre 2026 | `v0.8.0-dev.4-wifi` | J4, J5, J11, J13 | **OK** : clé enregistrée dans le module et dans HA, gardée après la mise à jour ; coupure d'alimentation sans rien ressaisir ; nom long coupé proprement ; depuis le PC, port de l'OTA (3232) fermé, API (6053) ouverte | J9, J10 et J14 reportés au guide d'installation, qui passera par ces écrans |
| 4 novembre 2026 | `4091687` | I | Titres visibles. Ligne du haut **bien plus fréquente à 20 MHz**, pas sur toute la largeur ; point du milieu qui clignote quand le bouton maison est affiché ; ligne au passage du Menu à une autre page | Diagnostic au banc : à l'écran immobile, aucun envoi de LVGL, donc pas un dessin du programme. Idée du propriétaire retenue : la dernière rangée de pixels réapparaît sur la première (le point est dans l'axe du bouton maison ; la ligne vient avec le redessin complet, dont le dernier morceau va jusqu'à la rangée 319). 40 MHz rétabli ; barre du haut et barre du bas décalées de 2 px des bords (I11 à refaire) |
| 4 novembre 2026 | `a3a8864` | I | Vidéo : **titre de la page absent** de la barre ; ligne claire fugace sur la première ligne de l'écran (une image, environ toutes les 4 s) et point fixe en haut au milieu | Titre : la couche commune n'hérite pas du texte blanc des pages, texte sombre sur gris ; corrigé (couleur sur la barre). Ligne : hypothèse d'écriture parasite sur le bus de l'écran, essai à 20 MHz au lieu de 40 (I11) |
| 4 novembre 2026 | `2f00f00` | I | Premier aperçu : fond bleu autour du ☰ disgracieux, ☰ préféré à gauche avant le titre ; **ligne blanche qui clignote en haut de l'écran** | Corrigé (`a3a8864`) : ☰ à gauche, sans fond. Ligne blanche : à décrire (quand, quelle page, toute la largeur ?) |
| 4 novembre 2026 | `420fdbe` | C, H | OK : C2, H10 à H14 | **Fusion de `feature/reglages-ecran` dans `main`**, accord du propriétaire |
| 4 novembre 2026 | `20dda6e` | A, C | OK : A13, C3, C5 ; C4 sauf redémarrage. **KO : C2**, réglages LED et écran perdus au redémarrage | Cause : ESPHome n'écrit la flash que toutes les 60 s, une coupure avant perd le réglage. Corrigé (D034) : écriture sous 5 s ; C2 à refaire après flash, en attendant 10 s avant de couper |

| Partie | Sujet | Bloque la fusion de |
|---|---|---|
| A | Message d'accueil, côté module (D028) | `feature/message-accueil` (fusionnée) |
| B | Message d'accueil, côté blueprint (D028) ; réglé dans le blueprint du module (D042, B10 à B19) | `feature/message-accueil` (fusionnée) ; B10 à B19 : `feature/accueil-blueprint-module` (fusionnée) |
| C | Réglages de la LED par module (D027) et bouton Accueil (D025) | `feature/reglages-ecran` (fusionnée ; C2 seulement) |
| D | Icônes et couleurs des scénarios (D026) | — |
| E | LED selon la lumière (D018) et rétroéclairage (D023) | — |
| F | Cas d'erreur jamais confirmés séparément | — |
| G | Cas qui demandent une date particulière | — |
| H | Page Réglages (D031), menu (D025 révisée), tactile (D009 révisée) ; intensité écran au démarrage (H20) | `feature/reglages-ecran` (fusionnée) ; H20 : `fix/intensite-ecran-demarrage` (fusionnée) |
| I | Barre d'état commune et navigation (D036, D025 révisée) | `feature/barre-etat` (fusionnée) |
| J | Déploiement public (D039) ; guide d'installation (J9, J10, J14) | `feature/poc-deploiement` (fusionnée) ; J9, J10, J14 : `docs/guide-installation` (fusionnée) |
| 7 novembre 2026 | `9b78597` (S028, USB) | K1, K2, K3 | Écran et couleurs OK (contrôleur ST7789V, sans inversion) ; tactile : x brut décroît de gauche à droite (3605 à 449), y de 419 à 3662. Premier téléversement impossible avec le premier câble USB-C (aucune donnée reçue) ; OK avec un autre câble | Calibrage et `mirror_x` reportés ; K4 sur le binaire suivant |
| 7 novembre 2026 | `174aa99` (S028, USB) | K4 à K11 | Tout OK ; K5 : glissière Éteint / Chauffage capricieuse au doigt sur dalle résistive, boutons fiables. Mémoire libre 153 Ko, plus grand bloc 96 Ko. Remarque du propriétaire : avoir à configurer le blueprint du message d'accueil en plus de celui du module n'est pas pratique (TODO rang 1) | **Partie K validée**, fusion dans `main` (accord du propriétaire) ; glissière : TODO rang 5 |
| 7 novembre 2026 | `745126b` (blueprint, branche) | B10 à B19 | Tout OK : migration, module sans section, même texte sur deux modules, message unique, entité désactivée, météo, plage horaire ; B3 refait (B13) | **Fusion de `feature/accueil-blueprint-module` dans `main`**, accord du propriétaire |
| 7 novembre 2026 | `v0.9.0-dev.1` (`3ad92cc`, Release) | J16 (fichiers) | Vérifié par l'agent : six fichiers, Release marquée Latest, `manifest.json` en `0.9.0-dev.1` vers `hapanel-2432s024c-ota.bin` | Reste J16 (mise à jour de la cuisine depuis HA) et K12 à K15 ; puis `v0.9.0` |
| 7 novembre 2026 | `v0.9.0-dev.1` (Release), module de la cuisine | J16 | **J16 OK** (propriétaire) : mise à jour depuis HA | Publication de `v0.9.0` (accord du propriétaire) ; K12 à K15 (S028) restent à faire, K14 et K15 sur la mise à jour vers `v0.9.0` |

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
| B10 | Migration (`CONFIGURATION.md` § 6, « Venir de l'ancien blueprint ») : noter les réglages de l'automatisation « HAPanel — message d'accueil », la supprimer ; réimporter `module.yaml` depuis la branche `feature/accueil-blueprint-module` ; dans l'automatisation du module de l'atelier, section **Message d'accueil** : la porte d'entrée, période **1 min**, les deux listes ; enregistrer ; supprimer le blueprint « HAPanel — message d'accueil » | Automatisation enregistrée sans erreur ; plus aucune automatisation ni blueprint « message d'accueil » dans HA | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B11 | Automatisation du module de la cuisine : l'ouvrir et l'enregistrer **sans** remplir la section Message d'accueil | Enregistrée sans erreur ; accueil, consigne (+/−), météo, planning et scénarios du module de la cuisine fonctionnent comme avant | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B12 | Porte fermée, rien touché depuis plus d'1 min, entre 6 h et 23 h : ouvrir la porte | Message avec la ligne météo sur le module de l'atelier ; **rien** sur le module de la cuisine (pas de déclencheur) | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B13 | B3 refait : trois fois, attendre 1 min de calme puis ouvrir ; noter les trois textes | Un message à chaque fois. Le même texte peut revenir deux fois de suite (accepté, D042) | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B14 | Remplir la section Message d'accueil du module de la cuisine avec les mêmes réglages qu'en B10 ; attendre 1 min, ouvrir | Le **même** texte sur les deux modules | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B15 | Ajouter une tâche « Test unique » dans « Messages uniques » ; attendre 1 min, ouvrir | « Test unique » sur les deux modules, puis la tâche est **cochée**. Si un module montre un autre texte, le noter (cas prévu en D042) | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B16 | Désactiver l'entité « Message d'accueil » du module de la cuisine ; attendre 1 min, ouvrir | Message sur l'atelier seulement ; la trace de l'automatisation de la cuisine s'arrête sur la condition de l'entité | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B17 | Section Message d'accueil de l'atelier : désactiver **Météo sous le message** ; attendre 1 min, ouvrir | Message sans ligne météo | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B18 | Changer la plage (« jusqu'à » une heure déjà passée) ; attendre 1 min, ouvrir | Pas de message ; la trace montre la condition d'horaire | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |
| B19 | **Fin des tests :** remettre la plage, la météo, l'entité « Message d'accueil » de la cuisine et la période à 30 min sur les deux modules | Réglages de tous les jours rétablis | `feature/accueil-blueprint-module` (fusionnée) | OK 7 nov. |

## C — Réglages de la LED par module (D027) et bouton Accueil (D025)

Binaire `966fb2d` et suivants, jamais rapportés.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| C1 | Page de l'appareil | Entités « LED », « Intensité LED » et « Alerte LED » présentes | — | OK 4 nov. |
| C2 | Changer « Intensité LED » et « Intensité écran », attendre 10 s, couper l'alimentation du module puis la rétablir | Valeurs conservées | `feature/reglages-ecran` (fusionnée) | KO 4 nov. (valeurs perdues) ; corrigé (D034), OK 4 nov. |
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

Fusionnée dans `main` le 4 novembre 2026. Avant H4 (pour mémoire) : **importer le blueprint « module »
depuis la branche** (Paramètres › Automatisations et scènes › Blueprints › Importer
un blueprint), en acceptant de remplacer l'existant, avec l'adresse
`https://github.com/cnuma/HAPanel/blob/feature/reglages-ecran/blueprints/automation/hapanel/module.yaml`.
**Pas** « Réimporter le blueprint » : il reprendrait la version de `main`. Rouvrir
ensuite l'automatisation du module et l'enregistrer.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| H1 | Toucher brièvement, comme sur un téléphone, les boutons de la barre et des tuiles | Chaque toucher bref est pris en compte, sans laisser le doigt | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H2 | Ouvrir le Menu | Seul le bouton maison reste dans la barre ; pas de tuile Accueil ; tuiles Météo, Planning, Scénarios, **Réglages**, À propos | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H3 | Quitter le Menu par une tuile | Le bouton Menu revient sur la nouvelle page | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H4 | Ouvrir Réglages, blueprint sur « Ne pas imposer » partout | 4 réglages actifs, mêmes valeurs que la page de l'appareil dans HA ; aucun cadenas ; interrupteur à l'arrêt lisible (fond sombre bordé, bouton blanc) | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H5 | Basculer « LED » | La LED s'éteint ou reprend sa respiration ; « LED » change aussi sur la page de l'appareil | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H6 | Glisser « Intensité LED », relâcher | Valeur affichée pendant le glissement, par pas de 5 ; LED et page de l'appareil suivent au relâchement | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H7 | Basculer « Alerte LED » | Même valeur sur la page de l'appareil | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H8 | Glisser « Intensité écran » jusqu'à 20 % | L'écran baisse aussitôt sans devenir illisible (plancher) | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H9 | Changer « Intensité écran » sur la page de l'appareil | Le curseur de la page Réglages suit | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H10 | Redémarrer le module | Les 4 réglages sont conservés | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H11 | Dans le blueprint, imposer « Alerte LED », enregistrer | Sur l'écran, cadenas devant Alerte LED, qui ne réagit plus ; « imposé par HA » avec un cadenas en bas | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H12 | Remettre « Ne pas imposer », enregistrer | Alerte LED de nouveau modifiable, cadenas et mention disparus | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H13 | Rester 1 min sur Réglages sans toucher | Retour à l'accueil, puis écran éteint | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H14 | HA coupé (comme A13), ouvrir Réglages | La page marche, réglages modifiables | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H15 | Éteindre la lumière d'une pièce éclairée | L'écran baisse en moins de 10 s, sans clignoter ensuite | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H16 | Sur Réglages, déplacer « Intensité LED » et lever le doigt | Disquette **grise** au-dessus du bouton Menu, à droite ; **verte** 5 s après, puis disparaît 2 s plus tard | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H17 | Déplacer trois fois de suite un curseur, à 2 s d'intervalle | Disquette grise sans interruption, verte seulement 5 s après le dernier geste | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H18 | Écran sur l'Accueil, changer « Intensité écran » sur la page de l'appareil dans HA | La disquette apparaît sur l'Accueil, comme en H16 | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H19 | Couper puis rétablir le courant | Pas de disquette au démarrage | `feature/reglages-ecran` (fusionnée) | OK 4 nov. |
| H20 | Pièce éclairée : « Intensité écran » à 40 %, attendre 10 s, couper puis rétablir le courant ; comparer avec un réglage à 100 % | Dès la fin du démarrage, l'écran est aussi faible qu'avant la coupure, sans attendre une mise en veille | `fix/intensite-ecran-demarrage` (fusionnée) | OK 6 nov. |

## I — Barre d'état et navigation (D036)

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| I1 | Écran d'accueil | En haut : bouton ☰ à gauche, sans fond, puis date et heure (« 4 nov.  17:20 ») ; Wi-Fi et point vert à droite. **Pas de barre en bas** | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I2 | Toucher brièvement ☰ | Le Menu s'ouvre ; titre « Menu » dans la barre, pas de ☰ ; maison centrée en bas | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I3 | Ouvrir chaque tuile du Menu | Titre de la barre = nom de la page (Météo, Planning, Scénarios, Réglages, À propos) ; ☰ présent ; maison en bas | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I4 | Toucher la maison | Accueil : la date revient à la place du titre ; la barre du bas disparaît | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I5 | Sur Menu, Météo (3e jour), Planning (dernière ligne), Scénarios (6e bouton), Réglages, À propos | Rien n'est caché par la barre du haut ni par celle du bas ; rien ne déborde | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I6 | Couper HA (comme A13), ouvrir Météo puis Scénarios | Point rouge dans la barre sur chaque page ; texte orange « HA non connecté » sur la page | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I7 | Sur Réglages, déplacer un curseur puis ouvrir aussitôt une autre page | La disquette reste dans la barre, grise puis verte ; rien ne s'affiche par-dessus la page | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I8 | Laisser Météo 1 min sans toucher | Retour à l'accueil : date dans la barre, pas de barre du bas | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I9 | Envoyer un message d'accueil (comme A1) | Le message couvre tout l'écran, barre du haut comprise ; à la fermeture, la barre revient | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I10 | HA coupé, sur l'accueil (D015) | Message « Pas de communication » lisible sous la barre ; point rouge | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I11 | Observer 1 min la barre du haut sur Réglages, sur l'accueil, puis passer du Menu à chaque page | Aucune ligne ni point parasite en haut de l'écran (2 rangées noires en haut et en bas) | `feature/barre-etat` (fusionnée) | OK 4 nov. |
| I12 | Toucher le ☰ dix fois, vite, un peu à côté de l'icône (dessous, à droite) | Le Menu s'ouvre à chaque fois | `feature/barre-etat` (fusionnée) | OK 4 nov. |

## J — Déploiement public (D039)

Binaires publiés par GitHub (`hapanel_public.yaml`), sur une carte qui n'est pas le
module de banc. Procédure : `docs/DEPLOIEMENT_PUBLIC.md`.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| J1 | Publication : pousser l'étiquette `v0.8.0-dev.1` (§ 1 de `DEPLOIEMENT_PUBLIC.md`) | Release créée, marquée Latest, avec `hapanel-factory.bin`, `hapanel-ota.bin` et `manifest.json` | `feature/poc-deploiement` | OK 5 nov. |
| J2 | Nouvelle carte : première installation par web.esphome.io, Wi-Fi par Improv (§ 2) | Le module démarre, l'écran d'accueil s'affiche, le module rejoint le Wi-Fi | `feature/poc-deploiement` | OK 5 nov. |
| J3 | Adoption dans HA (§ 3) | Appareil découvert ; **aucune clé demandée** (sinon noter le message) ; entités présentes, dont « Firmware » et « Version » (`0.8.0-dev.1 (sha)`) | `feature/poc-deploiement` | OK 5 nov. |
| J4 | Après J3, journaux du module ou une seconde adoption depuis un autre HA | La clé est enregistrée (« Noise PSK saved ») ; une connexion sans cette clé est refusée | `feature/poc-deploiement` | OK 5 nov. |
| J5 | Couper et rétablir l'alimentation | Le module rejoint le Wi-Fi et HA sans rien ressaisir | `feature/poc-deploiement` | OK 5 nov. |
| J6 | Publier `v0.8.0-dev.3`, redémarrer le module, puis dans HA : entité Firmware › Installer (§ 4) | « Mise à jour disponible 0.8.0-dev.3 » ; téléchargement depuis GitHub sans erreur ; redémarrage | `feature/poc-deploiement` | OK 5 nov. (avec `0.8.0-dev.4-wifi`) |
| J7 | Après J6 | Version `0.8.0-dev.2` ; Wi-Fi et HA reconnectés sans rien ressaisir ; réglages du module (LED, intensité) conservés | `feature/poc-deploiement` | OK 5 nov. (avec `0.8.0-dev.4-wifi`) |
| J8 | Pendant J6, journaux par USB ; page À propos avant et après | Pas de manque de mémoire ni de redémarrage pendant le téléchargement ; noter la mémoire libre (G6) | `feature/poc-deploiement` | OK 5 nov. |
| J9 | Nouvelle carte sans Improv : point d'accès `hapanel-xxxxxx` depuis un téléphone (§ 2) | Portail captif, choix du réseau, le module rejoint le Wi-Fi | `docs/guide-installation` (fusionnée) | OK 7 nov. |
| ~~J10~~ | Laisser une carte effacée sans Wi-Fi 16 min, puis tenter le point d'accès | Point d'accès fermé après 15 min ; rouvert après une coupure d'alimentation | `docs/guide-installation` (fusionnée) | Clôturé sans essai (propriétaire, 7 nov.) |
| J11 | Depuis le PC, `esphome upload` vers un module public par le réseau | Refusé : le binaire public n'a pas d'OTA depuis un PC | `feature/poc-deploiement` | OK 5 nov. (port 3232 fermé, API 6053 ouverte) |
| J12 | Après J6 : réimporter le blueprint depuis la branche (`CONFIGURATION.md` § 2), laisser « Nom de la pièce » vide, enregistrer l'automatisation | L'accueil affiche la zone du thermomètre (« Cuisine ») au lieu de « Séjour » | `feature/poc-deploiement` | OK 5 nov. |
| J13 | Saisir « Chambre des parents » dans « Nom de la pièce » | « Chambre des pa… » ou le nom coupé proprement, sans chevaucher « indisponible » à droite | `feature/poc-deploiement` | OK 5 nov. |
| J14 | Module de production : reflasher le binaire public par USB (`hapanel-factory.bin`), Wi-Fi par Improv, puis HA | Le module retrouve HA ; si HA demande une clé ou crée un nouvel appareil, le noter et réassocier l'automatisation du module | `docs/guide-installation` (fusionnée) | OK 7 nov. (connexion non chiffrée proposée par HA, refusée) |
| J16 | Release `v0.9.0-dev.1` (D041) : vérifier ses fichiers, puis mettre à jour le module de la cuisine depuis HA (§ 4) | Six fichiers : `hapanel-2432s024c-factory.bin`, `hapanel-2432s024c-ota.bin`, `manifest.json`, et les trois de la S028 ; la cuisine voit la mise à jour, l'installe et garde Wi-Fi, clé et réglages | — | OK 7 nov. |

## K — Carte ESP32-2432S028 (écran 2,8", tactile résistif)

Configuration `hapanel_2432s028_banc.yaml` (binaire privé, clé de `secrets.yaml`),
premier flash par USB. Fichier matériel `packages/hardware_2432s028.yaml`, brochage repris
d'AquaLook. Carte du banc à deux prises (USB-C et micro-USB) : modèle d'écran
`ESP32-2432S028-7789`.

| N° | Action | Attendu | Bloque la fusion de | OK / KO |
|---|---|---|---|---|
| K1 | Flasher par USB, alimentation sur bloc secteur | Écran allumé, page d'accueil lisible, barre d'état en haut | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K2 | Regarder les couleurs : barre d'état, icônes, température extérieure | Mêmes couleurs que sur la S024C (pas de négatif, pas de rouge et bleu échangés) | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K3 | Toucher les quatre coins de l'écran, puis le centre ; envoyer les lignes `toucher … brut` des journaux | Une ligne par toucher ; valeurs brutes relevées pour le calibrage | `feature/carte-2432s028` (fusionnée) | OK 7 nov. (x inversé, calibrage reporté) |
| K4 | Après calibrage et nouveau flash : ☰, puis chaque page du Menu, puis le bouton Accueil | Chaque bouton répond du premier coup, à l'endroit touché | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K5 | Accueil : glissière Éteint / Chauffage et consigne ± (HA connecté) | Même comportement que sur la S024C | `feature/carte-2432s028` (fusionnée) | OK 7 nov., avec réserve : glissière capricieuse (dalle résistive), boutons fiables |
| K6 | Laisser le module sans toucher 1 min, puis toucher l'écran | Écran éteint puis rallumé au toucher, retour à l'accueil | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K7 | LED : couleur à l'accueil selon le chauffage | LED allumée de la bonne couleur (pas éteinte quand elle devrait être allumée) | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K8 | Cacher puis éclairer la LDR, lire les lignes `LDR … V` | La tension monte dans le noir ; l'écran baisse dans le noir | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K9 | Bords haut et bas de l'écran pendant l'usage | Pas de ligne ni de point parasite en haut (piège des bords, D036) | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K10 | Page À propos ; entités « Mémoire libre » et « Plus grand bloc libre » dans HA | Version et SHA du binaire flashé ; mémoire notée (G6) | `feature/carte-2432s028` (fusionnée) | OK 7 nov. : mémoire libre 153 Ko, plus grand bloc 96 Ko |
| K11 | Après K1 à K10, refaire G ou un test d'accueil sur la S024C du banc avec le binaire de cette branche | Aucun changement sur la S024C (la configuration fusionnée est identique, à confirmer sur le module) | `feature/carte-2432s028` (fusionnée) | OK 7 nov. |
| K12 | Binaire public S028 (D041), Release `v0.9.0-dev.1` : installer `hapanel-2432s028-factory.bin` par web.esphome.io, Wi-Fi par Improv (`DEPLOIEMENT_PUBLIC.md` § 2) | Écran allumé, accueil lisible, tactile juste (mêmes réglages que le banc) | — | |
| K13 | Adoption dans HA (§ 3) | Aucune clé demandée ; entités « Firmware » et « Version » présentes | — | |
| K14 | Entité « Firmware » après une Release suivante (§ 4) | Mise à jour proposée depuis `manifest-2432s028.json` : le résumé cite la carte `2432s028` ; installée sans erreur, écran et tactile toujours justes | — | À faire sur la mise à jour vers `v0.9.0` |
| K15 | Après K14 : Wi-Fi, clé et réglages du module (LED, intensité) | Conservés sans rien ressaisir | — | À faire sur la mise à jour vers `v0.9.0` |
