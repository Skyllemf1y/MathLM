import json
import os

from modules.stockage_joueur import chemin_fichier_joueur
from modules.classement import mettre_a_jour_classement
from modules.invite import est_invite

AVATARS_DISPONIBLES = ["🦉", "🦊", "🐱", "🐼", "🦁", "🐸", "🤖", "🧮"]
PROFIL_PAR_DEFAUT = {"avatar": "🦉", "score_total": 0}


def obtenir_profil(pseudo: str) -> dict:
    chemin = chemin_fichier_joueur(pseudo, "profil.json")
    if not os.path.exists(chemin):
        data = dict(PROFIL_PAR_DEFAUT)
    else:
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)

    return {
        "pseudo": pseudo,
        "avatar": data.get("avatar", PROFIL_PAR_DEFAUT["avatar"]),
        "score_total": data.get("score_total", 0),
    }


def _sauvegarder_fichier(pseudo: str, avatar: str, score_total: int):
    chemin = chemin_fichier_joueur(pseudo, "profil.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump({"avatar": avatar, "score_total": score_total}, f, ensure_ascii=False, indent=2)


def sauvegarder_avatar(pseudo: str, avatar: str):
    profil_actuel = obtenir_profil(pseudo)
    if avatar not in AVATARS_DISPONIBLES:
        avatar = PROFIL_PAR_DEFAUT["avatar"]

    _sauvegarder_fichier(pseudo, avatar, profil_actuel["score_total"])
    if not est_invite(pseudo):
        mettre_a_jour_classement(pseudo, avatar, profil_actuel["score_total"])


def ajouter_score(pseudo: str, points: int):
    if points <= 0:
        return
    profil = obtenir_profil(pseudo)
    nouveau_score = profil["score_total"] + points
    _sauvegarder_fichier(pseudo, profil["avatar"], nouveau_score)
    if not est_invite(pseudo):
        mettre_a_jour_classement(pseudo, profil["avatar"], nouveau_score)