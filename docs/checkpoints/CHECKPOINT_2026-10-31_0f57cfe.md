# Checkpoint du 31 octobre 2026 — `0f57cfe`

Huitième checkpoint de HAPanel : version `0.3.0`, accueil allégé (D015)
validé à l'écran. Réimport du blueprint et test du refus de consigne non
confirmés. Remplace `CHECKPOINT_2026-10-30_dba8a48.md`.

## Identité

| Rubrique | Valeur |
|---|---|
| Dépôt | `cnuma/HAPanel` (public, `main` protégée : ni suppression ni push forcé) |
| Branche | `main`, seule branche à ce checkpoint |
| Configuration validée | `0f57cfe` ; le commit suivant n'ajoute que de la documentation |
| Binaire sur le panneau | `hapanel_banc.yaml`, `0.3.0 (a81d3bb)`, compilé le 31 octobre 2026 à 08:35, OTA chiffrée, « Boot seems successful », pas de retour arrière ; `0f57cfe` n'ajoute que de la documentation |
| Version | `0.3.0` (fichier `VERSION`) |
| ESPHome | 2026.10.1 (`requirements.txt`), ESP-IDF 5.5.6, LVGL 9.5.0, framework `esp-idf` |
| Home Assistant | HA OS, Core 2026.9.4, sur 192.168.1.155 |
| Carte | ESP32-2432S024C, ESP32 rev 3.1, flash 4 Mo, sans PSRAM |
| Alimentation | bloc secteur externe 1 A (le port USB du PC provoque des brownouts, R7) |
| Module de banc | nœud `hapanel-a85bfc`, « HAPanelSejourCheminee » dans HA, IP 192.168.1.197 le 31 octobre 2026 (DHCP, à redemander) ; OTA uniquement |

## Changements depuis `dba8a48`

| Fichier | Changement |
|---|---|
| `packages/pages/accueil.yaml` | Chauffage éteint : préréglages, − / + et consigne masqués et interdits. HA déconnecté : bandeau, navigation, icône et message selon la cause. Rafraîchissement à `on_boot` et aux changements de Wi-Fi |
| `packages/lvgl.yaml` | Glyphes `mdi:wifi-off` (`F05AA`) et `mdi:lan-disconnect` (`F0319`) |
| `blueprints/automation/hapanel/ecran_accueil.yaml` | Refus de `chauffage_consigne` si le thermostat n'est pas `heat` |
| `VERSION` | `0.2.1` → `0.3.0` |
| `AGENTS.md`, `docs/codex/00`, `02`, `03`, `08`, `docs/TODO.md` | D015 ; mentions périmées corrigées (mot de passe OTA, nom du nœud, surface de commande) ; nouvelles idées P3 |

Volontairement non modifiés : `packages/liaison_ha.yaml`,
`packages/base.yaml`, `packages/hardware.yaml`, `hapanel.yaml`,
`hapanel_banc.yaml`, `tools/build.ps1`. Aucun identifiant renommé (G10).

## Validé

| Point | Binaire | Résultat |
|---|---|---|
| OTA, version relue, « Boot seems successful » | `a81d3bb` | ✅ journaux |
| Valeurs reçues de HA au démarrage | `a81d3bb` | ✅ journaux |
| Liste de tests D015 à l'écran (chauffage éteint et rallumé, HA coupé, Wi-Fi coupé, navigation, « indisponible », redémarrage) | `a81d3bb` | ✅ propriétaire, retour global « ça marche », sans détail test par test |
| Compilation de production (`hapanel.yaml`) | `0f57cfe` | ✅ compile, jamais flashée |

## Non vérifié / ouvert

- **Blueprint D015 :** l'import a d'abord échoué dans HA (« source
  introuvable ») alors que l'adresse répond depuis le PC (code 200). Résultat
  du nouvel essai non connu : HA peut encore tourner avec l'ancien blueprint.
  Sans conséquence avec ce firmware, qui n'envoie pas de consigne chauffage
  éteint. Refus de consigne non constaté.
- « périmée » : test reporté par le propriétaire (automatisation désactivée
  16 min sans redémarrage : la péremption survient entre 10 et 15 min 30).
- Délai d'affichage de « Pas de Wi-Fi » non relevé.

## Mémoire de référence (G6)

| Mesure | dba8a48 | a81d3bb |
|---|---|---|
| Mémoire libre (capteur `debug`) | 189 460 à 189 532 o | 189 072 à 189 124 o (première minute) |
| Plus grand bloc libre | 110 592 o | 110 592 o |
| RAM statique (banc) | 49 896 o (27,6 %) | 49 968 o (27,6 %) |
| Flash (banc) | 1 093 935 o (59,6 %) | 1 095 043 o (59,7 %) |

## Décisions, risques, invariants

- D015 implémentée, complément du 31 octobre 2026.
- Ouverts : R2, R4, R5, R7, R8, R9 ; dette T1.
- Invariants : P2, P4 et P5 préservés par D015 ; G5, G6 (mesure ci-dessus),
  G10.

## Pièges connus

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash.
- `build.ps1 upload` ne compile pas : enchaîner `compile` puis `upload`, ou
  utiliser `run`, avec `-Config hapanel_banc.yaml`.
- `hapanel.yaml` et `hapanel_banc.yaml` partagent leur répertoire de
  compilation : recompiler le banc avant tout `upload` de banc.
- `build.ps1 logs` affiche le SHA du dépôt local, pas celui du binaire : lire
  `Project cnuma.hapanel version` et la date de compilation.
- « Bootloader rollback: supported » n'est pas un retour arrière ; seul « OTA
  rollback detected » en est un.
- HA ne garde que les 5 dernières traces d'une automatisation.
- Après chaque OTA, relire la version après 60 s (« Boot seems successful »).
- `secrets.yaml` : ligne `ota_password` devenue inutile.

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
(`-Device <IP_PANNEAU>`). Suite : réimport du blueprint et test du refus,
version 0.4.0 (toucher sur la glissière, température extérieure, icônes en
couleur), puis 0.5.0 (LED et extinction de l'écran).
