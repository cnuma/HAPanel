# Checkpoints

Un checkpoint est un document de reprise, nommé
`CHECKPOINT_YYYY-MM-DD_<sha-court>.md`, créé selon le déclencheur « checkpoint » de
`AGENTS.md`.

Créer un checkpoint après : fusion d'une fonctionnalité majeure, évolution de
la persistance, modification matérielle, correction critique, mise à jour
significative du socle de règles, ou avant de changer de chat.

## Règles de rédaction (G14)

- **Court et variable seulement :** le checkpoint ne contient que ce qui change d'un
  jour à l'autre. Toute information réutilisable est d'abord écrite dans son fichier
  de référence, puis citée :

  | Information | Fichier de référence |
  |---|---|
  | Reste à faire et ordre des développements | `docs/TODO.md` (colonnes « Ordre » et « N° ») |
  | Tests restants, fusions bloquées | `docs/CAHIER_DE_TESTS.md` |
  | Pièges | `docs/codex/09_PIEGES.md` |
  | Procédure de reprise, ordre de lecture | `docs/START_HERE.md` |
  | Matériel, Home Assistant, écrans | `docs/codex/00_CONTEXT.md` |
  | Compilation, banc, alimentation | `docs/codex/05_BUILD_AND_TEST.md` |
  | Décisions, invariants, risques | `02_DECISIONS.md`, `03_INVARIANTS.md`, `08_RISKS_AND_DEBT.md` |

- **Jamais :** adresse IP, port COM, mot de passe, clé, nom de réseau Wi-Fi (G9). Le
  checkpoint écrit « à redemander au propriétaire ».
- **Le reste à faire** n'est pas recopié : le checkpoint cite les trois premiers sujets du TODO, par leur numéro (`T…`), et
  les tests qui bloquent la prochaine fusion.

## Modèle

```markdown
# Checkpoint du <date> — `<sha>`

<Une phrase : ce qui a changé depuis le checkpoint précédent, qu'il remplace.>

## État

| Rubrique | Valeur |
|---|---|
| Branche | `<branche>`, `<sha>`, poussée et vérifiée sur le dépôt distant |
| Version | `<VERSION>` |
| Binaire sur le module de banc | `<sha du binaire>` (banc ou production) |

## Depuis le checkpoint précédent

| Commit | Contenu |
|---|---|

## Mesures

| Mesure | Valeur |
|---|---|
| Compilation production / banc | code, RAM, flash |
| Mémoire libre, plus grand bloc (G6) | |
| `verifier_doc_technique.py --verifier`, `git diff --check` | |

## Suite

- Prochaine étape : T<nn> de `docs/TODO.md` : <sujet>.
- Tests qui bloquent la prochaine fusion : <codes> (`docs/CAHIER_DE_TESTS.md`).
- Nouveaux pièges : ajoutés à `docs/codex/09_PIEGES.md` (ou « aucun »).

Reprise : `docs/START_HERE.md`, branche `<branche>`.
```
