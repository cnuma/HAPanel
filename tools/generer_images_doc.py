"""Genere les maquettes de docs/images a partir des positions et couleurs des
YAML de packages/pages. Ce sont des illustrations, pas des captures du module.

Depuis la racine du depot, apres une compilation (polices dans .esphome/font) :
    .venv/Scripts/python tools/generer_images_doc.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "docs" / "images"
POLICES = RACINE / ".esphome" / "font"
S = 2  # echelle de rendu

BLANC, GRIS, GRIS_FONCE, ORANGE = "#FFFFFF", "#9E9E9E", "#303030", "#FF9800"
BLEU, VERT, ROUGE = "#2196F3", "#4CAF50", "#F44336"
INACTIF = "#424242"

MDI = {
    "maison": "\U000F02DC", "manuel": "\U000F09DE", "horsgel": "\U000F0717", "eco": "\U000F032A",
    "confort": "\U000F04B9", "boost": "\U000F14DE", "sans_wifi": "\U000F05AA", "sans_ha": "\U000F0319",
    "meteo": "\U000F0595", "planning": "\U000F00F0", "scenarios": "\U000F0D19", "menu": "\U000F035C",
    "info": "\U000F02FD", "soleil": "\U000F0599", "pluie": "\U000F0597", "nuage": "\U000F0590",
    "canape": "\U000F04B9", "depart": "\U000F0A48", "lune": "\U000F0594", "lumiere_eteinte": "\U000F0E4F",
    "film": "\U000F0FCE", "reveil": "\U000F0020",
}


def police_mdi(taille):
    for chemin in POLICES.glob("*/font.ttf"):
        police = ImageFont.truetype(str(chemin), taille)
        if police.getmask(MDI["menu"]).getbbox():
            return police
    raise FileNotFoundError("Police d'icones absente : compiler d'abord le projet.")


def police(taille, graisse=400):
    return ImageFont.truetype(str(POLICES / f"Roboto@{graisse}@False@v1.ttf"), taille * S)


class Ecran:
    """Ecran de 240 x 320 du module, coordonnees en pixels du module."""

    def __init__(self, barre=True):
        self.image = Image.new("RGB", (240 * S, 320 * S), "#000000")
        self.d = ImageDraw.Draw(self.image)
        self.reperes = []
        if barre:
            self.rect(0, 276, 240, 44, "#212121")
            self.bouton(4, 280, 68, 36, BLEU)
            self.icone("maison", 38, 298, 24)
            self.bouton(76, 280, 160, 36, BLEU)
            self.icone("menu", 126, 298, 24)
            self.texte(170, 298, "Menu", BLANC, 22, 500, "mm")

    def rect(self, x, y, l, h, couleur, rayon=0, bord=None, epaisseur=0):
        boite = [x * S, y * S, (x + l) * S - 1, (y + h) * S - 1]
        self.d.rounded_rectangle(boite, rayon * S, fill=couleur, outline=bord, width=epaisseur * S)

    def bouton(self, x, y, l, h, couleur=BLEU, bord=None, epaisseur=0):
        self.rect(x, y, l, h, couleur, 8, bord, epaisseur)

    def texte(self, x, y, texte, couleur=BLANC, taille=16, graisse=400, ancre="la"):
        self.d.text((x * S, y * S), texte, fill=couleur, font=police(taille, graisse), anchor=ancre)

    def multi(self, x, y, texte, couleur=BLANC, taille=16):
        self.d.multiline_text((x * S, y * S), texte, fill=couleur, font=police(taille), anchor="mm",
                              align="center", spacing=2 * S)

    def icone(self, nom, x, y, taille=24, couleur=BLANC):
        self.d.text((x * S, y * S), MDI[nom], fill=couleur, font=police_mdi(taille * S), anchor="mm")

    def repere(self, numero, x, y):
        self.reperes.append((numero, x, y))

    def finir(self, nom):
        return encadrer(self, nom)


def encadrer(ecran, nom=None):
    """Ajoute le cadre du module et les reperes numerotes."""
    marge = 14 * S
    image = Image.new("RGB", (ecran.image.width + 2 * marge, ecran.image.height + 2 * marge), "#FFFFFF")
    d = ImageDraw.Draw(image)
    d.rounded_rectangle([0, 0, image.width - 1, image.height - 1], 14 * S, fill="#16181C")
    image.paste(ecran.image, (marge, marge))
    for numero, x, y in ecran.reperes:
        cx, cy = marge + x * S, marge + y * S
        d.ellipse([cx - 10 * S, cy - 10 * S, cx + 10 * S, cy + 10 * S], fill="#FFEB3B", outline="#000000", width=S)
        d.text((cx, cy), str(numero), fill="#000000", font=police(13, 500), anchor="mm")
    if nom:
        image.save(SORTIE / nom, optimize=True)
    return image


def cote_a_cote(images, nom, legendes):
    h_legende = 34 * S
    espace = 18 * S
    largeur = sum(i.width for i in images) + espace * (len(images) - 1)
    hauteur = images[0].height + h_legende
    sortie = Image.new("RGB", (largeur, hauteur), "#FFFFFF")
    d = ImageDraw.Draw(sortie)
    x = 0
    for image, legende in zip(images, legendes):
        sortie.paste(image, (x, 0))
        d.text((x + image.width // 2, images[0].height + 18 * S), legende, fill="#20242A",
               font=police(15, 500), anchor="mm")
        x += image.width + espace
    sortie.save(SORTIE / nom, optimize=True)


def bandeau(e, ha=True):
    e.texte(8, 6, "dim. 1 nov.  14:32")
    for i, (x, y, h) in enumerate([(186, 18, 4), (192, 15, 7), (198, 12, 10), (204, 9, 13)]):
        e.rect(x, y, 4, h, BLANC if ha and i < 3 else INACTIF)
    e.rect(218, 9, 13, 13, VERT if ha else ROUGE, 7)


def glissiere(e, chauffage=True):
    e.rect(12, 226, 216, 40, GRIS_FONCE, 20)
    e.rect(120 if chauffage else 12, 226, 108, 40, ORANGE, 20)
    e.texte(66, 246, "Éteint", BLANC if not chauffage else GRIS, 16, 400, "mm")
    e.texte(174, 246, "Chauffage", BLANC if chauffage else GRIS, 16, 400, "mm")


def accueil():
    e = Ecran()
    bandeau(e)
    e.texte(12, 32, "Séjour")
    e.texte(120, 46, "20,5 °C", BLANC, 48, 500, "ma")
    e.texte(12, 102, "Extérieur 8,5 °C")
    prereglages = [("manuel", "#AB47BC", 12), ("horsgel", "#42A5F5", 56), ("eco", "#66BB6A", 100),
                   ("confort", ORANGE, 144), ("boost", ROUGE, 188)]
    for nom, couleur, x in prereglages:
        e.rect(x, 126, 40, 40, GRIS_FONCE, 8, BLANC if nom == "eco" else None, 3 if nom == "eco" else 0)
        e.icone(nom, x + 20, 146, 24, couleur)
    e.bouton(12, 174, 56, 44, "#1E88E5")
    e.texte(40, 196, "-", BLANC, 22, 500, "mm")
    e.texte(120, 196, "19,0 °C", BLANC, 22, 500, "mm")
    e.bouton(172, 174, 56, 44, "#E53935")
    e.texte(200, 196, "+", BLANC, 22, 500, "mm")
    glissiere(e)
    for numero, x, y in [(1, 148, 15), (2, 226, 62), (3, 180, 110), (4, 232, 146), (5, 76, 196),
                         (6, 120, 246), (7, 38, 276), (8, 214, 276)]:
        e.repere(numero, x, y)
    e.finir("accueil.png")
    return e


def accueil_eteint():
    e = Ecran()
    bandeau(e)
    e.texte(12, 32, "Séjour")
    e.texte(120, 46, "20,5 °C", BLANC, 48, 500, "ma")
    e.texte(12, 102, "Extérieur 8,5 °C")
    glissiere(e, False)
    return encadrer(e)


def accueil_hs(wifi):
    e = Ecran()
    e.texte(8, 6, "dim. 1 nov.  14:32")
    for x, y, h in [(186, 18, 4), (192, 15, 7), (198, 12, 10), (204, 9, 13)]:
        e.rect(x, y, 4, h, BLANC if wifi else INACTIF)
    e.rect(218, 9, 13, 13, ROUGE, 7)
    e.icone("sans_ha" if wifi else "sans_wifi", 120, 130, 24, ROUGE)
    e.multi(120, 170, "Pas de communication\navec Home Assistant" if wifi else "Pas de Wi-Fi")
    return encadrer(e)


def menu():
    e = Ecran()
    tuiles = [("maison", "Accueil", 8, 8), ("meteo", "Météo", 124, 8), ("planning", "Planning", 8, 96),
              ("scenarios", "Scénarios", 124, 96), ("info", "À propos", 8, 184)]
    for nom, texte, x, y in tuiles:
        e.bouton(x, y, 108, 80)
        e.icone(nom, x + 54, y + 24, 24)
        e.texte(x + 54, y + 58, texte, BLANC, 16, 400, "mm")
    e.finir("menu.png")


def meteo():
    e = Ecran()
    e.texte(8, 6, "Météo")
    e.icone("nuage", 28, 56, 32)
    e.texte(228, 26, "12,5°", BLANC, 48, 500, "ra")
    e.texte(12, 82, "Nuageux")
    for y, jour, icone, temp in [(124, "lun.", "soleil", "14° / 6°"), (176, "mar.", "nuage", "12° / 7°"),
                                 (228, "mer.", "pluie", "10° / 5°")]:
        e.texte(12, y, jour)
        e.icone(icone, 92, y + 8, 32)
        e.texte(228, y - 4, temp, BLANC, 22, 500, "ra")
    e.finir("meteo.png")


def planning():
    e = Ecran()
    e.texte(12, 8, "Aujourd'hui")
    e.texte(228, 8, "14:32", GRIS, 16, 400, "ra")
    e.texte(12, 36, "Maison", GRIS)
    e.texte(12, 58, "Prévu jusqu'à 22:00", ORANGE, 22, 500)
    e.rect(12, 92, 216, 18, GRIS_FONCE, 6)
    e.rect(66, 92, 23, 18, ORANGE, 6)
    e.rect(138, 92, 72, 18, ORANGE, 6)
    e.rect(12 + 87 * 3 // 2 - 1, 88, 2, 26, BLANC)
    for x, t, ancre in [(12, "0", "la"), (66, "6", "ma"), (120, "12", "ma"), (174, "18", "ma"), (228, "24", "ra")]:
        e.texte(x, 114, t, GRIS, 16, 400, ancre)
    lignes = [(144, "Salon", "17:00 - 21:00", False), (184, "Chambre", "14:00 - 16:00", True),
              (224, "Atelier", "terminé", False)]
    for y, nom, horaire, actif in lignes:
        e.rect(12, y + 6, 8, 8, ORANGE if actif else INACTIF, 4)
        e.texte(28, y, nom)
        e.texte(228, y, horaire, ORANGE if actif else GRIS, 16, 400, "ra")
    e.finir("planning.png")


def scenarios_ecran(etat="", couleur=ORANGE, attente=False, noms=None):
    e = Ecran()
    e.texte(12, 6, "Scénarios")
    e.texte(12, 28, etat, couleur)
    noms = noms if noms is not None else [("Soirée", "canape", "#6A1B9A"), ("Je pars", "depart", "#2E7D32"), ("Nuit", "lune", "#1976D2"),
                                          ("Tout éteindre", "lumiere_eteinte", "#C62828"), ("Film", "film", "#00838F"), ("Réveil", "reveil", "#E65100")]
    position = [(8, 52), (124, 52), (8, 126), (124, 126), (8, 200), (124, 200)]
    for (x, y), (nom, icone, couleur) in zip(position, noms):
        e.bouton(x, y, 108, 68, "#3A3A3A" if attente else couleur)
        e.icone(icone, x + 54, y + 21, 24, GRIS if attente else BLANC)
        e.multi(x + 54, y + 49, nom, GRIS if attente else BLANC)
    return e


def apropos():
    e = Ecran()
    e.texte(120, 12, "À propos", BLANC, 22, 500, "ma")
    e.texte(12, 60, "HAPanel 0.6.0-dev")
    e.texte(12, 88, "SHA 3e880f3")
    e.texte(12, 128, "Home Assistant : connecté", VERT)
    e.texte(12, 168, "Mémoire : 162 Ko libres,")
    e.texte(12, 188, "plus grand bloc 108 Ko")
    e.finir("apropos.png")


def schema_scenario():
    """Trajet d'un toucher, du panneau au scenario."""
    image = Image.new("RGB", (1180, 330), "#FFFFFF")
    d = ImageDraw.Draw(image)
    boites = [(20, "HAPanel", "Bouton touché :\nenvoie son numéro", "#E3F2FD"),
              (420, "Blueprint du module", "Trouve l'entité du numéro,\nvérifie qu'elle est disponible", "#FFF3E0"),
              (820, "Home Assistant", "Exécute la scène,\nle script ou l'automatisation", "#E8F5E9")]
    for x, titre, texte, fond in boites:
        d.rounded_rectangle([x, 40, x + 340, 230], 18, fill=fond, outline="#607D8B", width=2)
        d.text((x + 170, 86), titre, fill="#20242A", font=ImageFont.truetype(str(POLICES / "Roboto@500@False@v1.ttf"), 30), anchor="mm")
        d.multiline_text((x + 170, 160), texte, fill="#20242A", font=ImageFont.truetype(str(POLICES / "Roboto@400@False@v1.ttf"), 25), anchor="mm", align="center", spacing=8)
    for x in (360, 760):
        d.line([(x + 4, 135), (x + 52, 135)], fill="#20242A", width=4)
        d.polygon([(x + 60, 135), (x + 46, 126), (x + 46, 144)], fill="#20242A")
    d.line([(590, 230), (590, 285), (190, 285), (190, 238)], fill="#2E7D32", width=4)
    d.polygon([(190, 232), (181, 246), (199, 246)], fill="#2E7D32")
    d.text((590, 307), "Réponse à l'écran : « Lancé : nom » ou « Refusé par HA » ; rien après 10 s : « Pas de réponse de HA »", fill="#2E7D32",
           font=ImageFont.truetype(str(POLICES / "Roboto@400@False@v1.ttf"), 21), anchor="mm")
    image.save(SORTIE / "schema_scenario.png", optimize=True)


def formulaire():
    """Illustration du formulaire de l'automatisation dans Home Assistant."""
    f = lambda t, g=400: ImageFont.truetype(str(POLICES / f"Roboto@{g}@False@v1.ttf"), t)
    image = Image.new("RGB", (900, 700), "#F5F6F8")
    d = ImageDraw.Draw(image)
    d.rounded_rectangle([20, 20, 880, 680], 14, fill="#FFFFFF", outline="#D5D9DE", width=2)
    d.text((48, 42), "HAPanel — module", fill="#20242A", font=f(34, 500))
    d.text((48, 90), "Maquette : l'affichage réel dépend de la version de Home Assistant", fill="#667085", font=f(21))
    y = 136
    for titre in ["Panneau, thermomètres, thermostat, météo, calendriers"]:
        d.rounded_rectangle([48, y, 852, y + 54], 8, fill="#F1F3F5")
        d.text((68, y + 27), titre, fill="#667085", font=f(23), anchor="lm")
    y = 206
    d.text((48, y), "Scénarios", fill="#20242A", font=f(27, 500))
    y += 50
    champs = [("Scénario 1", "scene.soiree_salon", "Nom du bouton 1", "Soirée"),
              ("Icône du bouton 1", "Canapé", "Couleur du bouton 1", "Violet"),
              ("Scénario 2", "script.depart_maison", "Nom du bouton 2", "(vide : nom de l'entité)")]
    for titre, valeur, titre_nom, nom in champs:
        for x, largeur, t, v, vide in [(48, 470, titre, valeur, False), (534, 318, titre_nom, nom, nom.startswith("("))]:
            d.rounded_rectangle([x, y, x + largeur, y + 84], 8, fill="#FFFFFF", outline="#98A2B3", width=2)
            d.text((x + 16, y + 12), t, fill="#667085", font=f(19))
            d.text((x + 16, y + 42), v, fill="#98A2B3" if vide else "#20242A", font=f(23))
        y += 100
    d.text((48, y + 8), "… jusqu'à Scénario 6 et Nom du bouton 6", fill="#667085", font=f(23))
    d.rounded_rectangle([660, 604, 852, 660], 8, fill="#03A9F4")
    d.text((756, 632), "Enregistrer", fill="#FFFFFF", font=f(24, 500), anchor="mm")
    image.save(SORTIE / "formulaire_blueprint.png", optimize=True)


def led():
    """Couleurs de la LED selon le prereglage."""
    lignes = [("Manuel", "#D500F9"), ("Hors-gel", "#2979FF"), ("Éco", "#00E676"), ("Confort", "#FFB300"),
              ("Boost", "#FF1744"), ("Préréglage inconnu", "#F5F5F5")]
    f = ImageFont.truetype(str(POLICES / "Roboto@400@False@v1.ttf"), 24)
    image = Image.new("RGB", (900, 210), "#16181C")
    d = ImageDraw.Draw(image)
    for i, (nom, couleur) in enumerate(lignes):
        x = 40 + (i % 3) * 290
        y = 50 + (i // 3) * 110
        d.ellipse([x, y - 22, x + 44, y + 22], fill=couleur)
        d.text((x + 58, y), nom, fill="#FFFFFF", font=f, anchor="lm")
    image.save(SORTIE / "led.png", optimize=True)


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    accueil()
    cote_a_cote([accueil_eteint(), accueil_hs(True), accueil_hs(False)], "accueil_etats.png",
                ["Chauffage éteint", "Home Assistant injoignable", "Wi-Fi coupé"])
    menu()
    meteo()
    planning()
    encadrer(scenarios_ecran(), "scenarios.png")
    cote_a_cote([encadrer(scenarios_ecran("Envoi en cours", ORANGE, True)),
                 encadrer(scenarios_ecran("Lancé : Soirée", VERT)),
                 encadrer(scenarios_ecran("Pas de réponse de HA", ORANGE))],
                "scenarios_etats.png", ["Envoi", "Accepté par HA", "Sans réponse"])
    apropos()
    schema_scenario()
    formulaire()
    led()
    for f in sorted(SORTIE.glob("*.png")):
        print(f.name, f.stat().st_size // 1024, "Ko")


main()
