# 00 — Contexte du projet

Créé le 27 octobre 2026. Les rubriques « À définir » bloquent toute
implémentation qui en dépend : elles se tranchent avec le propriétaire puis
s'inscrivent ici et dans `02_DECISIONS.md`.

## Produit

HAThermostat est un thermostat sur ESP32-S3 intégré à Home Assistant.

**Principe directeur (proposé) :** la régulation et les sécurités fonctionnent
sans Wi-Fi, sans Home Assistant et sans Internet ; Home Assistant supervise et
règle, il n'est pas indispensable à la régulation.

## Périmètre fonctionnel

| Rubrique | État |
|---|---|
| Grandeurs mesurées (température, humidité…) et capteurs | À définir |
| Organe commandé (chaudière, radiateur, clim, pompe à chaleur…) et type de sortie (relais, contact sec, IR, bus) | À définir |
| Modes (chauffage, froid, hors-gel, absence, programmation locale) | À définir |
| Interface locale (écran, boutons, aucune) | À définir |

## Intégration Home Assistant

| Rubrique | État |
|---|---|
| Mode d'intégration : MQTT avec auto-découverte, API native ESPHome, ou autre | À définir |
| Entités exposées (`climate`, capteurs, diagnostic) | À définir |

## Matériel de référence

| Rubrique | État |
|---|---|
| Carte ESP32-S3 (référence exacte, flash, PSRAM) | À définir |
| Capteurs et étage de sortie (référence, broches) | À définir |
| Alimentation | À définir |

## Environnement de développement

PlatformIO, framework Arduino, comme le socle d'origine (décision D002,
statut « proposé » tant que le mode d'intégration n'est pas tranché).

## Hors périmètre

À définir.
