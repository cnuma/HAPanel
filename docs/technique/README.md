# Documentation technique du YAML

Ce dossier s'adresse à la personne qui **maintient** HAPanel : corriger un défaut,
ajouter une valeur, changer un écran. Il décrit chaque fichier YAML bloc par bloc.

| Document | Pour |
|---|---|
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Vue d'ensemble : comment les morceaux s'emboîtent |
| **Ce dossier** | Détail de chaque fichier : chaque bloc, chaque `id`, chaque lambda |
| [CONFIGURATION.md](../CONFIGURATION.md) | Installer et régler dans Home Assistant |
| [codex/](../codex/) | Règles, décisions (`Dxxx`), invariants (`Gx`, `Px`) |

## Pages

| Page | Fichier documenté | État |
|---|---|---|
| [hapanel.md](hapanel.md) | `hapanel.yaml`, `hapanel_banc.yaml` | Rédigée |
| base.md | `packages/base.yaml` | À venir |
| hardware.md | `packages/hardware.yaml` | À venir |
| lvgl.md | `packages/lvgl.yaml` | À venir |
| liaison_ha.md | `packages/liaison_ha.yaml` | À venir |
| led_veille.md | `packages/led_veille.yaml` | À venir |
| message_accueil.md | `packages/message_accueil.yaml` | À venir |
| pages/accueil.md, meteo.md, planning.md, scenarios.md, menu.md | `packages/pages/` | À venir |
| Blueprints | `blueprints/automation/hapanel/` | À venir |
| [INDEX_IDS.md](INDEX_IDS.md) | Tous les `id`, générés | Généré |

**Ordre de lecture conseillé :** cette page, `hapanel.md`, `base.md`, `hardware.md`,
`lvgl.md`, `liaison_ha.md`, puis `pages/scenarios.md`, la page la plus simple ;
`pages/accueil.md` en dernier.

## Lire le YAML d'ESPHome

ESPHome transforme le YAML en programme C++ pour l'ESP32. Les notions utilisées dans le
projet :

| Notion | Exemple | Ce que cela fait |
|---|---|---|
| Substitution | `${version}` | Remplacée par sa valeur avant tout le reste. Déclarée sous `substitutions:` ; celles de `hapanel.yaml` priment sur celles des packages. |
| Package | `base: !include packages/base.yaml` | Fichier fusionné dans la configuration. Les listes (`script:`, `sensor:`…) s'additionnent d'un fichier à l'autre. |
| `!secret` | `!secret wifi_password` | Valeur lue dans `secrets.yaml`, hors de Git (G9). |
| `!extend` | `id: !extend tactile` | Complète un composant déclaré dans un autre fichier, sans modifier ce fichier. |
| `id` | `id: liaison_chauffage_consigne` | Nom interne d'un composant. **Global à tous les fichiers**, sans espace de noms : deux fichiers ne peuvent pas déclarer le même. |
| `name` | `name: "Version"` | Nom de l'entité dans Home Assistant. Absent : rien n'est exposé. Stable (G10). |
| `globals` | `type: float`, `initial_value` | Variable en mémoire, lue et écrite par les lambdas avec `id(nom)`. `restore_value: true` la garde en flash (G3). |
| `script` | `script.execute: accueil_rafraichir` | Suite d'actions nommée, appelée depuis plusieurs endroits. `mode` fixe ce qui se passe si elle est relancée pendant son exécution. |
| `interval` | `interval: 2s` | Exécute ses actions à intervalle fixe. |
| Déclencheur | `on_boot`, `on_click`, `on_turn_off` | Actions lancées par un événement. |
| Action | `lvgl.label.update`, `globals.set` | Une étape d'une suite d'actions (`then:`). `if` / `condition` / `else` pour les choix. |
| Lambda | `lambda: \|-` | Code C++ inséré tel quel. `id(x)` accède à un composant, `return` donne la valeur d'une condition. Aucune attente (G1). |
| Widget LVGL | `label`, `button`, `obj` | Élément graphique : position (`align`, `x`, `y`), taille, style, `hidden`. Les `pages` sont les écrans, `top_layer` est dessiné par-dessus toutes les pages. |
| Action API | `api: actions:` | Fonction que Home Assistant peut appeler sur le module, par exemple `maj_valeur`. |

Pour voir la configuration une fois tous les fichiers fusionnés :
`.\tools\build.ps1 config` (voir [05_BUILD_AND_TEST.md](../codex/05_BUILD_AND_TEST.md)).

## Conventions du projet

**Préfixes des `id`.** Le préfixe dit à qui appartient l'élément :

| Préfixe | Élément | Exemple |
|---|---|---|
| `page_` | Écran LVGL | `page_accueil` |
| `lbl_` | Texte (label) | `lbl_apropos_version` |
| `btn_` | Bouton | `btn_nav_menu` |
| `obj_` | Conteneur ou forme | `obj_nav` |
| `ico_` | Icône (label en police d'icônes) | `ico_sce_1` |
| `police_` | Police | `police_icones` |
| `liaison_` | Valeur reçue de Home Assistant et son état | `liaison_chauffage_consigne` |
| `accueil_`, `meteo_`, `planning_`, `scenarios_` | Variable ou script d'un écran | `accueil_rafraichir` |
| `led_`, `retro_`, `veille_`, `ldr_` | LED, rétroéclairage, veille, capteur de lumière | |
| `message_` | Message d'accueil | `message_fermer` |
| `banc_` | Outil du panneau de banc seulement | `banc_memoire_libre` |

**Autres conventions :**
- **Langue :** noms et commentaires en français, sans accent dans les `id` et les
  commentaires YAML ; avec accents dans les textes affichés.
- **Journaux :** tag `hapanel.<domaine>`, par exemple `hapanel.message`.
- **Références :** une règle du projet est citée par son code, par exemple « (G3) »
  ou « (D028) », expliqué dans [codex/](../codex/).

## Plan de chaque page

1. **Rôle** du fichier, et ce qui cesse de fonctionner sans lui.
2. **Dépendances :** ce qu'il utilise des autres fichiers, et ce qu'il leur fournit.
3. **Bloc par bloc :** pour chaque bloc YAML, un tableau des éléments (`id`, type,
   valeur, rôle, qui le lit ou l'écrit) ; les lambdas importantes sont expliquées
   étape par étape.
4. **Maintenance :** où intervenir pour un changement courant, pièges connus, tests à
   refaire.

Les éléments sont désignés par leur `id`, stable, et non par un numéro de ligne, qui
change à chaque modification. Le code n'est recopié que par courts extraits.

## Garder la documentation à jour

Toute modification du YAML met à jour sa page dans le même commit (G12). Le script
de contrôle le vérifie :

```powershell
.\.venv\Scripts\python tools\verifier_doc_technique.py             # index + rapport
.\.venv\Scripts\python tools\verifier_doc_technique.py --verifier  # code 1 si écart
```

- **Index :** il réécrit [INDEX_IDS.md](INDEX_IDS.md), la liste de tous les `id` avec
  leur type, leur fichier et les fichiers qui les utilisent.
- **Contrôle :** pour chaque fichier YAML qui a une page, chaque `id` et chaque
  substitution doit y apparaître entre accents graves (`` `nom` ``). Un fichier sans
  page n'est pas contrôlé.
- **`--verifier` :** échoue aussi si l'index n'a pas été régénéré. À lancer avant chaque
  commit qui touche le YAML.
