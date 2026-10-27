# 07 — Git et branches

## Branches

- `main` : stable et compilable ; aucun développement exploratoire direct.
- Branches de travail : `feature/sujet`, `fix/sujet`, `docs/sujet`,
  `chore/sujet`.

## Cycle

```powershell
git checkout main
git pull origin main
git checkout -b feature/sujet
# ... modification, compilation, test ...
git -c core.whitespace=cr-at-eol diff --check
git status
git add <fichiers>
git commit -m "Message impératif précis"
git push -u origin feature/sujet
```

Fusion vers `main` après validation sur le panneau, puis suppression de la branche.
Si `git checkout -b` répond que la branche existe déjà, s'arrêter et le
signaler : ne pas poursuivre la séquence sur `main`.

## Commits

Un commit correspond à une intention, compile si un YAML est modifié, ne
contient aucun fichier temporaire et porte un message impératif précis.

## Interdictions

- ne pas versionner `.esphome/`, `.venv/`, builds, sauvegardes, `*.bak`,
  logs, archives intermédiaires, `secrets.yaml` ;
- ne pas réécrire une branche publiée sans accord explicite du propriétaire ;
- vérifier un patch dans une copie détachée
  (`git worktree add --detach <dossier> <base>`), jamais sur une branche
  existante.
