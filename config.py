NOM_APPLICATION = "MathLM"

VIES_INITIALES = 3
POINTS_PAR_BONNE_REPONSE = 10
NB_QUESTIONS_PAR_NIVEAU = 10
NB_QUESTIONS_TEST = 20

# Pseudos ayant accès à la page /admin/stats -- REMPLACE PAR TON VRAI PSEUDO
PSEUDOS_ADMIN = ["Skyllem.dev"]

RANGS = [
    {"nom": "Bronze", "icone": "🥉", "seuil": 0},
    {"nom": "Argent", "icone": "🥈", "seuil": 300},
    {"nom": "Or", "icone": "🥇", "seuil": 800},
    {"nom": "Platine", "icone": "💎", "seuil": 2000},
    {"nom": "Diamant", "icone": "👑", "seuil": 5000},
]

CHAPITRES = {
    "arithmetique": {
        "nom": "Arithmétique", "nb_niveaux": 20, "generateur": "arithmetique",
        "base_difficulte": 5, "taux_croissance": 1.15,
    },
    "equations": {
        "nom": "Équations et inéquations", "nb_niveaux": 20, "generateur": "equations",
        "base_difficulte": 2, "taux_croissance": 1.20,
    },
    "derivees": {
        "nom": "Dérivées", "nb_niveaux": 20, "generateur": "derivees",
        "base_difficulte": 1, "taux_croissance": 1.12,
    },
    "integrales": {
        "nom": "Intégrales", "nb_niveaux": 20, "generateur": "integrales",
        "base_difficulte": 1, "taux_croissance": 1.12,
    },
    "trigonometrie": {
        "nom": "Trigonométrie", "nb_niveaux": 20, "generateur": "trigo",
        "base_difficulte": 4, "taux_croissance": 1.08,
    },
    "suites": {
        "nom": "Suites numériques", "nb_niveaux": 20, "generateur": "suites",
        "base_difficulte": 5, "taux_croissance": 1.12,
    },
    "probabilites": {
        "nom": "Probabilités", "nb_niveaux": 20, "generateur": "probabilites",
        "base_difficulte": 5, "taux_croissance": 1.10,
    },
}


def difficulte(chapitre_id: str, niveau: int) -> float:
    chap = CHAPITRES[chapitre_id]
    return chap["base_difficulte"] * (chap["taux_croissance"] ** niveau)