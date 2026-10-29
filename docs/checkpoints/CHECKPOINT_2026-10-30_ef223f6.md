# Checkpoint du 30 octobre 2026 — `ef223f6`

Cinquième checkpoint de HAPanel : écran d'accueil et blueprint dédié
(D014), commandes du chauffage par événement, validés au banc en usage
nominal. Tests de dégradation restants. Remplace
`CHECKPOINT_2026-10-29_96227cf.md`.

## Identité

| Rubrique | Valeur |
|---|---|
| Dépôt | `cnuma/HAPanel` (public, `main` protégée : ni suppression ni push forcé) |
| Branche | `main` (fusion en avance rapide de `feature/p2-ecran-accueil`) |
| Configuration validée | commit `ef223f6` ; les commits suivants n'ajoutent que de la documentation |
| Binaire sur le panneau | `hapanel_banc.yaml`, `0.1.0 (ef223f6)`, OTA chiffrée, « Boot seems successful » |
| Version | `0.1.0` (fichier `VERSION`, inchangé : 0.2.0 après les tests de dégradation) |
| ESPHome | 2026.10.1 (`requirements.txt`), ESP-IDF 5.5.6, LVGL 9.5.0, framework `esp-idf` |
| Home Assistant | HA OS, Core 2026.9.4, sur 192.168.1.155 |
| Carte | ESP32-2432S024C, ESP32 rev 3.1, flash 4 Mo, sans PSRAM |
| Alimentation | bloc secteur externe 1 A (le port USB du PC provoque des brownouts, R7) |
| Module de banc | nœud `hapanel-a85bfc`, renommé « HAPanelSejourCheminee » dans HA (nom affiché seulement), IP 192.168.1.197 (DHCP, à redemander) ; OTA uniquement |

## Écran d'accueil (D014)

```
┌────────────────────────────┐
│ ven. 30 oct.  00:05  ▂▄▆ ● │  heure HA, barres Wi-Fi, point HA
│ Séjour          (périmée)  │  état en orange si anormal
│         22,3 °C            │
│ (Chauffage : périmé)       │  seulement si non reçu / périmé / indisponible
│ [●] [❄] [🍃] [🛋] [🚀]      │  Manuel, Hors-gel, Éco, Confort, Boost
│ [ − ]     20,5 °C    [ + ] │  bleu / rouge, pas 0,5 °C, bornes 15–25 °C
│ ( Éteint ▐██Chauffage██▌ ) │  glissière, pastille orange = mode réel
│    [ ⌂ ]          [ i ]    │  navigation commune (top_layer)
└────────────────────────────┘
```

- Page de démarrage : l'accueil (package inclus avant `lvgl.yaml`, l'ordre
  des packages fixe l'ordre des pages).
- Glissière : glisser le doigt d'un tiers de sa largeur, n'importe où
  dessus, envoie l'autre mode ; un simple toucher ne fait rien. Pas de
  pastille si le mode est inconnu, grise si verrouillé, orange atténué en
  attente.
- Préréglages : appui simple, préréglage réel entouré d'orange, grisés si
  le chauffage est éteint (choix du propriétaire).
- Consigne : envoyée 2 s après le dernier appui, orange jusqu'à
  confirmation, retour à la valeur réelle après 10 s.
- Commandes : événement `esphome.hapanel_commande` (`chauffage_mode`,
  `chauffage_consigne`, `chauffage_prereglage`) ; le blueprint
  `blueprints/automation/hapanel/ecran_accueil.yaml` refait les contrôles
  (panneau émetteur, thermostat disponible et non verrouillé, bornes,
  préréglage connu, chauffage allumé pour un préréglage).
- Clés reçues : `temperature`, `chauffage_mode`, `chauffage_action` (reçue,
  plus affichée), `chauffage_consigne`, `chauffage_prereglage`,
  `chauffage_verrou`, `consigne_min`, `consigne_max`.
- Côté HA : automatisation « écran d'accueil » (panneau, thermomètre
  `sensor.sejour_cheminee_radiateur_ema_temperature`, thermostat
  `climate.entree_thermostat`, bornes 15 / 25,5 dans l'automatisation ;
  le thermostat ramène le maximum à 25,0).

## Fichiers modifiés depuis le checkpoint `96227cf`

| Fichier | Changement |
|---|---|
| `hapanel.yaml` | package `accueil`, inclus avant `lvgl` |
| `packages/pages/accueil.yaml` | nouveau : page, rafraîchissement unique (`accueil_rafraichir`), consigne, glissière, préréglages, heure, Wi-Fi |
| `packages/liaison_ha.yaml` | huit clés, péremption par groupe (température, chauffage), effacement à la déconnexion ; ligne de prototype retirée |
| `packages/lvgl.yaml` | police d'icônes Material Design (6 glyphes), barre de navigation en icônes, ligne de prototype retirée |
| `blueprints/automation/hapanel/ecran_accueil.yaml` | nouveau blueprint |
| `docs/codex/00_CONTEXT.md`, `02_DECISIONS.md` (D014), `04_DEVELOPMENT_RULES.md`, `08_RISKS_AND_DEBT.md`, `docs/TODO.md` | accueil, commandes, surface `esphome.hapanel_commande` |

Volontairement non modifiés : `hapanel_banc.yaml`, `packages/base.yaml`,
`packages/hardware.yaml`, `tools/build.ps1`, `VERSION`,
`blueprints/automation/hapanel/envoyer_valeur.yaml`.

## Validé sur le panneau

| Point | Résultat |
|---|---|
| OTA chiffrée de `f282b26` à `ef223f6`, SHA relu après « Boot seems successful » | ✅ |
| Huit clés reçues du blueprint | ✅ journaux |
| Consigne − / + : envoi groupé 2 s après le dernier appui, confirmée par HA (≈ 100 ms) | ✅ journaux et propriétaire |
| Glissière Éteint ↔ Chauffage, retour rapide après confirmation | ✅ propriétaire (`c2fc035`) |
| Redémarrage du panneau, blueprint désactivé : « non reçu » jusqu'à la réactivation | ✅ propriétaire |

## Non vérifié

- Préréglages (blueprint réimporté par le propriétaire, essai non
  consigné).
- « indisponible » (thermomètre désactivé dans HA).
- « périmée » : test interrompu par le redémarrage ; refaire en
  désactivant l'automatisation 15 min sans redémarrer.
- Indicateur rouge avec `esphome logs` ouvert (D013), HA déconnecté.
- Centrage des icônes et du « − » / « + », lisibilité des accents à
  l'écran.
- Configuration de production (`hapanel.yaml`) compilée, jamais flashée.

## Mémoire de référence (G6)

| Mesure | 96227cf | ef223f6 |
|---|---|---|
| Mémoire libre (capteur `debug`) | 197 100 o | 188 888 o (−8 Ko) |
| Plus grand bloc libre | 110 592 o | 110 592 o |
| RAM statique (banc) | 46,4 Ko | 49 896 o (27,6 %) |
| Flash (banc) | 58,0 % | 1 093 915 o (59,6 %) |
| Production (`hapanel.yaml`, compilée le 30 octobre 2026) | — | RAM 49 752 o (27,5 %), flash 1 082 035 o (59,0 %) |

## Décisions et risques

- Décision ajoutée : D014 (écran d'accueil, commandes par événement,
  glissière, préréglages, ligne d'anomalie).
- Ouverts : R2, R4 (réduit par le double contrôle panneau / blueprint),
  R5, R7, R8, R9 ; dette T1.
- Surface ajoutée : événement `esphome.hapanel_commande` (`08`).
- Invariants : P2 (point HA, effacement à la déconnexion), P3 (« non
  reçu », « périmé », « indisponible »), P4 (commandes grisées hors état
  connu), G6 (mesure ci-dessus), G10 (aucun identifiant existant renommé ;
  `lbl_proto_temperature` supprimé avec le prototype).

## Ménage restant

- HA : réimporter `ecran_accueil.yaml` depuis `main` ; confirmer la
  désactivation de l'automatisation `temperature` (`envoyer_valeur`).
- Branches fusionnées à supprimer : `docs/test-p2-alimentation`,
  `feature/p1-banc-minimal`, `feature/p1-options-esp32`,
  `feature/p2-proto-liaison-ha`, `feature/p2-ecran-accueil`.
- `secrets.yaml` : ligne `ota_password` devenue inutile ; `AGENTS.md` et
  G9 citent encore le « mot de passe OTA ».
- Blueprint : un changement d'attribut du thermostat renvoie les huit
  clés ; Versatile Thermostat en enchaîne plusieurs (bavard, sans effet).

## Pièges connus

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash.
- Alterner production et banc recompile tout (≈ 10 min).
- Ligne `NativeCommandError` sous PowerShell 5.1 : sans effet.
- Après chaque OTA, relire le SHA après 60 s (« Boot seems successful ») ;
  les journaux ouverts après le démarrage ne montrent pas les valeurs
  reçues dans les premières secondes.
- Blueprint : un modèle Jinja qui produit une liste échoue si elle
  contient un attribut énuméré (`hvac_action`) ; écrire la liste en YAML.
- Réimport d'un blueprint : le cache de GitHub peut servir l'ancienne
  version quelques minutes ; « Réimporter » lit `source_url` (`main`).
- LVGL : le curseur natif saute à l'endroit touché (d'où la glissière sur
  mesure) ; `text:` d'un bouton n'est pas centré, utiliser un `label`
  enfant `align: CENTER`.

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

Puis demander au propriétaire l'IP courante du module avant tout `upload`,
`run` ou `logs` (`-Device <IP_PANNEAU>`), et reprendre les tests restants
de `docs/TODO.md` (P2).
