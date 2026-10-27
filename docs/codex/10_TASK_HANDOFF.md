# 10 — Transmission de tâches à un agent

La référence est toujours `main` et le checkpoint le plus récent de
`docs/checkpoints/`. Un résumé de chat ne remplace jamais les fichiers du
dépôt.

## Format de mission

```text
Titre :
Branche de base :
Commit de base :
Checkpoint applicable :
Documents obligatoires lus :
Objectif :
Hors périmètre :
Fichiers pressentis :
Invariants :
Critères d'acceptation :
Commandes de test :
Tests matériels :
Livrables :
```

## Réponse attendue avant code

1. compréhension de l'objectif ;
2. base, branche, commit et checkpoint ;
3. confirmation des fichiers de gouvernance lus ;
4. fichiers concernés ;
5. risques et invariants ;
6. plan de modification et plan de test ;
7. confirmation que le port COM sera redemandé avant upload.

## Réponse attendue après code

```text
Base utilisée :
Fichiers modifiés :
Positions et fonctions modifiées :
Fichiers non modifiés :
Diff hors périmètre :
Compilation HAThermostat :
Tests matériels :
Port COM confirmé :
Résultat observé :
Risques résiduels :
Commit proposé :
Checkpoint proposé :
```

## Définition de terminé

Les critères sont couverts, les tests requis sont exécutés ou explicitement
laissés à faire, le diff est limité, la documentation est à jour, le dépôt
est propre et un checkpoint est créé si l'état de reprise change.
