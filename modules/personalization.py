# =============================================================
#  modules/personalization.py
# -------------------------------------------------------------
#  Gère le PROFIL du joueur : pseudo + avatar + score total.
# =============================================================

import json
import os

from modules.classement import mettre_a_jour_classement, retirer_du_classement

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_PROFIL = os.path.join(DOSSIER_DATA, "profil.json")

AVATARS_DISPONIBLES = ["🦉", "🦊", "🐱", "🐼", "🦁", "🐸", "🤖", "🧮"]

PROFIL_PAR_DEFAUT = {"pseudo": "Mathématicien", "avatar": "🦉", "score_total": 0}


def obtenir_profil() -> dict:
    if not os.path.exists(FICHIER_PROFIL):
        return dict(PROFIL_PAR_DEFAUT)

    with open(FICHIER_PROFIL, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "pseudo": data.get("pseudo", PROFIL_PAR_DEFAUT["pseudo"]),
        "avatar": data.get("avatar", PROFIL_PAR_DEFAUT["avatar"]),
        "score_total": data.get("score_total", 0),
    }


def _sauvegarder_fichier(profil: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_PROFIL, "w", encoding="utf-8") as f:
        json.dump(profil, f, ensure_ascii=False, indent=2)


def sauvegarder_profil(pseudo: str, avatar: str):
    ancien_profil = obtenir_profil()

    pseudo = pseudo.strip() or PROFIL_PAR_DEFAUT["pseudo"]
    if avatar not in AVATARS_DISPONIBLES:
        avatar = PROFIL_PAR_DEFAUT["avatar"]

    nouveau_profil = {
        "pseudo": pseudo,
        "avatar": avatar,
        "score_total": ancien_profil["score_total"],
    }
    _sauvegarder_fichier(nouveau_profil)

    if pseudo != ancien_profil["pseudo"]:
        retirer_du_classement(ancien_profil["pseudo"])
    mettre_a_jour_classement(pseudo, avatar, nouveau_profil["score_total"])


def ajouter_score(points: int):
    if points <= 0:
        return

    profil = obtenir_profil()
    profil["score_total"] += points
    _sauvegarder_fichier(profil)
    mettre_a_jour_classement(profil["pseudo"], profil["avatar"], profil["score_total"])