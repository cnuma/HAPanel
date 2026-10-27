# 04 — Règles de développement

Règles génériques ESP32 reprises du socle AquaLook (`docs/codex/04_DEVELOPMENT_RULES.md`
et `docs/developer/DEV-005`), sans les règles propres à son matériel.

## C++

- Compatible avec la configuration PlatformIO/Arduino de `platformio.ini`.
- API minimale, types explicites, une responsabilité par module ; éviter les
  dépendances circulaires ; `main.cpp` assemble, il ne porte pas de logique
  métier.
- Pas d'allocation dynamique répétée dans les chemins fréquents ; préférer
  buffers bornés, `strlcpy`, `snprintf`, chaînes toujours terminées.
- Pas de `String` dans les modules temps réel sans justification écrite.
- Aucun appel bloquant sans timeout ; gestion correcte du débordement de
  `millis()`.
- Valider les entrées à la frontière (réseau, MQTT, série, configuration).
- Toute constante matérielle compile-time va dans `include/config.h` ; toute
  valeur modifiable en production va dans le gestionnaire de configuration.
- Différer les écritures persistantes et les redémarrages hors des callbacks
  réseau (AsyncTCP, client MQTT).
- Mesurer le coût de tout traitement ajouté à `loop()`.

## Mémoire, flux et régressions indirectes

- Évaluer le pic transitoire du chemin complet : pile de tâche, buffers
  réseau, `String`, documents JSON, caches, allocations concurrentes.
- Toute tâche FreeRTOS ajoute une pile dédiée : en tenir compte avant de
  rendre asynchrone une fonction synchrone.
- Pour JSON, fichiers et réponses réseau volumineux : parsing en flux,
  filtres de champs, buffers bornés ; pas de double représentation d'une
  même donnée.
- Toute hausse de l'empreinte RAM globale impose de retester les fonctions
  stables qui font des allocations transitoires importantes.
- Avant validation, relever le heap libre au repos, avant et après
  l'opération sensible, et le plus grand bloc libre lors d'ajouts réseau/TLS.
- Les diagnostics distinguent : erreur réseau, réponse vide, erreur de
  format, manque de mémoire, authentification refusée.

## ESP32-S3

- USB natif : `ARDUINO_USB_CDC_ON_BOOT=1` et `monitor_dtr = 1` ; le port COM
  se ré-énumère à chaque redémarrage.
- PSRAM : n'activer `BOARD_HAS_PSRAM` et le type de mémoire (`qio_opi`,
  `opi`) qu'après identification exacte du module ; une mauvaise
  configuration empêche le boot.
- Épingler explicitement les tâches réseau au cœur 0 (pile Wi-Fi/lwIP) et
  laisser la régulation sur le cœur 1, sauf décision documentée.
- Conserver un boot anti-blocage : sortie en état sûr d'abord, réseau ensuite.

## Persistance

Avant de modifier une structure persistée :

1. mesurer sa taille (`sizeof`) ;
2. décider d'un changement de schéma ;
3. définir le comportement face à l'ancien blob ;
4. vérifier le CRC ;
5. tester les valeurs par défaut et le reset ;
6. documenter la migration.

Ne jamais changer silencieusement l'ordre, le type ou la taille d'un champ
persisté.

## Interfaces exposées

- Une route, une entité ou un topic Home Assistant est un contrat versionné :
  pas de renommage sans décision.
- Aucune donnée sensible dans une URL ou un topic.
- Schémas JSON validés à la réception.

## Logs

- Niveaux INFO, WARN, ERROR ; buffer borné ; messages courts et actionnables,
  sans secret.
- Code mnémonique entre crochets en tête de ligne quand le sens n'est pas
  évident hors contexte (ex. `[REG-TIMEOUT]`).
- INFO pour un état normal même inhabituel ; WARN et ERROR réservés à ce qui
  appelle une action.

## Commentaires

Documenter pourquoi une contrainte existe, le risque supprimé et l'invariant
concerné ; pas de commentaire qui répète le code.

## Encodage

- UTF-8 sans BOM pour les sources.
- Vérifier accents et emoji dans les scripts PowerShell ; préférer des
  marqueurs ASCII dans les scripts de transformation.
