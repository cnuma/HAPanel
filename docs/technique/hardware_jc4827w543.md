# packages/hardware_jc4827w543.yaml

## Rôle

La description de la carte **Guition JC4827W543C_I** : écran 4,3" de 480 × 272,
tactile **capacitif** GT911, puce **ESP32-S3** avec 8 Mo de PSRAM (D049). Même rôle que
[hardware.md](hardware.md) pour l'ESP32-2432S024C : seul fichier qui nomme une broche
ou un bus pour cette carte (G2).

Il déclare **les mêmes `id`** que `hardware.yaml`. Le reste du panneau (pages, LVGL,
veille, LED) les utilise sans savoir quelle carte est montée.

**État :** validée au banc le 9 novembre 2026 en portrait provisoire (cahier Q) ;
paysage à valider (cahier U). Le brochage vient d'AquaLook, qui a validé cette
carte sur matériel le 27 août 2026 (`docs/architecture/HW_JC4827W543_PORT_IMPACT.md` du
dépôt `cnuma/AquaLook`), et du modèle `JC4827W543` d'ESPHome.

**Paysage (D053) :** l'écran est en paysage, 480 × 272, port USB à gauche ; les pages
prennent leurs positions dans `packages/format_paysage.yaml`, inclus par ce fichier.
Jusqu'à 0.11.2, il était tourné en portrait, pages de 240 × 320 centrées (D049).

## Dépendances

- **Inclut :** `format_paysage.yaml`, positions et tailles des pages pour 480 × 272
  (D053).
- **Fournit :** les mêmes `id` que `hardware.yaml` (`bus_spi_ecran`, `bus_i2c_tactile`,
  `sortie_retroeclairage`, `sortie_led_rouge`, `sortie_led_vert`, `sortie_led_bleu`,
  `ldr_tension`, `retroeclairage`, `ecran`, `tactile`).
- **Inclus par :** `hapanel_jc4827w543_public.yaml` (D049).

## Différences avec la S024C

| Élément | S024C (`hardware.yaml`) | JC4827W543 (ce fichier) |
|---|---|---|
| Puce | ESP32, révision 3.1, sans PSRAM | **ESP32-S3**, 8 Mo de PSRAM octale |
| Écran | ILI9341, 240 × 320, bus SPI | **NV3041A, 480 × 272, bus QSPI** (4 lignes de données) |
| Orientation | Portrait natif, format portrait | Paysage, tourné de 180° par LVGL (port USB à gauche), format paysage |
| Tactile | CST820, lu toutes les 20 ms | **GT911**, interruption sur GPIO3 |
| Rétroéclairage | GPIO27 | **GPIO1** |
| LED RVB, LDR | GPIO4/16/17, GPIO34 | **Aucune** : sorties et capteur sans effet |

## Bloc par bloc

### Bloc `substitutions` : le brochage

| Substitution | Valeur | Rôle |
|---|---|---|
| `pin_qspi_clk` | `GPIO47` | Horloge du bus QSPI de l'écran. |
| `pin_qspi_d0`, `pin_qspi_d1`, `pin_qspi_d2`, `pin_qspi_d3` | `GPIO21`, `GPIO48`, `GPIO40`, `GPIO39` | Quatre lignes de données. **GPIO21 n'est pas le rétroéclairage ici** (il l'est sur la S028) : le reprogrammer casse l'écran en silence (piège d'AquaLook). |
| `pin_retroeclairage` | `GPIO1` | Rétroéclairage, variable. |
| `pin_i2c_sda`, `pin_i2c_scl` | `GPIO8`, `GPIO4` | Bus I²C du tactile. |
| `pin_tactile_int`, `pin_tactile_rst` | `GPIO3`, `GPIO38` | Interruption et remise à zéro du GT911. GPIO3 est une broche de démarrage (`ignore_strapping_warning`). |

### Bloc `packages` : le format de l'écran (D053)

`format: !include format_paysage.yaml` : positions, tailles et polices des pages pour
480 × 272 (substitutions `ecran_largeur`, `ecran_hauteur`, `fmt_…`). Les cartes en
240 × 320 incluent `format_portrait.yaml`, aux mêmes clés.

### Blocs `esp32` et `psram`

| Clé | Valeur | Rôle |
|---|---|---|
| `board`, `variant` | `esp32-s3-devkitc-1`, `esp32s3` | ESP32-S3. |
| `flash_size` | `4MB` | Flash de la carte. |
| `framework.type` | `esp-idf` | Comme les autres cartes (D008). Pas de `minimum_chip_revision` : propre à l'ESP32. |
| `psram.mode`, `psram.speed` | `octal`, `80MHz` | Exigée par le modèle d'écran d'ESPHome ; elle porte aussi le tampon de LVGL et la rotation. |

### Blocs `spi` et `i2c`

`spi` est de type `quad` : quatre lignes de données au lieu d'une. `i2c` sert au seul
tactile, à 400 kHz comme sur la S024C.

### Blocs `output`, `sensor`, `light`

| id | Rôle |
|---|---|
| `sortie_retroeclairage` | `ledc` sur GPIO1. |
| `sortie_led_rouge`, `sortie_led_vert`, `sortie_led_bleu` | `template` sans action : `led_veille.yaml` y écrit sans effet. Les réglages de la LED restent affichés et sans effet (D049). |
| `ldr_tension` | `template`, toujours 0 V (plein jour) : rétroéclairage de jour, réglable par « Intensité écran ». Interne. |
| `retroeclairage` | Lumière monochrome sur `sortie_retroeclairage`, interne, comme sur la S024C. |

### Blocs `display`, `touchscreen`, `lvgl`

| Bloc | Contenu | Rôle |
|---|---|---|
| `display` | `mipi_spi`, modèle `JC4827W543` | Le modèle d'ESPHome fournit la séquence d'initialisation du NV3041A, `cs` sur GPIO45, couleurs inversées, 20 MHz. |
| `touchscreen` | `gt911`, interruption et remise à zéro, `transform` : `mirror_x` et `mirror_y` | Le GT911 donne sa propre résolution ; pas de calibrage. Il est monté à 180° de l'écran : ses deux axes sont inversés, comme dans AquaLook (cahier Q3). |
| `lvgl.rotation` | `180` | Paysage, port USB à gauche (D053, cahier U2). En portrait, `270` mettait la barre d'état du côté opposé au port USB (cahier Q2) : le port est donc à droite de l'image native, et 180° le met à gauche. LVGL tourne l'image en mémoire (PSRAM), le tactile suit. |

## Maintenance

| Opération | Méthode |
|---|---|
| Écran à l'envers ou tactile inversé | **D'abord couper le courant** (piège ci-dessous). Puis changer `lvgl.rotation` (`0` ou `180` en paysage) : l'image et le toucher tournent ensemble ; si seul le tactile est inversé, changer `transform` (`mirror_x`, `mirror_y`) du bloc `touchscreen`. |
| Déplacer un élément d'une page | Changer sa substitution `fmt_…` dans `format_paysage.yaml` (D053), régénérer les maquettes (`tools/generer_maquettes_paysage.py`). |
| Nouvel élément ou nouvelle page | Ses positions en substitutions, ajoutées aux deux fichiers de format, aux mêmes clés. |

**Pièges :**
- L'écran n'a pas de broche de remise à zéro : après un flash par USB, il garde l'état
  du firmware précédent (couleurs inversées, image à 180°) jusqu'à une coupure de
  courant. Juger l'image après avoir débranché et rebranché la carte (cahier Q2).
- Un binaire d'une autre carte s'installe sur celle-ci (et inversement) seulement par USB ;
  la mise à jour par Wi-Fi le refuse grâce au champ `chipFamily` du manifeste
  (`ESP32-S3`).
- AquaLook a vu des redémarrages par chien de garde en parcourant le tas avec 8 Mo de
  PSRAM (`heap_caps_get_largest_free_block`) ; la page À propos ne parcourt que la
  mémoire interne, mais un redémarrage toutes les 10 s environ viendrait de là (cahier Q).
