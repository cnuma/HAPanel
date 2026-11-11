# 00 — Contexte du projet

Mis à jour le 28 octobre 2026. Les rubriques « À définir » bloquent toute
implémentation qui en dépend : elles se tranchent avec le propriétaire puis
s'inscrivent ici et dans `02_DECISIONS.md`.

## Produit

HAPanel est un panneau de commande mural multi-écrans pour Home Assistant.
Il affiche l'état de la maison et envoie des commandes ; toute la logique et
tous les appareils restent dans Home Assistant (D007).

**Principe directeur :** le panneau ne ment jamais. Un état inconnu,
indisponible ou périmé est affiché comme tel, et aucune commande n'est
envoyée sur un tel état.

## Écrans

Définis pas à pas ; chaque écran validé est ajouté ici avec les entités
Home Assistant qu'il lit et les actions qu'il déclenche.

| Écran | Entités lues | Actions | État |
|---|---|---|---|
| Accueil (page de démarrage) | Températures du séjour et de l'extérieur ; mode, activité, consigne, préréglage et verrou du thermostat ; bornes ; heure de HA (entités choisies dans le blueprint `module.yaml`, D012, D014, D021) | Allumer / couper le chauffage (glissière Éteint / Chauffage), préréglage (icônes Manuel, Hors-gel, Éco, Confort, Boost, chauffage allumé), consigne ±0,5 °C entre les bornes (15 à 25 °C par défaut), chauffage allumé seulement (D015) | Implémenté (`packages/pages/accueil.yaml`, D014, D015) ; validé au banc le 30 octobre 2026 : usage nominal, préréglages, redémarrage, HA déconnecté, « indisponible » (0.2.1) ; accueil allégé (0.3.0), toucher sur la glissière, température extérieure et icônes en couleur (0.4.0, D016), LED et écran éteint par inactivité (0.5.0, D017) validés le 31 octobre 2026 ; « périmée » non vérifiée (`docs/CAHIER_DE_TESTS.md`, F1) |
| Météo | Entité `weather.*` choisie dans le blueprint `module.yaml` : condition et température actuelles, prévisions quotidiennes sur 3 jours (`weather.get_forecasts`) ; clés `meteo_*` (D019) | Aucune | Implémenté (`packages/pages/meteo.yaml`), validé par le propriétaire le 1er novembre 2026 ; états dégradés non confirmés (`docs/CAHIER_DE_TESTS.md`) |
| Planning | 1 à 4 entités `calendar.*` choisies dans le blueprint `module.yaml` : créneaux du jour (`calendar.get_events`) ; clés `plan_*` (D020) | Aucune | Implémenté (`packages/pages/planning.yaml`), validé par le propriétaire le 1er novembre 2026 ; états dégradés non confirmés (`docs/CAHIER_DE_TESTS.md`) |
| Scénarios | Noms de 6 scènes, scripts ou automatisations au plus, choisis dans le blueprint `module.yaml` ; clés `scen_*` (D024) | Lancer un scénario par son numéro, avec réponse de HA (`esphome.hapanel_commande`) | Implémenté (`packages/pages/scenarios.yaml`), validé par le propriétaire le 1er novembre 2026 ; états dégradés non confirmés (`docs/CAHIER_DE_TESTS.md`) |
| Menu | Aucune | Navigation vers toutes les pages (D025) | Implémenté (`packages/pages/menu.yaml`), validé par le propriétaire le 1er novembre 2026 |
| À propos (version, SHA, connexion, adresse IP, mémoire) | Internes | Aucune | Validé au banc le 28 octobre 2026, y compris connecté / non connecté ; adresse IP le 7 novembre 2026 (cahier M) (`packages/lvgl.yaml`) |

## Home Assistant

| Rubrique | Valeur |
|---|---|
| Installation | HA OS, en natif sur Raspberry Pi |
| Version | Core 2026.9.4, Supervisor 2026.10.4, OS 18.3 (relevé le 27 octobre 2026) |
| Intégration | ESPHome, API native chiffrée (D005) |
| Modules | Plusieurs prévus, un seul binaire : nœud `hapanel-xxxxxx` (D012) ; en service, tous en binaire public et sans module d'atelier à part : cuisine `hapanel-583c28` et séjour `hapanel-a85bfc` (S024C), salle de bain (S028), Guition 4,3" en essai (D049) ; tous en 0.11.0 depuis le 9 novembre 2026 |
| Liaison | Valeurs poussées par le blueprint unique `blueprints/automation/hapanel/module.yaml`, une automatisation par module (D021 ; action `maj_valeur`, clés listées en D014, D019, D020, D024, D026, D027) ; demande de renvoi par l'événement `esphome.hapanel_demande_valeurs` (D012) ; commandes par l'événement `esphome.hapanel_commande` (D014) ; message d'accueil par l'action `message_accueil`, section du même blueprint (D028, D042) ; verrouillage enfants : entité « Verrouillage enfants » par module, imposable par la clé `verrou_enfants` (D056). Le blueprint générique `envoyer_valeur.yaml` reste disponible |

## Matériel de référence

| Rubrique | Valeur |
|---|---|
| Carte | ESP32-2432S024C (D004) : ESP32 classique (module WROOM, double cœur), sans PSRAM |
| Écran | 2,4", 240 × 320, contrôleur ILI9341 (confirmé au banc le 28 octobre 2026) |
| Tactile | Capacitif CST820, bus I²C (adresse `0x15`), composant ESPHome `cst816`, lecture périodique 50 ms (D009) ; coordonnées conformes à l'écran sans calibrage |
| LED | RVB de face avant, allumée à l'état bas : GPIO4 rouge, GPIO16 vert, GPIO17 bleu (D017) ; mode, intensité et alerte réglables par module (D027) |
| LDR | GPIO34, relevée le 31 octobre 2026, règle l'intensité de la LED (D018) et le rétroéclairage (D023), pièce sombre non testée |
| Flash | 4 Mo (détectée au premier flash) ; ESP32 rev 3.1 |
| Liaison USB | Convertisseur USB-série CH340 (Windows : « USB-SERIAL CH340 », relevé le 6 novembre 2026 ; liste de Chrome et Edge : « USB Serial (COMx) », le 7 novembre) ; pilote, si Windows ne l'installe pas : site du fabricant WCH uniquement (guide d'installation) |
| Alimentation | Bloc secteur externe 1 A validé au banc ; port USB du PC insuffisant (R7) |
| Montage mural | À définir |
| Autre carte | ESP32-2432S028 à deux prises USB (2,8", contrôleur ST7789V, tactile résistif XPT2046, rétroéclairage GPIO21) : `packages/hardware_2432s028.yaml`, validée au banc le 7 novembre 2026 (cahier K ; mémoire libre 153 Ko, plus grand bloc 96 Ko) ; binaire public `hapanel_2432s028_public.yaml` (D041), validé en `v0.9.0` le 7 novembre 2026 (cahier K12 à K15) |
| Carte 4,3" | Guition JC4827W543C_I (ESP32-S3, 4 Mo de flash, 8 Mo de PSRAM, écran NV3041A 480 × 272 en QSPI, tactile GT911, rétroéclairage GPIO1, ni LED ni LDR), brochage validé par AquaLook le 27 août 2026 : `packages/hardware_jc4827w543.yaml`, binaire public `hapanel_jc4827w543_public.yaml` (D049) ; validée au banc le 9 novembre 2026 en portrait provisoire (cahier Q1 à Q9), en essai dans la maison depuis 0.11.0 ; pages en paysage 480 × 272, port USB à gauche (D053, format `packages/format_paysage.yaml`), à valider (cahier U) |

## Environnement de développement

ESPHome en ligne de commande, version figée dans `requirements.txt`, YAML
dans le dépôt (D005). Nœud `hapanel-xxxxxx` (D012), framework `esp-idf`
(D008).

## Hors périmètre

- pilotage direct d'un appareil par le panneau (relais, sortie) : D007 ;
- édition des YAML dans l'outil ESPHome de Home Assistant.
