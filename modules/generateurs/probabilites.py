# =============================================================
#  modules/generateurs/probabilites.py
# -------------------------------------------------------------
#  Génère des questions de probabilités, en 4 familles :
#    1-5   : probabilité simple (univers équiprobable)
#    6-10  : événement contraire
#    11-15 : deux événements indépendants (tirages avec remise)
#    16-20 : dénombrement (combinaisons)
# =============================================================

import math
import random


def generer_question(niveau: int, difficulte: float) -> dict:
    if niveau <= 5:
        total = random.randint(4, 10)
        favorables = random.randint(1, total - 1)
        reponse = round(favorables / total, 2)

        explication = f"P = (cas favorables) / (cas possibles) = {favorables}/{total} = {reponse}"
        texte = (f"Une urne contient {total} boules numérotées de 1 à {total}. "
                  f"Quelle est la probabilité de tirer un numéro parmi {favorables} numéros gagnants fixés à l'avance ?")
        return {"texte": texte, "reponse": reponse, "tolerance": 0.01, "explication": explication}

    elif niveau <= 10:
        total = random.randint(4, 10)
        favorables = random.randint(1, total - 1)
        reponse = round(1 - favorables / total, 2)

        explication = f"P(contraire) = 1 − P(événement) = 1 − {favorables}/{total} = {reponse}"
        texte = (f"La probabilité qu'un événement A se réalise est {favorables}/{total}. "
                  f"Quelle est la probabilité que A NE se réalise PAS ?")
        return {"texte": texte, "reponse": reponse, "tolerance": 0.01, "explication": explication}

    elif niveau <= 15:
        total = random.randint(2, 6)
        favorables1 = random.randint(1, total)
        favorables2 = random.randint(1, total)
        reponse = round((favorables1 / total) * (favorables2 / total), 3)

        explication = (f"Événements indépendants : P = P1 × P2 = "
                        f"({favorables1}/{total}) × ({favorables2}/{total}) = {reponse}")
        texte = (f"On tire au hasard, AVEC REMISE, 2 fois de suite dans un ensemble de {total} éléments équiprobables. "
                  f"Quelle est la probabilité d'obtenir un élément parmi {favorables1} favorables au 1er tirage, "
                  f"ET un élément parmi {favorables2} favorables au 2e tirage ?")
        return {"texte": texte, "reponse": reponse, "tolerance": 0.01, "explication": explication}

    else:
        n = random.randint(4, 10)
        k = random.randint(2, n - 1)
        reponse = math.comb(n, k)

        explication = f"Nombre de façons de choisir {k} éléments parmi {n} (sans tenir compte de l'ordre) = C({n},{k}) = {reponse}"
        texte = f"Combien y a-t-il de façons de choisir {k} éléments parmi {n} (l'ordre ne compte pas) ?"
        return {"texte": texte, "reponse": reponse, "tolerance": 0, "explication": explication}