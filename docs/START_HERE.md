# HAThermostat — START HERE

Point d'entrée officiel de la documentation.

## Ordre de lecture

1. `AGENTS.md` — règles impératives et checklist de démarrage ;
2. le checkpoint le plus récent de `docs/checkpoints/` — état du jour ;
3. `docs/TODO.md` — reste à faire, par priorité ;
4. `docs/codex/00_CONTEXT.md` — périmètre, matériel, intégration ;
5. `docs/codex/03_INVARIANTS.md`, `04_DEVELOPMENT_RULES.md`,
   `05_BUILD_AND_TEST.md` ;
6. `docs/codex/02_DECISIONS.md`, `06_ANTI_REGRESSION.md`,
   `08_RISKS_AND_DEBT.md`, `10_TASK_HANDOFF.md` pour une évolution
   significative.

## Source de vérité

Le dépôt `cnuma/HAthermostat` est la mémoire officielle du projet. En cas de
contradiction, l'ordre de confiance est :

1. code et configuration du commit ciblé ;
2. checkpoint exact ;
3. invariants et décisions ;
4. documentation `docs/codex/` ;
5. TODO et notes ;
6. conversations.

Une contradiction détectée se corrige dans le dépôt, pas oralement.

## Principes documentaires

- faire évoluer le document de référence existant plutôt que créer un doublon ;
- conserver l'historique et la justification des décisions ;
- ne jamais présenter une hypothèse ou une fonction prévue comme un
  comportement implémenté ;
- mettre à jour la documentation dans le même lot que le code.
