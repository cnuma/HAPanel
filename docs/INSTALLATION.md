# Installer un module HAPanel

Ce guide s'adresse à une personne qui n'a jamais installé de module ESPHome. Il va
du module neuf, sorti de sa boîte, jusqu'au module qui affiche votre maison. Comptez
30 minutes. Aucune ligne de commande, aucun mot de passe à inventer.

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
2. En bas de la page, sous **Assets**, cliquez sur `hapanel-factory.bin`. Le fichier
   arrive dans votre dossier Téléchargements.

> 📷 Capture 01 — page de la Release, rubrique Assets, `hapanel-factory.bin` entouré.

Ne prenez pas `hapanel-ota.bin` : il sert aux mises à jour, que Home Assistant fera
seul (étape 6).

## 2. Brancher le module à l'ordinateur

1. Branchez le module à l'ordinateur avec le câble USB.
2. Dans Chrome ou Edge, ouvrez <https://web.esphome.io>.
3. Cliquez sur **Connect**.

> 📷 Capture 02 — page d'accueil de web.esphome.io, bouton Connect.

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

> 📷 Capture 10 — photo de l'écran du module après démarrage : accueil, point HA rouge
> (Home Assistant n'est pas encore relié).

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

## 5. Ajouter le module dans Home Assistant

1. Dans Home Assistant, **Paramètres › Appareils et services**. Sous « Nouveaux
   appareils découverts », HAPanel apparaît : **Ajouter**.

> 📷 Capture 13 — appareil découvert dans Appareils et services.

2. Confirmez. Home Assistant crée lui-même la clé qui chiffre les échanges avec le
   module et la lui envoie : **aucune clé n'est à saisir.**

> 📷 Capture 14 — fenêtre de confirmation de l'ajout.

3. Choisissez la pièce du module, puis **Terminer**.

> 📷 Capture 15 — choix de la pièce.

**Home Assistant demande une clé de chiffrement :** ne saisissez rien, notez ce
qu'affiche Home Assistant et consultez le [Dépannage](#dépannage).

Le module doit maintenant afficher un point HA vert. Il affiche encore « non reçu » :
il ne sait pas quoi afficher, c'est l'étape suivante.

## 6. Choisir ce que le module affiche

1. Importez le blueprint HAPanel : [CONFIGURATION.md, section 2](CONFIGURATION.md#2-importer-le-blueprint).

> 📷 Capture 16 — fenêtre « Importer un blueprint » avec le lien collé.

2. Créez l'automatisation du module : [CONFIGURATION.md, section 3](CONFIGURATION.md#3-créer-lautomatisation-du-module).
   Choisissez le module dans « Panneau », puis vos thermomètres, thermostat, météo et
   calendriers.

> 📷 Capture 17 — formulaire de l'automatisation, partie haute (Panneau, Thermomètre).

3. Enregistrez. En quelques secondes, le module affiche vos températures.

> 📷 Capture 18 — photo de l'accueil du module avec les valeurs de la maison.

## 7. Recevoir les mises à jour

Rien à installer : quand une nouvelle version est publiée, Home Assistant la propose.

1. **Paramètres** : une ligne « Mise à jour disponible » apparaît pour le Firmware du
   module (le module vérifie au démarrage, puis toutes les 6 heures).
2. Ouvrez-la, **Installer**. Le module télécharge la nouvelle version, l'écrit et
   redémarre (2 à 3 minutes). Le Wi-Fi et la clé sont conservés.

> 📷 Capture 19 — mise à jour du Firmware proposée dans Home Assistant (à prendre à la
> première version publiée après celle installée).

## Remplacer le logiciel d'un module déjà installé

Pour un module qui tournait avec une version compilée sur un ordinateur, ou pour
repartir de zéro : refaites les étapes 1 à 4. Le Wi-Fi est à ressaisir.

Dans Home Assistant, si l'ancien appareil ne se reconnecte pas et qu'un nouveau est
découvert : ajoutez-le (étape 5), ouvrez l'automatisation du module, choisissez le
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
| Home Assistant ne découvre pas le module | **Ajouter une intégration › ESPHome**, puis l'adresse IP du module (donnée par la box) |
| Home Assistant demande une clé | Ne rien saisir ; noter le message. Si le module a déjà été ajouté à un autre Home Assistant, refaire les étapes 1 à 4 pour l'effacer |
| Point HA vert mais « non reçu » partout | Automatisation du module absente ou incomplète (étape 6) ; voir le [dépannage de la configuration](CONFIGURATION.md#dépannage) |
