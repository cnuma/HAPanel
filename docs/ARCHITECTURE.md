# Architecture de HAPanel

Document pour les ingénieurs qui reprennent ou font évoluer le projet. Il explique le
fonctionnement global ; le détail et l'historique des choix sont dans
[02_DECISIONS.md](codex/02_DECISIONS.md), notés `Dnnn` ci-dessous.

État décrit : version `0.6.0-dev`, commit `dc83077`, ESPHome 2026.10.1.

## Vue d'ensemble

HAPanel est un panneau mural sur ESP32 sans PSRAM, réalisé en YAML ESPHome avec LVGL.
Trois idées structurent tout le reste :

- **Le module ne décide de rien (D007).** Il affiche des valeurs et émet des demandes.
  Toute action sur un appareil est exécutée par Home Assistant (HA).
- **Un seul binaire, aucune entité compilée (D012).** Le firmware ne connaît que des
  clés génériques. Le choix des entités se fait dans HA, par une automatisation par
  module, créée depuis un blueprint unique (D021).
- **Le panneau ne ment pas (P2 à P4).** Une valeur inconnue, indisponible ou ancienne
  est affichée comme telle, et aucune commande ne se calcule à partir d'elle.

![Contexte du système](images/architecture/01_contexte.png)

| Chemin | Protocole | Sens | Rôle |
|---|---|---|---|
| Action `maj_valeur(cle, valeur)` | API native chiffrée | HA vers module | Toutes les valeurs affichées |
| Événement `esphome.hapanel_demande_valeurs` | API native | Module vers HA | Demande un envoi complet à la connexion |
| Événement `esphome.hapanel_commande` | API native | Module vers HA | Toutes les commandes |
| OTA | Réseau local chiffré | PC vers module | Mise à jour du firmware |

## Organisation du code

![Organisation des packages](images/architecture/02_packages.png)

- **Assemblage :** `hapanel.yaml` ne contient que des inclusions et des substitutions.
  `hapanel_banc.yaml` y ajoute le suivi mémoire et les journaux DEBUG.
- **Ordre d'inclusion :** ESPHome garde l'ordre des packages pour les pages, et la
  première page est affichée au démarrage. `accueil.yaml` doit donc rester avant
  `lvgl.yaml`.
- **Matériel :** seul `hardware.yaml` déclare broches et bus (G2).
- **Couplage :** les packages partagent des identifiants ESPHome globaux, sans
  encapsulation. Renommer un `id` ou une entité exposée exige une décision (G10).

## Matériel

![Matériel et brochage](images/architecture/03_materiel.png)

La carte est une ESP32-2432S024C (D004), au brochage publié sans documentation vendeur
et confirmé au banc (R6). Deux particularités :

- Aucune interruption n'arrive sur GPIO21 : le tactile est lu toutes les 50 ms (D009, dette T1).
- Un pic de courant au démarrage du Wi-Fi peut faire redémarrer la carte sur un port
  USB de PC et provoquer un retour silencieux au binaire précédent (R7).

## Flux des valeurs

![Flux des valeurs de HA vers l'écran](images/architecture/04_flux_valeurs.png)

Le blueprint pousse les valeurs une à une, sous forme de texte. `maj_valeur` copie clé
et valeur dans des tampons bornés (24 et 32 octets), car les paramètres pointent dans le
tampon de réception sans zéro terminal.

| Préfixe | Clés | Lecture |
|---|---|---|
| `temperature*` | `temperature`, `temperature_exterieure` | `accueil_rafraichir` |
| `chauffage_*`, `consigne_*` | mode, action, consigne, préréglage, verrou, bornes | `accueil_rafraichir` |
| `meteo_*` | condition, température, `meteo_jN_*` (N de 1 à 3) | `meteo_rafraichir` |
| `plan_*` | `plan_N_nom`, `plan_N_creneaux` (N de 1 à 4) | `planning_rafraichir` |
| `scen_*` | `scen_N_nom`, `scen_N_icone`, `scen_N_couleur` (N de 1 à 6), `scen_resultat` | `scenarios_rafraichir` |

**Traitement à part :** météo, planning et scénarios ne redessinent que leur page, pour ne
pas rafraîchir le chauffage et sa logique de commande à chaque valeur.

**Créneaux du planning :** `h` puis 24 chiffres hexadécimaux, soit 96 bits d'un quart
d'heure chacun. Le préfixe évite que HA interprète la chaîne comme un nombre (D020).

**Quand le blueprint envoie :**

| Déclencheur | Envoi |
|---|---|
| Changement d'un capteur ou du thermostat | Accueil |
| Changement de la météo | Météo |
| Changement d'un calendrier | Planning |
| Toutes les 5 min, démarrage de HA, demande du module | Tout |

Le `mode: queued` du blueprint sérialise les exécutions, avec 20 au plus en attente. Une
commande peut donc attendre la fin d'un envoi en cours.

## Connexion à Home Assistant

![Séquence de connexion](images/architecture/05_connexion.png)

`state_subscription_only` ne suffit pas : `esphome logs` s'abonne aussi aux états. Le
module considère donc HA connecté seulement si un client de l'API s'annonce avec un nom
commençant par « Home Assistant » (D013). Ce contrôle a lieu toutes les 2 s.

## Cycle de vie d'une valeur

![États d'une valeur](images/architecture/06_etats_valeur.png)

Chaque valeur ou groupe porte un état et l'instant de sa dernière réception. Un
`interval` de 30 s applique une péremption de 15 min. C'est le garde-fou quand le
blueprint est absent ou en erreur (R9).

## Commandes

Une commande est un événement `esphome.hapanel_commande` avec `commande` et `valeur`. HA y
ajoute le `device_id`, que le blueprint compare à son panneau.

![Séquence d'une consigne](images/architecture/07_consigne.png)

**Accueil :** le module applique une confirmation optimiste. La cible s'affiche en orange
jusqu'à ce que la valeur réelle la rejoigne, ou elle est abandonnée après 10 s. Le mode et
le préréglage suivent le même schéma, sans le délai de 2 s.

![Séquence d'un scénario](images/architecture/08_scenario.png)

**Scénarios :** le module n'envoie qu'un numéro, et le blueprint le traduit en entité : ce
chemin ne permet de lancer que les entités choisies. `Lancé` signifie que HA a accepté
l'action, pas qu'elle a abouti (D024).

| Commande | Valeur | Conditions vérifiées par le blueprint |
|---|---|---|
| `chauffage_mode` | `heat`, `off` | État différent, non verrouillé |
| `chauffage_consigne` | Nombre | Chauffage allumé, non verrouillé, dans les bornes |
| `chauffage_prereglage` | Préréglage | Connu du thermostat, chauffage allumé, non verrouillé |
| `scenario` | Numéro de 1 à 6 | Dans la liste, entité existante et non `unavailable` |

## Navigation et interface

![Navigation](images/architecture/11_navigation.png)

La barre est dans le `top_layer` de LVGL, donc commune à toutes les pages (D025). Une page
visible ou non reçoit ses mises à jour de la même façon : les widgets vivent en mémoire pour
toute la durée d'exécution.

**Ajouter une page :** créer `packages/pages/<page>.yaml`, l'inclure dans `hapanel.yaml`, ajouter
sa tuile dans `menu.yaml`, puis, si elle reçoit des valeurs, ajouter un préfixe dans `liaison_ha.yaml`
et un envoi dans le blueprint. Mesurer ensuite la mémoire (G6).

## Veille et retour à l'accueil

![Machine à états de la veille](images/architecture/09_veille.png)

`resume_on_input` est désactivé : le module se réveille au relâchement du doigt, alors que LVGL
en pause ignore le toucher. Le geste de réveil ne peut donc pas devenir un clic (D017).

## Lumière de la pièce

![Traitement de la LDR](images/architecture/10_lumiere.png)

Une même grandeur, `ldr_obscurite`, pilote le rétroéclairage (D023) et la LED (D018). La LDR
distingue mal les niveaux courants : c'est en pratique un réglage jour / nuit. Son comportement
en pièce sombre et l'influence de l'écran sur la mesure restent à confirmer au banc.

## Compilation et déploiement

![Chaîne de compilation](images/architecture/12_build.png)

- **Identité :** `tools/build.ps1` injecte `VERSION` et le SHA. Le suffixe `+modif` signale un
  binaire qui ne correspond à aucun commit et ne vaut pas validation (G5).
- **Version figée :** ESPHome est fixé par `requirements.txt` (D005).
- **Vérification :** après une OTA, relire la version et le SHA, puis attendre « Boot seems
  successful », car un échec peut ramener sans bruit au binaire précédent.
- **Blueprint :** `source_url` pointe sur `main`. Il suit Git et non le firmware : un changement de
  clés demande de mettre à jour les deux.
- **Dossier de compilation :** `hapanel.yaml` et `hapanel_banc.yaml` partagent `.esphome/build/hapanel` ;
  les alterner recompile environ 1 500 fichiers.

## Sécurité

![Frontières de confiance](images/architecture/13_securite.png)

| Risque | État |
|---|---|
| Clé d'API commune aux modules (R8) | Accepté : la clé d'un module ouvre l'API et l'OTA de tous |
| `maj_valeur` accessible à tout détenteur de la clé | Peut changer l'affichage, pas commander un appareil |
| Autorisation des actions HA du module | Nécessaire aux événements ; un firmware modifié pourrait s'en servir pour d'autres actions. La liste de scénarios ne remplace donc pas la protection de la clé |
| Secrets dans le dépôt (R3, G9) | `secrets.yaml` est ignoré par Git |
| Commande sur état inconnu (R4) | Refus côté module et côté blueprint |

Toute nouvelle surface s'inscrit dans [08_RISKS_AND_DEBT.md](codex/08_RISKS_AND_DEBT.md) avant fusion.

## Mémoire

![Occupation de la mémoire](images/architecture/14_memoire.png)

Sans PSRAM, la mémoire est la principale limite (R2). Chaque glyphe de police occupe de la flash,
d'où des listes de glyphes limitées : c'est pourquoi les scénarios proposent 25 icônes et non toute la
police (D026). Mesurer la mémoire libre et le plus grand bloc à chaque palier (G6).

## Limites connues

- **Tests :** il n'y a pas de test automatisé. La validation se fait au banc, et plusieurs états
  dégradés restent à confirmer (`docs/TODO.md`).
- **Latence des scénarios :** noms et disponibilité ne sont rafraîchis que toutes les 5 min.
- **Changement d'heure :** la frise du planning est décalée ce jour-là (D020).
- **Duplication :** `scenarios.yaml` répète six fois le même bouton, car ESPHome n'a pas de boucle
  de widgets simple.
- **Liste d'icônes :** elle existe dans le blueprint et dans `scenarios.yaml`, à garder alignée.

## Pour aller plus loin

| Sujet | Document |
|---|---|
| Invariants | [03_INVARIANTS.md](codex/03_INVARIANTS.md) |
| Règles de développement | [04_DEVELOPMENT_RULES.md](codex/04_DEVELOPMENT_RULES.md) |
| Compilation et tests | [05_BUILD_AND_TEST.md](codex/05_BUILD_AND_TEST.md) |
| Utilisation et configuration | [UTILISATION.md](UTILISATION.md), [CONFIGURATION.md](CONFIGURATION.md) |

Les schémas se régénèrent avec `tools/generer_schemas_architecture.py`.
