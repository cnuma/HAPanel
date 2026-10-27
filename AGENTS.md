# AGENTS.md — HAThermostat

## Mission

Ce dépôt contient le firmware du thermostat HAThermostat sur ESP32 (carte
ESP32-2432S024, sans PSRAM), intégré à Home Assistant.

Toute intervention automatisée ou assistée (Claude Code, Codex) doit préserver
en priorité :

1. la sécurité de commande de l'organe de chauffage ou de climatisation
   (état sûr au démarrage, en cas de perte de mesure et en cas de perte
   réseau) ;
2. la persistance de la configuration ;
3. le fonctionnement autonome du thermostat sans Wi-Fi, sans Home Assistant
   et sans Internet ;
4. les invariants documentés dans `docs/codex/03_INVARIANTS.md`.

Le périmètre fonctionnel, le matériel et le mode d'intégration Home Assistant
sont fixés dans `docs/codex/00_CONTEXT.md`. Tant qu'une rubrique y est
marquée « À définir », aucune implémentation ne s'appuie sur une hypothèse
à sa place : poser la question au propriétaire.

## Source de vérité

- Dépôt : `cnuma/HAthermostat`
- Branche stable : `main`
- Point d'entrée de reprise : `docs/START_HERE.md`, puis le checkpoint le plus
  récent de `docs/checkpoints/`
- Origine du socle : AquaLook, voir `SOCLE_MANIFEST.md`

Ne jamais reconstruire un fichier depuis un ancien extrait, un souvenir, une
conversation ou une version locale non vérifiée si le dépôt contient une
version plus récente. Une décision n'est acquise que lorsqu'elle est inscrite
dans le dépôt (document, décision, invariant, test, checkpoint ou code).

## Lecture obligatoire avant modification

1. `AGENTS.md`
2. `docs/codex/00_CONTEXT.md`
3. `docs/codex/03_INVARIANTS.md`
4. `docs/codex/04_DEVELOPMENT_RULES.md`
5. `docs/codex/05_BUILD_AND_TEST.md`
6. le ou les fichiers réellement concernés

Pour une évolution significative, lire aussi `docs/codex/02_DECISIONS.md`,
`docs/codex/06_ANTI_REGRESSION.md` et `docs/codex/10_TASK_HANDOFF.md`.

### Checklist automatique au début de chaque chat HAThermostat

L'utilisateur ne doit pas avoir à demander cette passe. Avant toute analyse,
proposition, commande Git, compilation, téléversement ou test matériel :

1. commencer la numérotation conversationnelle à `HAT-R001` ;
2. identifier le dépôt, la branche ou le checkpoint de reprise demandé ;
3. lire la version courante de `AGENTS.md` depuis Git ;
4. exécuter l'ordre de lecture obligatoire ;
5. vérifier le dernier checkpoint applicable ;
6. relire `platformio.ini` avant de proposer une commande de build, d'upload,
   de buildfs ou de monitoring, et confirmer le nom exact des environnements ;
7. demander le port COM courant avant toute commande qui en dépend ;
8. regrouper les commandes Git, compilation, téléversement et monitoring dans
   un seul bloc continu, dans l'ordre exact d'exécution ;
9. signaler toute divergence entre branche de travail, `main`, checkpoint et
   règles documentaires ;
10. ne commencer aucune modification tant que cette passe n'est pas terminée.

## Règles impératives

### Numérotation des réponses de l'agent

- Toute réponse principale commence par `HAT-RNNN` (`HAT-R001`, `HAT-R002`…),
  remis à `HAT-R001` à chaque nouveau chat ; les messages intermédiaires
  d'une même réponse prennent un suffixe (`HAT-R004.1`).
- Au-delà d'environ `HAT-R030`, signaler que le chat devient profond et
  proposer un checkpoint autonome avant de poursuivre.
- Cette numérotation ne remplace ni les versions, ni les commits, ni les
  identifiants d'issues.

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
- Ne pas modifier un nom d'API, une route, une entité ou un topic Home
  Assistant, ni une structure persistée sans décision documentée.
- Ne pas supprimer un comportement existant sous prétexte de simplification.

### Vérification fonctionnelle obligatoire (tout développement ESP)

- Une modification n'est validée ni par sa présence dans le dépôt ni par la
  réussite de la compilation.
- Vérifier toute la chaîne : inclusion, instanciation, appel, déclencheur,
  conditions d'entrée, rafraîchissement et effet observable.
- Toute nouvelle fonction, classe, tâche, route ou callback est reliée à un
  point d'entrée réellement exécuté (`setup()`, `loop()`, tâche FreeRTOS,
  événement, route, callback matériel).
- Vérifier qu'aucun cache, rendu ou rechargement de configuration ne masque
  le résultat, et vérifier tous les modes concernés.
- Si la vérification matérielle n'a pas été faite, le dire explicitement.

### Port série

Avant la première compilation, le premier téléversement ou l'ouverture du
moniteur d'une session, demander le port COM. Ne jamais reprendre celui de
`platformio.ini` ou d'une ancienne session. Tant qu'il n'est pas confirmé,
utiliser `<PORT_COM>` et proposer `pio device list`.

La carte ESP32-2432S024 passe par un convertisseur USB-série : la règle
`--dtr 1` du socle d'origine (USB natif de l'ESP32-S3) ne s'applique pas.
Fermer le moniteur avant un téléversement (il tient le port).

### Versionnement, identité de build et espace « À propos »

- Version fonctionnelle `MAJEUR.MINEUR.CORRECTIF` (suffixe `-dev`, `-beta`,
  `-rc`), dans le fichier unique `VERSION`.
- Identité de build automatique (numéro de build, SHA court, branche,
  environnement, date) injectée par `tools/version_build.py`, exposée par
  `include/BuildInfo.h` : aucune version écrite en dur ailleurs.
- Un binaire compilé avec des sources non commitées porte le suffixe `+modif`
  sur son SHA.
- Le produit expose un espace « À propos » (série au boot, diagnostic, page
  ou entité Home Assistant) affichant nom, version et identifiant de build.
- Proposer une évolution de version à chaque palier, release ou correction
  publiée.

### Identité et progression de démarrage

- La sortie série de démarrage identifie produit, version, cible matérielle,
  environnement PlatformIO, numéro de build, SHA et branche, depuis
  `BuildInfo`.
- Chaque étape significative du boot produit un état : en cours, réussi,
  dégradé ou échec ; un mode dégradé est nommé, jamais présenté comme nominal.
- La fin du boot produit un bilan : version, cible, durée de démarrage, état
  réseau ou IP, mémoire libre utile.
- Aucun délai long ou non borné n'est ajouté au boot ; aucune attente ne
  retarde la mise en état sûr de la sortie de commande.

### Cybersécurité

- Le dépôt peut devenir public : la sécurité ne repose jamais sur le secret du
  code ; aucun secret dans Git, un journal ou un chat (`secrets.h` ignoré).
- Toute nouvelle surface (route, port, service, secret, intégration) est
  inscrite dans `docs/codex/08_RISKS_AND_DEBT.md` avant fusion.

### Validation obligatoire des fichiers livrés

- Tout patch, script, archive ou fichier de configuration destiné à
  l'utilisateur est testé avant livraison avec l'outil exact prévu.
- Patch Git : `git apply --check`, application réelle dans une copie, puis
  `git diff --check`.
- Ne jamais utiliser l'utilisateur comme premier testeur d'un artefact que
  l'agent pouvait vérifier. Si la validation est impossible, le dire avant
  livraison et fournir la commande de contrôle locale.

## Déclencheur permanent : checkpoint

Lorsque l'utilisateur écrit exactement « checkpoint » :

1. identifier branche, commit et état Git ;
2. vérifier que le code validé compile et que le dépôt est propre ;
3. créer `docs/checkpoints/CHECKPOINT_YYYY-MM-DD_<sha-court>.md`, autonome :
   dépôt, branche, commit, version, fonctionnalités validées, fichiers et
   fonctions modifiés, invariants préservés, état compilation et matériel,
   risques et limites, procédure exacte de reprise, commandes Git ;
4. ajouter, committer et pousser ce document, puis vérifier qu'il est bien
   sur le dépôt distant avant de l'annoncer ;
5. fournir un bloc minimal de reprise prêt à copier dans un nouveau chat.

## Procédure obligatoire avant livraison

1. Identifier la branche et le commit de base.
2. Lister les fichiers et fonctions concernés.
3. Énoncer les invariants à préserver.
4. Faire la modification minimale.
5. Vérifier que les changements sont réellement appelés.
6. Demander et confirmer le port COM avant toute commande qui en dépend.
7. `git -c core.whitespace=cr-at-eol diff --check`.
8. Compiler l'environnement de production ; si essai matériel, téléverser
   l'environnement de banc (voir `05_BUILD_AND_TEST.md`).
9. Ouvrir le moniteur et effectuer le test matériel du nouveau chemin.
10. Relire le diff final : duplication, hors périmètre, hausse de taille.
11. Documenter : fichiers modifiés et volontairement non modifiés,
    compilation, profil et port flashés, tests réalisés et restant à faire,
    risques.

## Livrables

Quand plus de deux fichiers sont modifiés, fournir directement les fichiers
complets ou un package, avec l'emplacement exact de chacun dans le dépôt.

## Git

- `main` est stable ; toute évolution passe par `feature/…`, `fix/…`,
  `docs/…` ou `chore/…`.
- Commits petits, explicites, testables ; pas de code non compilé poussé.
- Ne pas fusionner vers `main` avant validation firmware.
- Ne jamais réécrire une branche publiée sans accord explicite du
  propriétaire ; si accordé, `git push --force-with-lease=<branche>:<sha>`.

## Style de travail

- Expliquer hypothèses et limites ; préserver les décisions validées.
- Ne jamais masquer une régression sous une simplification.
- Documenter toute dette technique introduite volontairement.
- Mettre à jour la documentation dans le même lot que le code.
