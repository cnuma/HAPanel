# 08 — Risques, surfaces exposées et dette technique

Toute nouvelle surface (serveur Web, point d'accès, action Home Assistant
autorisée, secret) et toute dette introduite volontairement ajoute une ligne
avant fusion.

## Risques

| ID | Risque | Impact | Mesure | État |
|---|---|---|---|---|
| R1 | Tactile CST820 non reconnu par le composant `cst816` (compatibilité annoncée sans garantie) | Panneau inutilisable au doigt | Essai sur banc avant tout écran (TODO P1) | Fermé le 28 octobre 2026 : puce reconnue, coordonnées conformes (D009) |
| R2 | Mémoire saturée sans PSRAM (tampon LVGL, polices, images, nombre d'écrans) | Échec LVGL, redémarrages | Invariant G6, `buffer_size` explicite, mesure à chaque écran | Ouvert |
| R3 | Secrets exposés dans le dépôt | Compromission du réseau domestique ou du panneau | Invariant G9, `secrets.yaml` ignoré | Ouvert |
| R4 | Commande envoyée sur un état inconnu ou sans Home Assistant | Action inattendue dans la maison | Invariants P2 à P4 | Ouvert |
| R5 | Écart de version entre l'ESPHome du dépôt et Home Assistant | Incompatibilité de l'API ou de l'OTA | Version figée (D005), mise à jour par décision et test ; au 27 octobre 2026, ESPHome 2026.10.1 pour Home Assistant 2026.9.4 | Ouvert |
| R6 | Brochage de `packages/hardware.yaml` repris des valeurs publiées pour la carte, sans documentation vendeur | Écran noir ou tactile muet au premier flash, sans dommage | Essai sur banc (TODO P1) ; corriger les substitutions de `hardware.yaml` seulement | Réduit le 28 octobre 2026 : tout confirmé sauf l'interruption du tactile (GPIO21), contournée par D009 ; LED (GPIO4, 16, 17) et LDR (GPIO34) confirmées le 31 octobre 2026. Le tableau de broches trouvé sur Internet (rétroéclairage GPIO21, tactile SPI) ne vaut pas pour cette carte |
| R7 | Alimentation insuffisante au pic de démarrage du Wi-Fi (sous-tension, *brownout*) | Boucle de redémarrages, mode sans échec, retour silencieux au binaire précédent après une OTA | Bloc secteur externe (1 A validé) ; SHA relu après chaque OTA (`05_BUILD_AND_TEST.md`) | Ouvert le 28 octobre 2026 : constaté sur le port USB du PC ; alimentation du montage mural à définir |
| R8 | Clé d'API et d'OTA commune à tous les modules (D012) | La clé d'un module donne accès à tous (lecture, affichage, OTA) | Choix du propriétaire ; option ouverte : clé par module, fournie à l'exécution | Ouvert le 28 octobre 2026 |
| R9 | Valeurs affichées poussées par un blueprint (D012) : un blueprint absent ou en erreur laisse l'écran vide ou périmé | Affichage incomplet, jamais une valeur fausse non signalée | Garde-fous « indisponible », « périmée », effacement à la déconnexion | Ouvert le 28 octobre 2026 |
| R10 | Binaire public (D039) : compte GitHub ou Releases compromis | Un firmware malveillant proposé à tous les modules publics, installé au premier clic sur « Installer » | Double authentification sur le compte GitHub ; publication par étiquette seulement ; installation jamais automatique (choix à confirmer) | Ouvert le 4 novembre 2026 (maquette) |

## Surfaces exposées

| Surface | Protocole | Authentification | Document |
|---|---|---|---|
| API native ESPHome | TCP local | Clé de chiffrement (`secrets.yaml`) | `04_DEVELOPMENT_RULES.md` |
| Mise à jour OTA | Réseau local, chiffré (Noise) | Clé de chiffrement de l'API (`secrets.yaml`, D010) | `04_DEVELOPMENT_RULES.md` |
| Fenêtre d'installation du binaire public : point d'accès Wi-Fi, portail captif, Improv par USB, API sans clé | Wi-Fi, HTTP, série, API native | Aucune, 15 min après chaque démarrage tant que le module n'a ni Wi-Fi ni clé | D039 : le premier qui se connecte choisit le Wi-Fi ou la clé ; une fois provisionné, plus rien n'est ouvert |
| Mise à jour du binaire public depuis GitHub | HTTPS (certificats vérifiés) | Lancée depuis HA (clé de l'API) ; binaire vérifié par MD5 contre le manifeste | D039 : pas d'OTA depuis un PC sur le binaire public (ESPHome l'accepterait sans clé) ; voir R10 |
| Actions Home Assistant autorisées pour le panneau | API native | Autorisation dans l'intégration ESPHome | Inutile : le 2 novembre 2026, option désactivée, une commande du chauffage et un scénario ont été exécutés (HA émet les événements `esphome.*` sans elle). Activée sur le module de banc à la date du test |
| Portée de l'autorisation des actions HA | API native | Clé de chiffrement de l'API | Option activée : un firmware modifié pourrait appeler d'autres actions que les événements du panneau. Désactivée : il ne peut qu'émettre des événements. La liste de scénarios (D024) ne limite que le chemin normal |
| Action ESPHome `maj_valeur(cle, valeur)` | API native | Clé de chiffrement de l'API | D012 : n'importe quel client muni de la clé peut changer ce qu'affiche le panneau |
| Entités de configuration « LED », « Intensité LED », « Alerte LED » et clés `led_*` | API native | Clé de chiffrement de l'API ; utilisateurs et automatisations de HA | D027 : peuvent éteindre la LED ou son alerte, rien d'autre ; l'écran montre toujours l'état réel (P2) |
| Entité « Intensité écran », clé `ecran_intensite`, valeur `libre` des clés de réglage, page Réglages | API native ; écran du module | Clé de chiffrement de l'API ; utilisateurs et automatisations de HA ; toute personne devant le module (sans protection, D031) | D031 : peuvent baisser la luminosité, jamais sous le plancher `retro_plancher` (écran lisible) ; `libre` ne fait que dégriser un réglage à l'écran |
| Action ESPHome `message_accueil(texte, infos)` et entité « Message d'accueil » | API native | Clé de chiffrement de l'API ; utilisateurs et automatisations de HA | D028 : un client muni de la clé peut afficher un texte (240 octets au plus) pendant 3 min, sans commande ; le toucher le ferme, la déconnexion de HA aussi (P2) |
| Listes de tâches du message d'accueil | Home Assistant | Utilisateurs de HA | D028, D042 : leur contenu s'affiche sur les modules qui les utilisent ; l'automatisation de chaque module peut cocher un message unique |
| Événement `esphome.hapanel_commande` (commande du chauffage et scénarios choisis dans le blueprint, D024) | API native, puis blueprint | Clé de chiffrement de l'API ; le blueprint n'accepte que l'événement de son panneau, thermostat disponible et non verrouillé, consigne dans les bornes ; consigne et préréglage chauffage allumé seulement (D015) | D014 : le panneau ne peut qu'allumer, couper, régler la consigne ou le préréglage du thermostat choisi dans le blueprint |

## Dette technique

| ID | Dette | Raison | Échéance |
|---|---|---|---|
| T1 | Tactile lu toutes les 50 ms au lieu de l'interruption (D009) | Aucune interruption reçue sur GPIO21 | À reprendre seulement si la veille profonde devient nécessaire |
