# HAPanel — START HERE

Point d'entrée officiel de la documentation.

## Ordre de lecture

1. `AGENTS.md` — règles impératives et checklist de démarrage ;
2. le checkpoint le plus récent de `docs/checkpoints/` — état du jour, court ;
3. `docs/TODO.md` — reste à faire, **par ordre de priorité** ;
4. `docs/CAHIER_DE_TESTS.md` — tests restants et ce qui bloque chaque fusion ;
5. `docs/codex/09_PIEGES.md` — pièges connus ;
6. `docs/codex/00_CONTEXT.md` — écrans, matériel, Home Assistant ;
7. `docs/codex/03_INVARIANTS.md`, `04_DEVELOPMENT_RULES.md`,
   `05_BUILD_AND_TEST.md` ;
8. `docs/codex/02_DECISIONS.md`, `06_ANTI_REGRESSION.md`,
   `08_RISKS_AND_DEBT.md`, `10_TASK_HANDOFF.md` pour une évolution
   significative.

## Reprise d'un chat

Le checkpoint donne la branche ; le reste ne change pas d'un chat à l'autre (G14).

```powershell
cd C:\Users\Emman\00_DevClaude\HAPanel
git fetch origin
git checkout <branche du checkpoint>
git pull origin <branche du checkpoint>
git status
.\.venv\Scripts\Activate.ps1
esphome version
.\.venv\Scripts\python tools\verifier_doc_technique.py --verifier
```

Puis demander au propriétaire l'adresse IP courante du module, ou le port COM,
avant tout `upload`, `run` ou `logs` : elle n'est jamais écrite dans le dépôt (G9).

## Source de vérité

Le dépôt `cnuma/HAPanel` est la mémoire officielle du projet. En cas de
contradiction, l'ordre de confiance est :

1. configuration YAML du commit ciblé ;
2. checkpoint exact ;
3. invariants et décisions ;
4. documentation `docs/codex/` ;
5. TODO, cahier de tests et notes ;
6. conversations.

Une contradiction détectée se corrige dans le dépôt, pas oralement.

## Principes documentaires

- faire évoluer le document de référence existant plutôt que créer un doublon ;
- conserver l'historique et la justification des décisions ;
- ne jamais présenter une hypothèse ou une fonction prévue comme un
  comportement implémenté ;
- mettre à jour la documentation dans le même lot que la configuration ;
- une information utile d'un chat à l'autre s'écrit d'abord dans son fichier de
  référence ; le checkpoint y renvoie (G14).
