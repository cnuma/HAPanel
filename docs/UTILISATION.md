# Utiliser HAPanel

HAPanel est un petit écran tactile mural relié à Home Assistant. Il sert à
régler le chauffage de la pièce, consulter la météo et le planning, et lancer des
scénarios de la maison.

*Les images sont des maquettes : les valeurs sont des exemples, et l'écran réel
peut légèrement différer.*

## L'essentiel

- La barre du bas est présente sur toutes les pages : **la maison** ramène à
  l'accueil (elle n'apparaît pas sur l'accueil), **Menu** ouvre la liste des pages.
- Après **1 minute sans toucher**, le panneau revient à l'accueil et l'écran
  s'éteint.
- Quand l'écran est éteint, **le premier toucher ne fait que le rallumer** : il ne
  déclenche aucune commande.
- Le panneau n'affiche jamais une valeur douteuse comme si elle était sûre. Un
  texte orange signale une valeur manquante, ancienne ou indisponible.

## Accueil

![Page d'accueil](images/accueil.png)

| Repère | Élément | Utilisation |
|---|---|---|
| 1 | Date, heure, Wi-Fi, point de connexion | Point vert : relié à Home Assistant. Point rouge : non relié. |
| 2 | Température de la pièce | Affichage seul. |
| 3 | Température extérieure | Affichage seul. |
| 4 | Préréglages : Manuel, Hors-gel, Éco, Confort, Boost | Touchez une icône pour changer. Le préréglage actif est entouré de blanc. |
| 5 | Consigne, avec **-** et **+** | Chaque toucher change de 0,5 °C. L'envoi part 2 secondes après le dernier toucher. |
| 6 | Glissière Éteint / Chauffage | Touchez le côté inactif, ou faites glisser la pastille. |
| 7 | Maison | Revient à l'accueil. |
| 8 | Menu | Ouvre la liste des pages. |

**Après une commande**, la valeur demandée reste en attente jusqu'à la confirmation
de Home Assistant. Sans confirmation au bout de 10 secondes, l'écran revient à la
valeur réelle : la commande n'a pas abouti.

**Quand le thermostat est verrouillé**, les réglages ne répondent plus et la
pastille de la glissière devient grise.

### Autres affichages de l'accueil

![Accueil, chauffage éteint et sans connexion](images/accueil_etats.png)

- **Chauffage éteint :** préréglages et consigne disparaissent.
- **Sans Home Assistant ou sans Wi-Fi :** un message donne la cause et aucune
  commande ne peut partir. L'écran reste allumé et la navigation continue de
  fonctionner.

## Menu

![Page Menu](images/menu.png)

Touchez une tuile pour ouvrir la page correspondante.

## Météo

![Page Météo](images/meteo.png)

Conditions actuelles en haut, puis prévisions sur 3 jours : température maximale /
minimale. Cette page ne commande rien.

## Planning

![Page Planning](images/planning.png)

- **En haut :** le calendrier principal, avec son résumé et la frise de la journée
  de 0 à 24 h. Les plages orange sont prévues, le trait blanc marque l'heure
  actuelle.
- **En dessous :** jusqu'à 3 autres calendriers. Leur point est orange pendant un
  créneau.

Le planning montre ce qui est **prévu** au calendrier, pas l'état réel du chauffage.
Cette page ne commande rien.

## Scénarios

![Page Scénarios](images/scenarios.png)

Chaque bouton a son nom et, selon la configuration, sa couleur et son icône. Un bouton
gris ne répond pas : la demande est en cours ou Home Assistant est déconnecté.

**Un seul toucher lance le scénario, sans confirmation.** Le message sous le titre
indique ensuite ce qui se passe :

![Messages après un lancement](images/scenarios_etats.png)

| Message | Signification |
|---|---|
| Envoi en cours | La demande est partie. Les boutons sont bloqués pendant l'attente. |
| Lancé : nom | Home Assistant a accepté. Cela ne garantit pas que le scénario ait réussi jusqu'au bout. |
| Refusé par HA | Le scénario n'est pas disponible ou n'existe plus. |
| Pas de réponse de HA | Aucune réponse en 10 secondes. Vérifiez le résultat avant de relancer. |
| Aucun scénario choisi | Rien n'est encore configuré pour ce panneau. |

Un bouton marqué **Indisponible** ne peut pas être touché.

## À propos

![Page À propos](images/apropos.png)

Version du logiciel, connexion à Home Assistant et mémoire. Ces informations sont
utiles en cas de dépannage.

## Écran et LED

**Luminosité de l'écran :** elle baisse dans une pièce sombre et remonte quand la
pièce est éclairée. Le changement est progressif et peut prendre environ une minute.

**LED de façade :** elle montre l'état du chauffage même écran éteint.

![Couleurs de la LED](images/led.png)

| LED | Signification |
|---|---|
| Couleur qui « respire » | Chauffage allumé, dans le préréglage de cette couleur. |
| Éteinte | Chauffage éteint. |
| Rouge clignotant | Anomalie : Home Assistant déconnecté, ou température ou chauffage non reçu, ancien ou indisponible. |

Boost est un rouge qui respire doucement, l'anomalie un rouge qui clignote franchement.

La respiration s'éteint un instant au creux de chaque cycle. Selon les réglages du
module (une chambre par exemple), la LED peut être éteinte en permanence et l'alerte
désactivée : seul l'écran montre alors une anomalie.

## Message d'accueil

Quand quelqu'un arrive après une absence, le panneau peut afficher un message de
bienvenue en plein écran, avec la météo. La LED change alors de couleur en continu.
Le message disparaît après 3 minutes. Pour le fermer avant, touchez **la croix** en
haut à droite, ou n'importe où sur l'écran : rien d'autre n'est déclenché.

## Textes orange

| Texte | Signification |
|---|---|
| non reçu | Le panneau n'a pas encore reçu la valeur depuis son démarrage. |
| indisponible | Home Assistant ne connaît pas la valeur actuellement. |
| périmé | Aucune nouvelle valeur depuis 15 minutes. |
| HA non connecté | Le panneau n'est pas relié à Home Assistant. |

Si un de ces messages persiste, consultez la section Dépannage de
[la configuration](CONFIGURATION.md#dépannage).
