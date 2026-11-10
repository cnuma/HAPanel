"""Maquettes des pages en paysage, 480 x 272 (TODO T04, D053), validees par le
proprietaire le 10 novembre 2026, puis calees sur packages/format_paysage.yaml. Memes elements, memes couleurs et meme barre d'etat que le
portrait (D036) ; seules les positions et les tailles changent (fichier de format,
D053 option A). L'accueil se sert de la bande du bas, sans bouton Accueil (T16).

Depuis la racine du depot, apres une compilation (polices dans .esphome/font) :
    .venv/Scripts/python tools/generer_maquettes_paysage.py
"""
from generer_images_doc import (BLANC, BLEU, GRIS, GRIS_FONCE, INACTIF, ORANGE, ROUGE, SORTIE, VERT,
                                VIOLET, Ecran, cote_a_cote, encadrer)

L, H = 480, 272
DOSSIER = "paysage"


def ecran(titre=None, **options):
    return Ecran(titre, largeur=L, hauteur=H, **options)


def finir(e, nom):
    return encadrer(e, f"{DOSSIER}/{nom}")


def glissiere(e, chauffage=True):
    """Glissiere sur toute la largeur, plus haute qu'en portrait (48 au lieu de 40)."""
    e.rect(12, 212, 456, 48, GRIS_FONCE, 24)
    e.rect(240 if chauffage else 12, 212, 228, 48, ORANGE, 24)
    e.texte(126, 236, "Éteint", BLANC if not chauffage else GRIS, 22, 500, "mm")
    e.texte(354, 236, "Chauffage", BLANC if chauffage else GRIS, 22, 500, "mm")


def accueil(chauffage=True):
    """Gauche : pieces et temperatures ; droite : prereglages et consigne ; bas : glissiere."""
    e = ecran(maison=False)
    e.texte(12, 44, "Séjour")
    e.texte(120, 72, "20,5 °C", BLANC, 48, 500, "ma")
    e.texte(12, 150, "Extérieur 8,5 °C")
    if chauffage:
        prereglages = [("manuel", "#AB47BC"), ("horsgel", "#42A5F5"), ("eco", "#66BB6A"),
                       ("confort", ORANGE), ("boost", ROUGE)]
        for i, (nom, couleur) in enumerate(prereglages):
            x = 252 + i * 44
            e.rect(x, 48, 40, 40, GRIS_FONCE, 8, BLANC if nom == "eco" else None, 3 if nom == "eco" else 0)
            e.icone(nom, x + 20, 68, 24, couleur)
        e.bouton(252, 112, 64, 52, "#1E88E5")
        e.texte(284, 138, "-", BLANC, 22, 500, "mm")
        e.texte(360, 138, "19,0 °C", BLANC, 22, 500, "mm")
        e.bouton(404, 112, 64, 52, "#E53935")
        e.texte(436, 138, "+", BLANC, 22, 500, "mm")
    glissiere(e, chauffage)
    return e


def accueil_hs(wifi):
    e = ecran(maison=False, wifi=wifi, ha=False)
    e.icone("sans_ha" if wifi else "sans_wifi", 240, 118, 24, ROUGE)
    e.multi(240, 160, "Pas de communication\navec Home Assistant" if wifi else "Pas de Wi-Fi")
    return e


def menu():
    """Six tuiles sur trois colonnes ; la tuile violette n'apparait que si une mise a jour attend."""
    e = ecran("Menu", menu=False)
    tuiles = [("meteo", "Météo", BLEU), ("planning", "Planning", BLEU), ("scenarios", "Scénarios", BLEU),
              ("reglages", "Réglages", BLEU), ("info", "À propos", BLEU), ("maj", "Mise à jour", VIOLET)]
    for i, (nom, texte, couleur) in enumerate(tuiles):
        x, y = 8 + (i % 3) * 156, 44 + (i // 3) * 92
        e.bouton(x, y, 152, 84, couleur)
        e.icone(nom, x + 76, y + 28, 24)
        e.texte(x + 76, y + 62, texte, BLANC, 16, 400, "mm")
    return e


def meteo():
    """Gauche : temps actuel ; droite : trois jours en colonnes de 88 px."""
    e = ecran("Météo")
    e.icone("nuage", 36, 80, 32)
    e.texte(196, 58, "12,5°", BLANC, 48, 500, "ra")
    e.texte(12, 130, "Nuageux")
    for i, (jour, icone, temp) in enumerate([("lun.", "soleil", "14° / 6°"), ("mar.", "nuage", "12° / 7°"),
                                             ("mer.", "pluie", "10° / 5°")]):
        x = 214 + i * 88 + 44
        e.texte(x, 64, jour, BLANC, 16, 400, "ma")
        e.icone(icone, x, 110, 32)
        e.texte(x, 140, temp, BLANC, 22, 500, "ma")
    return e


def planning():
    """Resume a droite du nom, frise sur toute la largeur, trois calendriers en dessous."""
    e = ecran("Planning")
    e.texte(12, 38, "Aujourd'hui")
    e.texte(468, 38, "14:32", GRIS, 16, 400, "ra")
    e.texte(12, 66, "Maison", GRIS)
    e.texte(468, 62, "Prévu jusqu'à 22:00", ORANGE, 22, 500, "ra")
    largeur = 456
    e.rect(12, 96, largeur, 18, GRIS_FONCE, 6)
    e.rect(12 + largeur * 20 // 96, 96, largeur * 8 // 96, 18, ORANGE, 6)
    e.rect(12 + largeur * 56 // 96, 96, largeur * 24 // 96, 18, ORANGE, 6)
    e.rect(12 + largeur * 870 // 1440, 92, 2, 26, BLANC)
    for h in (0, 6, 12, 18, 24):
        ancre = "la" if h == 0 else "ra" if h == 24 else "ma"
        e.texte(12 + largeur * h // 24, 118, str(h), GRIS, 16, 400, ancre)
    lignes = [(144, "Salon", "17:00 - 21:00", False), (170, "Chambre", "14:00 - 16:00", True),
              (196, "Atelier", "terminé", False)]
    for y, nom, horaire, actif in lignes:
        e.rect(12, y + 6, 8, 8, ORANGE if actif else INACTIF, 4)
        e.texte(28, y, nom)
        e.texte(468, y, horaire, ORANGE if actif else GRIS, 16, 400, "ra")
    return e


def scenarios(etat="", couleur=ORANGE, attente=False):
    """Six boutons sur trois colonnes, ligne d'etat au-dessus."""
    e = ecran("Scénarios")
    e.texte(12, 40, etat, couleur)
    noms = [("Soirée", "canape", "#6A1B9A"), ("Je pars", "depart", "#2E7D32"), ("Nuit", "lune", "#1976D2"),
            ("Tout éteindre", "lumiere_eteinte", "#C62828"), ("Film", "film", "#00838F"), ("Réveil", "reveil", "#E65100")]
    for i, (nom, icone, fond) in enumerate(noms):
        x, y = 8 + (i % 3) * 156, 62 + (i // 3) * 82
        e.bouton(x, y, 152, 76, "#3A3A3A" if attente else fond)
        e.icone(icone, x + 76, y + 24, 24, GRIS if attente else BLANC)
        e.texte(x + 76, y + 56, nom, GRIS if attente else BLANC, 16, 400, "mm")
    return e


def interrupteur(e, x_libelle, x_droite, y, libelle, actif):
    """Libelle a gauche de la colonne, interrupteur cale a droite (x_droite : bord droit)."""
    e.texte(x_libelle, y + 6, libelle)
    xi = x_droite - 56
    e.rect(xi, y, 56, 30, BLEU if actif else GRIS_FONCE, 15, None if actif else GRIS, 0 if actif else 2)
    e.rect(xi + 29 if actif else xi + 3, y + 3, 24, 24, BLANC, 12)


def curseur(e, x_libelle, x_droite, centre, y, y_curseur, libelle, valeur, minimum):
    e.texte(x_libelle, y, libelle)
    e.texte(x_droite, y, f"{valeur} %", BLANC, 16, 400, "ra")
    x = centre - 98
    plein = round(196 * (valeur - minimum) / (100 - minimum))
    e.rect(x, y_curseur, 196, 10, "#123C5E", 5)
    e.rect(x, y_curseur, max(plein, 10), 10, BLEU, 5)
    e.rect(x + plein - 10, y_curseur - 5, 20, 20, BLEU, 10)


def reglages():
    """La LED a gauche (interrupteur, alerte, intensite), l'ecran a droite :
    intensite, et intensite pendant le message d'accueil (T13) (proprietaire,
    10 novembre 2026)."""
    e = ecran("Réglages", disquette=VERT)
    interrupteur(e, 12, 228, 48, "LED", True)
    interrupteur(e, 12, 228, 90, "Alerte LED", True)
    curseur(e, 12, 228, 120, 138, 172, "Intensité LED", 20, 0)
    curseur(e, 252, 468, 360, 54, 88, "Intensité écran", 80, 20)
    curseur(e, 252, 468, 360, 138, 172, "Intensité message", 100, 20)
    return e


def apropos():
    e = ecran("À propos")
    e.texte(12, 46, "HAPanel 0.12.0")
    e.texte(12, 72, "SHA 3e880f3")
    e.texte(12, 104, "Home Assistant : connecté", VERT)
    # Adresse masquee : aucune adresse reelle dans le depot (G9).
    e.texte(12, 130, "Adresse IP : 192.168.x.x")
    e.texte(252, 46, "Mémoire : 162 Ko libres,")
    e.texte(252, 66, "plus grand bloc 108 Ko")
    e.bouton(12, 168, 456, 44)
    e.texte(240, 190, "Rechercher une mise à jour", BLANC, 16, 400, "mm")
    return e


def main():
    (SORTIE / DOSSIER).mkdir(parents=True, exist_ok=True)
    finir(accueil(), "accueil.png")
    cote_a_cote([encadrer(accueil(False)), encadrer(accueil_hs(True))], f"{DOSSIER}/accueil_etats.png",
                ["Chauffage éteint", "Home Assistant injoignable"])
    finir(menu(), "menu.png")
    finir(meteo(), "meteo.png")
    finir(planning(), "planning.png")
    finir(scenarios(), "scenarios.png")
    finir(reglages(), "reglages.png")
    finir(apropos(), "apropos.png")
    for f in sorted((SORTIE / DOSSIER).glob("*.png")):
        print(f.name, f.stat().st_size // 1024, "Ko")


if __name__ == "__main__":
    main()
