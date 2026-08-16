# =============================================================
#  modules/generateurs/trigo.py
# =============================================================

import math
import random

ANGLES_IDENTITES = [0, 30, 45, 60, 90, 120, 135, 150, 180,
                     210, 225, 240, 270, 300, 315, 330, 360]

ANGLES_EQUATION_SIN = [0, 30, 45, 60, 90]
ANGLES_EQUATION_COS = [0, 30, 45, 60, 90, 120, 135, 150, 180]

SIN_EXACT = {
    0: "0", 30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1",
    120: "√3/2", 135: "√2/2", 150: "1/2", 180: "0",
    210: "−1/2", 225: "−√2/2", 240: "−√3/2", 270: "−1",
    300: "−√3/2", 315: "−√2/2", 330: "−1/2", 360: "0",
}
COS_EXACT = {
    0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0",
    120: "−1/2", 135: "−√2/2", 150: "−√3/2", 180: "−1",
    210: "−√3/2", 225: "−√2/2", 240: "−1/2", 270: "0",
    300: "1/2", 315: "√2/2", 330: "√3/2", 360: "1",
}
TAN_EXACT = {
    0: "0", 30: "√3/3", 45: "1", 60: "√3", 120: "−√3", 135: "−1",
    150: "−√3/3", 180: "0", 210: "√3/3", 225: "1", 240: "√3",
    300: "−√3", 315: "−1", 330: "−√3/3", 360: "0",
}

VALEURS_EXACTES = {"sin": SIN_EXACT, "cos": COS_EXACT, "tan": TAN_EXACT}


def _valeur(fonction: str, angle_degres: int) -> float:
    angle_rad = math.radians(angle_degres)
    if fonction == "sin":
        v = math.sin(angle_rad)
    elif fonction == "cos":
        v = math.cos(angle_rad)
    else:
        v = math.tan(angle_rad)
    return round(v, 4)


def generer_question(niveau: int, difficulte: float) -> dict:
    if niveau < 11:
        index_max = min(len(ANGLES_IDENTITES) - 1, max(4, int(difficulte)))
        angles_disponibles = ANGLES_IDENTITES[:index_max + 1]

        angle = random.choice(angles_disponibles)
        fonctions_possibles = ["sin", "cos"] if angle in (90, 270) else ["sin", "cos", "tan"]
        fonction = random.choice(fonctions_possibles)

        reponse = _valeur(fonction, angle)
        valeur_exacte = VALEURS_EXACTES[fonction].get(angle, str(reponse))

        explication = (
            f"{fonction}({angle}°) = {valeur_exacte}  "
            f"(valeur remarquable à connaître par cœur -- revois le cours si besoin)"
        )

        return {
            "texte": f"{fonction}({angle}°) = ?",
            "reponse": reponse,
            "tolerance": 0.01,
            "explication": explication,
        }

    else:
        fonction = random.choice(["sin", "cos"])

        if fonction == "sin":
            angle_base = random.choice(ANGLES_EQUATION_SIN)
            valeur_texte = SIN_EXACT[angle_base]
        else:
            angle_base = random.choice(ANGLES_EQUATION_COS)
            valeur_texte = COS_EXACT[angle_base]

        explication = (
            f"{fonction}(x) = {valeur_texte} correspond à l'angle remarquable {angle_base}°, "
            f"qui est bien la plus petite solution positive."
        )

        return {
            "texte": f"{fonction}(x) = {valeur_texte}   —   quelle est la plus petite solution positive (en degrés, entre 0° et 360°) ?",
            "reponse": angle_base,
            "tolerance": 0.5,
            "explication": explication,
        }