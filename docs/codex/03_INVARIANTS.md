# 03 — Invariants

Un invariant ne se modifie que sur demande explicite du propriétaire, avec une
décision dans `02_DECISIONS.md`, des tests et un checkpoint.

## Invariants génériques (hérités du socle AquaLook)

| ID | Règle | Origine |
|---|---|---|
| G1 | **Non-blocage :** `loop()` et les tâches de régulation n'attendent jamais indéfiniment Serial, Wi-Fi, NTP, HTTP ou MQTT ; toute attente a un timeout ; les temporisations utilisent `millis()` en gérant son débordement. | F1, DEV-005 |
| G2 | **Propriétaire unique :** chaque ressource matérielle (bus, broche, sortie) et persistante (espace NVS, système de fichiers) a un seul module propriétaire. | I1, DEV-005 |
| G3 | **Persistance contrôlée :** la configuration persistée est validée par magic, version de schéma, taille et CRC ; toute évolution de format a une migration ou un repli, et l'ancienne donnée n'est effacée qu'après vérification de la nouvelle. | F8, F9 |
| G4 | **Réponse avant redémarrage :** une opération suivie d'un redémarrage répond au client avant de redémarrer. | I10 |
| G5 | **Source unique de version :** version et identité de build viennent de `VERSION` et `tools/version_build.py` via `BuildInfo`, sur toutes les interfaces. | F12 à F14 |
| G6 | **Marge mémoire :** toute tâche, buffer, cache, document JSON ou `String` volumineux ajouté réévalue le pic mémoire du chemin complet ; une fonction stable est retestée après toute hausse d'empreinte RAM globale. | F15 |
| G7 | **Artefacts vérifiés :** tout patch, script, archive ou fichier de configuration livré est validé avec l'outil exact prévu. | F16 |
| G8 | **Noms de fichiers :** un fichier modifié ou livré conserve exactement son nom d'origine, sans suffixe ni renommage non demandé. | F11 |
| G9 | **Aucun secret dans le dépôt :** identifiants Wi-Fi, mots de passe MQTT et clés viennent de la configuration NVS ou d'un `secrets.h` ignoré par Git. | I9 |

## Invariants propres à HAThermostat

| ID | Règle | État |
|---|---|---|
| T1 | La sortie de commande est dans un état sûr (arrêt) au démarrage, tant que l'initialisation n'est pas terminée. | Proposé |
| T2 | Une mesure absente, invalide ou figée met la sortie dans un état sûr défini et produit un défaut visible localement et dans Home Assistant. | Proposé |
| T3 | La régulation continue sans Wi-Fi ni Home Assistant, sur la dernière consigne valide persistée. | Proposé |
| T4 | Une durée maximale de fonctionnement continu et un anti-court-cycle (durées minimales marche et arrêt) protègent l'organe commandé. | Proposé |

Les invariants T1 à T4 passent à « Accepté » après validation du périmètre
(`00_CONTEXT.md`).
