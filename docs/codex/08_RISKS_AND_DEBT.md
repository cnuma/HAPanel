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
| R6 | Brochage de `packages/hardware.yaml` repris des valeurs publiées pour la carte, sans documentation vendeur | Écran noir ou tactile muet au premier flash, sans dommage | Essai sur banc (TODO P1) ; corriger les substitutions de `hardware.yaml` seulement | Réduit le 28 octobre 2026 : tout confirmé sauf l'interruption du tactile (GPIO21), contournée par D009 |
| R7 | Alimentation insuffisante au pic de démarrage du Wi-Fi (sous-tension, *brownout*) | Boucle de redémarrages, mode sans échec, retour silencieux au binaire précédent après une OTA | Bloc secteur externe (1 A validé) ; SHA relu après chaque OTA (`05_BUILD_AND_TEST.md`) | Ouvert le 28 octobre 2026 : constaté sur le port USB du PC ; alimentation du montage mural à définir |

## Surfaces exposées

| Surface | Protocole | Authentification | Document |
|---|---|---|---|
| API native ESPHome | TCP local | Clé de chiffrement (`secrets.yaml`) | `04_DEVELOPMENT_RULES.md` |
| Mise à jour OTA | Réseau local, chiffré (Noise) | Clé de chiffrement de l'API (`secrets.yaml`, D010) | `04_DEVELOPMENT_RULES.md` |
| Actions Home Assistant autorisées pour le panneau | API native | Autorisation dans l'intégration ESPHome | À activer au premier écran qui commande |

## Dette technique

| ID | Dette | Raison | Échéance |
|---|---|---|---|
| T1 | Tactile lu toutes les 50 ms au lieu de l'interruption (D009) | Aucune interruption reçue sur GPIO21 | À reprendre seulement si la veille profonde devient nécessaire |
