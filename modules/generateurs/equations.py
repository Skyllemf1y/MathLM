# =============================================================
#  modules/generateurs/equations.py
# =============================================================

import random


def _formatter_terme(b: int) -> str:
    return f"+ {b}" if b >= 0 else f"- {abs(b)}"


def generer_question(niveau: int, difficulte: float) -> dict:
    borne = max(3, int(difficulte))
    a = random.randint(1, max(2, borne // 2))
    b = random.randint(-borne, borne)

    if niveau < 10:
        x_solution = random.randint(-borne, borne)
        c = a * x_solution + b
        c_moins_b = c - b

        explication = (
            f"{a}x {_formatter_terme(b)} = {c}   →   "
            f"on isole d'abord le terme en x : {a}x = {c_moins_b}   →   "
            f"puis on divise par {a} : x = {x_solution}"
        )

        return {
            "texte": f"Résous : {a}x {_formatter_terme(b)} = {c}  (donne la valeur de x)",
            "reponse": x_solution,
            "tolerance": 0,
            "explication": explication,
        }

    else:
        frontiere = random.randint(-borne, borne)
        c = a * frontiere + b
        sens = random.choice([">", "<"])
        c_moins_b = c - b

        if sens == ">":
            reponse = frontiere + 1
            consigne = "la plus petite valeur entière"
        else:
            reponse = frontiere - 1
            consigne = "la plus grande valeur entière"

        explication = (
            f"{a}x {_formatter_terme(b)} {sens} {c}   →   "
            f"{a}x {sens} {c_moins_b}   →   "
            f"x {sens} {frontiere}  (÷ par {a}, positif, donc le sens ne change pas)   →   "
            f"{consigne} qui convient : {reponse}"
        )

        return {
            "texte": f"Résous : {a}x {_formatter_terme(b)} {sens} {c}  (donne {consigne} de x qui convient)",
            "reponse": reponse,
            "tolerance": 0,
            "explication": explication,
        }