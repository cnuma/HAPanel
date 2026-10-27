# Identite de build HAThermostat (source unique, invariant G5).
#
# Repris du socle AquaLook (tools/version_build.py, commit d34ef52), sans la
# partie cible OTA propre a AquaLook. Declare dans platformio.ini par :
#     extra_scripts = pre:tools/version_build.py
# Injecte HAT_VERSION, HAT_BUILD_NUMBER, HAT_GIT_SHA, HAT_GIT_BRANCH et
# HAT_PIO_ENV, lus par include/BuildInfo.h.

Import("env")

from pathlib import Path
import re
import subprocess


VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")

# Chemins qui entrent dans le binaire. Un binaire compile avec du code non
# commite porterait sinon le SHA du commit de base, identique a celui du
# binaire propre (constate sur AquaLook le 15 oct. 2026) : le suffixe
# "+modif" le rend visible partout ou le SHA s'affiche.
FIRMWARE_PATHS = (
    "src",
    "include",
    "lib",
    "platformio.ini",
    "VERSION",
    "tools/version_build.py",
)
DIRTY_SUFFIX = "+modif"


def git_value(args, fallback):
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=env.subst("$PROJECT_DIR"),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return fallback


def firmware_sources_modified():
    # Fichiers suivis modifies ET fichiers nouveaux non suivis.
    status = git_value(
        ["status", "--porcelain", "--untracked-files=all", "--", *FIRMWARE_PATHS],
        "",
    )
    return status != ""


def read_version(project_dir):
    version_path = Path(project_dir) / "VERSION"
    version = version_path.read_text(encoding="utf-8").strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Invalid HAThermostat VERSION value: {version!r}")
    return version


project_dir = env.subst("$PROJECT_DIR")
version = read_version(project_dir)
build_number = git_value(["rev-list", "--count", "HEAD"], "local")
git_sha = git_value(["rev-parse", "--short=7", "HEAD"], "unknown")
if git_sha != "unknown" and firmware_sources_modified():
    git_sha += DIRTY_SUFFIX
git_branch = git_value(["rev-parse", "--abbrev-ref", "HEAD"], "unknown")
pio_environment = env.subst("$PIOENV")

env.Append(
    CPPDEFINES=[
        ("HAT_VERSION", f'\\"{version}\\"'),
        ("HAT_BUILD_NUMBER", f'\\"{build_number}\\"'),
        ("HAT_GIT_SHA", f'\\"{git_sha}\\"'),
        ("HAT_GIT_BRANCH", f'\\"{git_branch}\\"'),
        ("HAT_PIO_ENV", f'\\"{pio_environment}\\"'),
    ]
)

print(
    f"[BuildInfo] HAThermostat {version} build {build_number} "
    f"sha {git_sha} branch {git_branch} env {pio_environment}"
)
