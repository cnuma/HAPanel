# Déploiement public — HAPanel (D039, D037 révisée)

Procédure du binaire public, sans secret : publication sur GitHub, première
installation d'un module, adoption dans Home Assistant, mises à jour depuis Home
Assistant. C'est le mode de déploiement de **tous les modules de la maison** (D037
révisée), validé par la partie J du cahier de tests. Ce document s'adresse au
développeur ; le guide pas à pas pour un débutant est
[INSTALLATION.md](INSTALLATION.md).

Les configurations privées (`hapanel.yaml`, `hapanel_banc.yaml`, secrets compilés,
mise à jour depuis le PC par `tools/build.ps1 upload`) ne servent plus qu'aux modules
de test de l'atelier.

## 1. Publier une version

1. Le commit à publier est poussé sur GitHub. Le fichier `VERSION` donne la base de
   la version, par exemple `0.8.0-dev`. `NOUVEAUTES.md` contient une ligne courte pour
   cette version, sous `## <version>` (`## 0.8.0` suffit pour `0.8.0-dev.1`) : c'est le
   résumé affiché par le module avant l'installation et par HA (D047). Sans ligne,
   la publication le signale (avertissement dans Actions) et rien ne s'affiche.
2. Créer et pousser l'étiquette, dont la version commence par le contenu de
   `VERSION` :

   ```powershell
   git tag v0.8.0-dev.1
   git push origin v0.8.0-dev.1
   ```

3. GitHub Actions lance « Publication » (onglet **Actions** du dépôt, environ 6 min) :
   il compile une configuration publique par carte et crée la Release `v0.8.0-dev.1`
   avec, pour chaque carte, trois fichiers (D041) :

   | Carte | Configuration | Première installation | Mise à jour | Manifeste |
   |---|---|---|---|---|
   | ESP32-2432S024C (2,4", capacitif) | `hapanel_public.yaml` | `hapanel-2432s024c-factory.bin` | `hapanel-2432s024c-ota.bin` | `manifest.json` |
   | ESP32-2432S028, deux prises USB (2,8", résistif) | `hapanel_2432s028_public.yaml` | `hapanel-2432s028-factory.bin` | `hapanel-2432s028-ota.bin` | `manifest-2432s028.json` |
   | Guition JC4827W543 (4,3", ESP32-S3, D049) | `hapanel_jc4827w543_public.yaml` | `hapanel-jc4827w543-factory.bin` | `hapanel-jc4827w543-ota.bin` | `manifest-jc4827w543.json` |

   Le manifeste de la S024C garde le nom `manifest.json` : son adresse est compilée
   dans les modules déjà installés. Jusqu'à `v0.8.1` incluse, la Release ne contenait
   que la S024C, sous les noms `hapanel-factory.bin` et `hapanel-ota.bin`.
4. Vérifier la Release : les neuf fichiers sont présents, elle est marquée
   **Latest** ; `manifest-jc4827w543.json` porte `"chipFamily": "ESP32-S3"`, les deux
   autres `"ESP32"` (D049).

**Forme des versions :** toujours `X.Y.Z-dev.N`, puis `X.Y.Z`, sans suffixe ajouté.
HA ne propose une mise à jour que si la version publiée est plus récente que
l'installée ; or il juge incomparables `0.8.0-dev.3-usb` et `0.8.0-dev.4` (constaté le
5 novembre 2026) : l'entité reste « À jour ». Un binaire de test local ne porte donc
pas de suffixe ; s'il en porte un, lancer l'action `update.install` de HA sur
l'entité Firmware (à confirmer, cahier J6).

Le binaire publié ne contient aucun secret : la configuration publique n'en lit
aucun (`secrets.yaml` n'existe pas sur GitHub).

## 2. Première installation d'un module

Il faut un ordinateur avec Chrome ou Edge, un câble USB de données et le module.

1. Télécharger le binaire complet **de la carte** depuis la Release (`hapanel-<carte>-factory.bin`,
   tableau du § 1). Un binaire d'une autre carte s'installe, mais l'écran reste noir ou
   le tactile muet.
2. Ouvrir <https://web.esphome.io>, brancher le module, **Connection**, choisir son
   port (« USB Serial (COM…) »), **Connexion**.
3. Petite flèche « Installer » (pas « Préparation pour la première utilisation »,
   qui installe le logiciel ESPHome de base), **Choisir un fichier** :
   `hapanel-<carte>-factory.bin`, **Installer**. L'écriture efface le module. Attendre la
   fin (environ 2 min).
4. Fenêtre « Configure Wi-Fi » (Improv) : choisir le réseau, saisir son mot de
   passe, **Connect** ; « Provisioned! » quand le module a rejoint le réseau.
5. **Couper l'alimentation** (débrancher, rebrancher), puis seulement juger l'écran
   et le toucher : sans broche de remise à zéro (Guition 4,3"), l'écran garde l'état
   du logiciel précédent jusqu'à la coupure (couleurs inversées, image à 180°).

**Sans câble ou si Improv échoue :** dans les 15 min qui suivent la mise sous
tension, le module ouvre un point d'accès Wi-Fi à son nom (`hapanel-xxxxxx`). S'y
connecter avec un téléphone : une page s'ouvre pour choisir le réseau. Passé ce délai,
couper et rétablir l'alimentation pour rouvrir la fenêtre.

## 3. Adoption dans Home Assistant

1. **Paramètres › Appareils et services** : HA signale un appareil ESPHome découvert,
   `HAPanel xxxxxx (hapanel-xxxxxx)`. **Ajouter**, **Valider**, puis pièce et
   **Terminer**.
2. HA envoie au module une clé de chiffrement qu'il crée lui-même ; le module la garde
   et n'accepte plus que cette clé. Aucune clé n'est à saisir.
3. Importer le blueprint et créer l'automatisation du module :
   `docs/CONFIGURATION.md`.

Aucune clé n'a été demandée lors du test du 5 novembre 2026 (cahier J3, J4). **Si HA
en demande une**, noter ce que HA affiche et ne rien saisir.

**Module qui tournait avec le binaire privé** (passage au binaire public) : refaire
le § 2 ; le Wi-Fi est à ressaisir. Même démarche dans HA qu'au § 5.

## 4. Mettre à jour un module

1. Une fois la nouvelle Release publiée (§ 1), l'entité **Firmware** du module
   passe à « Mise à jour disponible » ; depuis 0.10.0, le module le montre aussi : flèche
   violette qui clignote dans la barre du haut, deux éclairs violets de la LED toutes les
   10 s (D045, [UTILISATION.md](UTILISATION.md)). Le module vérifie 10 s après sa
   première connexion au Wi-Fi, puis chaque nuit à 3 h, heure de HA (D047). Pour
   forcer : bouton « Rechercher une mise à jour » de la page À propos, ou redémarrer
   le module ; l'action « Mettre à jour l'entité » de HA ne déclenche pas la
   vérification (constaté le 5 nov.). Le module peut aussi installer lui-même :
   Menu, tuile violette « Mise à jour », Installer (D047).
   Juste après une publication, HA peut encore proposer la version précédente, vue
   à la dernière vérification : redémarrer le module, puis vérifier la version
   proposée avant d'installer (sinon, deux mises à jour successives, sans dégât).
2. **Mettre à jour** (fenêtre « Firmware »). Le module télécharge le binaire depuis GitHub, vérifie son
   empreinte (MD5), l'écrit et redémarre (2 à 3 min).
3. Vérifier l'entité **Version** : elle donne la nouvelle version et son SHA.

Le Wi-Fi et la clé ne sont pas à ressaisir : ils sont gardés en flash. Chaque module
lit le manifeste de sa carte : HA ne lui propose jamais le binaire d'une autre carte.

## 5. Remise à zéro

Pour céder un module ou repartir de zéro : refaire le § 2, dont l'écriture efface le
module. Le Wi-Fi et la clé sont effacés ; dans HA, supprimer l'ancien appareil
avant de l'adopter de nouveau, puis rouvrir l'automatisation du module et l'y choisir
de nouveau dans « Panneau » : sans cela, l'accueil n'affiche rien de la maison.
Sans suppression préalable, HA propose de réassocier le module en prévenant que la
connexion ne sera plus chiffrée : refuser (D010), supprimer l'appareil, puis
l'adopter de nouveau ; il reçoit une nouvelle clé (constaté le 7 novembre 2026,
cahier J14).
