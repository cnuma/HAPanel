# 00 — Contexte du projet

Mis à jour le 28 octobre 2026. Les rubriques « À définir » bloquent toute
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
| Accueil | Température du séjour, état et consigne du chauffage (entités choisies dans le blueprint, D012) | Allumer / couper le chauffage, consigne ±0,5 °C | En définition (`docs/TODO.md`) ; prototype : clé `temperature` affichée sur « À propos » |
| À propos (version, SHA, connexion, mémoire) | Internes | Aucune | Validé au banc le 28 octobre 2026, y compris connecté / non connecté (`packages/lvgl.yaml`) |

## Home Assistant

| Rubrique | Valeur |
|---|---|
| Installation | HA OS, en natif sur Raspberry Pi |
| Version | Core 2026.9.4, Supervisor 2026.10.4, OS 18.3 (relevé le 27 octobre 2026) |
| Intégration | ESPHome, API native chiffrée (D005) |
| Modules | Plusieurs prévus, un seul binaire : nœud `hapanel-xxxxxx` (D012) |
| Liaison | Valeurs poussées par le blueprint `blueprints/automation/hapanel/envoyer_valeur.yaml` (action `maj_valeur`, clé `temperature`) ; demande de renvoi par l'événement `esphome.hapanel_demande_valeurs` (D012) |

## Matériel de référence

| Rubrique | Valeur |
|---|---|
| Carte | ESP32-2432S024C (D004) : ESP32 classique (module WROOM, double cœur), sans PSRAM |
| Écran | 2,4", 240 × 320, contrôleur ILI9341 (confirmé au banc le 28 octobre 2026) |
| Tactile | Capacitif CST820, bus I²C (adresse `0x15`), composant ESPHome `cst816`, lecture périodique 50 ms (D009) ; coordonnées conformes à l'écran sans calibrage |
| Flash | 4 Mo (détectée au premier flash) ; ESP32 rev 3.1 |
| Alimentation | Bloc secteur externe 1 A validé au banc ; port USB du PC insuffisant (R7) |
| Montage mural | À définir |

## Environnement de développement

ESPHome en ligne de commande, version figée dans `requirements.txt`, YAML
dans le dépôt (D005). Nœud `hapanel`, framework `esp-idf` (D008).

## Hors périmètre

- pilotage direct d'un appareil par le panneau (relais, sortie) : D007 ;
- édition des YAML dans l'outil ESPHome de Home Assistant.
