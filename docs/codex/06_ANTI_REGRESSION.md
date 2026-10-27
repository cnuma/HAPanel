# 06 — Protocole anti-régression

## Principe

La dernière version de `main` ou le dernier checkpoint explicitement validé
est la seule base autorisée.

## Avant modification

Documenter branche, commit, checkpoint, fichiers et fonctions concernés,
invariants, comportement actuel et comportement attendu.

## Pendant la modification

- petites étapes, aucun changement opportuniste ;
- pas de reformatage global, pas de duplication ;
- sauvegardes hors du dépôt ;
- contrôle fréquent du diff.

## Contrôle source

- pas de second propriétaire d'une ressource (bus, broche, NVS) ;
- pas de blocage long dans `loop()` ni dans une tâche de régulation ;
- pas de secret compilé en dur ;
- pas de changement de broche non documenté ;
- pas de renommage d'entité, de topic ou de route.

## Après modification

```powershell
git -c core.whitespace=cr-at-eol diff --check
pio run -e HAThermostat_s3
```

## Revue du diff

1. Chaque ligne modifiée est-elle nécessaire ?
2. Une route, une entité ou un topic a-t-il changé ?
3. Une structure persistée a-t-elle changé ?
4. L'empreinte mémoire a-t-elle augmenté ?
5. Le comportement de la sortie de commande est-il affecté ?
6. Un test matériel est-il requis ?
7. La documentation doit-elle être mise à jour ?

## Conditions d'arrêt

Revenir à la base si : patch corrompu, transformation ambiguë, ancre non
trouvée, occurrences inattendues, compilation cassée hors périmètre,
différence de taille inexpliquée, fichier entier remplacé sans justification.

## Livraison

Le bilan indique base utilisée, fichiers modifiés et non modifiés,
compilation, tests réalisés et restants, risques résiduels, commit et
checkpoint.
