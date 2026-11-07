# packages/hardware_2432s028.yaml

## Rôle

La description de la carte ESP32-2432S028 : écran 2,8" de 240 × 320, tactile
**résistif**, prises USB-C et micro-USB (carte du banc). Même rôle que [hardware.md](hardware.md) pour
l'ESP32-2432S024C : seul fichier qui nomme une broche ou un bus pour cette carte (G2).

Il déclare **les mêmes `id`** que `hardware.yaml`. Le reste du panneau (pages, LVGL,
veille, LED) les utilise sans savoir quelle carte est montée. Une configuration inclut
l'un **ou** l'autre fichier, jamais les deux : leurs `id` se heurteraient.

**État : en essai au banc** (branche `feature/carte-2432s028`, cahier K). Le brochage
vient d'AquaLook, qui utilise cette carte avec TFT_eSPI, et du modèle `ESP32-2432S028`
d'ESPHome. Il n'est pas encore confirmé sur la carte.

## Dépendances

- **Utilise :** rien des autres fichiers.
- **Fournit :** les mêmes `id` que `hardware.yaml` (tableau « Dépendances » de
  [hardware.md](hardware.md)), sauf `bus_i2c_tactile`, remplacé par `bus_spi_tactile`.
- **Inclus par :** `hapanel_2432s028_banc.yaml`.

## Différences avec la S024C

| Élément | S024C (`hardware.yaml`) | S028 (ce fichier) |
|---|---|---|
| Rétroéclairage `pin_retroeclairage` | GPIO27 | **GPIO21** : avec le binaire de la S024C, l'écran de la S028 reste noir |
| Tactile | Capacitif CST820, bus I²C | Résistif XPT2046, second bus SPI `bus_spi_tactile` |
| Calibrage du tactile | Aucun | **Obligatoire** : valeurs brutes de 0 à 4095 converties en pixels |
| Contrôleur de l'écran | ILI9341 | ST7789V (variante à deux prises USB) |
| Écran (bus), LED, LDR | GPIO14/13/12/15/2, GPIO4/16/17, GPIO34 | Identiques |

## Bloc par bloc

### Bloc `substitutions` : le brochage

| Substitution | Valeur | Rôle |
|---|---|---|
| `display_model` | `ESP32-2432S028-7789` | Modèle d'ESPHome pour la variante à deux prises USB, contrôleur ST7789V. Une seule prise micro-USB : `ILI9341`. Écran brouillé : `ESP32-2432S028-9342` (ILI9342, paysage natif, mise en page à reprendre). |
| `pin_spi_clk`, `pin_spi_mosi`, `pin_spi_miso` | `GPIO14`, `GPIO13`, `GPIO12` | Bus SPI de l'écran, comme la S024C. |
| `pin_ecran_cs`, `pin_ecran_dc` | `GPIO15`, `GPIO2` | Sélection de l'écran, commande ou donnée. |
| `pin_retroeclairage` | `GPIO21` | Rétroéclairage, variable. |
| `pin_tactile_clk`, `pin_tactile_mosi`, `pin_tactile_miso` | `GPIO25`, `GPIO32`, `GPIO39` | Bus SPI du tactile. GPIO39 est une broche d'entrée seule, ce qui suffit pour `miso`. |
| `pin_tactile_cs` | `GPIO33` | Sélection du tactile. |
| `pin_tactile_irq` | `GPIO36` | Signal « dalle appuyée » du XPT2046. |
| `pin_led_rouge`, `pin_led_vert`, `pin_led_bleu` | `GPIO4`, `GPIO16`, `GPIO17` | LED RVB, supposée allumée à l'état bas comme sur la S024C. |
| `pin_ldr` | `GPIO34` | LDR. |

### Bloc `spi` : deux bus

| id | Rôle |
|---|---|
| `bus_spi_ecran` | Bus de l'écran, identique à la S024C. |
| `bus_spi_tactile` | Bus du tactile, séparé : la carte câble le XPT2046 sur d'autres broches que l'écran. L'ESP32 dispose de deux bus SPI matériels libres. |

### Blocs `output`, `sensor`, `light`, `display`

Identiques à `hardware.yaml` : `sortie_retroeclairage`, `sortie_led_rouge`,
`sortie_led_vert`, `sortie_led_bleu`, `ldr_tension`, `retroeclairage` et `ecran`. Seule
la broche du rétroéclairage change. Voir [hardware.md](hardware.md) pour le détail.

### Bloc `touchscreen`

| id | Clé | Valeur | Rôle |
|---|---|---|---|
| `tactile` | `platform` | `xpt2046` | Contrôleur des dalles résistives. |
| | `spi_id` | `bus_spi_tactile` | Bus utilisé. |
| | `display` | `ecran` | Coordonnées rapportées à l'écran. |
| | `interrupt_pin` | `${pin_tactile_irq}` | Lecture seulement quand la dalle est appuyée. Si aucun toucher n'arrive, retirer cette ligne (même cas que D009 sur la S024C). |
| | `update_interval` | `20ms` | Même cadence que la S024C. |
| | `calibration` | 200 à 3900 sur les deux axes | Valeurs provisoires, à remplacer par celles relevées au banc. |

**Calibrer :** flasher `hapanel_2432s028_banc.yaml`, toucher les quatre coins, lire
dans les journaux les lignes `toucher … brut x=… y=…`. La plus petite et la plus grande
valeur brute de chaque axe vont dans `x_min`, `x_max`, `y_min`, `y_max`. Si un axe est
inversé ou si les axes sont croisés, ajouter `transform` (`mirror_x`, `mirror_y`,
`swap_xy`) : ESPHome refuse un `x_min` plus grand que `x_max`.

## Maintenance

**Pièges :**
- Même piège des bords de la dalle que la S024C (D036) : à vérifier sur cette carte.
- Les variantes de la S028 n'ont pas le même contrôleur : un écran blanc ou brouillé
  avec le rétroéclairage allumé fait penser à `display_model`. Couleurs en négatif :
  ajouter `invert_colors: true` sous `ecran`.

**Contrôle après modification :**
`.\tools\build.ps1 compile -Config hapanel_2432s028_banc.yaml`, puis au banc : affichage
et couleurs, toucher aux quatre coins, LED, ligne `LDR … V` des journaux.
