# =============================================================
#  modules/generateurs/integrales.py
# =============================================================

import random
from modules.generateurs.utils import en_exposant, en_indice


def _formater_monome(a: int, n: int, est_premier: bool) -> str:
    base = "x" if n == 1 else f"x{en_exposant(n)}"
    coeff = "" if abs(a) == 1 else str(abs(a))
    if est_premier:
        signe = "−" if a < 0 else ""
        return f"{signe}{coeff}{base}"
    else:
        signe = "−" if a < 0 else "+"
        return f" {signe} {coeff}{base}"


def _formater_terme_primitive(a: int, n: int, est_premier: bool) -> str:
    exposant = n + 1
    base = "x" if exposant == 1 else f"x{en_exposant(exposant)}"
    fraction = f"{abs(a)}/{exposant}"

    if est_premier:
        signe = "−" if a < 0 else ""
        return f"{signe}({fraction}){base}"
    else:
        signe = "−" if a < 0 else "+"
        return f" {signe} ({fraction}){base}"


def generer_question(niveau: int, difficulte: float) -> dict:
    nb_termes = 1 if niveau < 12 else 2
    exposant_max = min(4, max(1, int(difficulte)))

    termes = []
    for _ in range(nb_termes):
        a = random.choice([x for x in range(-5, 6) if x != 0])
        n = random.randint(1, exposant_max)
        termes.append((a, n))

    p, q = sorted(random.sample(range(-3, 4), 2))

    f_texte = "".join(
        _formater_monome(a, n, est_premier=(i == 0))
        for i, (a, n) in enumerate(termes)
    )

    reponse = sum(
        (a / (n + 1)) * (q ** (n + 1) - p ** (n + 1))
        for a, n in termes
    )
    reponse = round(reponse, 2)

    primitive_texte = "".join(
        _formater_terme_primitive(a, n, est_premier=(i == 0))
        for i, (a, n) in enumerate(termes)
    )

    symbole_integrale = f"∫{en_indice(p)}{en_exposant(q)}"

    explication = (
        f"Primitive : F(x) = {primitive_texte}   →   "
        f"F({q}) − F({p}) = {reponse}"
    )

    return {
        "texte": f"{symbole_integrale} ({f_texte}) dx = ?",
        "reponse": reponse,
        "tolerance": 0.05,
        "explication": explication,
    }