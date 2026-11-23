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

| Titre de l'événement | Préréglage appliqué |
|---|---|
| Confort | Confort (`comfort`) |
| Éco | Éco (`eco`) |
| Hors-gel | Hors-gel (`away`) |
| Boost | Boost (`activity`) |
| tout autre titre | Confort |
| aucun événement | réglable dans le blueprint (Éco par défaut) |

Seul **le début du titre** compte : « Boost douche » donne Boost, « Douche boost »
Confort. Majuscules et accents sont ignorés (« eco », « HORS GEL » fonctionnent).
Hors événement, c'est déjà le préréglage par défaut (Éco) : créer surtout les
créneaux Confort, Boost et, pour les absences, Hors-gel. Les
répétitions (tous les jours ouvrés, de 6 h 30 à 8 h, etc.) se règlent dans
l'événement. Évitez de superposer deux événements : seul le premier compte.

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
