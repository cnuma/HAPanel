"""Genere les schemas de docs/ARCHITECTURE.md dans docs/images/architecture.

Depuis la racine du depot, apres une compilation (polices dans .esphome/font) :
    .venv/Scripts/python tools/generer_schemas_architecture.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "docs" / "images" / "architecture"
POLICES = RACINE / ".esphome" / "font"

ENCRE, DOUX, TRAIT = "#20242A", "#5F6B7A", "#455A64"
BLEU, ORANGE, VERT, VIOLET, ROUGE, GRIS, JAUNE = ("#E3F2FD", "#FFF3E0", "#E8F5E9", "#F3E5F5", "#FFEBEE", "#ECEFF1", "#FFFDE7")
B_BLEU, B_ORANGE, B_VERT, B_ROUGE, B_VIOLET = "#1565C0", "#E65100", "#2E7D32", "#C62828", "#6A1B9A"


def f(taille, gras=False):
    return ImageFont.truetype(str(POLICES / f"Roboto@{500 if gras else 400}@False@v1.ttf"), taille)


class S:
    def __init__(self, l, h):
        self.im = Image.new("RGB", (l, h), "#FFFFFF")
        self.d = ImageDraw.Draw(self.im)

    def zone(self, x, y, l, h, titre, couleur="#90A4AE"):
        self.d.rounded_rectangle([x, y, x + l, y + h], 16, fill="#FAFBFC", outline=couleur, width=3)
        self.d.text((x + 16, y + 10), titre, fill=couleur, font=f(22, True))

    def boite(self, x, y, l, h, titre, texte="", fond=BLEU, bord=TRAIT):
        self.d.rounded_rectangle([x, y, x + l, y + h], 12, fill=fond, outline=bord, width=2)
        cx = x + l / 2
        if texte:
            nb = texte.count("\n") + 1
            hauteur = 30 + nb * 25
            haut = y + (h - hauteur) / 2
            self.d.text((cx, haut + 13), titre, fill=ENCRE, font=f(23, True), anchor="mm")
            self.d.multiline_text((cx, haut + 32 + nb * 25 / 2), texte, fill=ENCRE, font=f(19), anchor="mm", align="center", spacing=5)
        else:
            self.d.multiline_text((cx, y + h / 2), titre, fill=ENCRE, font=f(23, True), anchor="mm", align="center", spacing=4)

    def fleche(self, points, couleur=TRAIT, texte=None, pos=None, ancre="mm", epaisseur=3, double=False):
        self.d.line(points, fill=couleur, width=epaisseur, joint="curve")
        def pointe(a, b):
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            t = 14
            self.d.polygon([b, (b[0] - t * math.cos(ang - .45), b[1] - t * math.sin(ang - .45)),
                            (b[0] - t * math.cos(ang + .45), b[1] - t * math.sin(ang + .45))], fill=couleur)
        pointe(points[-2], points[-1])
        if double:
            pointe(points[1], points[0])
        if texte:
            if pos is None:
                a, b = points[len(points) // 2 - 1], points[len(points) // 2]
                pos = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            self.etiquette(pos, texte, couleur, ancre)

    def etiquette(self, pos, texte, couleur=DOUX, ancre="mm", taille=18):
        p = f(taille)
        b = self.d.multiline_textbbox(pos, texte, font=p, anchor=ancre, align="center", spacing=3)
        self.d.rectangle([b[0] - 4, b[1] - 2, b[2] + 4, b[3] + 2], fill="#FFFFFF")
        self.d.multiline_text(pos, texte, fill=couleur, font=p, anchor=ancre, align="center", spacing=3)

    def sauver(self, nom):
        self.im.save(SORTIE / nom, optimize=True)


def sequence(nom, acteurs, etapes, largeur=1100):
    """etapes : (de, vers, texte, couleur) ; (acteur, None, note, fond) pour une note ;
    (None, None, texte, None) pour un separateur."""
    pas = (largeur - 200) / (len(acteurs) - 1)
    xs = [100 + i * pas for i in range(len(acteurs))]
    hauts = []
    for e in etapes:
        hauts.append(40 + 24 * (e[2].count("\n") + 1))
    h = 110 + sum(hauts) + 40
    s = S(largeur, int(h))
    for x in xs:
        s.d.line([(x, 80), (x, h - 20)], fill="#B0BEC5", width=2)
    for x, a in zip(xs, acteurs):
        s.boite(x - 92, 14, 184, 62, a, "", GRIS)
    y = 96
    for e, hl in zip(etapes, hauts):
        de, vers, texte, c = e
        if de is None:
            s.d.line([(30, y + hl / 2), (largeur - 30, y + hl / 2)], fill="#CFD8DC", width=2)
            s.etiquette((largeur / 2, y + hl / 2), texte, DOUX)
        elif vers is None:
            x = xs[acteurs.index(de)]
            lignes = texte.count("\n") + 1
            p = f(18)
            lg = max(s.d.textlength(t, font=p) for t in texte.split("\n")) + 24
            gauche = min(max(x - lg / 2, 8), largeur - lg - 8)
            s.d.rounded_rectangle([gauche, y + 5, gauche + lg, y + hl - 5], 8, fill=c or JAUNE, outline="#B0BEC5")
            s.d.multiline_text((gauche + lg / 2, y + hl / 2), texte, fill=ENCRE, font=p, anchor="mm", align="center", spacing=3)
        else:
            a, b = xs[acteurs.index(de)], xs[acteurs.index(vers)]
            ya = y + hl - 12
            s.fleche([(a, ya), (b, ya)], c or TRAIT)
            s.d.multiline_text(((a + b) / 2, ya - 7), texte, fill=c or ENCRE, font=f(18), anchor="md", align="center", spacing=3)
        y += hl
    s.sauver(nom)


def contexte():
    s = S(1100, 760)
    s.zone(20, 20, 1060, 540, "Réseau local de la maison")
    s.boite(50, 90, 290, 200, "Modules HAPanel", "un même binaire pour tous\nhapanel-xxxxxx (MAC)\nécran, tactile, LED, LDR\naucune entité connue", BLEU, B_BLEU)
    s.boite(450, 90, 300, 200, "Home Assistant", "intégration ESPHome\nautomatisation par module\ndepuis le blueprint unique\nmodule.yaml", ORANGE, B_ORANGE)
    s.boite(840, 90, 210, 200, "Appareils", "thermostats\nscènes, scripts\ncalendriers\nmétéo, capteurs", VERT, B_VERT)
    s.fleche([(340, 150), (450, 150)], B_BLEU, "événements", (395, 128))
    s.fleche([(450, 230), (340, 230)], B_ORANGE, "maj_valeur", (395, 252))
    s.etiquette((395, 310), "API native chiffrée (Noise)", DOUX)
    s.fleche([(750, 190), (840, 190)], B_VERT, double=True)
    s.boite(50, 400, 290, 130, "PC de développement", "ESPHome CLI figé\ntools/build.ps1", GRIS)
    s.fleche([(195, 400), (195, 290)], DOUX, "OTA chiffrée\nou USB", (280, 345))
    s.boite(450, 400, 210, 130, "secrets.yaml", "Wi-Fi, clé d'API\nignoré par Git", ROUGE, B_ROUGE)
    s.fleche([(450, 465), (340, 465)], B_ROUGE, "à la compilation", (395, 442))
    s.boite(250, 620, 600, 110, "GitHub : cnuma/HAPanel", "YAML, blueprint et documentation : seule source de vérité", VIOLET, B_VIOLET)
    s.fleche([(195, 620), (195, 530)], B_VIOLET, "git", (225, 590))
    s.fleche([(700, 620), (700, 290)], B_VIOLET, "import du blueprint (URL)", (860, 590))
    s.sauver("01_contexte.png")


def packages():
    s = S(1100, 900)
    s.boite(250, 20, 600, 80, "hapanel_banc.yaml", "production + debug mémoire + journaux DEBUG", GRIS)
    s.fleche([(550, 100), (550, 150)])
    s.boite(250, 150, 600, 80, "hapanel.yaml", "assemble les packages et les substitutions", BLEU, B_BLEU)
    s.d.line([(550, 230), (550, 265)], fill=TRAIT, width=3)
    s.d.line([(150, 265), (950, 265)], fill=TRAIT, width=3)
    for x in (150, 550, 950):
        s.fleche([(x, 265), (x, 300)])
    s.zone(20, 300, 260, 390, "Socle")
    s.boite(40, 345, 220, 150, "base.yaml", "nœud, Wi-Fi, API,\nOTA, journaux,\nidentité de build", GRIS)
    s.boite(40, 515, 220, 150, "hardware.yaml", "seul propriétaire\ndes broches et bus\n(G2)", GRIS)
    s.zone(300, 300, 500, 390, "Écran : pages dans l'ordre d'inclusion")
    pages = [("accueil", 320, 350), ("météo", 560, 350), ("planning", 320, 430), ("scénarios", 560, 430), ("menu", 320, 510)]
    for t, x, y in pages:
        s.boite(x, y, 220, 65, t + ".yaml", "", ORANGE, B_ORANGE)
    s.boite(560, 510, 220, 65, "lvgl.yaml", "", BLEU, B_BLEU)
    s.etiquette((550, 625), "lvgl.yaml : À propos, barre de navigation, suivi de la connexion.\nL'accueil est inclus d'abord : c'est la page de démarrage.", DOUX)
    s.zone(820, 300, 260, 390, "Services")
    s.boite(840, 345, 220, 150, "liaison_ha.yaml", "action maj_valeur,\nétat et péremption\ndes valeurs", VERT, B_VERT)
    s.boite(840, 515, 220, 150, "led_veille.yaml", "veille, retour accueil,\nLED, rétroéclairage,\nLDR", VERT, B_VERT)
    s.zone(20, 720, 1060, 160, "Couplage par identifiants ESPHome")
    s.etiquette((550, 800), "liaison_ha écrit les globals puis appelle accueil / meteo / planning / scenarios_rafraichir.\nLes pages lisent ces globals et ha_connecte_affiche. accueil_rafraichir calcule la couleur de la LED.\nled_veille lit ldr_tension (hardware) et pilote retroeclairage et page_accueil.", ENCRE, taille=20)
    s.sauver("02_packages.png")


def materiel():
    s = S(1100, 760)
    s.boite(400, 180, 300, 400, "ESP32 rév. 3.1", "sans PSRAM\nflash 4 Mo\nESP-IDF\nLVGL 9\nWi-Fi", BLEU, B_BLEU)
    s.boite(30, 40, 290, 150, "Écran ILI9341", "240 x 320, SPI 40 MHz\nCLK 14, MOSI 13\nMISO 12, CS 15, DC 2", ORANGE, B_ORANGE)
    s.fleche([(320, 115), (400, 230)], double=True)
    s.boite(30, 230, 290, 120, "Rétroéclairage", "GPIO27, PWM LEDC\ngamma de la lumière ESPHome", ORANGE, B_ORANGE)
    s.fleche([(400, 290), (320, 290)])
    s.boite(30, 390, 290, 180, "Tactile CST820", "composant cst816\nI2C : SDA 33, SCL 32\nRST 25 ; lu toutes les 50 ms\nINT 21 inutilisée (D009)", VERT, B_VERT)
    s.fleche([(320, 480), (400, 480)], double=True)
    s.boite(780, 120, 290, 170, "LED RVB", "active à l'état bas, PWM\nR 4, V 16, B 17", VIOLET, B_VIOLET)
    s.fleche([(700, 230), (780, 200)])
    s.boite(780, 340, 290, 200, "LDR", "GPIO34, ADC 0 dB\n8 échantillons toutes les 2 s\nmoyenne glissante de 30,\npublie toutes les 10 s", JAUNE)
    s.fleche([(780, 440), (700, 440)])
    s.boite(400, 630, 300, 100, "Alimentation", "bloc 1 A recommandé (R7)", ROUGE, B_ROUGE)
    s.fleche([(550, 630), (550, 580)], B_ROUGE)
    s.sauver("03_materiel.png")


def flux():
    s = S(1100, 1040)
    s.zone(20, 20, 1060, 340, "Home Assistant")
    s.boite(50, 70, 300, 110, "Entités", "climate, sensor, weather,\ncalendar, scene, script...", VERT, B_VERT)
    s.boite(480, 70, 560, 110, "Déclencheurs du blueprint", "changement d'état, toutes les 5 min, démarrage de HA,\nesphome.hapanel_demande_valeurs", ORANGE, B_ORANGE)
    s.fleche([(350, 125), (480, 125)], B_VERT)
    s.boite(250, 230, 600, 100, "Actions du blueprint", "calcule les clés : chauffage_*, meteo_*, plan_*, scen_*...", ORANGE, B_ORANGE)
    s.fleche([(760, 180), (600, 230)], B_ORANGE)
    s.fleche([(550, 330), (550, 420)], B_ORANGE, "esphome.<noeud>_maj_valeur(cle, valeur) : texte par texte", (550, 385))
    s.zone(20, 400, 1060, 620, "Module HAPanel")
    s.boite(250, 450, 600, 110, "maj_valeur (liaison_ha.yaml)", "copie bornée k[24] et v[32], analyse, aiguillage par préfixe", BLEU, B_BLEU)
    s.d.line([(550, 560), (550, 600)], fill=TRAIT, width=3)
    s.d.line([(170, 600), (930, 600)], fill=TRAIT, width=3)
    xs = [170, 423, 677, 930]
    tit = [("temperature\nchauffage_*", "accueil"), ("meteo_*", "meteo"), ("plan_*", "planning"), ("scen_*", "scenarios")]
    for x, (cle, page) in zip(xs, tit):
        s.fleche([(x, 600), (x, 640)])
        s.boite(x - 115, 640, 230, 90, cle, "", GRIS)
        s.fleche([(x, 730), (x, 770)])
        s.boite(x - 115, 770, 230, 90, "globals", "valeur, état, horodatage", VERT, B_VERT)
        s.fleche([(x, 860), (x, 900)])
        s.boite(x - 115, 900, 230, 90, page + "_rafraichir", "widgets LVGL", ORANGE, B_ORANGE)
    s.sauver("04_flux_valeurs.png")


def etats():
    s = S(1100, 650)
    pos = {"0": (70, 240), "1": (440, 80), "2": (810, 80), "3": (440, 400)}
    s.boite(*pos["0"], 240, 130, "0 : non reçue", "affichée --, orange", GRIS)
    s.boite(*pos["1"], 240, 130, "1 : valide", "valeur affichée", VERT, B_VERT)
    s.boite(*pos["2"], 240, 130, "2 : indisponible", "effacée, signalée", ORANGE, B_ORANGE)
    s.boite(*pos["3"], 240, 130, "3 : périmée", "effacée, signalée", ROUGE, B_ROUGE)
    s.fleche([(190, 240), (190, 145), (440, 145)], B_VERT, "valeur valide", (290, 122))
    s.fleche([(680, 115), (810, 115)], B_ORANGE, "unavailable\nou illisible", (745, 75))
    s.fleche([(810, 180), (680, 180)], B_VERT, "valeur valide", (745, 205))
    s.fleche([(560, 210), (560, 400)], B_ROUGE, "15 min sans valeur\ncontrôle toutes les 30 s", (690, 300))
    s.fleche([(490, 400), (490, 210)], B_VERT, "valeur valide", (410, 305))
    s.fleche([(440, 465), (190, 465), (190, 370)], DOUX, "connexion HA perdue :\ntout revient à 0", (300, 510))
    s.etiquette((550, 595), "Température et extérieur suivent ce cycle valeur par valeur ; chauffage, météo, planning et scénarios par groupe.\nPlanning et scénarios portent l'indisponibilité élément par élément (« ? »).", DOUX)
    s.sauver("06_etats_valeur.png")


def veille():
    s = S(1100, 700)
    s.boite(60, 80, 300, 150, "Autre page", "écran allumé\nnavigation possible", BLEU, B_BLEU)
    s.boite(600, 80, 300, 150, "Accueil", "écran allumé", VERT, B_VERT)
    s.boite(600, 430, 300, 150, "Écran éteint", "LVGL en pause, toucher ignoré,\nLED seule (P2)", GRIS)
    s.fleche([(360, 125), (600, 125)], B_VERT, "60 s sans toucher\n(même sans HA)", (480, 85))
    s.fleche([(600, 190), (360, 190)], B_BLEU, "Menu ou tuile", (480, 215))
    s.fleche([(700, 230), (700, 430)], TRAIT, "60 s sans toucher\net HA connecté", (590, 320))
    s.fleche([(830, 430), (830, 230)], B_ORANGE, "relâchement du doigt (aucune commande)\nou HA déconnecté", (900, 330), "mm")
    s.boite(60, 430, 390, 150, "Sans Home Assistant", "l'écran ne s'éteint jamais :\nle message de cause reste lisible", ORANGE, B_ORANGE)
    s.etiquette((550, 645), "Contrôle toutes les secondes dans led_veille.yaml, à partir de lv_display_get_inactive_time.\nLe retour à l'accueil précède la pause dans le même cycle.", DOUX)
    s.sauver("09_veille.png")


def lumiere():
    s = S(1100, 650)
    s.boite(30, 240, 220, 130, "LDR", "tension moyenne\nsur 1 min", JAUNE)
    s.boite(330, 240, 270, 130, "ldr_obscurite", "(V - 0,09) / (0,20 - 0,09)\nbornée de 0 à 1, 10 s\nsans mesure : 0", BLEU, B_BLEU)
    s.fleche([(250, 305), (330, 305)])
    s.boite(690, 60, 380, 170, "Rétroéclairage", "de 1,0 à 0,40 (gamma : environ 8 %)\nchange à partir de 5 points d'écart\ntransition de 2 s\nécran éteint : appliqué au réveil", ORANGE, B_ORANGE)
    s.fleche([(600, 280), (690, 170)], B_ORANGE)
    s.boite(690, 280, 380, 150, "Plafond de la LED", "de 0,25 à 0,05\nrespiration de 6 s\nplancher 20 % du plafond", VIOLET, B_VIOLET)
    s.fleche([(600, 320), (690, 350)], B_VIOLET)
    s.boite(690, 470, 380, 130, "LED en alerte", "rouge à pleine intensité, 500 ms\nne dépend pas de la LDR", ROUGE, B_ROUGE)
    s.boite(330, 470, 270, 130, "accueil_rafraichir", "couleur du préréglage,\nalerte si valeur douteuse", GRIS)
    s.fleche([(600, 535), (690, 535)], B_ROUGE)
    s.fleche([(500, 470), (760, 430)], B_VIOLET)
    s.fleche([(690, 150), (140, 150), (140, 240)], B_ROUGE, epaisseur=2)
    s.etiquette((400, 130), "Boucle possible : la lumière de l'écran peut atteindre la LDR (à vérifier, D023)", B_ROUGE)
    s.sauver("10_lumiere.png")


def navigation():
    s = S(1100, 560)
    s.boite(60, 40, 980, 90, "Barre de navigation (top_layer), toujours visible", "Accueil : un toucher ; Menu : tout le reste en deux touchers", GRIS)
    s.boite(430, 190, 240, 90, "page_menu", "", BLEU, B_BLEU)
    s.fleche([(550, 130), (550, 190)], TRAIT, "Menu", (600, 160))
    s.d.line([(550, 280), (550, 325)], fill=TRAIT, width=3)
    s.d.line([(150, 325), (950, 325)], fill=TRAIT, width=3)
    for x, t, c in [(150, "page_accueil", VERT), (350, "page_meteo", ORANGE), (550, "page_planning", ORANGE), (750, "page_scenarios", ORANGE), (950, "page_apropos", GRIS)]:
        s.fleche([(x, 325), (x, 370)])
        s.boite(x - 95, 370, 190, 80, t, "", c)
    s.fleche([(100, 130), (100, 370)], B_VERT, "Accueil", (58, 250))
    s.etiquette((550, 505), "Inactivité de 60 s depuis toute page : retour à page_accueil (D022). La navigation ne dépend ni de HA ni du Wi-Fi (P5).", DOUX)
    s.sauver("11_navigation.png")


def build():
    s = S(1100, 900)
    entrees = [(30, "VERSION", "0.6.0-dev"), (295, "Git", "SHA, +modif"), (560, "secrets.yaml", "hors dépôt"), (825, "requirements.txt", "ESPHome figé")]
    for x, t, d in entrees:
        s.boite(x, 30, 245, 100, t, d, GRIS)
    s.boite(150, 210, 800, 110, "tools/build.ps1", "injecte version et git_sha par substitution, appelle esphome config / compile / upload / logs", BLEU, B_BLEU)
    for x in (152, 417):
        s.fleche([(x, 130), (x if x > 200 else 200, 210)])
    s.fleche([(682, 130), (682, 210)])
    s.fleche([(947, 130), (900, 210)])
    s.boite(150, 390, 800, 90, "firmware.bin", "code C++ généré, compilé par ESP-IDF", ORANGE, B_ORANGE)
    s.fleche([(550, 320), (550, 390)])
    s.boite(150, 550, 800, 90, "OTA chiffrée vers le module", "clé de l'API ; bloc secteur 1 A", VIOLET, B_VIOLET)
    s.fleche([(550, 480), (550, 550)])
    s.boite(150, 710, 370, 150, "Nouveau binaire", "« Boot seems successful »\naprès 60 s\nversion et SHA relus", VERT, B_VERT)
    s.boite(580, 710, 370, 150, "Rollback du bootloader", "échec de démarrage :\nretour silencieux au binaire\nprécédent (R7)", ROUGE, B_ROUGE)
    s.fleche([(400, 640), (335, 710)], B_VERT)
    s.fleche([(700, 640), (765, 710)], B_ROUGE)
    s.sauver("12_build.png")


def securite():
    s = S(1100, 780)
    s.zone(20, 20, 1060, 300, "Zone de confiance : Home Assistant, décide et vérifie")
    s.boite(50, 70, 450, 220, "Blueprint module.yaml", "accepte seulement l'événement de son panneau\nthermostat disponible et non verrouillé\nconsigne dans les bornes\nscénario : numéro dans la liste, entité disponible", ORANGE, B_ORANGE)
    s.boite(600, 70, 450, 220, "Autorisation ESPHome", "inutile aux événements du panneau\n(testé le 2 novembre 2026)\nactivée : un firmware modifié\npourrait appeler d'autres actions", ORANGE, B_ORANGE)
    s.zone(20, 410, 1060, 330, "Module : affiche et demande, ne décide pas")
    s.boite(50, 460, 450, 240, "Garde-fous locaux", "aucune commande si HA déconnecté (P2)\nni sur état inconnu ou périmé (P4)\nle premier toucher ne fait que réveiller\nvaleur en attente jusqu'à confirmation", BLEU, B_BLEU)
    s.boite(600, 460, 450, 240, "Secrets", "clé d'API commune aux modules (R8)\nprotège API et OTA\nWi-Fi et clé dans secrets.yaml\nce fichier reste hors de Git", ROUGE, B_ROUGE)
    s.fleche([(275, 410), (275, 320)], B_BLEU, "événements esphome.hapanel_*", (275, 365))
    s.fleche([(825, 320), (825, 410)], B_ORANGE, "maj_valeur : API chiffrée", (825, 365))
    s.sauver("13_securite.png")


def memoire():
    s = S(1100, 480)
    lignes = [("RAM statique", 54400, 180736, "54,4 Ko / 180,7 Ko (30,1 %)", "#1565C0"),
              ("Flash de l'application", 1151139, 1835008, "1 151 Ko / 1 835 Ko (62,7 %)", "#E65100")]
    y = 50
    for t, v, m, l, c in lignes:
        s.d.text((40, y), t, fill=ENCRE, font=f(24, True))
        s.d.rounded_rectangle([40, y + 40, 1060, y + 85], 8, fill="#ECEFF1")
        s.d.rounded_rectangle([40, y + 40, 40 + 1020 * v / m, y + 85], 8, fill=c)
        s.d.text((1060, y), l, fill=DOUX, font=f(22), anchor="ra")
        y += 125
    s.d.text((40, y), "Mesures sur le module (build de banc dc83077)", fill=ENCRE, font=f(24, True))
    s.d.multiline_text((40, y + 42), "Mémoire libre : 162,6 Ko\nPlus grand bloc libre : 106,5 Ko\nTampon LVGL : 25 % de l'écran (sans PSRAM, R2, G6)", fill=ENCRE, font=f(22), spacing=8)
    s.sauver("14_memoire.png")


def blueprint_principe():
    s = S(1100, 640)
    s.boite(30, 150, 300, 280, "Blueprint", "un fichier YAML\nsaisies déclarées\ndéclencheurs\nconditions\nactions avec !input\njamais exécuté", ORANGE, B_ORANGE)
    for i, t in enumerate("ABC"):
        y = 50 + i * 170
        s.boite(420, y, 250, 130, "Saisies " + t, "réponses au formulaire\nentités, nombres, textes", JAUNE)
        s.boite(790, y, 280, 130, "Automatisation " + t, "entité automation.*\ntraces, activable", VERT, B_VERT)
        s.fleche([(330, 290), (420, y + 65)], B_ORANGE)
        s.fleche([(670, y + 65), (790, y + 65)], B_VERT)
    s.etiquette((550, 580), "Un modèle, autant d'automatisations que de jeux de saisies. Un blueprint ressemble à une classe,\nune automatisation à une instance. Corriger le modèle corrige toutes ses automatisations.", DOUX, taille=20)
    s.sauver("15_blueprint_principe.png")


def blueprint_execution():
    s = S(1100, 1110)
    s.zone(20, 15, 1060, 180, "Déclencheurs")
    for x, t, d in [(40, "État d'entité", "capteur, thermostat,\nmétéo, calendrier"), (295, "Horloge, démarrage", "toutes les 5 min,\nstart de HA"),
                    (550, "Demande", "esphome.hapanel_\ndemande_valeurs"), (805, "Commande", "esphome.hapanel_\ncommande")]:
        s.boite(x, 55, 245, 125, t, d, BLEU, B_BLEU)
    s.boite(150, 240, 800, 90, "variables", "évaluées à chaque exécution : action_maj, scenarios, noms...", GRIS)
    s.fleche([(550, 195), (550, 240)])
    s.boite(150, 375, 800, 90, "conditions", "une demande ou une commande vient-elle de ce panneau ?", ORANGE, B_ORANGE)
    s.fleche([(550, 330), (550, 375)])
    s.fleche([(950, 420), (1050, 420), (1050, 510)], B_ROUGE)
    s.etiquette((1000, 530), "non : fin,\nhors file", B_ROUGE)
    s.boite(150, 510, 800, 80, "mode: queued", "une exécution à la fois, 20 au plus en attente", GRIS)
    s.fleche([(550, 465), (550, 510)], B_VERT, "oui", (585, 487))
    s.fleche([(350, 590), (250, 650)], B_BLEU, "commande", (250, 615))
    s.fleche([(750, 590), (810, 650)], B_VERT, "tout le reste", (850, 615))
    s.boite(30, 650, 480, 190, "Vérifier, puis exécuter", "thermostat : disponible, verrou, bornes\nscénario : numéro connu, entité disponible\nrefus : journal hapanel.blueprint", ORANGE, B_ORANGE)
    s.boite(570, 650, 500, 190, "Calculer et envoyer", "accueil : 9 valeurs\nscénarios : 18 valeurs\nmétéo : 14 valeurs\nplanning : 8 valeurs", VERT, B_VERT)
    s.boite(30, 900, 480, 130, "Actions sur les entités", "climate.set_*, scene/script.turn_on,\nautomation.trigger", VERT, B_VERT)
    s.fleche([(270, 840), (270, 900)], B_ORANGE)
    s.boite(570, 900, 500, 130, "esphome.<noeud>_maj_valeur", "une action par clé, vers ce seul module", BLEU, B_BLEU)
    s.fleche([(820, 840), (820, 900)], B_ORANGE)
    s.fleche([(510, 800), (540, 800), (540, 965), (570, 965)], B_ROUGE)
    s.etiquette((550, 1070), "Scénario : le résultat revient aussi par maj_valeur (scen_resultat). Chaque envoi complet compte 49 valeurs.", DOUX)
    s.sauver("17_blueprint_execution.png")


def blueprint_modules():
    s = S(1100, 650)
    s.boite(30, 90, 250, 130, "Module A", "hapanel-aaaaaa", BLEU, B_BLEU)
    s.boite(30, 370, 250, 130, "Module B", "hapanel-bbbbbb", BLEU, B_BLEU)
    s.boite(400, 215, 240, 160, "Bus d'événements", "hapanel_commande\ndevice_id = A", GRIS)
    s.boite(790, 90, 280, 130, "Automatisation A", "panneau = A", ORANGE, B_ORANGE)
    s.boite(790, 370, 280, 130, "Automatisation B", "panneau = B", ORANGE, B_ORANGE)
    s.fleche([(280, 180), (400, 255)], B_BLEU, "événement", (385, 190))
    s.fleche([(640, 255), (790, 180)], B_VERT, "accepté", (670, 190))
    s.fleche([(640, 335), (790, 410)], B_ROUGE, "écarté :\nA différent de B", (680, 425))
    s.fleche([(930, 90), (930, 40), (155, 40), (155, 90)], B_ORANGE, "esphome.hapanel_aaaaaa_maj_valeur : ce module seulement", (540, 40))
    s.etiquette((550, 590), "Toutes les automatisations reçoivent chaque événement : seule la condition sur device_id les sépare.\nDans l'autre sens, le nom de l'action désigne directement un module.", DOUX, taille=20)
    s.sauver("18_blueprint_modules.png")


def blueprint_structure():
    s = S(1100, 1240)
    blocs = [
        (20, 250, "blueprint:", "lu à l'import et au formulaire", ORANGE, B_ORANGE, [
            (0, 66, "métadonnées", "name, description, domain, source_url"),
            (72, 100, "input: champs principaux", "panneau, thermomètres, thermostat,\nbornes, météo, calendriers"),
            (178, 72, "input: section Scénarios", "scenario_N, nom_N, icone_N, couleur_N")]),
        (290, 90, "mode: / max:", "file d'exécution", GRIS, TRAIT, [(5, 80, "queued, 20", "une exécution à la fois par module")]),
        (400, 90, "variables:", "à chaque déclenchement", GRIS, TRAIT, [(5, 80, "saisies, action_maj", "rend les saisies visibles des modèles")]),
        (510, 110, "triggers:", "toujours actifs", BLEU, B_BLEU, [(0, 110, "9 déclencheurs", "états ; meteo, planning, periodique,\ndemarrage, demande, commande")]),
        (640, 90, "conditions:", "filtre", ORANGE, B_ORANGE, [(5, 80, "un seul test", "demande ou commande de ce panneau")]),
    ]
    for y, h, t, d, fond, bord, lignes in blocs:
        s.boite(20, y, 300, h, t, d, fond, bord)
        for dy, hl, a, b in lignes:
            s.boite(390, y + dy, 690, hl, a, b, "#FFFFFF")
        s.fleche([(320, y + h / 2), (390, y + h / 2)])
    s.boite(20, 750, 300, 470, "actions:", "selon trigger.id", VERT, B_VERT)
    s.boite(390, 750, 690, 80, "variables communes", "etat, disponible, verrou, borne_min, borne_max", "#FFFFFF")
    s.zone(390, 845, 335, 375, "choose : commande", B_BLEU)
    for i, t in enumerate(["scenario", "chauffage_mode", "chauffage_consigne", "chauffage_prereglage", "default : journal de refus"]):
        s.boite(405, 890 + i * 64, 305, 54, t, "", BLEU if i < 4 else ROUGE, B_BLEU if i < 4 else B_ROUGE)
    s.zone(745, 845, 335, 375, "default : envois", B_VERT)
    for i, (t, d) in enumerate([("Accueil", "sauf meteo, planning"), ("Scénarios", "périodique, démarrage, demande"), ("Météo", "weather.get_forecasts"), ("Planning", "calendar.get_events")]):
        s.boite(760, 890 + i * 80, 305, 70, t, d, VERT, B_VERT)
    s.fleche([(320, 985), (390, 985)])
    s.sauver("19_blueprint_structure.png")


def yaml_matrice():
    colonnes = ["subst.", "esphome", "wifi", "api", "font", "globals", "lvgl", "script", "interval", "sensor", "switch", "tactile", "autres"]
    lignes = [("base", "esphome wifi api sensor autres", GRIS, "#607D8B"),
              ("hardware", "subst. sensor tactile autres", GRIS, "#607D8B"),
              ("accueil", "subst. esphome wifi font globals lvgl script sensor autres", ORANGE, B_ORANGE),
              ("meteo", "esphome font lvgl script", ORANGE, B_ORANGE),
              ("planning", "esphome lvgl script interval", ORANGE, B_ORANGE),
              ("scenarios", "subst. esphome font globals lvgl script interval", ORANGE, B_ORANGE),
              ("menu", "lvgl", ORANGE, B_ORANGE),
              ("lvgl", "font globals lvgl interval", BLEU, B_BLEU),
              ("liaison_ha", "subst. api globals script interval", VERT, B_VERT),
              ("led_veille", "subst. globals script interval switch tactile autres", VERT, B_VERT),
              ("message_accueil", "subst. api globals lvgl script interval switch", ORANGE, B_ORANGE)]
    s = S(1260, 900)
    x0, y0, lc, hl = 255, 110, 76, 52
    yf = y0 + len(lignes) * hl
    xf = x0 + len(colonnes) * lc
    # Axes : titre des colonnes centre au-dessus d'elles, titre des lignes
    # vertical a leur gauche, centre sur leur hauteur ; un trait montre l'etendue.
    s.d.text(((x0 + xf) / 2, 28), "Colonnes : les blocs YAML (script:, sensor:…)", fill=ENCRE, font=f(21, True), anchor="mm")
    s.d.line([(x0 + 8, 52), (xf - 8, 52)], fill=ENCRE, width=2)
    titre = "Lignes : les fichiers de packages/"
    police = f(21, True)
    lt = int(s.d.textlength(titre, font=police)) + 10
    tampon = Image.new("RGB", (lt, 30), "#FFFFFF")
    ImageDraw.Draw(tampon).text((lt / 2, 15), titre, fill=ENCRE, font=police, anchor="mm")
    s.im.paste(tampon.rotate(90, expand=True), (14, int((y0 + yf) / 2 - lt / 2)))
    s.d.line([(52, y0 + 8), (52, yf - 8)], fill=ENCRE, width=2)
    for i, c in enumerate(colonnes):
        s.d.text((x0 + i * lc + lc / 2, 85), c, fill=ENCRE, font=f(17, True), anchor="mm")
    for j, (nom, blocs, fond, bord) in enumerate(lignes):
        y = y0 + j * hl
        s.d.line([(70, y), (xf, y)], fill="#CFD8DC", width=1)
        s.d.text((245, y + hl / 2), nom, fill=ENCRE, font=f(22, True), anchor="rm")
        for i, c in enumerate(colonnes):
            if c in blocs.split():
                cx = x0 + i * lc
                s.d.rounded_rectangle([cx + 8, y + 9, cx + lc - 8, y + hl - 9], 7, fill=fond, outline=bord, width=2)
    s.d.line([(70, yf), (xf, yf)], fill="#CFD8DC", width=1)
    # Legende : une case = le fichier declare ce bloc ; couleur = role du fichier.
    s.d.text((20, yf + 40), "Légende : une case = ce fichier déclare ce bloc. La couleur donne le rôle du fichier :", fill=ENCRE, font=f(19, True), anchor="lm")
    roles = [(GRIS, "#607D8B", "socle : carte, Wi-Fi, API"), (ORANGE, B_ORANGE, "écran affiché"),
             (BLEU, B_BLEU, "graphisme commun, navigation"), (VERT, B_VERT, "service sans écran")]
    for cx, (fond, bord, texte) in zip([30, 320, 530, 880], roles):
        s.d.rounded_rectangle([cx, yf + 68, cx + 46, yf + 100], 7, fill=fond, outline=bord, width=2)
        s.d.text((cx + 56, yf + 84), texte, fill=ENCRE, font=f(18), anchor="lm")
    s.d.text((20, yf + 135), "Abréviations : subst. = substitutions ; tactile = touchscreen.", fill=DOUX, font=f(17), anchor="lm")
    s.d.text((20, yf + 162), "autres : ota, logger, text_sensor (base) ; spi, output, light, display (hardware) ; time (accueil) ; select, number (led_veille).", fill=DOUX, font=f(17), anchor="lm")
    s.sauver("20_yaml_matrice.png")


def yaml_execution():
    s = S(1100, 760)
    s.zone(20, 20, 1060, 390, "Entrée : une valeur arrive")
    y = 70
    s.boite(35, y, 220, 130, "maj_valeur", "liaison_ha.yaml\naiguillage par préfixe", BLEU, B_BLEU)
    s.boite(310, y, 220, 130, "globals", "liaison_*\nvaleur, état, instant", VERT, B_VERT)
    s.boite(585, y, 240, 130, "*_rafraichir", "un script par page\nrecalcule tout", ORANGE, B_ORANGE)
    s.boite(875, y, 190, 130, "Widgets", "visibles ou non", GRIS)
    s.fleche([(255, y + 65), (310, y + 65)])
    s.fleche([(530, y + 65), (585, y + 65)])
    s.fleche([(825, y + 65), (875, y + 65)])
    s.boite(310, 270, 220, 120, "Péremption", "interval 30 s\nefface le groupe", ROUGE, B_ROUGE)
    s.fleche([(420, 270), (420, 200)], B_ROUGE)
    s.boite(585, 270, 240, 120, "Connexion", "interval 2 s\nliaison_connectee\nliaison_deconnectee", ORANGE, B_ORANGE)
    s.fleche([(705, 270), (705, 200)], B_ORANGE)
    s.zone(20, 440, 1060, 200, "Sortie : l'utilisateur touche l'écran")
    y = 490
    s.boite(35, y, 220, 130, "on_click", "bouton LVGL", BLEU, B_BLEU)
    s.boite(310, y, 220, 130, "Script de la page", "*_lancer, *_envoyer_*\nvérifie état et connexion", ORANGE, B_ORANGE)
    s.boite(585, y, 240, 130, "homeassistant.event", "esphome.hapanel_\ncommande", VERT, B_VERT)
    s.boite(875, y, 190, 130, "Blueprint", "vérifie, exécute", GRIS)
    s.fleche([(255, y + 65), (310, y + 65)])
    s.fleche([(530, y + 65), (585, y + 65)])
    s.fleche([(825, y + 65), (875, y + 65)])
    s.etiquette((550, 695), "La boucle se referme par HA : l'entité change, le blueprint envoie maj_valeur, la page se redessine.\nEn général, un script met à jour l'état puis appelle *_rafraichir, sans modifier lui-même les widgets.", DOUX)
    s.sauver("21_yaml_execution.png")


def sequences():
    sequence("16_blueprint_cycle.png", ["Administrateur", "Blueprint local", "Automatisation", "Moteur HA"], [
        ("Administrateur", "Blueprint local", "importe l'URL", B_BLEU),
        ("Blueprint local", None, "Fichier copié dans config/blueprints/automation/", JAUNE),
        ("Administrateur", "Automatisation", "remplit le formulaire", B_BLEU),
        ("Automatisation", None, "automations.yaml : use_blueprint, chemin et saisies", JAUNE),
        ("Automatisation", "Moteur HA", "modèle + saisies : !input remplacés", B_ORANGE),
        ("Moteur HA", None, "Écoute les déclencheurs,\ngarde une trace par exécution", VERT),
        (None, None, "Mise à jour", None),
        ("Administrateur", "Blueprint local", "réimporte", B_BLEU),
        ("Blueprint local", "Moteur HA", "fichier remplacé, automatisations rechargées", B_ORANGE),
        (None, None, "Suppression", None),
        ("Blueprint local", None, "Refusée tant qu'une automatisation l'utilise", ROUGE),
    ])
    sequence("05_connexion.png", ["Module", "API ESPHome", "Home Assistant", "Blueprint"], [
        ("Module", None, "Contrôle toutes les 2 s : un client dont le nom commence par « Home Assistant » (D013)", JAUNE),
        ("Home Assistant", "API ESPHome", "connexion chiffrée", B_ORANGE),
        ("API ESPHome", "Module", "client trouvé : ha_connecte_affiche = 1", TRAIT),
        ("Module", "Blueprint", "esphome.hapanel_demande_valeurs", B_BLEU),
        ("Blueprint", None, "Vérifie que l'événement vient de son panneau", ORANGE),
        ("Blueprint", "Module", "maj_valeur(...) pour toutes les clés", B_ORANGE),
        ("Module", None, "États à 1, pages redessinées", VERT),
        (None, None, "Connexion perdue", None),
        ("Module", None, "Client absent : valeurs effacées, états à 0,\nLED rouge clignotante, message de cause, écran rallumé", ROUGE),
    ])
    sequence("07_consigne.png", ["Utilisateur", "Module", "Blueprint", "Thermostat"], [
        ("Utilisateur", "Module", "touche + ou -", B_BLEU),
        ("Module", None, "Consigne cible en orange (pas de 0,5 °C, bornée) ; toute nouvelle pression relance 2 s", ORANGE),
        ("Module", "Blueprint", "hapanel_commande : chauffage_consigne", B_BLEU),
        ("Blueprint", None, "Panneau, chauffage allumé, verrou, bornes", ORANGE),
        ("Blueprint", "Thermostat", "climate.set_temperature", B_ORANGE),
        ("Thermostat", "Blueprint", "changement d'état (déclencheur)", B_VERT),
        ("Blueprint", "Module", "maj_valeur chauffage_consigne", B_ORANGE),
        ("Module", None, "Valeur réelle = cible : confirmation, affichage blanc", VERT),
        (None, None, "Sans confirmation en 10 s", None),
        ("Module", None, "Cible abandonnée : retour à la valeur réelle (journal WARN)", ROUGE),
    ])
    sequence("08_scenario.png", ["Utilisateur", "Module", "Blueprint", "Entité HA"], [
        ("Utilisateur", "Module", "touche le bouton N", B_BLEU),
        ("Module", None, "Vérifie connexion et état ; « Envoi en cours » ; boutons bloqués", ORANGE),
        ("Module", "Blueprint", "hapanel_commande : scenario, N", B_BLEU),
        ("Blueprint", None, "N donne scenario_N ; existe et n'est pas unavailable", ORANGE),
        ("Blueprint", "Entité HA", "turn_on ou automation.trigger", B_ORANGE),
        ("Blueprint", "Module", "maj_valeur scen_resultat = ok", B_VERT),
        ("Module", None, "« Lancé : nom » pendant 5 s", VERT),
        (None, None, "Autres issues", None),
        ("Blueprint", "Module", "scen_resultat = refus : « Refusé par HA »", B_ROUGE),
        ("Module", None, "Rien en 10 s : « Pas de réponse de HA » ; réponse tardive ignorée", ROUGE),
    ])


SORTIE.mkdir(parents=True, exist_ok=True)
contexte()
packages()
materiel()
flux()
sequences()
etats()
veille()
lumiere()
navigation()
build()
securite()
memoire()
blueprint_principe()
blueprint_execution()
blueprint_modules()
blueprint_structure()
yaml_matrice()
yaml_execution()
for fichier in sorted(SORTIE.glob("*.png")):
    print(fichier.name, fichier.stat().st_size // 1024, "Ko")
