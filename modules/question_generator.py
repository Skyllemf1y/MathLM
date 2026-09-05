from config import CHAPITRES, difficulte
from modules.generateurs import arithmetique, equations, derivees, integrales, trigo, suites, probabilites

GENERATEURS = {
    "arithmetique": arithmetique,
    "equations": equations,
    "derivees": derivees,
    "integrales": integrales,
    "trigo": trigo,
    "suites": suites,
    "probabilites": probabilites,
}


def generer_question(chapitre_id: str, niveau: int) -> dict:
    chap = CHAPITRES[chapitre_id]
    module_generateur = GENERATEURS[chap["generateur"]]
    diff = difficulte(chapitre_id, niveau)
    question = module_generateur.generer_question(niveau, diff)
    question["chapitre"] = chapitre_id
    question["niveau"] = niveau
    return question