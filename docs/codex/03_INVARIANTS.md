# 03 — Invariants

Un invariant ne se modifie que sur demande explicite du propriétaire, avec une
décision dans `02_DECISIONS.md`, des tests et un checkpoint.

## Invariants de méthode et de plateforme (socle AquaLook, transposés à ESPHome)

| ID | Règle | Origine |
|---|---|---|
| G1 | **Non-blocage :** aucune lambda n'attend (`delay`, boucle d'attente) ni ne fait de traitement long ; les temporisations passent par les mécanismes ESPHome (`interval`, `delay` d'automatisation, `script`). | F1, DEV-005 |
| G2 | **Propriétaire unique :** une broche ou un bus est déclaré une seule fois ; `allow_other_uses` est interdit sans décision documentée. | I1, DEV-005 |
| G3 | **Persistance sobre :** seules les valeurs qui doivent survivre au redémarrage utilisent `restore_value` ; aucune écriture fréquente en flash. | F8 |
| G5 | **Source unique de version :** version et SHA viennent de `VERSION` et de Git, injectés par substitution ; jamais écrits à la main dans un YAML. | F12 à F14 |
| G6 | **Marge mémoire :** chaque écran, widget lourd, image ou police ajouté réévalue la mémoire ; la mémoire libre et le plus grand bloc libre sont mesurés à chaque palier et consignés au checkpoint. | F15 |
| G7 | **Artefacts vérifiés :** tout YAML, patch ou script livré est validé avec l'outil exact prévu (`esphome config`, `esphome compile`, `git apply --check`). | F16 |
| G8 | **Noms de fichiers :** un fichier modifié ou livré conserve exactement son nom d'origine, sans suffixe ni renommage non demandé. | F11 |
| G9 | **Aucun secret dans le dépôt :** Wi-Fi et clé de l'API (qui protège aussi l'OTA, D010) dans `secrets.yaml`, ignoré par Git. | I9 |
| G10 | **Identifiants stables :** le nom du nœud ESPHome, les `id` et les `name` des entités exposées à Home Assistant sont des contrats ; un renommage exige une décision et la mise à jour des tableaux de bord et automatisations concernés. | F5, F6 |

## Invariants propres au panneau

| ID | Règle | État |
|---|---|---|
| P1 | Le panneau ne commande aucun appareil directement : toute commande est une action de Home Assistant (D007). | Accepté |
| P2 | L'état de connexion à Home Assistant est toujours visible ; sans connexion, aucune commande n'est envoyée ni mise en attente silencieusement, et l'utilisateur le voit. | Accepté |
| P3 | Une valeur inconnue, indisponible ou non reçue depuis le démarrage est affichée comme telle, jamais comme 0, vide trompeur ou dernière valeur non signalée. | Accepté |
| P4 | Aucune commande n'est calculée à partir d'un état inconnu (par exemple une bascule sur un état non reçu). | Accepté |
| P5 | La navigation entre écrans fonctionne sans Home Assistant et sans Wi-Fi. | Accepté |
