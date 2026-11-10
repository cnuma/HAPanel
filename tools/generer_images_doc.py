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
VIOLET = "#AB47BC"
INACTIF = "#424242"

MDI = {
    "maison": "\U000F02DC", "manuel": "\U000F09DE", "horsgel": "\U000F0717", "eco": "\U000F032A",
    "confort": "\U000F04B9", "boost": "\U000F14DE", "sans_wifi": "\U000F05AA", "sans_ha": "\U000F0319",
    "meteo": "\U000F0595", "planning": "\U000F00F0", "scenarios": "\U000F0D19", "menu": "\U000F035C",
    "info": "\U000F02FD", "soleil": "\U000F0599", "pluie": "\U000F0597", "nuage": "\U000F0590",
    "canape": "\U000F04B9", "depart": "\U000F0A48", "lune": "\U000F0594", "lumiere_eteinte": "\U000F0E4F",
    "film": "\U000F0FCE", "reveil": "\U000F0020", "reglages": "\U000F0493", "verrou": "\U000F033E", "disquette": "\U000F0193",
    "maj": "\U000F005F",
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
    """Ecran du module, coordonnees en pixels du module : 240 x 320 (portrait), ou
    480 x 272 (paysage, maquettes de T04)."""

    def __init__(self, titre=None, maison=True, menu=True, wifi=True, ha=True, disquette=None,
                 largeur=240, hauteur=320):
        """Barre d'etat en haut (D036) : bouton Menu (masque sur le menu), titre, ou date et
        heure sur l'accueil (titre None), disquette, Wi-Fi et connexion a HA. En bas,
        maison centree, sans barre sur l'accueil (D025 revisee)."""
        self.largeur, self.hauteur = largeur, hauteur
        dx = largeur - 240  # elements de droite de la barre, cales sur le bord droit
        self.image = Image.new("RGB", (largeur * S, hauteur * S), "#000000")
        self.d = ImageDraw.Draw(self.image)
        self.reperes = []
        self.rect(0, 0, largeur, 36, "#212121")
        if menu:
            self.icone("menu", 22, 18, 24)
        self.texte(52, 9, titre if titre else "1 nov.  14:32")
        if disquette:
            self.icone("disquette", 172 + dx, 18, 24, disquette)
        for i, (x, y, h) in enumerate([(192, 21, 4), (198, 18, 7), (204, 15, 10), (210, 12, 13)]):
            self.rect(x + dx, y, 4, h, BLANC if wifi and i < 3 else INACTIF)
        self.rect(220 + dx, 12, 13, 13, VERT if ha else ROUGE, 7)
        if maison:
            self.rect(0, hauteur - 44, largeur, 44, "#212121")
            self.bouton(largeur // 2 - 34, hauteur - 40, 68, 36, BLEU)
            self.icone("maison", largeur // 2, hauteur - 22, 24)

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


# Accueil reparti sur toute la hauteur, la bande du bas etant libre (T16) :
# valeurs de packages/format_portrait.yaml (fmt_acc_...).
ACC_PIECE_Y, ACC_TEMP_Y, ACC_LIGNE_Y, ACC_PRE_Y = 44, 62, 124, 152
ACC_BTN_Y, ACC_BTN_H, ACC_GL_Y, ACC_GL_H = 206, 48, 266, 48


def glissiere(e, chauffage=True):
    milieu = ACC_GL_Y + ACC_GL_H // 2
    e.rect(12, ACC_GL_Y, 216, ACC_GL_H, GRIS_FONCE, ACC_GL_H // 2)
    e.rect(120 if chauffage else 12, ACC_GL_Y, 108, ACC_GL_H, ORANGE, ACC_GL_H // 2)
    e.texte(66, milieu, "Éteint", BLANC if not chauffage else GRIS, 16, 400, "mm")
    e.texte(174, milieu, "Chauffage", BLANC if chauffage else GRIS, 16, 400, "mm")


def accueil_haut(e):
    e.texte(12, ACC_PIECE_Y, "Séjour")
    e.texte(120, ACC_TEMP_Y, "20,5 °C", BLANC, 48, 500, "ma")
    e.texte(12, ACC_LIGNE_Y, "Extérieur 8,5 °C")


def accueil():
    e = Ecran(maison=False)
    accueil_haut(e)
    prereglages = [("manuel", "#AB47BC", 12), ("horsgel", "#42A5F5", 56), ("eco", "#66BB6A", 100),
                   ("confort", ORANGE, 144), ("boost", ROUGE, 188)]
    for nom, couleur, x in prereglages:
        e.rect(x, ACC_PRE_Y, 40, 40, GRIS_FONCE, 8, BLANC if nom == "eco" else None, 3 if nom == "eco" else 0)
        e.icone(nom, x + 20, ACC_PRE_Y + 20, 24, couleur)
    milieu = ACC_BTN_Y + ACC_BTN_H // 2
    e.bouton(12, ACC_BTN_Y, 56, ACC_BTN_H, "#1E88E5")
    e.texte(40, milieu, "-", BLANC, 22, 500, "mm")
    e.texte(120, milieu, "19,0 °C", BLANC, 22, 500, "mm")
    e.bouton(172, ACC_BTN_Y, 56, ACC_BTN_H, "#E53935")
    e.texte(200, milieu, "+", BLANC, 22, 500, "mm")
    glissiere(e)
    for numero, x, y in [(1, 150, 18), (2, 42, 32), (3, 226, ACC_TEMP_Y + 16), (4, 180, ACC_LIGNE_Y + 8),
                         (5, 232, ACC_PRE_Y + 20), (6, 76, milieu), (7, 120, ACC_GL_Y - 8)]:
        e.repere(numero, x, y)
    e.finir("accueil.png")
    return e


def accueil_eteint():
    e = Ecran(maison=False)
    accueil_haut(e)
    glissiere(e, False)
    return encadrer(e)


def accueil_hs(wifi):
    e = Ecran(maison=False, wifi=wifi, ha=False)
    e.icone("sans_ha" if wifi else "sans_wifi", 120, 138, 24, ROUGE)
    e.multi(120, 178, "Pas de communication\navec Home Assistant" if wifi else "Pas de Wi-Fi")
    return encadrer(e)


def menu():
    e = Ecran("Menu", menu=False)
    tuiles = [("meteo", "Météo", 8, 40), ("planning", "Planning", 124, 40), ("scenarios", "Scénarios", 8, 118),
              ("reglages", "Réglages", 124, 118), ("info", "À propos", 8, 196)]
    for nom, texte, x, y in tuiles:
        e.bouton(x, y, 108, 72)
        e.icone(nom, x + 54, y + 22, 24)
        e.texte(x + 54, y + 54, texte, BLANC, 16, 400, "mm")
    # Tuile de mise a jour (D047), seulement quand une mise a jour attend.
    e.bouton(124, 196, 108, 72, VIOLET)
    e.icone("maj", 124 + 54, 196 + 22, 24)
    e.texte(124 + 54, 196 + 54, "Mise à jour", BLANC, 16, 400, "mm")
    e.finir("menu.png")


def interrupteur(e, y, libelle, actif, impose):
    """Interrupteur de packages/pages/reglages.yaml : arret sur fond sombre borde."""
    e.texte(12, y + 6, libelle)
    if actif:
        e.rect(172, y, 56, 30, "#546E7A" if impose else BLEU, 15)
    else:
        e.rect(172, y, 56, 30, GRIS_FONCE, 15, GRIS, 2)
    e.rect(201 if actif else 175, y + 3, 24, 24, "#BDBDBD" if impose else BLANC, 12)
    if impose:
        e.icone("verrou", 152, y + 15, 24, GRIS)


def curseur(e, y, libelle, valeur, minimum, impose):
    """Curseur par pas de 5 et valeur affichee a droite, 28 px sous le libelle."""
    e.texte(12, y, libelle)
    e.texte(228, y, f"{valeur} %", BLANC, 16, 400, "ra")
    plein = round(196 * (valeur - minimum) / (100 - minimum))
    couleur = "#546E7A" if impose else BLEU
    e.rect(22, y + 28, 196, 10, "#123C5E", 5)
    e.rect(22, y + 28, max(plein, 10), 10, couleur, 5)
    e.rect(22 + plein - 10, y + 23, 20, 20, couleur, 10)
    if impose:
        e.icone("verrou", 162, y + 8, 24, GRIS)


def reglages_ecran(alerte=True, impose_alerte=False, disquette=None):
    e = Ecran("Réglages", disquette=disquette)
    # Positions de packages/format_portrait.yaml (fmt_reg_...), cinq rangees (T13).
    interrupteur(e, 40, "LED", True, False)
    curseur(e, 76, "Intensité LED", 20, 0, False)
    interrupteur(e, 124, "Alerte LED", alerte, impose_alerte)
    curseur(e, 160, "Intensité écran", 80, 20, False)
    curseur(e, 208, "Intensité message", 100, 20, False)
    if impose_alerte:
        e.icone("verrou", 68, 264, 24, GRIS)
        e.texte(84, 264, "imposé par HA", GRIS, 16, 400, "lm")
    return e


def reglages():
    e = reglages_ecran(disquette=VERT)
    for numero, x, y in [(1, 140, 55), (2, 140, 84), (3, 140, 139), (4, 150, 168), (6, 160, 216),
                         (5, 150, 18)]:
        e.repere(numero, x, y)
    e.finir("reglages.png")
    cote_a_cote([encadrer(reglages_ecran(alerte=False)), encadrer(reglages_ecran(impose_alerte=True))],
                "reglages_etats.png", ["Alerte LED arrêtée", "Alerte LED imposée par HA"])


def meteo():
    e = Ecran("Météo")
    e.icone("nuage", 28, 88, 32)
    e.texte(228, 58, "12,5°", BLANC, 48, 500, "ra")
    e.texte(12, 114, "Nuageux")
    for y, jour, icone, temp in [(152, "lun.", "soleil", "14° / 6°"), (198, "mar.", "nuage", "12° / 7°"),
                                 (244, "mer.", "pluie", "10° / 5°")]:
        e.texte(12, y, jour)
        e.icone(icone, 92, y + 8, 32)
        e.texte(228, y - 4, temp, BLANC, 22, 500, "ra")
    e.finir("meteo.png")


def planning():
    e = Ecran("Planning")
    e.texte(12, 38, "Aujourd'hui")
    e.texte(228, 38, "14:32", GRIS, 16, 400, "ra")
    e.texte(12, 66, "Maison", GRIS)
    e.texte(12, 88, "Prévu jusqu'à 22:00", ORANGE, 22, 500)
    e.rect(12, 122, 216, 18, GRIS_FONCE, 6)
    e.rect(66, 122, 23, 18, ORANGE, 6)
    e.rect(138, 122, 72, 18, ORANGE, 6)
    e.rect(12 + 87 * 3 // 2 - 1, 118, 2, 26, BLANC)
    for x, t, ancre in [(12, "0", "la"), (66, "6", "ma"), (120, "12", "ma"), (174, "18", "ma"), (228, "24", "ra")]:
        e.texte(x, 144, t, GRIS, 16, 400, ancre)
    lignes = [(174, "Salon", "17:00 - 21:00", False), (214, "Chambre", "14:00 - 16:00", True),
              (254, "Atelier", "terminé", False)]
    for y, nom, horaire, actif in lignes:
        e.rect(12, y + 6, 8, 8, ORANGE if actif else INACTIF, 4)
        e.texte(28, y, nom)
        e.texte(228, y, horaire, ORANGE if actif else GRIS, 16, 400, "ra")
    e.finir("planning.png")


def scenarios_ecran(etat="", couleur=ORANGE, attente=False, noms=None):
    e = Ecran("Scénarios")
    e.texte(12, 38, etat, couleur)
    noms = noms if noms is not None else [("Soirée", "canape", "#6A1B9A"), ("Je pars", "depart", "#2E7D32"), ("Nuit", "lune", "#1976D2"),
                                          ("Tout éteindre", "lumiere_eteinte", "#C62828"), ("Film", "film", "#00838F"), ("Réveil", "reveil", "#E65100")]
    position = [(8, 60), (124, 60), (8, 132), (124, 132), (8, 204), (124, 204)]
    for (x, y), (nom, icone, couleur) in zip(position, noms):
        e.bouton(x, y, 108, 66, "#3A3A3A" if attente else couleur)
        e.icone(icone, x + 54, y + 20, 24, GRIS if attente else BLANC)
        e.multi(x + 54, y + 48, nom, GRIS if attente else BLANC)
    return e


def apropos():
    e = Ecran("À propos")
    e.texte(12, 60, "HAPanel 0.7.0")
    e.texte(12, 88, "SHA 3e880f3")
    e.texte(12, 128, "Home Assistant : connecté", VERT)
    # Adresse masquee : aucune adresse reelle dans le depot (G9).
    e.texte(12, 156, "Adresse IP : 192.168.x.x")
    e.texte(12, 196, "Mémoire : 162 Ko libres,")
    e.texte(12, 216, "plus grand bloc 108 Ko")
    # Recherche d'une mise a jour (D047), binaire public seulement.
    e.bouton(12, 238, 216, 34)
    e.texte(120, 255, "Rechercher une mise à jour", BLANC, 16, 400, "mm")
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
    reglages()
    schema_scenario()
    formulaire()
    led()
    for f in sorted(SORTIE.glob("*.png")):
        print(f.name, f.stat().st_size // 1024, "Ko")



if __name__ == "__main__":
    main()
