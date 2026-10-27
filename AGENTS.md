# AGENTS.md — HAPanel

## Mission

Ce dépôt contient la configuration ESPHome de HAPanel, panneau de commande
mural multi-écrans pour Home Assistant, sur carte ESP32-2432S024C (ESP32 sans
PSRAM, écran tactile capacitif 2,4").

Le panneau affiche et commande des entités de Home Assistant ; il ne pilote
jamais directement un appareil (décision D007). Toute intervention
automatisée ou assistée (Claude Code, Codex) doit préserver en priorité :

1. l'absence de toute commande envoyée sur un état inconnu ou périmé ;
2. un état de connexion à Home Assistant toujours visible et véridique ;
3. la réactivité de l'écran, y compris sans Home Assistant ;
4. la stabilité des identifiants et des entités exposées à Home Assistant ;
5. les invariants documentés dans `docs/codex/03_INVARIANTS.md`.

Les écrans sont définis pas à pas dans `docs/codex/00_CONTEXT.md` et
`docs/TODO.md`. Aucun écran n'est implémenté sur une hypothèse : poser la
question au propriétaire.

## Source de vérité

- Dépôt : `cnuma/HAPanel`
- Branche stable : `main`
- Point d'entrée de reprise : `docs/START_HERE.md`, puis le checkpoint le plus
  récent de `docs/checkpoints/`
- Origine du socle de méthode : AquaLook, voir `SOCLE_MANIFEST.md`

Les fichiers YAML vivent dans le dépôt et se compilent avec la ligne de
commande ESPHome à version figée (D005). Ils ne sont jamais édités dans
l'outil ESPHome de Home Assistant, qui les ferait vivre hors de Git.

Ne jamais reconstruire un fichier depuis un ancien extrait, un souvenir, une
conversation ou une version locale non vérifiée si le dépôt contient une
version plus récente. Une décision n'est acquise que lorsqu'elle est inscrite
dans le dépôt.

## Lecture obligatoire avant modification

1. `AGENTS.md`
2. `docs/codex/00_CONTEXT.md`
3. `docs/codex/03_INVARIANTS.md`
4. `docs/codex/04_DEVELOPMENT_RULES.md`
5. `docs/codex/05_BUILD_AND_TEST.md`
6. le ou les fichiers réellement concernés

Pour une évolution significative, lire aussi `docs/codex/02_DECISIONS.md`,
`docs/codex/06_ANTI_REGRESSION.md` et `docs/codex/10_TASK_HANDOFF.md`.

### Checklist automatique au début de chaque chat HAPanel

L'utilisateur ne doit pas avoir à demander cette passe. Avant toute analyse,
proposition, commande Git, compilation, téléversement ou test matériel :

1. commencer la numérotation conversationnelle à `HAP-R001` ;
2. identifier le dépôt, la branche ou le checkpoint de reprise demandé ;
3. lire la version courante de `AGENTS.md` depuis Git ;
4. exécuter l'ordre de lecture obligatoire ;
5. vérifier le dernier checkpoint applicable ;
6. relire les YAML concernés et `requirements.txt` (version ESPHome) avant
   de proposer une commande ;
7. demander le port COM ou l'adresse IP courante avant toute commande qui en
   dépend ;
8. regrouper les commandes Git, validation, compilation, téléversement et
   journaux dans un seul bloc continu, dans l'ordre exact d'exécution ;
9. signaler toute divergence entre branche de travail, `main`, checkpoint et
   règles documentaires ;
10. ne commencer aucune modification tant que cette passe n'est pas terminée.

## Règles impératives

### Numérotation des réponses de l'agent

- Toute réponse principale commence par `HAP-RNNN` (`HAP-R001`, `HAP-R002`…),
  remis à `HAP-R001` à chaque nouveau chat ; les messages intermédiaires
  d'une même réponse prennent un suffixe (`HAP-R004.1`).
- Au-delà d'environ `HAP-R030`, signaler que le chat devient profond et
  proposer un checkpoint autonome avant de poursuivre.

### Choix soumis au propriétaire : impacts d'abord

Avant de demander une décision (choix entre options, action irréversible ou
visible de l'extérieur, écart à une règle du dépôt) :

- expliquer en mots simples ce qui est proposé, sans jargon non défini ;
- pour chaque option : l'action exacte, ce qu'elle change et ne change pas,
  ce que le propriétaire aura à faire ensuite, le risque et ce qui est
  irréversible ;
- donner une recommandation argumentée et dire quelles informations
  pourraient la changer ;
- ne jamais lancer l'action avant l'accord explicite donné après cette
  explication.

### Périmètre minimal

- Modifier le minimum nécessaire ; ne pas réécrire un fichier complet pour
  une modification locale ; pas de reformatage global.
- Ne jamais renommer un `id`, un `name` d'entité exposée ou le nom du nœud
  ESPHome sans décision documentée : Home Assistant lie ses tableaux de bord
  et automatisations à ces noms.
- Ne pas supprimer un comportement existant sous prétexte de simplification.

### Vérification fonctionnelle obligatoire

- Une modification n'est validée ni par sa présence dans le dépôt, ni par
  `esphome config`, ni par `esphome compile`.
- Vérifier toute la chaîne : package inclus, composant déclaré, entité Home
  Assistant importée, déclencheur (`on_value`, `on_click`…), action, effet
  observable à l'écran et dans Home Assistant.
- Vérifier les cas : Home Assistant connecté, déconnecté, entité
  indisponible, redémarrage du panneau et redémarrage de Home Assistant.
- Si la vérification sur le panneau n'a pas été faite, le dire explicitement.

### Port série et adresse

Avant le premier téléversement ou l'ouverture des journaux d'une session,
demander le port COM (USB) ou l'adresse IP (OTA). Ne jamais reprendre ceux
d'une ancienne session. Tant qu'ils ne sont pas confirmés, utiliser
`<PORT_COM>` ou `<IP_PANNEAU>`.

### Versionnement et identité de build

- Version fonctionnelle `MAJEUR.MINEUR.CORRECTIF` (suffixe `-dev`, `-beta`,
  `-rc`), dans le fichier unique `VERSION`.
- La version et le SHA Git sont injectés à la compilation par substitution
  (`-s version …`, `-s git_sha …`), jamais écrits à la main dans un YAML ; un
  SHA suffixé `+modif` signale des fichiers non commités.
- Le panneau expose son identité : bloc `project:` d'ESPHome, entité de
  diagnostic dans Home Assistant et page « À propos » sur l'écran (nom,
  version, SHA).
- Proposer une évolution de version à chaque palier ou correction publiée.

### Cybersécurité

- Le dépôt peut devenir public : aucun secret dans Git, un journal ou un
  chat. Mots de passe Wi-Fi, clé de chiffrement de l'API et mot de passe OTA
  vivent dans `secrets.yaml`, ignoré par Git ; `secrets.example.yaml` en
  donne la forme sans valeur réelle.
- API Home Assistant toujours chiffrée ; OTA toujours protégée.
- Toute nouvelle surface (serveur Web, point d'accès de secours, action Home
  Assistant autorisée) est inscrite dans `docs/codex/08_RISKS_AND_DEBT.md`
  avant fusion.

### Validation obligatoire des fichiers livrés

- Tout YAML livré passe `esphome config` puis `esphome compile` avec la
  version figée avant livraison ; tout patch passe `git apply --check`,
  une application réelle dans une copie, puis `git diff --check` ; tout
  script passe au minimum un contrôle syntaxique.
- Ne jamais utiliser l'utilisateur comme premier testeur d'un artefact que
  l'agent pouvait vérifier. Si la validation est impossible, le dire avant
  livraison et fournir la commande de contrôle locale.

## Déclencheur permanent : checkpoint

Lorsque l'utilisateur écrit exactement « checkpoint » :

1. identifier branche, commit et état Git ;
2. vérifier que la configuration validée compile et que le dépôt est propre ;
3. créer `docs/checkpoints/CHECKPOINT_YYYY-MM-DD_<sha-court>.md`, autonome :
   dépôt, branche, commit, version, version ESPHome, écrans et fonctions
   validés, fichiers modifiés, invariants préservés, état compilation et
   panneau, mémoire libre mesurée, risques et limites, procédure exacte de
   reprise, commandes Git ;
4. ajouter, committer et pousser ce document, puis vérifier qu'il est bien
   sur le dépôt distant avant de l'annoncer ;
5. fournir un bloc minimal de reprise prêt à copier dans un nouveau chat.

## Procédure obligatoire avant livraison

1. Identifier la branche et le commit de base.
2. Lister les fichiers YAML et composants concernés.
3. Énoncer les invariants à préserver.
4. Faire la modification minimale.
5. `esphome config`, puis `esphome compile` avec la version figée.
6. Demander le port COM ou l'IP avant tout téléversement.
7. Téléverser sur le panneau de banc, lire les journaux, tester les cas de
   la vérification fonctionnelle et relever la mémoire libre.
8. `git -c core.whitespace=cr-at-eol diff --check` et relecture du diff :
   duplication, hors périmètre, identifiant renommé.
9. Documenter : fichiers modifiés et volontairement non modifiés,
   compilation, mode de téléversement, tests réalisés et restant à faire,
   mémoire libre, risques.

## Livrables

Quand plus de deux fichiers sont modifiés, fournir directement les fichiers
complets ou un package, avec l'emplacement exact de chacun dans le dépôt.

## Git

- `main` est stable ; toute évolution passe par `feature/…`, `fix/…`,
  `docs/…` ou `chore/…`.
- Si `git checkout -b` répond qu'une branche existe déjà, s'arrêter et
  signaler : ne jamais poursuivre la séquence sur `main`.
- Commits petits, explicites, testables ; pas de configuration qui ne
  compile pas poussée.
- Ne jamais réécrire une branche publiée sans accord explicite du
  propriétaire ; si accordé, `git push --force-with-lease=<branche>:<sha>`.

## Style de travail

- Expliquer hypothèses et limites ; préserver les décisions validées.
- Ne jamais masquer une régression sous une simplification.
- Documenter toute dette technique introduite volontairement.
- Mettre à jour la documentation dans le même lot que la configuration.
