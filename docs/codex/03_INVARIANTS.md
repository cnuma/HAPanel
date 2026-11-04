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
| G11 | **Procédure d'installation versionnée :** tout blueprint, et plus largement tout élément à installer ou à régler dans Home Assistant, est livré avec sa procédure complète dans le dépôt (préparation des appareils, import, mise à jour, création de l'automatisation, premier test, dépannage), écrite ou mise à jour dans le même commit. Une explication donnée dans la conversation y est reportée. Vaut pour tous les dépôts du propriétaire. | Propriétaire, D029 |
| G13 | **Cahier de tests tenu à jour :** toute fonction livrée au test ajoute ses tests au cahier du dépôt (`docs/CAHIER_DE_TESTS.md`), dans le même commit que le code. Chaque test a un code stable : une lettre par fonction ou groupe de fonctions, puis un numéro (`H4`). Le code n'est jamais réattribué ; un test retiré est barré, pas renuméroté, et un test ajouté prend le numéro suivant. Chaque ligne donne l'action, l'attendu et une case OK / KO datée. Un tableau des résultats garde l'historique (date, binaire, tests, constats, suite) ; les retours du propriétaire y sont reportés dès réception, et un test à refaire après correction le dit. Le cahier dit quelle partie bloque quelle fusion. Vaut pour tous les dépôts du propriétaire. | Propriétaire, D032 |
| G12 | **Moment de la mise à jour documentaire :** la documentation de fonctionnement, d'installation et d'utilisation (`CONFIGURATION.md`, `UTILISATION.md`, `ARCHITECTURE.md`, décisions, procédures) est mise à jour dans le même commit que la modification, jamais regroupée plus tard. Le statut du projet (`TODO.md` « validé », `VERSION`, checkpoint) n'est mis à jour qu'après validation par le propriétaire sur le module, à la fusion dans `main` : un commit de branche n'atteste pas un état stable. Vaut pour tous les dépôts du propriétaire. | Propriétaire, D030 |

## Invariants propres au panneau

| ID | Règle | État |
|---|---|---|
| P1 | Le panneau ne commande aucun appareil directement : toute commande est une action de Home Assistant (D007). | Accepté |
| P2 | L'état de connexion à Home Assistant est toujours visible ; sans connexion, aucune commande n'est envoyée ni mise en attente silencieusement, et l'utilisateur le voit. | Accepté |
| P3 | Une valeur inconnue, indisponible ou non reçue depuis le démarrage est affichée comme telle, jamais comme 0, vide trompeur ou dernière valeur non signalée. | Accepté |
| P4 | Aucune commande n'est calculée à partir d'un état inconnu (par exemple une bascule sur un état non reçu). | Accepté |
| P5 | La navigation entre écrans fonctionne sans Home Assistant et sans Wi-Fi. | Accepté |
