#pragma once

// Identite du build : source unique (invariant G5). Les valeurs sont
// injectees a la compilation par tools/version_build.py depuis VERSION et
// Git ; les valeurs par defaut ci-dessous ne servent que si le script n'a
// pas tourne (elles signalent alors un build non identifie).

#include <stdint.h>

#ifndef HAT_VERSION
#define HAT_VERSION "0.0.0-unknown"
#endif

#ifndef HAT_BUILD_NUMBER
#define HAT_BUILD_NUMBER "local"
#endif

#ifndef HAT_GIT_SHA
#define HAT_GIT_SHA "unknown"
#endif

#ifndef HAT_GIT_BRANCH
#define HAT_GIT_BRANCH "unknown"
#endif

#ifndef HAT_PIO_ENV
#define HAT_PIO_ENV "unknown"
#endif

namespace BuildInfo {
constexpr const char* PRODUCT = "HAThermostat";
constexpr const char* VERSION = HAT_VERSION;
constexpr const char* BUILD_NUMBER = HAT_BUILD_NUMBER;
constexpr const char* GIT_SHA = HAT_GIT_SHA;
constexpr const char* GIT_BRANCH = HAT_GIT_BRANCH;
constexpr const char* PIO_ENV = HAT_PIO_ENV;
constexpr const char* BUILD_DATE = __DATE__ " " __TIME__;
}
