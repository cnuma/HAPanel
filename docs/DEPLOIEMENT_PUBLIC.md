# Déploiement public — HAPanel (maquette D039)

Procédure du binaire public, sans secret : publication sur GitHub, première
installation d'un module, adoption dans Home Assistant, mises à jour depuis Home
Assistant. **État : maquette** (branche `feature/poc-deploiement`), validée par la
partie J du cahier de tests.

Les modules du propriétaire compilés avec `hapanel.yaml` (secrets compilés) ne sont
pas concernés : ils se mettent à jour depuis le PC (`tools/build.ps1 upload`).

## 1. Publier une version

1. Le commit à publier est poussé sur GitHub. Le fichier `VERSION` donne la base de
   la version, par exemple `0.8.0-dev`.
2. Créer et pousser l'étiquette, dont la version commence par le contenu de
   `VERSION` :

   ```powershell
   git tag v0.8.0-dev.1
   git push origin v0.8.0-dev.1
   ```

3. GitHub Actions lance « Publication » (onglet **Actions** du dépôt, 15 à 25 min) :
   il compile `hapanel_public.yaml` et crée la Release `v0.8.0-dev.1` avec
   `hapanel-factory.bin`, `hapanel-ota.bin` et `manifest.json`.
4. Vérifier la Release : les trois fichiers sont présents, elle est marquée
   **Latest**.

Le binaire publié ne contient aucun secret : la configuration publique n'en lit
aucun (`secrets.yaml` n'existe pas sur GitHub).

## 2. Première installation d'un module

Il faut un ordinateur avec Chrome ou Edge, un câble USB de données et le module.

1. Télécharger `hapanel-factory.bin` depuis la Release.
2. Ouvrir <https://web.esphome.io>, brancher le module, **Connect**, choisir son port.
3. **Install**, choisir `hapanel-factory.bin`, accepter l'effacement. Attendre la
   fin (environ 2 min).
4. Quand la page propose de configurer le Wi-Fi (Improv), choisir le réseau et
   saisir son mot de passe. Le module redémarre et rejoint le réseau.

**Sans câble ou si Improv échoue :** dans les 15 min qui suivent la mise sous
tension, le module ouvre un point d'accès Wi-Fi à son nom (`hapanel-xxxxxx`). S'y
connecter avec un téléphone : une page s'ouvre pour choisir le réseau. Passé ce délai,
couper et rétablir l'alimentation pour rouvrir la fenêtre.

## 3. Adoption dans Home Assistant

1. **Paramètres › Appareils et services** : HA signale un appareil ESPHome découvert,
   `hapanel-xxxxxx`. **Configurer**.
2. HA envoie au module une clé de chiffrement qu'il crée lui-même ; le module la garde
   et n'accepte plus que cette clé. Aucune clé n'est à saisir.
3. Importer le blueprint et créer l'automatisation du module :
   `docs/CONFIGURATION.md`.

**Si HA demande une clé :** la maquette n'a pas encore confirmé l'envoi automatique
(cahier J3). Noter ce que HA affiche et ne rien saisir.

## 4. Mettre à jour un module

1. Une fois la nouvelle Release publiée (§ 1), l'entité **Firmware** du module
   passe à « Mise à jour disponible ». Le module vérifie environ 20 s après son
   démarrage, puis toutes les 6 h. Pour forcer, redémarrer le module ; l'action
   « Mettre à jour l'entité » de HA ne déclenche pas la vérification (constaté le
   5 nov.).
2. **Installer**. Le module télécharge le binaire depuis GitHub, vérifie son
   empreinte (MD5), l'écrit et redémarre (2 à 3 min).
3. Vérifier l'entité **Version** : elle donne la nouvelle version et son SHA.

Le Wi-Fi et la clé ne sont pas à ressaisir : ils sont gardés en flash.

## 5. Remise à zéro

Pour céder un module ou repartir de zéro : refaire le § 2 en acceptant
l'effacement. Le Wi-Fi et la clé sont effacés ; dans HA, supprimer l'ancien appareil
avant de l'adopter de nouveau.
