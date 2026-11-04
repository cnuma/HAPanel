# packages/hardware.yaml

## Rôle

La description de la carte ESP32-2432S024C (D004) : broches, bus, écran, tactile,
rétroéclairage, LED RVB et capteur de lumière (LDR). C'est le **seul** fichier qui
nomme une broche ou un bus (G2) : les autres fichiers utilisent les `id` déclarés ici.

Sans ce fichier, rien ne s'affiche et aucun toucher n'est reçu. Il ne contient aucun
comportement : il dit seulement ce que la carte possède.

Le brochage vient de publications pour cette carte, sans documentation du vendeur. Il
a été confirmé au banc : écran, bus et tactile le 28 octobre 2026, LED et LDR le
31 octobre 2026.

## Dépendances

- **Utilise :** rien des autres fichiers.
- **Fournit :**

| id | Utilisé par | Pour |
|---|---|---|
| `ecran`, `tactile` | `lvgl.yaml` | Affichage et toucher de LVGL. |
| `tactile` | `led_veille.yaml`, `hapanel_banc.yaml` (`!extend`) | Réveil de l'écran, journal des touchers. |
| `retroeclairage` | `led_veille.yaml` | Luminosité selon la pièce (D023), extinction en veille (D017). |
| `ldr_tension` | `led_veille.yaml` | Obscurité de la pièce (D018, D023). |
| `sortie_led_rouge`, `sortie_led_vert`, `sortie_led_bleu` | `led_veille.yaml`, `pages/accueil.yaml` | Couleur et respiration de la LED (D017, D018). |

## Bloc par bloc

### Bloc `substitutions` : le brochage

Toutes les broches sont regroupées ici : changer de carte revient d'abord à modifier ce
tableau.

| Substitution | Valeur | Rôle |
|---|---|---|
| `display_model` | `ILI9341` | Contrôleur de l'écran 240 × 320. |
| `pin_spi_clk` | `GPIO14` | Horloge du bus SPI de l'écran. |
| `pin_spi_mosi` | `GPIO13` | Données vers l'écran. |
| `pin_spi_miso` | `GPIO12` | Données depuis l'écran (peu utilisé). |
| `pin_ecran_cs` | `GPIO15` | Sélection de l'écran sur le bus SPI. |
| `pin_ecran_dc` | `GPIO2` | Distingue commande et donnée pour l'écran. |
| `pin_retroeclairage` | `GPIO27` | Rétroéclairage, variable. |
| `pin_i2c_sda` | `GPIO33` | Données du bus I²C du tactile. |
| `pin_i2c_scl` | `GPIO32` | Horloge du bus I²C du tactile. |
| `pin_tactile_int` | `GPIO21` | Interruption du tactile : **non utilisée** (D009). Gardée pour mémoire. |
| `pin_tactile_rst` | `GPIO25` | Remise à zéro du tactile. |
| `pin_led_rouge` | `GPIO4` | LED rouge, allumée à l'état bas (D017). |
| `pin_led_vert` | `GPIO16` | LED verte, allumée à l'état bas. |
| `pin_led_bleu` | `GPIO17` | LED bleue, allumée à l'état bas. |
| `pin_ldr` | `GPIO34` | LDR : la tension **monte** quand la pièce s'assombrit. |

### Bloc `spi`

| id | Clé | Rôle |
|---|---|---|
| `bus_spi_ecran` | `clk_pin`, `mosi_pin`, `miso_pin` | Bus de l'écran. |

`miso_pin` porte `ignore_strapping_warning: true`. GPIO12 est une broche lue par l'ESP32
au démarrage (« strapping »), et ESPHome avertit quand on l'utilise. C'est pourtant le
câblage d'origine de la carte : l'avertissement est volontairement masqué.

### Bloc `i2c`

| id | Clé | Rôle |
|---|---|---|
| `bus_i2c_tactile` | `sda`, `scl` | Bus du contrôleur tactile. |
| | `frequency` | `400kHz` au lieu des 50 kHz par défaut : chaque lecture du tactile est plus courte, ce qui permet de le lire toutes les 20 ms (D009). |

### Bloc `output` : sorties à modulation (PWM)

`ledc` est le générateur d'impulsions de l'ESP32 : il fait varier une sortie de 0 à
100 % en l'allumant et l'éteignant très vite.

| id | Broche | `inverted` | Piloté par |
|---|---|---|---|
| `sortie_retroeclairage` | `${pin_retroeclairage}` | non | La lumière `retroeclairage`, jamais directement. |
| `sortie_led_rouge` | `${pin_led_rouge}` | oui | Les lambdas de `led_veille.yaml` et `pages/accueil.yaml` (`set_level`). |
| `sortie_led_vert` | `${pin_led_vert}` | oui | Idem. |
| `sortie_led_bleu` | `${pin_led_bleu}` | oui | Idem. |

`inverted: true` : la LED s'allume quand la broche est à l'état bas. Grâce à
l'inversion, `set_level(1.0f)` allume à fond et `set_level(0.0f)` éteint, comme on
l'attend.

### Bloc `sensor` : la LDR

| id | Type | Nom dans HA | Rôle |
|---|---|---|---|
| `ldr_tension` | `adc` | aucun (interne) | Tension de la LDR, en volts. |

| Clé | Valeur | Rôle |
|---|---|---|
| `attenuation` | `0db` | Plage de mesure la plus fine de l'ESP32, jusqu'à environ 1 V. Les tensions relevées vont de 0,09 V (pièce éclairée) à 0,20 V (pièce sombre). |
| `samples` | `8` | Chaque mesure est la moyenne de 8 lectures. |
| `update_interval` | `1s` | Une mesure par seconde. |
| `sliding_window_moving_average` | `window_size: 5`, `send_every: 2`, `send_first_at: 1` | Moyenne des 5 dernières mesures, soit 5 s, publiée toutes les 2 mesures, soit 2 s. La première mesure est publiée dès le démarrage. Le signal est instable : la moyenne lisse les à-coups, et l'écart minimal de `led_veille.yaml` évite que l'écran varie sans cesse. Une minute auparavant : l'écran baissait trop lentement en éteignant une chambre (D023). |
| `on_value` | `logger.log` | Journalise la tension, tag `hapanel.led`, niveau `DEBUG` : visible sur le banc seulement. |

Les seuils jour et nuit (`ldr_tension_jour`, `ldr_tension_nuit`) ne sont pas ici : ils
sont dans `led_veille.yaml`, qui interprète la mesure.

### Bloc `light`

| id | Type | Nom dans HA | Rôle |
|---|---|---|---|
| `retroeclairage` | `monochromatic` | aucun (`internal: true`) | Lumière variable sur `sortie_retroeclairage`. Elle apporte les transitions douces et la correction gamma, que la sortie seule n'a pas. |

- `restore_mode: ALWAYS_ON` : l'écran s'allume toujours au démarrage, même s'il était
  éteint par la veille avant la coupure.
- `internal: true` : le `name` « Rétroéclairage » n'est pas exposé à Home Assistant.
  Seul le panneau gère son écran (D017, D023).

### Bloc `display`

| id | Clé | Valeur | Rôle |
|---|---|---|---|
| `ecran` | `platform` | `mipi_spi` | Pilote générique des écrans SPI d'ESPHome. |
| | `model` | `${display_model}` | Réglages propres à l'ILI9341. |
| | `spi_id` | `bus_spi_ecran` | Bus utilisé. |
| | `data_rate` | `40MHz` | Vitesse du bus : plus rapide, l'écran se redessine plus vite. Un essai à 20 MHz (cahier I11) a rendu la ligne parasite du haut plus fréquente. |
| | `cs_pin`, `dc_pin` | `ignore_strapping_warning: true` | GPIO15 et GPIO2 sont aussi des broches de démarrage : même raison que pour `miso_pin`. |

L'écran n'a ni `lambda` ni `pages` : c'est LVGL (`lvgl.yaml`) qui dessine dessus.

### Bloc `touchscreen`

| id | Clé | Valeur | Rôle |
|---|---|---|---|
| `tactile` | `platform` | `cst816` | Pilote de la famille CST816, qui convient à la puce CST820 de la carte. |
| | `i2c_id` | `bus_i2c_tactile` | Bus utilisé. |
| | `display` | `ecran` | Fait correspondre les coordonnées du toucher à celles de l'écran. |
| | `update_interval` | `20ms` | La puce est interrogée toutes les 20 ms (D009). À 50 ms, un toucher bref passait entre deux lectures : il fallait appuyer longtemps (retour du propriétaire, 3 novembre 2026). |
| | `reset_pin` | `${pin_tactile_rst}` | Remise à zéro au démarrage. |

**Pourquoi pas d'`interrupt_pin` :** au banc, aucune interruption n'arrive sur GPIO21.
Si on la déclare, ESPHome attend une interruption avant de lire la puce, et aucun
toucher n'est jamais reçu (D009). La lecture toutes les 20 ms coûte une courte
transaction I²C (environ 0,2 ms à 400 kHz) et ajoute au plus 20 ms de délai : sans
effet pour un panneau alimenté en permanence. Cette dette est notée T1.

## Maintenance

| Pour | Faire |
|---|---|
| Porter sur une autre carte | Modifier le tableau `substitutions`, puis `display_model`, la plateforme du tactile et, si besoin, `esp32.board` dans `base.yaml`. Revalider au banc écran, tactile (coins de l'écran, voir `hapanel.md`), LED et LDR. |
| Tactile lent ou touchers brefs ignorés | Baisser `update_interval` du tactile (20 ms aujourd'hui) ; garder `frequency: 400kHz` sur le bus. Vérifier au banc avec le journal des touchers. |
| Tactile décalé ou inversé | Ajouter `transform` (`swap_xy`, `mirror_x`, `mirror_y`) ou `calibration` sous `tactile`. Vérifier avec le journal des touchers du banc. |
| Couleurs de l'écran fausses | Options `invert_colors` ou `color_order` sous `ecran`. |
| LDR trop réactive ou trop lente | `window_size` (durée de la moyenne) et `send_every` (fréquence). Les seuils sont dans `led_veille.yaml`. |
| Exposer la LDR à Home Assistant | Lui donner un `name`. Une entité mise à jour toutes les 2 s : inutile en temps normal, et chargerait l'historique de HA. |

**Pièges :**
- Ne déclarer une broche ou un bus dans aucun autre fichier (G2) : utiliser `!extend`
  ou l'`id` déclaré ici.
- Retirer `inverted: true` d'une LED inverse toute sa logique : `0.0f` l'allumerait à
  fond.
- Ajouter `interrupt_pin` au tactile le rend muet (D009).
- Piloter `sortie_retroeclairage` directement contournerait la lumière
  `retroeclairage` : sa transition et son état (allumé ou éteint, utilisé par la veille)
  deviendraient faux.
- Monter `data_rate` au-delà de 40 MHz peut donner un écran brouillé.

**Contrôle après modification :** `.\tools\build.ps1 config`, puis `compile`, puis au
banc : affichage, toucher aux quatre coins, couleur de la LED et ligne `LDR … V` des
journaux en cachant puis en éclairant la LDR.
