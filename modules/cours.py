# =============================================================
#  modules/cours.py
# -------------------------------------------------------------
#  Contient le CONTENU PÉDAGOGIQUE (théorie) et les QCM de
#  chaque chapitre.
#
#  CHOIX DE CONCEPTION : contrairement aux questions d'entraînement
#  (générées aléatoirement à l'infini par modules/generateurs/...),
#  le cours et son QCM sont un contenu FIXE, écrit à la main. On ne
#  peut pas "générer" une explication de théorie au hasard -- ça
#  doit être rédigé avec soin. Le QCM sert juste de "quiz de
#  compréhension" : il n'est pas lié au système de vies/score, il
#  est corrigé directement dans le navigateur (voir static/js/cours.js).
#
#  Structure de chaque chapitre :
#    - "titre"       : titre de la leçon
#    - "paragraphes" : liste de paragraphes de texte (théorie)
#    - "exemple"     : un exemple concret pour illustrer
#    - "qcm"         : liste de questions, chacune avec :
#         - "question"      : l'énoncé
#         - "choix"         : liste de 4 réponses possibles
#         - "bonne_reponse" : index (0 à 3) de la bonne réponse dans "choix"
# =============================================================

COURS = {
    "arithmetique": {
        "titre": "La priorité des opérations",
        "paragraphes": [
            "En arithmétique, un calcul peut contenir plusieurs opérations "
            "différentes (+, −, ×, ÷). Pour que tout le monde trouve le même "
            "résultat, on suit toujours le même ordre de priorité.",
            "Règle : la multiplication et la division sont toujours calculées "
            "AVANT l'addition et la soustraction, même si elles apparaissent "
            "plus loin dans le calcul.",
            "Si des parenthèses sont présentes, leur contenu est toujours "
            "calculé en premier, avant tout le reste.",
            "Quand plusieurs opérations de même priorité se suivent (ex: "
            "seulement des + et des −), on les calcule de gauche à droite.",
        ],
        "exemple": "2 + 3 × 4 = 2 + 12 = 14  (la multiplication d'abord, pas l'addition)",
        "qcm": [
            {
                "question": "Quel est le résultat de 2 + 3 × 4 ?",
                "choix": ["20", "14", "24", "9"],
                "bonne_reponse": 1,
            },
            {
                "question": "Que fait une parenthèse dans un calcul ?",
                "choix": [
                    "Rien de spécial",
                    "Elle indique ce qui doit être calculé en priorité",
                    "Elle multiplie automatiquement",
                    "Elle sert de virgule",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Dans quel ordre calcule-t-on 10 − 4 + 2 ?",
                "choix": [
                    "De gauche à droite : (10 − 4) + 2",
                    "De droite à gauche : 10 − (4 + 2)",
                    "L'addition d'abord, dans tous les cas",
                    "On ne peut pas savoir",
                ],
                "bonne_reponse": 0,
            },
            {
                "question": "Combien font 5 × (2 + 3) ?",
                "choix": ["13", "25", "10", "17"],
                "bonne_reponse": 1,
            },
            {
                "question": "Laquelle de ces opérations est prioritaire sur l'addition ?",
                "choix": ["Aucune, elles sont égales", "La division", "Rien n'est prioritaire", "Seule la parenthèse compte"],
                "bonne_reponse": 1,
            },
        ],
    },

    "equations": {
        "titre": "Équations et inéquations",
        "paragraphes": [
            "Une équation est une égalité qui contient une inconnue (souvent "
            "notée x). \"Résoudre\" une équation, c'est trouver la (ou les) "
            "valeur(s) de x qui rendent l'égalité vraie.",
            "Règle d'or : pour garder une équation vraie, toute opération "
            "effectuée d'un côté du signe = doit aussi être effectuée de "
            "l'autre côté.",
            "Une inéquation ressemble à une équation, mais avec un symbole "
            "d'ordre (<, >, ≤ ou ≥) à la place du =. Elle a en général une "
            "infinité de solutions (un intervalle), pas une seule valeur.",
            "Point important : si on multiplie ou divise les deux côtés d'une "
            "inéquation par un nombre NÉGATIF, le sens de l'inégalité "
            "s'inverse (un < devient un >, et inversement).",
        ],
        "exemple": "3x + 2 = 11  →  3x = 9  →  x = 3",
        "qcm": [
            {
                "question": "Que signifie \"résoudre une équation\" ?",
                "choix": [
                    "Dessiner un graphique",
                    "Trouver la valeur de l'inconnue qui vérifie l'égalité",
                    "Simplifier l'écriture sans but précis",
                    "Additionner tous les nombres présents",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Si on multiplie les deux côtés d'une inéquation par un nombre négatif, que se passe-t-il ?",
                "choix": [
                    "Rien ne change",
                    "Le sens de l'inégalité s'inverse",
                    "L'inéquation devient une équation",
                    "Ce n'est pas autorisé",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Dans 3x + 2 = 11, que vaut x ?",
                "choix": ["2", "3", "9", "11"],
                "bonne_reponse": 1,
            },
            {
                "question": "Une inéquation utilise quel genre de symbole ?",
                "choix": ["=", "< > ≤ ≥", "+/−", "%"],
                "bonne_reponse": 1,
            },
            {
                "question": "Une équation a en général combien de solutions ?",
                "choix": [
                    "Toujours zéro",
                    "Une infinité, toujours",
                    "Un nombre précis (souvent une seule valeur)",
                    "Cela n'a pas de sens",
                ],
                "bonne_reponse": 2,
            },
        ],
    },

    "derivees": {
        "titre": "Les dérivées",
        "paragraphes": [
            "La dérivée d'une fonction en un point mesure sa VITESSE DE "
            "VARIATION à cet endroit précis : est-ce que la fonction monte "
            "vite, lentement, ou est-elle stable ?",
            "Géométriquement, la dérivée en un point correspond à la pente "
            "de la tangente à la courbe en ce point.",
            "On note la dérivée d'une fonction f par f' (on dit \"f prime\").",
            "Règle essentielle (pour les monômes) : la dérivée de a·xⁿ est "
            "a·n·xⁿ⁻¹. Par exemple, la dérivée de x² est 2x, et la dérivée "
            "d'une constante (comme 5) est toujours 0.",
        ],
        "exemple": "f(x) = 3x²  →  f'(x) = 6x  →  donc f'(2) = 12",
        "qcm": [
            {
                "question": "La dérivée d'une fonction représente...",
                "choix": [
                    "Sa valeur maximale",
                    "Sa vitesse de variation (pente de la tangente)",
                    "Son aire sous la courbe",
                    "Le nombre de solutions de f(x) = 0",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "La dérivée de xⁿ est...",
                "choix": ["xⁿ⁺¹/(n+1)", "n·xⁿ⁻¹", "n·x", "xⁿ"],
                "bonne_reponse": 1,
            },
            {
                "question": "La dérivée d'une constante (ex: 7) est...",
                "choix": ["7", "1", "0", "Cela dépend de x"],
                "bonne_reponse": 2,
            },
            {
                "question": "Comment note-t-on la dérivée d'une fonction f ?",
                "choix": ["f²", "f'", "f⁻¹", "∫f"],
                "bonne_reponse": 1,
            },
            {
                "question": "La dérivée de 3x² est...",
                "choix": ["3x", "6x", "x²", "9x"],
                "bonne_reponse": 1,
            },
        ],
    },

    "integrales": {
        "titre": "Les intégrales",
        "paragraphes": [
            "L'intégration est en quelque sorte l'opération INVERSE de la "
            "dérivation. Une primitive d'une fonction f est une fonction "
            "dont la dérivée redonne exactement f.",
            "Une intégrale DÉFINIE, notée avec deux bornes (par exemple entre "
            "a et b), calcule l'AIRE sous la courbe de la fonction, entre "
            "ces deux bornes.",
            "Le symbole utilisé pour une intégrale est ∫ (un \"S\" allongé, "
            "pour \"Somme\" — l'aire est vue comme une somme de toutes petites "
            "tranches).",
            "Règle essentielle : la primitive de xⁿ est xⁿ⁺¹/(n+1). C'est "
            "exactement la règle inverse de celle des dérivées.",
        ],
        "exemple": "∫ de 0 à 3 de (2x) dx = [x²] de 0 à 3 = 9 − 0 = 9",
        "qcm": [
            {
                "question": "Une primitive d'une fonction f est...",
                "choix": [
                    "Une fonction plus simple que f",
                    "Une fonction dont la dérivée redonne f",
                    "La valeur maximale de f",
                    "L'inverse mathématique 1/f",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "Une intégrale définie (avec bornes) calcule...",
                "choix": [
                    "La pente de la courbe",
                    "L'aire sous la courbe entre deux valeurs",
                    "Le nombre de solutions de l'équation",
                    "La valeur de f en un seul point",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "La primitive de xⁿ est...",
                "choix": ["n·xⁿ⁻¹", "xⁿ⁺¹/(n+1)", "xⁿ", "1/xⁿ"],
                "bonne_reponse": 1,
            },
            {
                "question": "Le symbole ∫ représente...",
                "choix": ["Une dérivée", "Une intégrale", "Une inéquation", "Un angle"],
                "bonne_reponse": 1,
            },
            {
                "question": "Intégrale et dérivée sont deux opérations...",
                "choix": ["Identiques", "Inverses l'une de l'autre", "Sans aucun lien", "Réservées à la trigonométrie"],
                "bonne_reponse": 1,
            },
        ],
    },

    "trigonometrie": {
        "titre": "La trigonométrie",
        "paragraphes": [
            "La trigonométrie étudie les relations entre les angles et les "
            "longueurs dans un triangle rectangle, à l'aide de 3 fonctions : "
            "sinus (sin), cosinus (cos) et tangente (tan).",
            "Dans un triangle rectangle : le cosinus d'un angle est le "
            "rapport (côté adjacent / hypoténuse), et le sinus est le "
            "rapport (côté opposé / hypoténuse).",
            "La tangente se calcule à partir des deux autres : "
            "tan(angle) = sin(angle) / cos(angle).",
            "Le \"cercle trigonométrique\" est un cercle de rayon 1 qui "
            "permet de visualiser sin et cos pour n'importe quel angle, "
            "même au-delà de 90° (jusqu'à 360° et plus).",
        ],
        "exemple": "sin(30°) = 1/2   et   cos(60°) = 1/2   (ces 2 angles sont complémentaires : 30° + 60° = 90°)",
        "qcm": [
            {
                "question": "Dans un triangle rectangle, le cosinus d'un angle est le rapport...",
                "choix": [
                    "opposé / hypoténuse",
                    "adjacent / hypoténuse",
                    "opposé / adjacent",
                    "hypoténuse / adjacent",
                ],
                "bonne_reponse": 1,
            },
            {
                "question": "sin(90°) vaut...",
                "choix": ["0", "1", "0.5", "Cela n'existe pas"],
                "bonne_reponse": 1,
            },
            {
                "question": "cos(0°) vaut...",
                "choix": ["0", "1", "-1", "0.5"],
                "bonne_reponse": 1,
            },
            {
                "question": "La tangente d'un angle est égale à...",
                "choix": ["sin × cos", "sin / cos", "cos / sin", "sin + cos"],
                "bonne_reponse": 1,
            },
            {
                "question": "Le cercle trigonométrique a pour rayon...",
                "choix": ["0", "1", "90", "360"],
                "bonne_reponse": 1,
            },
        ],
    },
        "suites": {
        "titre": "Les suites numériques",
        "paragraphes": [
            "Une suite numérique est une liste ordonnée de nombres (u0, u1, u2, ...), où chaque terme porte un indice qui indique sa position.",
            "Une suite est dite ARITHMÉTIQUE quand on passe d'un terme au suivant en ajoutant toujours le même nombre, appelé la raison (notée r). Formule du terme général : u_n = u0 + n×r.",
            "Une suite est dite GÉOMÉTRIQUE quand on passe d'un terme au suivant en multipliant toujours par le même nombre, la raison (notée q). Formule du terme général : u_n = u0 × q^n.",
            "Pour calculer la somme des n premiers termes, pas besoin d'additionner un par un : il existe une formule directe, différente pour une suite arithmétique et pour une suite géométrique.",
        ],
        "exemple": "Suite arithmétique u0 = 2, r = 3 → u1 = 5, u2 = 8, u3 = 11 (on ajoute toujours 3)",
        "qcm": [
            {"question": "Qu'est-ce qui caractérise une suite arithmétique ?", "choix": ["On multiplie toujours par le même nombre", "On ajoute toujours le même nombre", "Les termes sont toujours positifs", "Il n'y a pas de règle fixe"], "bonne_reponse": 1},
            {"question": "Quelle est la formule du terme général d'une suite arithmétique ?", "choix": ["u_n = u0 × n × r", "u_n = u0 + n×r", "u_n = u0^n", "u_n = u0 / n"], "bonne_reponse": 1},
            {"question": "Qu'est-ce qui caractérise une suite géométrique ?", "choix": ["On ajoute toujours le même nombre", "On multiplie toujours par le même nombre", "Les termes diminuent toujours", "Il n'y a pas de règle fixe"], "bonne_reponse": 1},
            {"question": "Si u0 = 3 et la raison arithmétique r = 4, que vaut u2 ?", "choix": ["7", "11", "12", "9"], "bonne_reponse": 1},
            {"question": "Pour calculer la somme des n premiers termes d'une suite, on...", "choix": ["additionne obligatoirement un par un", "utilise une formule directe", "ne peut pas la calculer", "multiplie le premier par le dernier"], "bonne_reponse": 1},
        ],
    },

    "probabilites": {
        "titre": "Introduction aux probabilités",
        "paragraphes": [
            "La probabilité d'un événement mesure ses chances de se réaliser : un nombre entre 0 (impossible) et 1 (certain).",
            "Dans un UNIVERS ÉQUIPROBABLE (tous les résultats ont la même chance de se produire), on calcule une probabilité avec : P(événement) = (nombre de cas favorables) / (nombre de cas possibles).",
            "La probabilité de l'ÉVÉNEMENT CONTRAIRE (que ça ne se produise PAS) vaut toujours 1 moins la probabilité de l'événement : P(non A) = 1 − P(A).",
            "Pour deux événements INDÉPENDANTS (l'un n'influence pas l'autre, comme 2 tirages avec remise), la probabilité qu'ils se produisent tous les deux est le PRODUIT de leurs probabilités.",
            "DÉNOMBRER, c'est compter le nombre de façons de choisir des éléments dans un ensemble — utile pour calculer des probabilités sur de grands ensembles.",
        ],
        "exemple": "Un dé à 6 faces : P(obtenir un nombre pair) = 3/6 = 0.5 (3 cas favorables : 2, 4, 6 ; sur 6 cas possibles)",
        "qcm": [
            {"question": "Une probabilité est toujours un nombre compris entre...", "choix": ["-1 et 1", "0 et 1", "0 et 100", "1 et 10"], "bonne_reponse": 1},
            {"question": "Dans un univers équiprobable, comment calcule-t-on une probabilité ?", "choix": ["cas favorables × cas possibles", "cas favorables / cas possibles", "cas possibles / cas favorables", "cas favorables + cas possibles"], "bonne_reponse": 1},
            {"question": "La probabilité de l'événement contraire de A vaut...", "choix": ["P(A)", "1 − P(A)", "1 + P(A)", "P(A) / 2"], "bonne_reponse": 1},
            {"question": "Pour 2 événements indépendants A et B, P(A et B) = ?", "choix": ["P(A) + P(B)", "P(A) × P(B)", "P(A) − P(B)", "P(A) / P(B)"], "bonne_reponse": 1},
            {"question": "Dénombrer signifie...", "choix": ["Calculer une moyenne", "Compter le nombre de façons de choisir des éléments", "Trouver la probabilité maximale", "Trier des nombres"], "bonne_reponse": 1},
        ],
    },
}