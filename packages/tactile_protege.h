// Commandes protegees des touchers fantomes (D059, TODO T25) : etat du
// coupe-circuit et dernier toucher, partages par les pages qui envoient une
// commande a Home Assistant (accueil, scenarios) et par
// packages/tactile_protege.yaml (deblocage, alarme). Aucun id() ici : les
// fonctions sont appelees depuis les lambdas.
#pragma once

#include <cstdint>
#include "esphome/core/hal.h"
#include "esphome/core/log.h"

namespace hapanel {

struct Tactile {
  // Instants des dernieres commandes envoyees (0 : libre), en anneau.
  uint32_t envois[16] = {0};
  int suivant = 0;
  bool coupe = false;
  uint32_t coupe_ms = 0;
  // Dernier toucher : position, appui, relachement (0 : doigt encore pose).
  int x = -1, y = -1;
  uint32_t appui_ms = 0, relache_ms = 0;
};

inline Tactile &tactile() {
  static Tactile t;
  return t;
}

inline void tactile_appui(int x, int y) {
  auto &t = tactile();
  t.x = x;
  t.y = y;
  t.appui_ms = esphome::millis();
  t.relache_ms = 0;
}

inline void tactile_relache() { tactile().relache_ms = esphome::millis(); }

// Dernier contact avec l'ecran (appui ou relachement), pour le deblocage.
inline uint32_t tactile_dernier_ms() {
  auto &t = tactile();
  return t.relache_ms > t.appui_ms ? t.relache_ms : t.appui_ms;
}

inline bool tactile_coupe() { return tactile().coupe; }

inline void tactile_debloquer(const char *raison) {
  auto &t = tactile();
  if (!t.coupe) return;
  t.coupe = false;
  for (auto &e : t.envois) e = 0;
  ESP_LOGI("hapanel.tactile", "commandes retablies (%s)", raison);
}

// Vrai si la commande peut partir, et l'enregistre ; faux si les commandes
// sont coupees, ou si elle depasserait max commandes en fenetre_ms : coupe
// alors les commandes. Appelee en dernier dans la condition d'envoi, quand
// tout le reste l'autorise. Journal : commande, position et duree du toucher.
inline bool tactile_autoriser(const char *commande, int max, uint32_t fenetre_ms) {
  auto &t = tactile();
  uint32_t m = esphome::millis();
  uint32_t duree = (t.relache_ms ? t.relache_ms : m) - t.appui_ms;
  if (t.coupe) {
    ESP_LOGW("hapanel.tactile", "%s refusee : tactile instable", commande);
    return false;
  }
  if (max > 16) max = 16;
  int recents = 0;
  for (int i = 0; i < max; i++)
    if (t.envois[i] != 0 && m - t.envois[i] < fenetre_ms) recents++;
  if (recents >= max) {
    t.coupe = true;
    t.coupe_ms = m;
    ESP_LOGW("hapanel.tactile", "%s refusee : plus de %d commandes en %u s, commandes coupees", commande, max,
             (unsigned) (fenetre_ms / 1000));
    return false;
  }
  t.envois[t.suivant % max] = m ? m : 1;
  t.suivant = (t.suivant + 1) % max;
  ESP_LOGI("hapanel.tactile", "%s : toucher (%d, %d), %u ms, %d en %u s", commande, t.x, t.y, (unsigned) duree,
           recents + 1, (unsigned) (fenetre_ms / 1000));
  return true;
}

}  // namespace hapanel
