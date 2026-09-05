# =============================================================
#  modules/generateurs/suites.py
# -------------------------------------------------------------
#  Génère des questions sur les suites numériques, en 4 familles
#  selon le niveau :
#    1-5   : terme d'une suite ARITHMÉTIQUE (u_n = u0 + n×r)
#    6-10  : somme des n premiers termes d'une suite arithmétique
#    11-15 : terme d'une suite GÉOMÉTRIQUE (u_n = u0 × q^n)
#    16-20 : somme des n premiers termes d'une suite géométrique
# =============================================================

import random


def generer_question(niveau: int, difficulte: float) -> dict:
    borne = max(3, int(difficulte))

    if niveau <= 5:
        u0 = random.randint(-borne, borne)
        r = random.choice([x for x in range(-5, 6) if x != 0])
        n = random.randint(2, 10)
        reponse = u0 + n * r

        explication = f"u_n = u0 + n×r = {u0} + {n}×{r} = {reponse}"
        texte = f"Suite arithmétique : u0 = {u0}, raison r = {r}. Quelle est la valeur de u{n} ?"
        return {"texte": texte, "reponse": reponse, "tolerance": 0, "explication": explication}

    elif niveau <= 10:
        u0 = random.randint(0, borne)
        r = random.randint(1, 5)
        n = random.randint(3, 10)
        dernier_terme = u0 + (n - 1) * r
        reponse = round(n * (u0 + dernier_terme) / 2, 2)

        explication = f"S = n×(u0 + u{n-1})/2 = {n}×({u0} + {dernier_terme})/2 = {reponse}"
        texte = f"Suite arithmétique : u0 = {u0}, raison r = {r}. Quelle est la somme u0 + u1 + ... + u{n-1} ({n} termes) ?"
        return {"texte": texte, "reponse": reponse, "tolerance": 0.01, "explication": explication}

    elif niveau <= 15:
        u0 = random.randint(1, max(2, borne // 2))
        q = random.choice([2, 3, -2, -3])
        n = random.randint(2, 5)
        reponse = u0 * (q ** n)

        explication = f"u_n = u0 × q^n = {u0} × {q}^{n} = {reponse}"
        texte = f"Suite géométrique : u0 = {u0}, raison q = {q}. Quelle est la valeur de u{n} ?"
        return {"texte": texte, "reponse": reponse, "tolerance": 0, "explication": explication}

    else:
        u0 = random.randint(1, max(2, borne // 2))
        q = random.choice([2, 3, -2])
        n = random.randint(3, 6)
        reponse = round(u0 * (1 - q ** n) / (1 - q), 2)

        explication = f"S = u0×(1−q^n)/(1−q) = {u0}×(1−{q}^{n})/(1−{q}) = {reponse}"
        texte = f"Suite géométrique : u0 = {u0}, raison q = {q}. Quelle est la somme des {n} premiers termes ?"
        return {"texte": texte, "reponse": reponse, "tolerance": 0.01, "explication": explication}