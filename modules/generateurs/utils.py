# =============================================================
#  modules/generateurs/utils.py
# -------------------------------------------------------------
#  Petites fonctions PARTAGÉES entre plusieurs générateurs
#  (dérivées, intégrales...) pour afficher de vrais symboles
#  mathématiques au lieu de texte brut ("x^2" -> "x²").
# =============================================================

_CHIFFRES_EXPOSANT = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
                       "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
                       "-": "⁻"}

_CHIFFRES_INDICE = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
                     "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
                     "-": "₋"}


def en_exposant(nombre) -> str:
    """Convertit un nombre en chiffres 'exposant' unicode (ex: 12 -> '¹²')."""
    return "".join(_CHIFFRES_EXPOSANT[c] for c in str(nombre))


def en_indice(nombre) -> str:
    """Convertit un nombre en chiffres 'indice' unicode (ex: -3 -> '₋₃')."""
    return "".join(_CHIFFRES_INDICE[c] for c in str(nombre))