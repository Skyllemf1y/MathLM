from config import CHAPITRES, RANGS
from modules.progression import dernier_niveau_valide, meilleure_note_test, cours_est_vu
from modules.streak import obtenir_streak
from modules.personalization import obtenir_profil
from modules.challenge import obtenir_meilleur_score_challenge


def calculer_badges(pseudo: str) -> list:
    profil = obtenir_profil(pseudo)
    streak = obtenir_streak(pseudo)
    seuil_or = next(r["seuil"] for r in RANGS if r["nom"] == "Or")

    badges = [
        {"id": "premier_pas", "nom": "Premier pas", "icone": "👣",
         "description": "Valider ton tout premier niveau.",
         "obtenu": any(dernier_niveau_valide(pseudo, cid) >= 1 for cid in CHAPITRES)},
        {"id": "sans_faute", "nom": "Sans faute", "icone": "💯",
         "description": "Obtenir 100% à un test de chapitre.",
         "obtenu": any(meilleure_note_test(pseudo, cid) == 100 for cid in CHAPITRES)},
        {"id": "bibliothecaire", "nom": "Bibliothécaire", "icone": "📚",
         "description": "Consulter le cours de chaque chapitre.",
         "obtenu": all(cours_est_vu(pseudo, cid) for cid in CHAPITRES)},
        {"id": "semaine_de_suite", "nom": "Une semaine de suite", "icone": "🔥",
         "description": "Atteindre une série de 7 jours.",
         "obtenu": streak["meilleure_streak"] >= 7},
        {"id": "medaille_or", "nom": "Médaille d'or", "icone": "🥇",
         "description": "Atteindre le rang Or.",
         "obtenu": profil["score_total"] >= seuil_or},
        {"id": "maitre_chapitre", "nom": "Maître d'un chapitre", "icone": "🎓",
         "description": "Terminer tous les niveaux d'un chapitre.",
         "obtenu": any(dernier_niveau_valide(pseudo, cid) >= CHAPITRES[cid]["nb_niveaux"] for cid in CHAPITRES)},
        {"id": "tout_termine", "nom": "MathLM terminé", "icone": "👑",
         "description": "Terminer tous les niveaux de tous les chapitres.",
         "obtenu": all(dernier_niveau_valide(pseudo, cid) >= CHAPITRES[cid]["nb_niveaux"] for cid in CHAPITRES)},
        {"id": "increvable", "nom": "Increvable", "icone": "🎲",
         "description": "Atteindre 200 points en mode Challenge infini.",
         "obtenu": obtenir_meilleur_score_challenge(pseudo) >= 200},
    ]

    return badges