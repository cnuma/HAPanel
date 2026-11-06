# Installer un module HAPanel

Ce guide s'adresse à une personne qui n'a jamais installé de module ESPHome. Il va
du module neuf, sorti de sa boîte, jusqu'au module relié à votre Wi-Fi ; la suite
est dans [CONFIGURATION.md](CONFIGURATION.md). Comptez 15 minutes. Aucune ligne de
commande, rien à compiler, aucun mot de passe à inventer.

*Brouillon : les emplacements « 📷 Capture » seront remplacés par les captures prises
au reflash du premier module de production (cahier J14).*

## Ce qu'il vous faut

- **Le module** HAPanel (carte ESP32-2432S024C).
- **Un câble USB de données.** Certains câbles ne font que charger : si l'ordinateur
  ne voit pas le module (étape 2), essayez-en un autre.
- **Un ordinateur avec Chrome ou Edge.** Firefox et Safari ne savent pas écrire dans
  un module.
- **Un bloc secteur USB de 1 A** pour l'usage normal. Le port USB d'un ordinateur
  suffit pour l'installation, mais peut faire redémarrer le module en boucle ensuite.
- **Le nom et le mot de passe de votre Wi-Fi.** Le module ne voit que le Wi-Fi
  2,4 GHz : si votre box sépare 2,4 et 5 GHz, choisissez le réseau 2,4 GHz.
- **Home Assistant**, sur le même réseau, avec un compte administrateur.

## 1. Télécharger le logiciel du module

1. Ouvrez la page des versions :
   <https://github.com/cnuma/HAPanel/releases/latest>.
2. En bas de la page, la rubrique **Assets** liste 5 fichiers. Cliquez sur le
   premier, `hapanel-factory.bin` (encadré en rouge). Il arrive dans votre dossier
   Téléchargements.

![Page de la version, fichier hapanel-factory.bin encadré](images/installation/01_release.png)

Les 4 autres ne servent pas ici : `hapanel-ota.bin` et `manifest.json` servent aux
mises à jour, que Home Assistant fera seul
([CONFIGURATION.md](CONFIGURATION.md), section 7) ; « Source code » est le code du
projet.

## 2. Brancher le module à l'ordinateur

1. Branchez le module à l'ordinateur avec le câble USB.
2. Dans Chrome ou Edge, ouvrez <https://web.esphome.io>.
3. Cliquez sur **Connection** (la page est en partie en anglais).

![Page d'accueil d'ESPHome Web, bouton Connection encadré](images/installation/02_web_esphome.png)

4. Une fenêtre liste les ports série. Choisissez celui qui apparaît quand vous
   branchez le module, puis **Connexion**.

> 📷 Capture 03 — fenêtre de choix du port (numéro du port masqué).

**La liste est vide ?** Changez de câble. Si rien n'y fait, installez le pilote du
convertisseur USB-série du module : son nom est écrit sur la petite puce près de la
prise USB (souvent CH340), le pilote se trouve sur le site de son fabricant.

## 3. Écrire le logiciel dans le module

1. Cliquez sur **Install**.

> 📷 Capture 04 — module connecté, bouton Install.

2. Choisissez le fichier `hapanel-factory.bin` téléchargé à l'étape 1.
3. Cochez l'effacement du module et confirmez. Tout ce qu'il contenait est effacé.

> 📷 Capture 05 — fenêtre de confirmation de l'effacement.

4. Attendez la fin de l'écriture, environ 2 minutes, sans débrancher.

> 📷 Capture 06 — barre de progression.
>
> 📷 Capture 07 — écriture terminée.

## 4. Relier le module au Wi-Fi

Juste après l'écriture, la page propose de configurer le Wi-Fi.

1. Cliquez sur **Configure Wi-Fi** (ou **Connect to Wi-Fi**).
2. Choisissez votre réseau 2,4 GHz, saisissez son mot de passe, **Connect**.

> 📷 Capture 08 — choix du réseau et mot de passe (nom du réseau masqué).

3. Le module redémarre et rejoint le Wi-Fi. La page l'indique.

> 📷 Capture 09 — Wi-Fi configuré.

Vous pouvez maintenant débrancher le module de l'ordinateur et le brancher sur son
bloc secteur : il garde le Wi-Fi.

L'écran affiche « Pas de communication avec Home Assistant » et un point rouge en
haut à droite : c'est normal, Home Assistant n'est pas encore relié (étape suivante).
La date ne s'affiche qu'une fois Home Assistant relié.

![Écran du module avant Home Assistant (maquette)](images/installation/10_module_sans_ha.png)

**La page n'a pas proposé le Wi-Fi, ou le module ne s'y connecte pas :** passez par
le point d'accès du module, ci-dessous.

### Autre méthode : depuis un téléphone

Tant qu'il n'a pas de Wi-Fi, le module crée son propre réseau Wi-Fi pendant
15 minutes après sa mise sous tension.

1. Sur le téléphone, ouvrez les réglages Wi-Fi et choisissez le réseau
   `hapanel-` suivi de six caractères.

> 📷 Capture 11 — liste des réseaux du téléphone, réseau `hapanel-xxxxxx`.

2. Une page s'ouvre seule (sinon, ouvrez <http://192.168.4.1> dans le navigateur
   du téléphone). Choisissez votre réseau, saisissez son mot de passe, **Save**.

> 📷 Capture 12 — page du module sur le téléphone (noms des réseaux masqués).

3. Le module redémarre et rejoint votre Wi-Fi ; son réseau `hapanel-…` disparaît.

**Le réseau `hapanel-…` n'apparaît pas :** les 15 minutes sont passées. Débranchez
puis rebranchez le module, et recommencez.

## 5. Suite : Home Assistant

Le module est sur votre Wi-Fi. Pour l'ajouter à Home Assistant et choisir ce qu'il
affiche, suivez [CONFIGURATION.md](CONFIGURATION.md), sections 1 à 3. Les mises à
jour suivantes passeront par Home Assistant, sans câble (section 7).

## Remplacer le logiciel d'un module déjà installé

Pour un module qui tournait avec une version compilée sur un ordinateur, pour le
céder ou pour repartir de zéro : refaites les étapes 1 à 4. Le Wi-Fi est à ressaisir.

Dans Home Assistant, si l'ancien appareil ne se reconnecte pas et qu'un nouveau est
découvert : ajoutez-le ([CONFIGURATION.md](CONFIGURATION.md), section 1), ouvrez l'automatisation du module, choisissez le
nouvel appareil dans « Panneau » et enregistrez. Supprimez ensuite l'ancien appareil.

## Dépannage

| Symptôme | Que faire |
|---|---|
| web.esphome.io ne liste aucun port | Autre câble USB ; pilote du convertisseur USB-série (étape 2) ; Chrome ou Edge |
| L'écriture s'arrête en erreur | Débrancher, rebrancher, recommencer l'étape 3 ; essayer un autre port USB de l'ordinateur |
| Pas de proposition de Wi-Fi après l'écriture | Méthode du téléphone (étape 4) |
| Le module ne rejoint pas le Wi-Fi | Réseau 2,4 GHz, mot de passe ; module trop loin de la box |
| Réseau `hapanel-…` absent | Plus de 15 minutes depuis la mise sous tension : débrancher, rebrancher |
| Le module redémarre en boucle | Alimentation trop faible : bloc secteur de 1 A |

Problème une fois dans Home Assistant : [dépannage de la configuration](CONFIGURATION.md#dépannage).
