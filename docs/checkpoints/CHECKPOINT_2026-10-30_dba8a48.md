# Checkpoint du 30 octobre 2026 — `dba8a48`

Septième checkpoint de HAPanel : version `0.2.1`, correctif de l'état de
la température (« indisponible » invisible), ménage de Home Assistant
terminé, spécification D015 (accueil allégé) acceptée et non implémentée.
Remplace `CHECKPOINT_2026-10-30_847e17c.md`.

## Identité

| Rubrique | Valeur |
|---|---|
| Dépôt | `cnuma/HAPanel` (public, `main` protégée : ni suppression ni push forcé) |
| Branche | `main`, seule branche du dépôt local et distant |
| Configuration validée | commit `dba8a48` (fusion en avance rapide de `fix/accueil-etat-temperature`) ; les commits suivants n'ajoutent que de la documentation |
| Binaire sur le panneau | `hapanel_banc.yaml`, `0.2.1 (dba8a48)`, compilé le 30 octobre 2026 à 22:15, OTA chiffrée, « Boot seems successful », pas de retour arrière |
| Version | `0.2.1` (fichier `VERSION`) |
| ESPHome | 2026.10.1 (`requirements.txt`), ESP-IDF 5.5.6, LVGL 9.5.0, framework `esp-idf` |
| Home Assistant | HA OS, Core 2026.9.4, sur 192.168.1.155 |
| Carte | ESP32-2432S024C, ESP32 rev 3.1, flash 4 Mo, sans PSRAM |
| Alimentation | bloc secteur externe 1 A (le port USB du PC provoque des brownouts, R7) |
| Module de banc | nœud `hapanel-a85bfc`, « HAPanelSejourCheminee » dans HA (nom affiché seulement), IP 192.168.1.197 le 30 octobre 2026 (DHCP, à redemander) ; OTA uniquement |

## Changements depuis `847e17c`

| Commit | Fichier | Changement |
|---|---|---|
| `dba8a48` | `packages/pages/accueil.yaml` | `lbl_acc_temperature_etat` : `width: 120`, `text_align: RIGHT` (le label aligné à droite, créé vide, s'élargissait hors de l'écran) |
| `dba8a48` | `VERSION` | `0.2.0` → `0.2.1` |
| `38b6deb` | `docs/codex/02_DECISIONS.md` | D015 : accueil allégé (chauffage éteint, HA déconnecté) |
| divers | `docs/TODO.md`, `docs/codex/00_CONTEXT.md`, `docs/codex/04_DEVELOPMENT_RULES.md` | résultats des tests, ménage HA, règle LVGL des labels non alignés à gauche |

Volontairement non modifiés : `packages/liaison_ha.yaml`,
`packages/lvgl.yaml`, `packages/base.yaml`, `packages/hardware.yaml`,
`hapanel.yaml`, `hapanel_banc.yaml`, `tools/build.ps1`, blueprints.
Aucun identifiant renommé (G10).

## Validé sur le panneau (30 octobre 2026)

| Point | Binaire | Résultat |
|---|---|---|
| Préréglages (allumé ; grisés chauffage éteint) | `ef223f6` | ✅ propriétaire |
| HA déconnecté, `esphome logs` ouvert (D013) ; renvoi des 8 clés en 2 s à la reconnexion | `ef223f6` | ✅ propriétaire et journaux |
| Centrage des icônes, « − » / « + », accents | `ef223f6` | ✅ propriétaire |
| Glissière Éteint → Chauffage, confirmée par HA en < 130 ms | `0.2.0` | ✅ journaux |
| « indisponible » (thermomètre forcé à `unavailable` dans Outils de développement › États) | `0.2.0` | ❌ texte invisible, `--,- °C` seul |
| « indisponible », même méthode | `0.2.1` | ✅ propriétaire et journaux |
| OTA `0.2.1`, version relue après 60 s | `0.2.1` | ✅ `Project cnuma.hapanel version 0.2.1` |

## Home Assistant

- Blueprint `ecran_accueil.yaml` à jour (`source_url` sur `main` depuis sa
  création) ; utilisé par une automatisation, « HAPanel — écran
  d'accueil », active.
- Automatisation `temperature` et blueprint `envoyer_valeur` supprimés de
  HA (le blueprint reste dans le dépôt).
- Anomalie de 18:18 (commandes non appliquées, API connectée) : non
  reproduite ; cause probable, automatisation en cours de rechargement
  après réimport. À rouvrir si elle revient.

## Non vérifié / ouvert

- « périmée » : automatisation de l'accueil désactivée 15 min sans
  redémarrage ; même label que « indisponible », corrigé mais non
  constaté.
- Consigne − / + : validée au checkpoint `ef223f6`, non refaite en 0.2.x
  (aucun changement de ce code).
- Configuration de production (`hapanel.yaml`) jamais flashée.

## Spécifié, non implémenté : D015

- Chauffage éteint : préréglages, − / + et consigne masqués, consigne non
  réglable ; le blueprint refuse aussi `chauffage_consigne` thermostat
  `off` (ajout de l'agent, à confirmer par le propriétaire avant code).
- HA déconnecté : bandeau et navigation conservés, icône et message
  centrés selon la cause (« Pas de Wi-Fi » / « Pas de communication avec
  Home Assistant »), sans temporisation.
- Implémentation : branche `feature/`, compilation, OTA, tests, version
  0.3.0 ; réimport du blueprint ensuite.

## Mémoire de référence (G6)

| Mesure | 847e17c | dba8a48 |
|---|---|---|
| Mémoire libre (capteur `debug`) | 188 620 à 188 772 o | 189 460 à 189 532 o (première minute) |
| Plus grand bloc libre | 110 592 o | 110 592 o |
| RAM statique (banc) | 49 896 o (27,6 %) | 49 896 o (27,6 %) |
| Flash (banc) | 1 093 899 o (59,6 %) | 1 093 935 o (59,6 %) |

## Décisions, risques, invariants

- Décision ajoutée : D015 (spécification).
- Ouverts : R2, R4, R5, R7, R8, R9 ; dette T1.
- Invariants : P3 rétabli pour « indisponible » (était violé à l'écran
  jusqu'en 0.2.0) ; P2, P4 inchangés ; G5 (version injectée) ; G6
  (mesure ci-dessus) ; G10 (aucun identifiant renommé).

## Ménage restant

- `secrets.yaml` : ligne `ota_password` devenue inutile ; `AGENTS.md` et
  G9 citent encore le « mot de passe OTA » (OTA par clé de l'API, D010).
- Blueprint : un changement d'attribut du thermostat renvoie les huit
  clés ; Versatile Thermostat en enchaîne plusieurs (bavard, sans effet).

## Pièges connus

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash.
- `build.ps1 upload` ne compile pas : enchaîner `compile` puis `upload`,
  ou utiliser `run`.
- `build.ps1 logs` affiche le SHA du dépôt local, pas celui du binaire :
  lire `Project cnuma.hapanel version` et la date de compilation.
- Journal redirigé par PowerShell 5.1 (`*>`) : UTF-16 ou UTF-8 avec BOM
  selon la commande.
- « Bootloader rollback: supported » au démarrage n'est pas un retour
  arrière ; seul « OTA rollback detected » en est un.
- LVGL : un label non aligné à gauche dont le texte change porte une
  largeur fixe (`04_DEVELOPMENT_RULES.md`).
- HA ne garde que les 5 dernières traces d'une automatisation ; Versatile
  Thermostat la déclenche souvent : lire les traces aussitôt après l'essai.
- Après chaque OTA, relire la version après 60 s (« Boot seems
  successful »).

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
`run` ou `logs` (`-Device <IP_PANNEAU>`). Suite proposée : test
« périmée », puis implémentation de D015 (après confirmation du refus de
consigne côté blueprint).
