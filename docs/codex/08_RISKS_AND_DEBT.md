# 08 — Risques, surfaces exposées et dette technique

Toute nouvelle surface (route, port, service, secret, intégration) et toute
dette introduite volontairement ajoute une ligne avant fusion.

## Risques

| ID | Risque | Impact | Mesure | État |
|---|---|---|---|---|
| R1 | Sortie de commande active au démarrage ou après plantage | Chauffage ou froid non maîtrisé | Invariant T1, test au boot et au reset | Ouvert |
| R2 | Mesure de température fausse ou figée | Surchauffe ou non-chauffe | Invariant T2, détection de capteur absent ou figé | Ouvert |
| R3 | Secrets (Wi-Fi, MQTT) exposés dans le dépôt | Compromission du réseau domestique | Invariant G9, `secrets.h` ignoré | Ouvert |

## Surfaces exposées

| Surface | Protocole | Authentification | Document |
|---|---|---|---|
| — | — | — | — |

## Dette technique

| ID | Dette | Raison | Échéance |
|---|---|---|---|
| — | — | — | — |
