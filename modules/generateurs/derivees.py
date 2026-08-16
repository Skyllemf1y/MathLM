# =============================================================
#  modules/generateurs/derivees.py
# =============================================================

import random
from modules.generateurs.utils import en_exposant


def _formater_monome(a: int, n: int, est_premier: bool) -> str:
    if n == 0:
        base = ""
    elif n == 1:
        base = "x"
    else:
        base = f"x{en_exposant(n)}"

    if base == "":
        if est_premier:
            return f"{a}"
        signe = "-" if a < 0 else "+"
        return f" {signe} {abs(a)}"

    coeff = "" if abs(a) == 1 else str(abs(a))
    if est_premier:
        signe = "-" if a < 0 else ""
        return f"{signe}{coeff}{base}"
    else:
        signe = "-" if a < 0 else "+"
        return f" {signe}{coeff}{base}"


def generer_question(niveau: int, difficulte: float) -> dict:
    nb_termes = 1
    if niveau >= 8:
        nb_termes = 2
    if niveau >= 15:
        nb_termes = 3

    exposant_max = min(6, max(1, int(difficulte)))

    termes = []
    for _ in range(nb_termes):
        a = random.choice([x for x in range(-5, 6) if x != 0])
        n = random.randint(1, exposant_max)
        termes.append((a, n))

    x0 = random.choice([-2, -1, 1, 2])

    f_texte = "".join(
        _formater_monome(a, n, est_premier=(i == 0))
        for i, (a, n) in enumerate(termes)
    )

    termes_derivee = [(a * n, n - 1) for a, n in termes]
    f_prime_texte = "".join(
        _formater_monome(a2, n2, est_premier=(i == 0))
        for i, (a2, n2) in enumerate(termes_derivee)
    )

    reponse = sum(a2 * (x0 ** n2) for a2, n2 in termes_derivee)

    explication = (
        f"f'(x) = {f_prime_texte}   (règle : dérivée de a·xⁿ = a·n·xⁿ⁻¹, appliquée à chaque terme)   →   "
        f"f'({x0}) = {reponse}"
    )

    return {
        "texte": f"f(x) = {f_texte}   —   quelle est f'({x0}) ?",
        "reponse": reponse,
        "tolerance": 0,
        "explication": explication,
    }