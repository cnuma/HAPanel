# Index des identifiants du YAML

Fichier généré par `tools/verifier_doc_technique.py` : ne pas le modifier à la main.
Relancer le script après toute modification du YAML.

| id | Type | Déclaré dans | Utilisé aussi dans |
|---|---|---|---|
| `accueil_consigne_cible` | globals | packages/pages/accueil.yaml | — |
| `accueil_consigne_permise` | globals | packages/pages/accueil.yaml | — |
| `accueil_envoyer_consigne` | script | packages/pages/accueil.yaml | — |
| `accueil_envoyer_mode` | script | packages/pages/accueil.yaml | — |
| `accueil_envoyer_prereglage` | script | packages/pages/accueil.yaml | — |
| `accueil_glisse_actif` | globals | packages/pages/accueil.yaml | — |
| `accueil_glisse_depart` | globals | packages/pages/accueil.yaml | — |
| `accueil_glisse_x0` | globals | packages/pages/accueil.yaml | — |
| `accueil_heure` | script | packages/pages/accueil.yaml | packages/lvgl.yaml |
| `accueil_mode_cible` | globals | packages/pages/accueil.yaml | — |
| `accueil_mode_permis` | globals | packages/pages/accueil.yaml | — |
| `accueil_prereglage_actuel` | globals | packages/pages/accueil.yaml | — |
| `accueil_prereglage_cible` | globals | packages/pages/accueil.yaml | — |
| `accueil_prereglage_permis` | globals | packages/pages/accueil.yaml | — |
| `accueil_rafraichir` | script | packages/pages/accueil.yaml | packages/led_veille.yaml, packages/liaison_ha.yaml, packages/lvgl.yaml |
| `accueil_regler_consigne` | script | packages/pages/accueil.yaml | — |
| `accueil_wifi` | script | packages/pages/accueil.yaml | packages/lvgl.yaml |
| `apropos_ip` | text_sensor (ip_address) | packages/lvgl.yaml | — |
| `apropos_maj_trouvee` | globals | packages/lvgl.yaml | packages/acces_public.yaml |
| `banc_memoire_libre` | sensor (free) | hapanel_banc.yaml | hapanel_2432s028_banc.yaml |
| `banc_memoire_libre` | sensor (free) | hapanel_2432s028_banc.yaml | hapanel_banc.yaml |
| `banc_plus_grand_bloc` | sensor (block) | hapanel_banc.yaml | hapanel_2432s028_banc.yaml |
| `banc_plus_grand_bloc` | sensor (block) | hapanel_2432s028_banc.yaml | hapanel_banc.yaml |
| `btn_acc_moins` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_plus` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_pre_boost` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_pre_comfort` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_pre_eco` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_pre_frost` | widget button | packages/pages/accueil.yaml | — |
| `btn_acc_pre_none` | widget button | packages/pages/accueil.yaml | — |
| `btn_apropos_maj` | widget button | packages/lvgl.yaml | packages/acces_public.yaml |
| `btn_maj_annuler` | widget button | packages/acces_public.yaml | — |
| `btn_maj_fermer` | widget button | packages/acces_public.yaml | — |
| `btn_maj_installer` | widget button | packages/acces_public.yaml | — |
| `btn_men_apropos` | widget button | packages/pages/menu.yaml | — |
| `btn_men_maj` | widget button | packages/pages/menu.yaml | packages/acces_public.yaml |
| `btn_men_meteo` | widget button | packages/pages/menu.yaml | — |
| `btn_men_planning` | widget button | packages/pages/menu.yaml | — |
| `btn_men_reglages` | widget button | packages/pages/menu.yaml | — |
| `btn_men_scenarios` | widget button | packages/pages/menu.yaml | — |
| `btn_msg_fermer` | widget button | packages/message_accueil.yaml | — |
| `btn_nav_accueil` | widget button | packages/lvgl.yaml | — |
| `btn_nav_menu` | widget button | packages/lvgl.yaml | packages/pages/menu.yaml |
| `btn_sce_1` | widget button | packages/pages/scenarios.yaml | — |
| `btn_sce_2` | widget button | packages/pages/scenarios.yaml | — |
| `btn_sce_3` | widget button | packages/pages/scenarios.yaml | — |
| `btn_sce_4` | widget button | packages/pages/scenarios.yaml | — |
| `btn_sce_5` | widget button | packages/pages/scenarios.yaml | — |
| `btn_sce_6` | widget button | packages/pages/scenarios.yaml | — |
| `bus_i2c_tactile` | i2c | packages/hardware.yaml | packages/hardware_jc4827w543.yaml |
| `bus_i2c_tactile` | i2c | packages/hardware_jc4827w543.yaml | packages/hardware.yaml |
| `bus_spi_ecran` | spi | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml |
| `bus_spi_ecran` | spi | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml |
| `bus_spi_ecran` | spi | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml |
| `bus_spi_tactile` | spi | packages/hardware_2432s028.yaml | — |
| `ecran` | display (mipi_spi) | packages/hardware.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/acces_prive.yaml, packages/acces_public.yaml, packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/liaison_ha.yaml, packages/lvgl.yaml, packages/message_accueil.yaml, packages/pages/accueil.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml, packages/pages/reglages.yaml, packages/pages/scenarios.yaml |
| `ecran` | display (mipi_spi) | packages/hardware_2432s028.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/acces_prive.yaml, packages/acces_public.yaml, packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/liaison_ha.yaml, packages/lvgl.yaml, packages/message_accueil.yaml, packages/pages/accueil.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml, packages/pages/reglages.yaml, packages/pages/scenarios.yaml |
| `ecran` | display (mipi_spi) | packages/hardware_jc4827w543.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/acces_prive.yaml, packages/acces_public.yaml, packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml, packages/liaison_ha.yaml, packages/lvgl.yaml, packages/message_accueil.yaml, packages/pages/accueil.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml, packages/pages/reglages.yaml, packages/pages/scenarios.yaml |
| `ecran_intensite` | number (template) | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `enregistrement_signaler` | script | packages/lvgl.yaml | packages/led_veille.yaml, packages/message_accueil.yaml |
| `ha_connecte_affiche` | globals | packages/lvgl.yaml | packages/led_veille.yaml, packages/pages/accueil.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml, packages/pages/scenarios.yaml |
| `heure_ha` | time (homeassistant) | packages/pages/accueil.yaml | packages/acces_public.yaml, packages/pages/planning.yaml |
| `ico_barre_enregistrement` | widget label | packages/lvgl.yaml | — |
| `ico_barre_maj` | widget label | packages/lvgl.yaml | — |
| `ico_reg_ecran_intensite_verrou` | widget label | packages/pages/reglages.yaml | — |
| `ico_reg_led_alerte_verrou` | widget label | packages/pages/reglages.yaml | — |
| `ico_reg_led_intensite_verrou` | widget label | packages/pages/reglages.yaml | — |
| `ico_reg_led_verrou` | widget label | packages/pages/reglages.yaml | — |
| `ico_sce_1` | widget label | packages/pages/scenarios.yaml | — |
| `ico_sce_2` | widget label | packages/pages/scenarios.yaml | — |
| `ico_sce_3` | widget label | packages/pages/scenarios.yaml | — |
| `ico_sce_4` | widget label | packages/pages/scenarios.yaml | — |
| `ico_sce_5` | widget label | packages/pages/scenarios.yaml | — |
| `ico_sce_6` | widget label | packages/pages/scenarios.yaml | — |
| `identite_build` | text_sensor (template) | packages/base.yaml | — |
| `lbl_acc_chauffage` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_consigne` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_exterieur` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_hs_icone` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_hs_message` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_option_chauffage` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_option_eteint` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_sejour` | widget label | packages/pages/accueil.yaml | packages/liaison_ha.yaml |
| `lbl_acc_temperature` | widget label | packages/pages/accueil.yaml | — |
| `lbl_acc_temperature_etat` | widget label | packages/pages/accueil.yaml | — |
| `lbl_apropos_connexion` | widget label | packages/lvgl.yaml | — |
| `lbl_apropos_ip` | widget label | packages/lvgl.yaml | — |
| `lbl_apropos_maj` | widget label | packages/lvgl.yaml | packages/acces_public.yaml |
| `lbl_apropos_memoire` | widget label | packages/lvgl.yaml | — |
| `lbl_apropos_sha` | widget label | packages/lvgl.yaml | — |
| `lbl_apropos_version` | widget label | packages/lvgl.yaml | — |
| `lbl_barre_date` | widget label | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `lbl_barre_titre` | widget label | packages/lvgl.yaml | packages/pages/accueil.yaml, packages/pages/menu.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml, packages/pages/reglages.yaml, packages/pages/scenarios.yaml |
| `lbl_maj_resume` | widget label | packages/acces_public.yaml | — |
| `lbl_maj_texte` | widget label | packages/acces_public.yaml | — |
| `lbl_met_condition` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_etat` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_icone` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j1_icone` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j1_jour` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j1_temp` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j2_icone` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j2_jour` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j2_temp` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j3_icone` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j3_jour` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_j3_temp` | widget label | packages/pages/meteo.yaml | — |
| `lbl_met_temperature` | widget label | packages/pages/meteo.yaml | — |
| `lbl_msg_infos` | widget label | packages/message_accueil.yaml | — |
| `lbl_msg_texte` | widget label | packages/message_accueil.yaml | — |
| `lbl_pla_etat` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_h0` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_h12` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_h18` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_h24` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_h6` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_horaire_2` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_horaire_3` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_horaire_4` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_nom_1` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_nom_2` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_nom_3` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_nom_4` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_resume` | widget label | packages/pages/planning.yaml | — |
| `lbl_pla_titre` | widget label | packages/pages/planning.yaml | — |
| `lbl_reg_ecran_intensite` | widget label | packages/pages/reglages.yaml | — |
| `lbl_reg_led_intensite` | widget label | packages/pages/reglages.yaml | — |
| `lbl_sce_1` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_2` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_3` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_4` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_5` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_6` | widget label | packages/pages/scenarios.yaml | — |
| `lbl_sce_etat` | widget label | packages/pages/scenarios.yaml | — |
| `ldr_obscurite` | globals | packages/led_veille.yaml | — |
| `ldr_tension` | sensor (adc) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `ldr_tension` | sensor (adc) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `ldr_tension` | sensor (template) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml |
| `led_alerte` | globals | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/accueil.yaml |
| `led_alerte_active` | switch (template) | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `led_allumee` | globals | packages/led_veille.yaml | — |
| `led_bleu` | globals | packages/led_veille.yaml | packages/pages/accueil.yaml |
| `led_intensite` | number (template) | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `led_mode` | select (template) | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `led_rouge` | globals | packages/led_veille.yaml | packages/pages/accueil.yaml |
| `led_vert` | globals | packages/led_veille.yaml | packages/pages/accueil.yaml |
| `liaison_chauffage_action` | globals | packages/liaison_ha.yaml | — |
| `liaison_chauffage_consigne` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_chauffage_effacer` | script | packages/liaison_ha.yaml | — |
| `liaison_chauffage_etat` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_chauffage_mode` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_chauffage_ms` | globals | packages/liaison_ha.yaml | — |
| `liaison_chauffage_prereglage` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_chauffage_verrou` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_connectee` | script | packages/liaison_ha.yaml | packages/lvgl.yaml |
| `liaison_consigne_max` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_consigne_min` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_deconnectee` | script | packages/liaison_ha.yaml | packages/lvgl.yaml |
| `liaison_exterieure` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_exterieure_etat` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_exterieure_ms` | globals | packages/liaison_ha.yaml | — |
| `liaison_meteo_condition` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_effacer` | script | packages/liaison_ha.yaml | — |
| `liaison_meteo_etat` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_jour` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_jour_condition` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_max` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_min` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_meteo_ms` | globals | packages/liaison_ha.yaml | — |
| `liaison_meteo_temperature` | globals | packages/liaison_ha.yaml | packages/pages/meteo.yaml |
| `liaison_planning_creneaux` | globals | packages/liaison_ha.yaml | packages/pages/planning.yaml |
| `liaison_planning_effacer` | script | packages/liaison_ha.yaml | — |
| `liaison_planning_etat` | globals | packages/liaison_ha.yaml | packages/pages/planning.yaml |
| `liaison_planning_ms` | globals | packages/liaison_ha.yaml | — |
| `liaison_planning_nom` | globals | packages/liaison_ha.yaml | packages/pages/planning.yaml |
| `liaison_scenarios_couleur` | globals | packages/liaison_ha.yaml | packages/pages/scenarios.yaml |
| `liaison_scenarios_effacer` | script | packages/liaison_ha.yaml | — |
| `liaison_scenarios_etat` | globals | packages/liaison_ha.yaml | packages/pages/scenarios.yaml |
| `liaison_scenarios_icone` | globals | packages/liaison_ha.yaml | packages/pages/scenarios.yaml |
| `liaison_scenarios_ms` | globals | packages/liaison_ha.yaml | — |
| `liaison_scenarios_nom` | globals | packages/liaison_ha.yaml | packages/pages/scenarios.yaml |
| `liaison_temperature` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_temperature_etat` | globals | packages/liaison_ha.yaml | packages/pages/accueil.yaml |
| `liaison_temperature_ms` | globals | packages/liaison_ha.yaml | — |
| `maj_disponible` | globals | packages/lvgl.yaml | packages/acces_public.yaml, packages/led_veille.yaml |
| `maj_fermer` | script | packages/acces_public.yaml | — |
| `maj_firmware` | update (http_request) | packages/acces_public.yaml | packages/lvgl.yaml |
| `maj_installation` | globals | packages/acces_public.yaml | — |
| `maj_installer` | script | packages/acces_public.yaml | — |
| `maj_proposer` | script | packages/acces_prive.yaml | packages/acces_public.yaml, packages/pages/menu.yaml |
| `maj_proposer` | script | packages/acces_public.yaml | packages/acces_prive.yaml, packages/pages/menu.yaml |
| `maj_recherche_debut` | globals | packages/acces_public.yaml | — |
| `maj_recherche_demarrage` | script | packages/acces_public.yaml | — |
| `maj_recherche_demarrage_lancer` | script | packages/acces_public.yaml | — |
| `maj_rechercher` | script | packages/acces_prive.yaml | packages/acces_public.yaml, packages/lvgl.yaml |
| `maj_rechercher` | script | packages/acces_public.yaml | packages/acces_prive.yaml, packages/lvgl.yaml |
| `maj_rechercher_reseau` | script | packages/acces_public.yaml | — |
| `maj_reponses` | globals | packages/acces_public.yaml | — |
| `message_actif` | switch (template) | packages/message_accueil.yaml | — |
| `message_fermer` | script | packages/message_accueil.yaml | packages/liaison_ha.yaml |
| `message_ms` | globals | packages/message_accueil.yaml | packages/led_veille.yaml |
| `meteo_rafraichir` | script | packages/pages/meteo.yaml | packages/liaison_ha.yaml |
| `obj_acc_glissiere` | widget obj | packages/pages/accueil.yaml | — |
| `obj_acc_pastille` | widget obj | packages/pages/accueil.yaml | — |
| `obj_barre` | widget obj | packages/lvgl.yaml | — |
| `obj_barre_point_ha` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_barre_wifi_1` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_barre_wifi_2` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_barre_wifi_3` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_barre_wifi_4` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_maj` | widget obj | packages/acces_public.yaml | — |
| `obj_message` | widget obj | packages/message_accueil.yaml | — |
| `obj_nav` | widget obj | packages/lvgl.yaml | packages/pages/accueil.yaml |
| `obj_pla_bande` | widget obj | packages/pages/planning.yaml | — |
| `obj_pla_maintenant` | widget obj | packages/pages/planning.yaml | — |
| `obj_pla_point_2` | widget obj | packages/pages/planning.yaml | — |
| `obj_pla_point_3` | widget obj | packages/pages/planning.yaml | — |
| `obj_pla_point_4` | widget obj | packages/pages/planning.yaml | — |
| `obj_reg_impose` | widget obj | packages/pages/reglages.yaml | — |
| `page_accueil` | page LVGL | packages/pages/accueil.yaml | packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/lvgl.yaml |
| `page_apropos` | page LVGL | packages/lvgl.yaml | packages/hardware_jc4827w543.yaml, packages/pages/menu.yaml |
| `page_menu` | page LVGL | packages/pages/menu.yaml | packages/hardware_jc4827w543.yaml, packages/lvgl.yaml |
| `page_meteo` | page LVGL | packages/pages/meteo.yaml | packages/hardware_jc4827w543.yaml, packages/pages/menu.yaml |
| `page_planning` | page LVGL | packages/pages/planning.yaml | packages/hardware_jc4827w543.yaml, packages/pages/menu.yaml |
| `page_reglages` | page LVGL | packages/pages/reglages.yaml | packages/hardware_jc4827w543.yaml, packages/pages/menu.yaml |
| `page_scenarios` | page LVGL | packages/pages/scenarios.yaml | packages/hardware_jc4827w543.yaml, packages/pages/menu.yaml |
| `planning_rafraichir` | script | packages/pages/planning.yaml | packages/liaison_ha.yaml |
| `police_grande` | font | packages/pages/accueil.yaml | packages/pages/meteo.yaml |
| `police_icones` | font | packages/lvgl.yaml | packages/acces_public.yaml, packages/message_accueil.yaml, packages/pages/accueil.yaml, packages/pages/menu.yaml, packages/pages/reglages.yaml |
| `police_meteo` | font | packages/pages/meteo.yaml | — |
| `police_scenarios` | font | packages/pages/scenarios.yaml | — |
| `police_texte` | font | packages/lvgl.yaml | packages/acces_public.yaml, packages/message_accueil.yaml |
| `police_titre` | font | packages/lvgl.yaml | packages/acces_public.yaml, packages/message_accueil.yaml, packages/pages/accueil.yaml, packages/pages/meteo.yaml, packages/pages/planning.yaml |
| `reglage_impose_ecran_intensite` | globals | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `reglage_impose_led_alerte` | globals | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `reglage_impose_led_intensite` | globals | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `reglage_impose_led_mode` | globals | packages/led_veille.yaml | packages/liaison_ha.yaml, packages/pages/reglages.yaml |
| `reglages_rafraichir` | script | packages/pages/reglages.yaml | packages/led_veille.yaml, packages/liaison_ha.yaml |
| `retro_cible` | globals | packages/led_veille.yaml | — |
| `retro_cible_calculer` | script | packages/led_veille.yaml | — |
| `retro_niveau` | globals | packages/led_veille.yaml | — |
| `retroeclairage` | light (monochromatic) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `retroeclairage` | light (monochromatic) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `retroeclairage` | light (monochromatic) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml |
| `scenarios_indice` | globals | packages/pages/scenarios.yaml | — |
| `scenarios_lancer` | script | packages/pages/scenarios.yaml | — |
| `scenarios_rafraichir` | script | packages/pages/scenarios.yaml | packages/liaison_ha.yaml |
| `scenarios_retour` | globals | packages/pages/scenarios.yaml | packages/liaison_ha.yaml |
| `scenarios_retour_ms` | globals | packages/pages/scenarios.yaml | packages/liaison_ha.yaml |
| `signal_wifi` | sensor (wifi_signal) | packages/base.yaml | packages/pages/accueil.yaml |
| `sld_reg_ecran_intensite` | widget slider | packages/pages/reglages.yaml | — |
| `sld_reg_led_intensite` | widget slider | packages/pages/reglages.yaml | — |
| `sortie_led_bleu` | output (ledc) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_led_bleu` | output (ledc) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_led_bleu` | output (template) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_led_rouge` | output (ledc) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `sortie_led_rouge` | output (ledc) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml |
| `sortie_led_rouge` | output (template) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml |
| `sortie_led_vert` | output (ledc) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_led_vert` | output (ledc) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_led_vert` | output (template) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml, packages/pages/accueil.yaml |
| `sortie_retroeclairage` | output (ledc) | packages/hardware.yaml | packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml |
| `sortie_retroeclairage` | output (ledc) | packages/hardware_2432s028.yaml | packages/hardware.yaml, packages/hardware_jc4827w543.yaml |
| `sortie_retroeclairage` | output (ledc) | packages/hardware_jc4827w543.yaml | packages/hardware.yaml, packages/hardware_2432s028.yaml |
| `sw_reg_led` | widget switch | packages/pages/reglages.yaml | — |
| `sw_reg_led_alerte` | widget switch | packages/pages/reglages.yaml | — |
| `tactile` | touchscreen (cst816) | packages/hardware.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/hardware_2432s028.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/lvgl.yaml |
| `tactile` | touchscreen (xpt2046) | packages/hardware_2432s028.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/hardware.yaml, packages/hardware_jc4827w543.yaml, packages/led_veille.yaml, packages/lvgl.yaml |
| `tactile` | touchscreen (gt911) | packages/hardware_jc4827w543.yaml | hapanel_banc.yaml, hapanel_2432s028_banc.yaml, packages/hardware.yaml, packages/hardware_2432s028.yaml, packages/led_veille.yaml, packages/lvgl.yaml |
| `veille_reveiller` | script | packages/led_veille.yaml | packages/message_accueil.yaml |
