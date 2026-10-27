# 06 — Protocole anti-régression

## Principe

La dernière version de `main` ou le dernier checkpoint explicitement validé
est la seule base autorisée.

## Avant modification

Documenter branche, commit, checkpoint, fichiers et composants concernés,
invariants, comportement actuel et comportement attendu.

## Pendant la modification

- petites étapes, aucun changement opportuniste ;
- pas de reformatage global, pas de duplication entre packages ;
- sauvegardes hors du dépôt ;
- contrôle fréquent du diff.

## Contrôle de la configuration

- pas de broche ou de bus déclaré deux fois (G2) ;
- pas d'attente ni de traitement long dans une lambda (G1) ;
- pas de secret en clair (G9) ;
- pas de renommage de nœud, d'`id` ou d'entité exposée (G10) ;
- pas de valeur utilisée sans contrôle `has_state()` ou `isnan()` (P3, P4).

## Après modification

```powershell
git -c core.whitespace=cr-at-eol diff --check
esphome config hapanel.yaml
esphome compile hapanel.yaml
```

## Revue du diff

1. Chaque ligne modifiée est-elle nécessaire ?
2. Un `id`, une entité exposée ou le nom du nœud a-t-il changé ?
3. Une valeur persistée (`restore_value`) a-t-elle changé de type ou de rôle ?
4. La mémoire libre a-t-elle baissé, et de combien ?
5. Une commande vers Home Assistant peut-elle partir sur un état inconnu ?
6. Les cas « Home Assistant déconnecté » et « entité indisponible » sont-ils
   retestés ?
7. La documentation (`00_CONTEXT.md`, registre des risques) doit-elle être
   mise à jour ?

## Conditions d'arrêt

Revenir à la base si : patch corrompu, transformation ambiguë, ancre non
trouvée, occurrences inattendues, compilation cassée hors périmètre, LVGL en
échec d'allocation, baisse de mémoire inexpliquée, fichier entier remplacé
sans justification.

## Livraison

Le bilan indique base utilisée, fichiers modifiés et non modifiés, version
ESPHome, compilation, tests réalisés et restants, mémoire libre, risques
résiduels, commit et checkpoint.
