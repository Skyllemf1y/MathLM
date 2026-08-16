# =============================================================
#  modules/question_generator.py
# -------------------------------------------------------------
#  Ce fichier est un "AIGUILLEUR" : il ne génère aucune question
#  lui-même. Il regarde quel générateur est associé au chapitre
#  demandé (voir config.py -> CHAPITRES) et lui délègue le travail.
# =============================================================

from config import CHAPITRES, difficulte
from modules.generateurs import arithmetique, equations, derivees, integrales, trigo

GENERATEURS = {
    "arithmetique": arithmetique,
    "equations": equations,
    "derivees": derivees,
    "integrales": integrales,
    "trigo": trigo,
}


def generer_question(chapitre_id: str, niveau: int) -> dict:
    """
    Génère une question pour un chapitre et un niveau donnés.
    Retourne toujours le même format, quel que soit le chapitre.
    """
    chap = CHAPITRES[chapitre_id]
    module_generateur = GENERATEURS[chap["generateur"]]

    diff = difficulte(chapitre_id, niveau)
    question = module_generateur.generer_question(niveau, diff)

    question["chapitre"] = chapitre_id
    question["niveau"] = niveau
    return question