# 00 — Contexte du projet

Mis à jour le 27 octobre 2026. Les rubriques « À définir » bloquent toute
implémentation qui en dépend : elles se tranchent avec le propriétaire puis
s'inscrivent ici et dans `02_DECISIONS.md`.

## Produit

HAPanel est un panneau de commande mural multi-écrans pour Home Assistant.
Il affiche l'état de la maison et envoie des commandes ; toute la logique et
tous les appareils restent dans Home Assistant (D007).

**Principe directeur :** le panneau ne ment jamais. Un état inconnu,
indisponible ou périmé est affiché comme tel, et aucune commande n'est
envoyée sur un tel état.

## Écrans

Définis pas à pas ; chaque écran validé est ajouté ici avec les entités
Home Assistant qu'il lit et les actions qu'il déclenche.

| Écran | Entités lues | Actions | État |
|---|---|---|---|
| Accueil | À définir | À définir | À définir |
| À propos (version, SHA, connexion, mémoire) | Internes | Aucune | Prévu (`docs/TODO.md`) |

## Home Assistant

| Rubrique | Valeur |
|---|---|
| Installation | HA OS, en natif sur Raspberry Pi |
| Version | À relever (Paramètres > À propos) |
| Intégration | ESPHome, API native chiffrée (D005) |

## Matériel de référence

| Rubrique | Valeur |
|---|---|
| Carte | ESP32-2432S024C (D004) : ESP32 classique (module WROOM, double cœur), sans PSRAM |
| Écran | 2,4", 240 × 320, contrôleur ILI9341 ou ST7789 selon la série — à confirmer au premier essai |
| Tactile | Capacitif CST820, bus I²C, composant ESPHome `cst816` (annoncé « devrait fonctionner ») |
| Flash | À confirmer (4 Mo attendus) |
| Alimentation et montage mural | À définir |

## Environnement de développement

ESPHome en ligne de commande, version figée dans `requirements.txt`, YAML
dans le dépôt (D005).

## Hors périmètre

- pilotage direct d'un appareil par le panneau (relais, sortie) : D007 ;
- édition des YAML dans l'outil ESPHome de Home Assistant.
