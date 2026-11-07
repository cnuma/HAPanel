"""HAPanel : index des identifiants du YAML et controle de docs/technique (G12).

Lit hapanel.yaml, hapanel_banc.yaml, hapanel_public.yaml et packages/, puis :
- ecrit docs/technique/INDEX_IDS.md : chaque id, son type, son fichier et les
  fichiers qui l'utilisent ;
- verifie que chaque id et chaque substitution d'un fichier YAML documente
  apparait, entre accents graves, dans sa page de docs/technique.

Un fichier YAML sans page n'est pas controle : la documentation se construit
page par page. Depuis la racine du depot :

    .venv\\Scripts\\python tools\\verifier_doc_technique.py             (index + rapport)
    .venv\\Scripts\\python tools\\verifier_doc_technique.py --verifier  (code 1 si ecart)
"""
import re
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
DOC = RACINE / "docs" / "technique"
INDEX = DOC / "INDEX_IDS.md"


class Chargeur(yaml.SafeLoader):
    """Accepte les etiquettes d'ESPHome (!include, !extend, !secret, !lambda)."""


class Etiquette(str):
    def __new__(cls, valeur, tag):
        s = super().__new__(cls, valeur)
        s.tag = tag
        return s


def _etiquette(chargeur, suffixe, noeud):
    if isinstance(noeud, yaml.ScalarNode):
        return Etiquette(chargeur.construct_scalar(noeud), "!" + suffixe)
    if isinstance(noeud, yaml.SequenceNode):
        return chargeur.construct_sequence(noeud)
    return chargeur.construct_mapping(noeud)


Chargeur.add_multi_constructor("!", _etiquette)


def fichiers_yaml():
    yield RACINE / "hapanel.yaml"
    yield RACINE / "hapanel_banc.yaml"
    yield RACINE / "hapanel_public.yaml"
    yield RACINE / "hapanel_2432s028_banc.yaml"
    yield RACINE / "hapanel_2432s028_public.yaml"
    yield from sorted((RACINE / "packages").rglob("*.yaml"))


def page_de(fichier):
    """Page de docs/technique qui documente ce fichier YAML."""
    rel = fichier.relative_to(RACINE)
    if rel.parts[0] != "packages":
        return DOC / "hapanel.md"  # hapanel.yaml, hapanel_banc.yaml, hapanel_public.yaml...
    return DOC.joinpath(*rel.parts[1:]).with_suffix(".md")


def dans_une_action(chemin):
    """Un id sous une action (script.execute, then, on_click...) est une reference."""
    return any(isinstance(c, str) and ("." in c or c in ("then", "else") or c.startswith("on_"))
               for c in chemin)


def parcourir(noeud, chemin, sortie):
    """Collecte (id, type) : le type vient de la cle parente et de platform."""
    if isinstance(noeud, dict):
        ident = noeud.get("id")
        if (isinstance(ident, str) and getattr(ident, "tag", None) != "!extend"
                and not dans_une_action(chemin)):
            cles = [c for c in chemin if isinstance(c, str)]
            racine = cles[0] if cles else "?"
            parent = cles[-1] if cles else "?"
            if "platform" in noeud:
                genre = f"{racine} ({noeud['platform']})"
            elif racine == "lvgl":
                genre = "page LVGL" if parent == "pages" else f"widget {parent}"
            elif parent != racine:
                genre = f"{racine} ({parent})"
            else:
                genre = racine
            sortie.append((str(ident), genre))
        for cle, valeur in noeud.items():
            parcourir(valeur, chemin + [cle], sortie)
    elif isinstance(noeud, list):
        for i, valeur in enumerate(noeud):
            parcourir(valeur, chemin + [i], sortie)


def main():
    textes, declares, substitutions = {}, [], {}
    for fichier in fichiers_yaml():
        texte = fichier.read_text(encoding="utf-8")
        textes[fichier] = texte
        contenu = yaml.load(texte, Loader=Chargeur) or {}
        trouves = []
        parcourir(contenu, [], trouves)
        declares += [(ident, genre, fichier) for ident, genre in trouves]
        substitutions[fichier] = list((contenu.get("substitutions") or {}).keys())

    def rel(f):
        return f.relative_to(RACINE).as_posix()

    lignes = ["# Index des identifiants du YAML", "",
              "Fichier généré par `tools/verifier_doc_technique.py` : ne pas le modifier à la main.",
              "Relancer le script après toute modification du YAML.", "",
              "| id | Type | Déclaré dans | Utilisé aussi dans |", "|---|---|---|---|"]
    for ident, genre, fichier in sorted(declares, key=lambda d: d[0]):
        motif = re.compile(rf"\b{re.escape(ident)}\b")
        autres = [rel(f) for f, t in textes.items() if f != fichier and motif.search(t)]
        lignes.append(f"| `{ident}` | {genre} | {rel(fichier)} | {', '.join(autres) or '—'} |")
    nouvel_index = "\n".join(lignes) + "\n"
    ancien_index = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""

    ecarts, couverts, non_couverts = [], 0, 0
    for fichier in textes:
        page = page_de(fichier)
        if not page.exists():
            continue
        doc = page.read_text(encoding="utf-8")
        attendus = [i for i, _, f in declares if f == fichier] + substitutions[fichier]
        for nom in attendus:
            if f"`{nom}`" in doc or f"`${{{nom}}}`" in doc:
                couverts += 1
            else:
                non_couverts += 1
                ecarts.append(f"{rel(fichier)} : `{nom}` absent de {page.relative_to(RACINE).as_posix()}")
    sans_page = sorted({rel(f) for f in textes if not page_de(f).exists()})

    if "--verifier" in sys.argv:
        if nouvel_index != ancien_index:
            ecarts.insert(0, "INDEX_IDS.md n'est pas à jour : relancer le script sans --verifier")
    else:
        DOC.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(nouvel_index, encoding="utf-8")
        print(f"Index : {len(declares)} identifiants -> {INDEX.relative_to(RACINE).as_posix()}")

    print(f"Documentés : {couverts} ; manquants : {non_couverts}")
    if sans_page:
        print("Fichiers sans page (non contrôlés) : " + ", ".join(sans_page))
    for e in ecarts:
        print("  " + e)
    return 1 if ecarts and "--verifier" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
