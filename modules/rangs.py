# =============================================================
#  modules/rangs.py
# -------------------------------------------------------------
#  Calcule le RANG d'un joueur (Bronze, Argent, Or...) à partir
#  de son score total. Les paliers sont définis dans config.py.
# =============================================================

from config import RANGS


def obtenir_rang(score_total: int) -> dict:
    rang_actuel = RANGS[0]
    for rang in RANGS:
        if score_total >= rang["seuil"]:
            rang_actuel = rang
    return rang_actuel


def obtenir_rang_suivant(score_total: int):
    for rang in RANGS:
        if score_total < rang["seuil"]:
            return rang
    return None


def progression_vers_rang_suivant(score_total: int) -> dict:
    rang_actuel = obtenir_rang(score_total)
    rang_suivant = obtenir_rang_suivant(score_total)

    if rang_suivant is None:
        return {"rang_suivant": None, "pourcentage": 100}

    points_dans_palier = score_total - rang_actuel["seuil"]
    largeur_palier = rang_suivant["seuil"] - rang_actuel["seuil"]
    pourcentage = round(100 * points_dans_palier / largeur_palier) if largeur_palier > 0 else 100

    return {"rang_suivant": rang_suivant, "pourcentage": pourcentage}