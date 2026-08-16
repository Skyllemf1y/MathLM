# =============================================================
#  modules/generateurs/calcul.py
# -------------------------------------------------------------
#  Génère des questions de calcul (+ − × ÷), AVEC une explication
#  adaptée aux nombres tirés pour cette question précise.
# =============================================================

import random

SYMBOLES_AFFICHAGE = {"+": "+", "-": "−", "*": "×", "/": "÷"}


def generer_question(niveau: int, difficulte: float) -> dict:
    borne_max = max(10, int(difficulte))

    operations = ["+", "-"]
    if niveau >= 5:
        operations.append("*")
    if niveau >= 10:
        operations.append("/")

    operation = random.choice(operations)

    if operation == "+":
        a = random.randint(0, borne_max)
        b = random.randint(0, borne_max)
        reponse = a + b
        explication = f"{a} + {b} = {reponse}"

    elif operation == "-":
        a = random.randint(0, borne_max)
        b = random.randint(0, a)
        reponse = a - b
        explication = f"{a} − {b} = {reponse}"

    elif operation == "*":
        petite_borne = max(2, int(borne_max ** 0.5))
        a = random.randint(1, petite_borne)
        b = random.randint(1, petite_borne)
        reponse = a * b
        explication = f"{a} × {b} = {reponse}"

    else:
        petite_borne = max(2, int(borne_max ** 0.5))
        b = random.randint(1, petite_borne)
        reponse = random.randint(1, petite_borne)
        a = b * reponse
        explication = f"{a} ÷ {b} = {reponse}  (car {b} × {reponse} = {a})"

    return {
        "texte": f"{a} {SYMBOLES_AFFICHAGE[operation]} {b} = ?",
        "reponse": reponse,
        "tolerance": 0,
        "explication": explication,
    }