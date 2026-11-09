#!/usr/bin/env bash
# Construit la page d'installation par carte (D044), publiee sur GitHub Pages par
# .github/workflows/publication.yml pour les versions sans suffixe.
#
# Usage : tools/construire_page.sh <dossier des fichiers de la Release> <version> <dossier de sortie>
#
# Une page ne peut pas lire les fichiers d'une Release (GitHub ne l'autorise pas) :
# le binaire complet et le manifeste de chaque carte sont copies dans un dossier par
# carte, a cote de la page. Le manifeste lu par l'entite « Firmware » des modules
# reste dans la Release (adresse compilee dans les modules, D041).
#
# ESP Web Tools : version figee, empreinte verifiee, servi par la page elle-meme ;
# le navigateur de l'utilisateur ne charge rien d'un autre site (D044). Changer de
# version : nouvelle version et nouvelle empreinte (sha256 du .tgz de npm).
set -euo pipefail

EWT_VERSION=10.4.0
EWT_SHA256=f18da75335d2f0dca044c4bb052848c0696e7b03cc23d61d8530dd6eba0a9008

publication="$1"
version="$2"
site="$3"
racine="$(cd "$(dirname "$0")/.." && pwd)"

case "$version" in
  *[!0-9.]* | "") echo "Version $version : la page n'installe que des versions sans suffixe (D044)"; exit 1 ;;
esac

rm -rf "$site"
mkdir -p "$site/esp-web-tools"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
curl -fsSL -o "$tmp/ewt.tgz" "https://registry.npmjs.org/esp-web-tools/-/esp-web-tools-$EWT_VERSION.tgz"
echo "$EWT_SHA256  $tmp/ewt.tgz" | sha256sum -c -
tar xzf "$tmp/ewt.tgz" -C "$tmp"
cp "$tmp/package/dist/web/"*.js "$site/esp-web-tools/"
cp "$tmp/package/LICENSE" "$site/esp-web-tools/LICENSE"

# <carte> <manifeste dans la Release>
while read -r carte manifeste; do
  mkdir "$site/$carte"
  cp "$publication/hapanel-$carte-factory.bin" "$site/$carte/"
  # Effacement impose (D044, complement) : sans la question « Erase device », ESP
  # Web Tools efface toujours le module ; la case, decochee par defaut, s'oubliait.
  sed 's/"new_install_prompt_erase": true/"new_install_prompt_erase": false/' \
    "$publication/$manifeste" > "$site/$carte/manifest.json"
  grep -q "\"version\": \"$version\"" "$site/$carte/manifest.json" \
    || { echo "$manifeste : version differente de $version"; exit 1; }
  grep -q '"new_install_prompt_erase": false' "$site/$carte/manifest.json" \
    || { echo "$manifeste : effacement non impose"; exit 1; }
done <<'CARTES'
2432s024c manifest.json
2432s028 manifest-2432s028.json
jc4827w543 manifest-jc4827w543.json
CARTES

sed "s/@VERSION@/$version/g" "$racine/page/index.html" > "$site/index.html"
echo "Page construite dans $site (HAPanel $version, ESP Web Tools $EWT_VERSION)"
