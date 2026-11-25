# Chauffage et clim pilotés par agenda

Facultatif : le module HAPanel accepte n'importe quel thermostat `climate.…`. Ce
guide propose une régulation simple, sans intégration complémentaire : un
« Thermostat générique » de Home Assistant par pièce, qui commande l'interrupteur
du radiateur (fil pilote), et le blueprint `chauffage/agenda_piece.yaml`, qui lui
applique le préréglage du calendrier de la pièce (D058). Le même blueprint pilote une
clim : mode chaud ou froid et consigne donnés par le titre de l'événement (§ 3 et § 4,
D059). Les §1 et §5 décrivent le passage depuis Versatile Thermostat ; sans lui,
passer directement au §2.

Ordre conseillé : **construire le nouveau d'abord, désinstaller ensuite**. Les
radiateurs ne restent jamais sans régulation.

## 1. Inventaire (avant de toucher à quoi que ce soit)

Pour chaque thermostat Versatile Thermostat (VT), noter :

- son identifiant d'entité (`climate.…`) ;
- l'interrupteur du fil pilote qu'il commande (`switch.…`, ou `select.…`) ;
- le capteur de température de la pièce ;
- les températures de ses préréglages Confort, Éco, Hors-gel et Boost, ainsi
  que ses bornes min et max (**Paramètres › Appareils et services ›
  Versatile Thermostat › Configurer**).

Lister ensuite ce qui utilise ces entités :

- **Paramètres › Appareils et services › Entités**, cliquer sur le thermostat VT,
  puis **⚙ › Connexes** : automatisations, scripts et scènes ;
- tableaux de bord : dans chacun, **⋮ › Modifier › ⋮ › Éditeur de configuration
  brute**, puis chercher `climate.` et `versatile` (dont la carte
  `versatile-thermostat-ui-card`) ;
- `configuration.yaml` et les paquets YAML éventuels : chercher `versatile_thermostat`.

## 2. Créer un thermostat générique par pièce

**Paramètres › Appareils et services › Entrées › Créer une entrée ›
Thermostat générique** :

| Champ | Valeur |
|---|---|
| Nom | celui de la pièce, par exemple « Bureau » (il deviendra `climate.bureau`, ajustable ensuite) |
| Mode | Chauffage : sans ce choix, le thermostat démarre **éteint** et le calendrier ne l'allume jamais (le blueprint ne change pas le mode) |
| Interrupteur de chauffage | l'interrupteur du fil pilote noté au §1 |
| Capteur de température | celui de la pièce |
| Durée minimale de cycle | 5 min (évite de faire claquer le fil pilote) |
| Tolérances froid / chaud | 0,3 °C |
| Préréglages | Confort et Éco : les valeurs VT ; **Absent (`away`) = température Hors-gel** ; **Activité (`activity`) = température Boost** ; laisser Maison (`home`) et Nuit (`sleep`) vides, inconnus du module |

Le thermostat générique n'a ni « frost » ni « boost » (ses préréglages : `away`,
`comfort`, `eco`, `home`, `sleep`, `activity`) : le Hors-gel passe par `away` et le
Boost par `activity`. Le blueprint fait déjà cette correspondance. Un préréglage
n'existe que si sa température est saisie ; pour en ajouter un à un thermostat déjà
créé : **Paramètres › Appareils et services › Entrées**, le thermostat, **⚙ ›
Options du thermostat générique**, puis la fenêtre **Préréglages de température** (Absent, Confort, Éco, Maison, Nuit, Activité).

**Si le fil pilote n'est pas un `switch.…` mais un `select.…`** (modes
confort / éco / hors-gel / arrêt), créez d'abord un interrupteur modèle :
**Entrées › Créer une entrée › Modèle › Interrupteur**. À l'allumage :
`select.select_option` sur `comfort` ; à l'extinction : sur `off` (ou
`frost`) ; état : `{{ states('select.…') == 'comfort' }}`. Le thermostat
générique commande alors cet interrupteur.

Pendant le test, éteignez le thermostat VT de la pièce : deux régulations ne
doivent jamais commander le même interrupteur en même temps.

## 3. Calendrier de la pièce

Un calendrier local par pièce (**Paramètres › Appareils et services ›
Ajouter une intégration › Calendrier local**), par exemple « Chauffage Bureau ».

**Titres reconnus.** Le titre de l'événement en cours choisit le préréglage. Seul
**le début du titre** compte ; majuscules et accents sont ignorés, le trait d'union
vaut une espace. La suite du titre est libre et sert de commentaire (elle s'affiche
sur la page Planning du module).

| Commencer le titre par | Préréglage du thermostat | Exemples de titres acceptés |
|---|---|---|
| **Confort** | Confort (`comfort`) | « Confort », « confort matin », « CONFORT soirée » |
| **Éco** | Éco (`eco`) | « Éco », « eco », « Eco journée » |
| **Hors-gel** | Absent (`away`), température Hors-gel | « Hors-gel », « hors gel », « Horsgel vacances » |
| **Boost** | Activité (`activity`), température Boost | « Boost », « boost douche soir » |
| tout autre mot | Confort | « Douche soir », « Réunion », « Douche boost » |
| aucun événement en cours | celui choisi dans le blueprint (Éco par défaut) | — |

Les températures sont celles saisies dans les préréglages du thermostat de la
pièce (§ 2), par exemple Hors-gel 7 °C, Éco 17 °C, Confort 20 °C, Boost 23 °C.

**Mode et consigne dans le titre (clim, ou radiateur à une température précise).**
Le titre se lit dans cet ordre : **un mode** facultatif, **un mot-clé** facultatif
(tableau ci-dessus ; sans mot-clé : Confort), **une consigne** facultative (le premier
nombre du titre, virgule ou point, « °C » facultatif).

| Commencer le titre par | Effet | Exemples |
|---|---|---|
| **Chaud** | Allume l'appareil en mode chaud (`heat`), puis applique la suite | « Chaud », « Chaud 21 », « Chaud éco » |
| **Froid** | Allume l'appareil en mode froid (`cool`), puis applique la suite | « Froid 25 », « Froid éco », « Froid confort sieste » |
| **Arrêt** | Éteint l'appareil (`off`) | « Arrêt », « arret nuit » |
| un mot-clé ou un nombre, sans mode | Mode de l'appareil inchangé ; un appareil éteint reste éteint | « Confort 21 », « 19,5 », « Éco » |

- **Une consigne dans le titre** l'emporte sur le mot-clé : « Froid 25 » règle 25 °C,
  « Confort 21 » règle 21 °C. Un préréglage actif est d'abord remis à « aucun »
  (`none`), sinon il reprendrait la main. Elle est bornée au minimum et au maximum de
  l'appareil. Attention : tout nombre compte (« Réunion 2 » demande 2 °C, ramené au
  minimum) ;
- **sans consigne**, le mot-clé applique le préréglage, ou la consigne de la série
  chaud ou froid si la méthode **Consigne** est choisie (§ 4) ;
- **mode automatique à deux bornes** (`heat_cool`, `auto` avec borne basse et borne
  haute) : un nombre donne la borne basse, un second la borne haute (« Confort 20
  25 ») ; sans nombre, la série chaud donne la borne basse et la série froid la borne
  haute. Le blueprint ne passe jamais lui-même en mode automatique ;
- **sans mode dans le titre**, le mode n'est jamais changé : pour qu'un événement
  rallume une clim éteinte, commencer son titre par « Chaud » ou « Froid ».

Exemple d'été (séjour, clim, hors événement **Arrêt**) : « Froid 26 » de 14 h à 19 h,
« Froid confort » de 19 h à 23 h ; la clim s'allume en froid à 14 h, passe à la
consigne Confort froid (25 °C) à 19 h et s'éteint à 23 h.

**Entre deux événements** (aucun événement en cours), le thermostat prend le
préréglage du champ **Hors événement** de l'automatisation de la pièce : Éco par
défaut, soit 17 °C dans l'exemple. Il se choisit pièce par pièce (Confort, Éco,
Hors-gel, Boost ou Arrêt) : Hors-gel, par exemple, pour une pièce peu utilisée qui ne
doit chauffer que pendant ses créneaux ; **Arrêt** pour une clim qui ne doit tourner
que pendant ses créneaux (elle est éteinte à la fin de chaque événement).

**Règles à retenir :**

- **Le mot-clé en premier** : « Boost douche » donne Boost, « Douche boost » donne
  Confort ;
- **un titre non reconnu chauffe en Confort**, jamais en Boost ni en Éco ;
- **pas de créneau Éco nécessaire** : hors événement, c'est déjà Éco. Créer
  surtout les créneaux Confort et Boost, et des créneaux Hors-gel pour les absences ;
- **pas de chevauchement** : quand deux événements se superposent, seul celui qui
  a commencé le premier compte, jusqu'à sa fin. Exemple : « Boost » de 21 h 18 à
  22 h et « Douche soir » de 21 h 30 à 22 h : Boost jusqu'à 22 h, « Douche soir »
  n'est jamais appliqué. Mettre les événements bout à bout (le second commence à
  l'heure de fin du premier) : le passage de l'un à l'autre est immédiat ;
- **répétitions** (tous les jours ouvrés, chaque samedi…) : se règlent dans
  l'événement ; une exception se modifie sur la seule occurrence (voir plus bas) ;
- **effet immédiat** : modifier l'heure de fin d'un événement en cours (par
  exemple l'avancer à maintenant) applique le préréglage suivant à cette heure-là.

**Exemple de semaine** (salle de bain), hors événement Éco :

| Jours | Événement | Effet |
|---|---|---|
| Lundi à vendredi, 6 h 30 – 7 h 15 | « Boost matin » | 23 °C pendant les douches |
| Lundi à vendredi, 7 h 15 – 8 h | « Confort » | 20 °C, puis Éco |
| Tous les jours, 21 h – 21 h 45 | « Boost douche soir » | 23 °C, puis Éco pour la nuit |
| Samedi et dimanche, 8 h – 11 h | « Confort week-end » | 20 °C |
| Vacances (du… au…) | « Hors-gel vacances », sur plusieurs jours | 7 °C ; commencé avant les créneaux de la période, il l'emporte sur eux (à vérifier, cahier Z14) ; au moindre doute, supprimer les occurrences de la période |

**Modifier ou supprimer un calendrier existant**

- **Nom affiché** : **Paramètres › Appareils et services › Entités**, cliquer le
  `calendar.…`, **⚙ › Nom › Mettre à jour**. L'identifiant ne change pas : les
  automatisations continuent de fonctionner.
- **Identifiant** (`calendar.…`) : même endroit, champ **ID d'entité**. Rechoisir
  ensuite le calendrier dans l'automatisation de chauffage de la pièce et dans le
  champ Calendriers de l'automatisation du module HAPanel.
- **Événements** : panneau **Calendrier** de la barre latérale, cliquer
  l'événement, **Modifier** ou **Supprimer** ; pour un événement répété, choisir
  cette occurrence, celle-ci et les suivantes, ou toutes.
- **Supprimer le calendrier** : d'abord le retirer de l'automatisation de chauffage
  et du champ Calendriers des modules (sinon « Entité inconnue »), puis
  **Paramètres › Appareils et services › Calendrier local**, sur sa ligne
  **⋮ › Supprimer**. Ses événements sont perdus, sans retour possible.

## 4. Importer le blueprint et créer une automatisation par pièce

1. Importer `blueprints/automation/chauffage/agenda_piece.yaml` par son URL GitHub (**Blueprints › Importer un blueprint**), ou le copier dans
   `config/blueprints/automation/chauffage/agenda_piece.yaml` (Studio Code
   Server ou partage Samba), puis **Outils de développement › YAML ›
   Recharger les automatisations**. Adresse à importer :
   `https://github.com/cnuma/HAPanel/blob/main/blueprints/automation/chauffage/agenda_piece.yaml`
   (avant la fusion, remplacer `main` par le nom de la branche d'essai).
2. **Paramètres › Automatisations et scènes › Blueprints › Chauffage et clim —
   agenda d'une pièce › Créer une automatisation** : choisir le calendrier et le
   thermostat (ou la clim) de la pièce. Laisser la correspondance par défaut.
3. **Méthode** : **Préréglage** (par défaut) pour un thermostat qui en a (thermostat
   générique, clim avec préréglages : vérifier l'attribut `preset_modes` dans
   **Outils de développement › États**) ; **Consigne** pour une clim sans
   préréglage. Avec Consigne, régler la section repliée **Consignes** : une
   température par mot-clé, série chaud et série froid.
   Home Assistant ne sait pas masquer la section de l'autre méthode : elle reste
   affichée, mais elle est ignorée (sa description le rappelle).

| Consigne par défaut | Confort | Éco | Hors-gel | Boost |
|---|---|---|---|---|
| Chaud (modes chaud et auto) | 20 °C | 17 °C | 7 °C | 23 °C |
| Froid (mode froid) | 25 °C | 28 °C | 32 °C (presque pas de froid) | 22 °C |

La série suit le mode de l'appareil au moment d'appliquer : passer la clim de chaud à
froid applique aussitôt la consigne froid du moment. Les consignes sont bornées au
minimum et au maximum de l'appareil (une clim limitée à 30 °C reçoit 30 pour 32).

Comportement :

- le réglage est réappliqué à chaque début ou fin d'événement, au démarrage de HA et
  à chaque changement de mode de l'appareil (rallumage, passage chaud ↔ froid) ;
- un changement manuel (panneau, tableau de bord) tient jusqu'au prochain
  changement du calendrier ; un mode changé à la main contre le titre en cours (clim
  mise en chaud pendant « Froid 25 », ou éteinte) est respecté jusqu'au prochain
  changement du calendrier ;
- le mode n'est changé que par un titre commençant par « Chaud », « Froid » ou
  « Arrêt », ou par « Arrêt » hors événement ; sinon un appareil éteint (été) reste
  éteint ; au démarrage de HA, le mode du titre en cours est réappliqué ;
- en déshumidification (`dry`) ou ventilation (`fan_only`), rien n'est fait, sauf
  sur un titre avec mode ;
- avec un calendrier ou un thermostat indisponible, rien n'est fait ;
- un préréglage ou un mode inconnu de l'appareil est écrit dans le journal, sous
  `chauffage.agenda`.

**Vérifier :** créez un événement « Boost » qui commence dans 2 minutes. À
l'heure dite, le thermostat passe en Activité (`activity`, le Boost) et l'interrupteur s'allume si la
pièce est sous la consigne. À la fin de l'événement, il revient au préréglage
« hors événement ».

### Présence (option désactivée par défaut)

Les capteurs de mouvement (infrarouge) de la pièce peuvent chauffer la pièce quand
quelqu'un y entre en dehors des événements, par exemple pendant une période Éco. C'est
une option, pièce par pièce : dans l'automatisation, ouvrir la section repliée
**Présence (option)** et allumer **Activer la présence**. Éteinte, les capteurs sont
ignorés et seul le calendrier compte, même si des capteurs restent choisis.

| Réglage | Rôle | Par défaut |
|---|---|---|
| Activer la présence | Allume ou coupe l'option pour cette pièce | éteint |
| Déclencheurs de présence | Autant de déclencheurs que voulu, de types mélangés, tous à « on » quand quelqu'un est là : capteur de mouvement, de présence ou d'ouverture (`binary_sensor`), lumière (`light`), prise ou interrupteur (`switch`), entrée booléenne (`input_boolean`, par exemple un bouton « Je suis là » du tableau de bord), ventilateur (`fan`). Un seul à « on » suffit ; la durée part du dernier changement de l'un d'eux. Sans déclencheur, la présence est ignorée | aucun |
| Préréglage de présence | Préréglage appliqué tant qu'une présence est détectée | Confort |
| Durée après le dernier mouvement | Le préréglage de présence tient encore cette durée après le dernier mouvement ; chaque nouveau mouvement la relance | 30 min (5 à 240) |
| Détection à partir de / jusqu'à | Plage horaire où un mouvement compte ; début égal à la fin = toute la journée ; la plage peut passer minuit (22:00 à 06:00) | 00:00 à 00:00 (toute la journée) |

Règles :

- **Le planning reprend toujours le dessus.** Pendant un événement, les capteurs sont
  ignorés. Quand un événement commence pendant une présence, son préréglage s'applique ;
  quand il finit et que quelqu'un a bougé depuis moins que la durée, le préréglage de
  présence s'applique au lieu du préréglage hors événement.
- **Fin de présence** : la durée écoulée sans mouvement, ou l'heure de fin de la plage,
  ramène le préréglage hors événement.
- **Un réglage manuel est respecté** : un mouvement ou une fin de présence ne change le
  préréglage que s'il est sur celui de hors événement ou de présence. Un Boost réglé
  sur le module tient donc jusqu'au prochain changement du calendrier.
- Le mode n'est jamais changé : un thermostat éteint ne s'allume pas sur un mouvement.
- Un capteur infrarouge ne voit pas une personne immobile (lecture, sieste) : prévoir une
  durée assez longue, ou un événement du calendrier pour les moments prévisibles.
- Après un redémarrage de HA, seul un capteur à « on » compte au démarrage. Si un
  événement finit dans les minutes qui suivent, la présence peut être retenue au plus
  pendant la durée choisie, puis le préréglage hors événement revient.

Exemple de séjour : deux capteurs IR qui couvrent chacun une partie de la pièce, pour le
même radiateur. On les choisit tous les deux : un mouvement devant l'un ou l'autre
chauffe, et chacun relance la durée.

Exemple de salle de bain : capteur de mouvement et lumière. Allumer la lumière suffit à
chauffer ; la présence tient tant que la lumière est allumée, puis la durée choisie après
l'avoir éteinte ou après le dernier mouvement. Éviter un déclencheur commandé par une
automatisation qui reste allumé longtemps (lumière d'ambiance, prise toujours sous
tension) : la pièce resterait chauffée.

Un déclencheur d'un autre type (lecteur multimédia, personne présente dans la maison)
n'est pas proposé, car son état n'est pas « on ». Le ramener à « on » par une entité
**Modèle** de type capteur binaire (**Paramètres › Appareils et services › Entrées ›
Créer une entrée › Modèle**), puis la choisir ici.

**Vérifier :** sans événement en cours (Éco), passer devant le capteur : le thermostat
passe en Confort. Ne plus bouger : il revient en Éco après la durée choisie.

## 5. Désinstaller Versatile Thermostat

À faire une fois toutes les pièces passées en thermostat générique et testées.

1. Mettre à jour les automatisations, scripts, scènes et tableaux de bord
   listés au §1 pour qu'ils pointent vers les nouveaux thermostats. Le
   blueprint HAPanel `module.yaml` sera traité à part (voir §6).
2. **Paramètres › Appareils et services › Versatile Thermostat** : pour
   chaque entrée (thermostats et configuration centrale), **⋮ › Supprimer**.
3. **HACS** : Versatile Thermostat, **⋮ › Supprimer**. Faire de même pour la
   carte `Versatile Thermostat UI Card` si elle est installée. Vérifier
   ensuite qu'elle a disparu de **Paramètres › Tableaux de bord › ⋮ ›
   Ressources**.
4. Retirer d'éventuelles lignes `versatile_thermostat:` de `configuration.yaml`.
5. **Paramètres › Système › ⏻ › Redémarrer Home Assistant**.
6. Contrôler :
   - le dossier `config/custom_components/versatile_thermostat` n'existe plus ;
   - dans **Entités**, filtre « Afficher les entités en lecture seule ou
     indisponibles », aucune entité VT ne reste ; sinon, la sélectionner et
     **Supprimer** ;
   - **Paramètres › Réparations** : rien qui mentionne VT ;
   - les fils pilotes sont bien commandés par les thermostats génériques
     (historique de l'interrupteur).
7. Facultatif : purger l'historique des anciennes entités avec
   `recorder.purge_entities` (Outils de développement › Actions).

**Astuce pour garder les mêmes noms :** une fois VT supprimé, vous pouvez
donner à chaque thermostat générique l'identifiant de l'ancien thermostat VT
(**Entité › ⚙ › ID d'entité**). Tableaux de bord et automatisations
retrouvent alors leur entité sans rien modifier.

## 6. Ce que cela change pour les modules HAPanel

- Le module connaît les préréglages `none`, `frost`, `eco`, `comfort` et
  `boost`. Le blueprint `module.yaml` traduit pour le thermostat générique :
  ses boutons Hors-gel et Boost commandent Absent (`away`) et Activité
  (`activity`), et un thermostat en Absent ou Activité (par le calendrier) est
  affiché en Hors-gel ou Boost. La traduction n'a lieu que si le thermostat ne
  connaît pas lui-même `frost` ou `boost` : un module resté sur Versatile
  Thermostat n'est pas touché. Réimporter `module.yaml` pour en profiter.
- `is_locked` n'existe plus : le verrou du thermostat ne s'affichera jamais.
  C'est sans gêne.
- L'alarme « Thermostat en sécurité » (préréglage `safety` de VT) ne se
  déclenchera plus.
- Le thermostat générique n'a pas de mise en sécurité : si le capteur de la
  pièce se tait, il garde son dernier état. L'alarme « température périmée »
  du module reste le garde-fou visible.

## 7. Dépannage

Pour savoir ce que l'automatisation a fait : **Paramètres › Automatisations et
scènes**, l'automatisation de la pièce, **⋮ › Traces**, choisir l'exécution de
l'heure voulue, onglet **Chronologie de l'exécution**. L'onglet **Variables
modifiées** donne le `titre` lu et le `prereglage` choisi.

| Ce qu'on voit | Cause | Que faire |
|---|---|---|
| Préréglage non appliqué ; trace : « Si : Action else exécutée », puis « System Log : Écrire dans le journal système » | Le thermostat ne connaît pas ce préréglage : sa température n'est pas saisie (le Boost demande **Activité**, le Hors-gel **Absent**). Le journal (**Paramètres › Système › Journaux**, chercher `Chauffage :`) donne le nom refusé et la liste connue | Saisir la température manquante (§ 2, **Préréglages de température**) ; vérifier dans **Outils de développement › États**, attribut `preset_modes` du thermostat |
| Toujours « boost » refusé après cela | Automatisation créée avec une ancienne version du blueprint, qui envoyait `boost` | Réimporter le blueprint (**Blueprints**, **⋮ › Réimporter le blueprint**) ; dans l'automatisation, **Correspondance avec le thermostat**, Boost sur `activity` |
| Trace arrêtée au premier test (« Tester Si le modèle… ») | Thermostat éteint (`off`), ou calendrier ou thermostat indisponible : rien n'est fait, volontairement | Rallumer le thermostat : le préréglage du moment s'applique aussitôt |
| Thermostat trouvé éteint sans savoir pourquoi | Thermostat générique créé sans **Mode** : il démarre éteint, puis garde son dernier état à chaque redémarrage ; ou glissière Éteint / Chauffage d'un module HAPanel ; ou une autre automatisation ou une personne | **Journal de bord** du thermostat : la ligne « est passé à Éteint » donne l'origine (rien à l'heure de la création ou d'un redémarrage, une automatisation, ou une personne par l'action `climate.set_hvac_mode`). Régler **Mode** sur Chauffage dans les options du thermostat |
| Confort au lieu du préréglage attendu | Titre qui ne commence pas par le mot-clé (« Douche boost ») | Mettre le mot-clé en premier (§ 3) |
| Préréglage d'un événement jamais appliqué | Il chevauche un événement commencé avant lui | Mettre les événements bout à bout (§ 3) |
| Bon préréglage, mais le radiateur ne chauffe pas | La pièce est déjà au-dessus de la consigne : attribut `hvac_action` à `idle` | Normal ; il chauffe dès que la température passe sous la consigne moins la tolérance |
| Module HAPanel : préréglages tous grisés, aucun entouré, quand le calendrier passe en Boost ou Hors-gel ; boutons Boost et Hors-gel refusés | Blueprint `module.yaml` antérieur à la traduction `away` / `activity` | Réimporter `module.yaml` (**Blueprints**, **⋮ › Réimporter le blueprint**) |
| Aucune trace à l'heure de l'événement | Automatisation désactivée, ou calendrier non choisi | Vérifier l'automatisation (activée, calendrier de la pièce) |
| « Entité inconnue sélectionnée » dans l'automatisation | Calendrier ou thermostat supprimé ou renommé (identifiant changé) | Rechoisir l'entité ; voir § 3, « Modifier ou supprimer un calendrier existant » |
| Clim : « Froid 25 » sans effet ; journal « Chauffage : mode « cool » inconnu » | La clim n'a pas ce mode (attribut `hvac_modes`) | Vérifier `hvac_modes` dans **Outils de développement › États** |
| Clim : l'événement sans « Chaud » ni « Froid » ne l'allume pas | Normal : sans mode dans le titre, le mode n'est jamais changé | Commencer le titre par « Chaud » ou « Froid » |
| Clim : consigne non appliquée, journal « préréglage … inconnu » | Méthode **Préréglage** sur une clim qui n'en a pas | Méthode **Consigne**, ou une consigne dans le titre |
| Consigne différente du titre | Bornée au minimum ou au maximum de l'appareil (`min_temp`, `max_temp`), ou un autre nombre dans le titre | Corriger le titre ; un seul nombre, la consigne |
| Un mouvement ne change rien | Option **Activer la présence** éteinte, événement en cours (le planning prime), heure hors de la plage de détection, préréglage changé à la main, ou capteur qui ne passe pas à « on » | Normal dans les trois premiers cas ; sinon, **Outils de développement › États**, état du capteur ; trace : arrêt au test « présence » (Variables modifiées : `present`, `dans_plage`) |
| Le Confort de présence ne s'arrête pas | Un déclencheur reste à « on » (lumière ou prise oubliée), ou détecte sans cesse (animal, rideau, radiateur dans son champ) | Historique du capteur ; le déplacer ou en retirer un de la liste |
