# Checkpoint du 28 octobre 2026 — `86adc26`

Troisième checkpoint de HAPanel : palier P1 clos, version `0.1.0`, OTA
chiffrée par la clé de l'API (D010), révision de puce fixée (D011).
Remplace `CHECKPOINT_2026-10-28_33bf440.md`.

## Identité

| Rubrique | Valeur |
|---|---|
| Dépôt | `cnuma/HAPanel` (public, `main` protégée : ni suppression ni push forcé) |
| Branche | `main` (fusion en avance rapide de `feature/p1-options-esp32`) |
| Configuration validée | commit `86adc26` ; le commit de ce checkpoint n'ajoute que de la documentation |
| Binaire sur le panneau | `hapanel_banc.yaml`, `0.1.0 (86adc26)`, compilé le 28 octobre 2026 à 20 h 32, OTA chiffrée |
| Version | `0.1.0` (fichier `VERSION`) |
| ESPHome | 2026.10.1 (`requirements.txt`), ESP-IDF 5.5.6, framework `esp-idf` |
| Home Assistant | HA OS, Core 2026.9.4, sur 192.168.1.155 |
| Carte | ESP32-2432S024C, ESP32 rev 3.1, flash 4 Mo, sans PSRAM |
| Alimentation | bloc secteur externe 1 A (le port USB du PC provoque des brownouts, R7) |
| Panneau | nœud `hapanel`, IP 192.168.1.197 (DHCP, à redemander à chaque session) ; plus branché en USB : tout passe par OTA |

## Fichiers modifiés depuis le checkpoint `33bf440`

| Fichier | Changement |
|---|---|
| `packages/base.yaml` | `ota: encryption:` (clé héritée de l'API), mot de passe OTA retiré ; `advanced: minimum_chip_revision: "3.1"` |
| `secrets.example.yaml` | `ota_password` retiré |
| `VERSION` | `0.1.0-dev` → `0.1.0` |
| `docs/codex/02_DECISIONS.md` | D010, D011 |
| `docs/codex/04_DEVELOPMENT_RULES.md`, `08_RISKS_AND_DEBT.md` | OTA chiffrée par la clé de l'API |
| `docs/TODO.md` | P1 clos ; `flash_chip` et `sram1_as_iram` reportés |

Volontairement non modifiés : `hapanel.yaml`, `hapanel_banc.yaml`,
`packages/hardware.yaml`, `packages/lvgl.yaml`, `tools/build.ps1`.
`AGENTS.md` et l'invariant G9 citent encore le « mot de passe OTA » parmi
les secrets : formulation à mettre à jour avec l'accord du propriétaire
(modification d'invariant).

`secrets.yaml` (hors Git) contient encore `ota_password`, devenu inutile :
le propriétaire peut retirer cette ligne.

## Validé sur le panneau (configuration de banc)

| Point | Résultat |
|---|---|
| OTA de transition (`7fbc947`, mot de passe + `allow_plaintext_upload`) | ✅ « Encrypted connection established » : le firmware précédent proposait déjà le chiffrement |
| OTA finale (`86adc26`, chiffrement exigé, aucun repli en clair) | ✅ « Encrypted connection established », « OTA successful » |
| Binaire exécuté = `86adc26` | ✅ journaux : « Project cnuma.hapanel version 0.1.0 », compilé 20 h 32, « Boot seems successful » |
| `Encryption: required` (OTA), `Noise encryption: YES` (API) | ✅ journaux |
| Avertissements du mot de passe OTA et de la révision de puce | ✅ disparus |
| Page « À propos » connecté / non connecté (P2) | ✅ au checkpoint `33bf440`, configuration de l'écran inchangée |

## Non vérifié

- Page « À propos » et entité « Version » affichant `0.1.0 (86adc26)` : à
  confirmer par le propriétaire.
- Redémarrage de Home Assistant panneau allumé : écarté par le propriétaire.
- Configuration de production (`hapanel.yaml`) : compilée, jamais flashée.

## Mémoire de référence (G6)

| Mesure | Valeur |
|---|---|
| Mémoire libre (capteur `debug`) | ≈ 197 Ko (201 604 o en régime établi, +700 o) |
| Plus grand bloc libre | 108 Ko (110 592 o, inchangé) |
| RAM statique (compilation) | 46 Ko sur 176 Ko (26,0 %) |
| Flash (application) | 1,05 Mo sur 1,79 Mo (57,3 %, −5 Ko) |

## Décisions et risques

- Décisions ajoutées : D010 (OTA chiffrée par la clé de l'API), D011
  (`minimum_chip_revision: "3.1"`, `flash_chip` et `sram1_as_iram` reportés).
- R2, R5, R7 ouverts ; dette T1 inchangée.
- Invariants préservés : G1, G2, G5, G9 (aucun secret ajouté), G10 (aucun
  nom changé), P1, P2, P5.

## Points ouverts

1. P2 : définir l'écran d'accueil avec le propriétaire.
2. Alimentation du montage mural (R7).
3. Glyphes manquants signalés par les polices (11 par police) : à relire
   avant d'afficher des textes nouveaux.
4. Formulation « mot de passe OTA » dans `AGENTS.md` et G9.

## Pièges connus

- Lancer ESPHome depuis PowerShell, jamais depuis Git Bash.
- Alterner production et banc recompile tout (≈ 10 min).
- Ligne `NativeCommandError` sous PowerShell 5.1 : sans effet, le code de
  sortie d'ESPHome fait foi.
- Ne jamais juger un démarrage alimenté par le port USB du PC (R7).
- Après chaque OTA, relire le SHA (écran ou journaux) après 60 s.
- Perdre `api_encryption_key` interdit toute OTA : flash par USB obligatoire.

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

Puis demander au propriétaire l'IP courante du panneau avant tout `upload`,
`run` ou `logs` (`-Device <IP_PANNEAU>`).
