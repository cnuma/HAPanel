# Checkpoint du 2 novembre 2026 — `55bb15b`

Onzième checkpoint de HAPanel : version `0.6.0-dev` avec météo, planning,
scénarios, menu, retour à l'accueil, lumière de la pièce, blueprint unique et
documentation complète. Remplace `CHECKPOINT_2026-10-31_97b1f34.md`.

## Identité

| Rubrique | Valeur |
|---|---|
| Dépôt | `cnuma/HAPanel` (public, `main` protégée : ni suppression ni push forcé) |
| Branche | `main`, seule branche locale restante ; `55bb15b` est aussi sur `origin/main` |
| Configuration | Code du module et blueprint inchangés depuis `dc83077` ; `083327c` et `55bb15b` ne touchent que la documentation et ses outils |
| Binaire sur le panneau | `0.6.0-dev (dc83077)`, sans `+modif`, OTA, « Boot seems successful » ; volontairement non reflashé : la page À propos affiche donc `dc83077` |
| Version | `0.6.0-dev` (fichier `VERSION`) |
| ESPHome | 2026.10.1 (`requirements.txt`), framework `esp-idf`, LVGL 9 |
| Home Assistant | HA OS sur <IP_HA> ; Core 2026.9.4 au dernier relevé (31 octobre 2026), à reconfirmer |
| Carte | ESP32-2432S024C, ESP32 rev 3.1, flash 4 Mo, sans PSRAM |
| Alimentation | Bloc secteur externe 1 A, OTA uniquement (R7) |
| Module de banc | Nœud `hapanel-a85bfc`, IP <IP_PANNEAU> au dernier relevé (DHCP, à redemander) |

## Changements depuis `97b1f34`

| Fichier | Changement |
|---|---|
| `packages/pages/meteo.yaml` (nouveau) | Conditions et prévisions sur 3 jours (D019) |
| `packages/pages/planning.yaml` (nouveau) | Résumé et frises de 1 à 4 calendriers (D020) |
| `packages/pages/scenarios.yaml` (nouveau) | 6 boutons, nom, icône, couleur (D024, D026) |
| `packages/pages/menu.yaml` (nouveau) | Tuiles de navigation (D025) |
| `packages/lvgl.yaml` | Barre Accueil + Menu, polices |
| `packages/led_veille.yaml` | Respiration de la LED (D018), retour à l'accueil (D022), rétroéclairage selon la LDR (D023) |
| `packages/liaison_ha.yaml` | Préfixes `meteo_`, `plan_`, `scen_` |
| `blueprints/automation/hapanel/module.yaml` (nouveau) | Blueprint unique par module (D021), remplace `ecran_accueil.yaml` |
| `docs/UTILISATION.md`, `docs/CONFIGURATION.md`, `docs/ARCHITECTURE.md` (nouveaux) | Documentation, 11 maquettes et 21 schémas générés |
| `tools/generer_images_doc.py`, `tools/generer_schemas_architecture.py` (nouveaux) | Génération des images |
| `docs/codex/00`, `02`, `08`, `docs/TODO.md`, `README.md` | D018 à D026, statuts, liens |

Dernier lot (`55bb15b`) : parties « Organisation du YAML » et « Le blueprint » de
`ARCHITECTURE.md`, schémas 15 à 21, deux points de sécurité ajoutés au TODO. Aucun
identifiant renommé (G10).

## Validé

| Point | Binaire | Résultat |
|---|---|---|
| Compilation de production (`hapanel.yaml`) | `55bb15b` | ✅ 2 novembre 2026, code 0, jamais flashée telle quelle |
| OTA, version relue, « Boot seems successful » | `dc83077` | ✅ journaux |
| Météo, planning, blueprint unique | Antérieur | ✅ propriétaire, « tout marche », 1er novembre 2026 |
| Scénarios, menu, retour à l'accueil | Antérieur à `dc83077` | ✅ propriétaire, « Nickel tout marche ! » ; l'agent n'a pas vu l'écran |
| Valeurs `scen_` reçues | `dc83077` | ✅ journaux, envoi périodique |

## Non vérifié / ouvert

Détail dans `docs/TODO.md`.

- **Autorisation des actions HA :** le code de HA (branche `dev`) émet les événements
  `esphome.*` sans vérifier cette option, alors que la documentation la dit nécessaire. À
  tester sur le module avant de corriger `CONFIGURATION.md`, `ARCHITECTURE.md`, `04`
  et `08`.
- **Usurpation de `device_id` :** les données d'un événement peuvent écraser celui de HA.
  Il faut un firmware modifié et la clé d'API. À évaluer, puis à inscrire au `08`.
- **Icônes et couleurs (D026) :** fusionnées à la demande du propriétaire, rendu non
  confirmé une par une.
- **Rétroéclairage (D023) :** pièce sombre, stabilité, influence de l'écran sur la LDR.
- **LED (D018) :** pièce sombre, blanc, Boost et alerte.
- **Retour à l'accueil :** cas sans HA.
- **États dégradés :** scénarios (« Refusé par HA », « Pas de réponse de HA », entité
  indisponible, noms longs), météo et planning (« non reçu », « indisponible »,
  « périmé », minuit, changement d'heure, 3 ou 4 calendriers), « périmée » de l'accueil.
- **`VERSION` :** reste `0.6.0-dev`, à passer en version stable après ces tests.
- **Documentation hors dépôt :** les PDF ne sont pas versionnés. Celui d'utilisation et de
  configuration déjà transmis contient encore l'ancienne phrase sur « les entités
  choisies » ; la version de `main` fait foi.
- **Noms dans `ARCHITECTURE.md` :** le lien entre `friendly_name` et nom d'action vient
  d'un résumé du code de HA ; « Prendre le contrôle » est décrit sans contrôle sur l'instance.

## Mémoire de référence (G6)

| Mesure | Valeur |
|---|---|
| Mémoire libre, `dc83077` sur le module | 162,6 Ko |
| Plus grand bloc libre, `dc83077` sur le module | 106,5 Ko |
| Banc `dc83077` | RAM 54 400 o (30,1 %), flash 1 151 139 o (62,7 %) |
| Production `55bb15b` | RAM 54 224 o (30,0 %), flash 1 138 455 o (62,0 %) |

## Décisions, risques, invariants

- Décisions D018 à D026 inscrites dans `02_DECISIONS.md`.
- Ouverts : R2, R4, R5, R7, R8, R9 ; dette T1. Portée de l'autorisation des actions
  HA inscrite au `08`.
- Invariants préservés : P2 à P5 ; G1, G2, G5, G6, G9, G10.

## Pièges connus

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash.
- `hapanel.yaml` et `hapanel_banc.yaml` partagent `.esphome/build/hapanel` : les alterner
  recompile environ 1 500 fichiers (environ 10 min). **La dernière compilation est celle de
  production** : recompiler le banc avant tout `upload` de banc.
- `build.ps1 upload` ne compile pas : enchaîner `compile` puis `upload`, ou utiliser `run`.
- `build.ps1 logs` affiche le SHA du dépôt local, pas celui du binaire : lire `Project
  cnuma.hapanel version`.
- Après chaque OTA, relire la version après 60 s (« Boot seems successful ») : seul « OTA
  rollback detected » signale un retour arrière.
- Ajouter une icône ou une couleur modifie `module.yaml` et `scenarios.yaml`.
- Un changement de clés demande de réimporter le blueprint et de recompiler le module.
- Une saisie obligatoire ajoutée au blueprint impose de reconfigurer l'automatisation.
- Enregistrer le formulaire n'envoie rien : les noms de scénarios arrivent sous 5 min ou à la
  reconnexion.
- Deux automatisations pour un module exécutent chaque commande deux fois.
- Le propriétaire lit souvent sur mobile : donner les valeurs à copier en blocs de code.

## Procédure de reprise

```powershell
cd C:\Users\Emman\00_DevClaude\HAPanel
git checkout main
git pull origin main
git status
.\.venv\Scripts\Activate.ps1
esphome version
.\tools\build.ps1 config
```

Puis demander l'IP courante du module avant tout `upload`, `run` ou `logs`
(`-Device <IP_PANNEAU>`). Suite proposée : test de l'autorisation des actions HA, tests
restants du TODO, puis passage à une version stable.
