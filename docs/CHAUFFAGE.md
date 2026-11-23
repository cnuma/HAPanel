# Chauffage : un thermostat générique piloté par agenda

Facultatif : le module HAPanel accepte n'importe quel thermostat `climate.…`. Ce
guide propose une régulation simple, sans intégration complémentaire : un
« Thermostat générique » de Home Assistant par pièce, qui commande l'interrupteur
du radiateur (fil pilote), et le blueprint `chauffage/agenda_piece.yaml`, qui lui
applique le préréglage du calendrier de la pièce (D058). Les §1 et §5 décrivent le
passage depuis Versatile Thermostat ; sans lui, passer directement au §2.

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
| Mode | Chauffage |
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

**Entre deux événements** (aucun événement en cours), le thermostat prend le
préréglage du champ **Hors événement** de l'automatisation de la pièce : Éco par
défaut, soit 17 °C dans l'exemple. Il se choisit pièce par pièce (Confort, Éco,
Hors-gel ou Boost) : Hors-gel, par exemple, pour une pièce peu utilisée qui ne doit
chauffer que pendant ses créneaux.

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
2. **Paramètres › Automatisations et scènes › Blueprints › Chauffage — agenda
   d'une pièce › Créer une automatisation** : choisir le calendrier et le
   thermostat de la pièce. Laisser la correspondance par défaut.

Comportement :

- le préréglage est réappliqué à chaque début ou fin d'événement, au démarrage
  de HA et quand on rallume le chauffage ;
- un changement manuel (panneau, tableau de bord) tient jusqu'au prochain
  changement du calendrier ;
- le mode n'est jamais changé : un chauffage éteint (été) reste éteint ;
- avec un calendrier ou un thermostat indisponible, rien n'est fait ;
- un préréglage inconnu du thermostat est écrit dans le journal, sous
  `chauffage.agenda`.

**Vérifier :** créez un événement « Boost » qui commence dans 2 minutes. À
l'heure dite, le thermostat passe en Activité (`activity`, le Boost) et l'interrupteur s'allume si la
pièce est sous la consigne. À la fin de l'événement, il revient au préréglage
« hors événement ».

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

- Le module envoie les préréglages `none`, `frost`, `eco`, `comfort` et
  `boost`. Le thermostat générique n'a ni `frost` ni `boost` : les boutons
  Hors-gel et Boost seront refusés tant que `module.yaml` ne traduit pas `frost`
  en `away` et `boost` en `activity` à l'envoi, et l'inverse dans la valeur
  renvoyée au module.
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
| Confort au lieu du préréglage attendu | Titre qui ne commence pas par le mot-clé (« Douche boost ») | Mettre le mot-clé en premier (§ 3) |
| Préréglage d'un événement jamais appliqué | Il chevauche un événement commencé avant lui | Mettre les événements bout à bout (§ 3) |
| Bon préréglage, mais le radiateur ne chauffe pas | La pièce est déjà au-dessus de la consigne : attribut `hvac_action` à `idle` | Normal ; il chauffe dès que la température passe sous la consigne moins la tolérance |
| Aucune trace à l'heure de l'événement | Automatisation désactivée, ou calendrier non choisi | Vérifier l'automatisation (activée, calendrier de la pièce) |
| « Entité inconnue sélectionnée » dans l'automatisation | Calendrier ou thermostat supprimé ou renommé (identifiant changé) | Rechoisir l'entité ; voir § 3, « Modifier ou supprimer un calendrier existant » |
