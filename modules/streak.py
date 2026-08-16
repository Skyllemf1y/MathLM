# =============================================================
#  modules/streak.py
# -------------------------------------------------------------
#  Gère la SÉRIE (streak) : le nombre de jours consécutifs où le
#  joueur a répondu correctement à au moins une question.
# =============================================================

import json
import os
from datetime import date

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_STREAK = os.path.join(DOSSIER_DATA, "streak.json")


def _charger() -> dict:
    if not os.path.exists(FICHIER_STREAK):
        return {"dernier_jour_joue": None, "streak_actuelle": 0, "meilleure_streak": 0}
    with open(FICHIER_STREAK, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(data: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_STREAK, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ecart_en_jours(dernier_jour_str) -> int:
    if dernier_jour_str is None:
        return None
    dernier_jour = date.fromisoformat(dernier_jour_str)
    return (date.today() - dernier_jour).days


def obtenir_streak() -> dict:
    data = _charger()
    ecart = _ecart_en_jours(data["dernier_jour_joue"])

    streak_affichee = data["streak_actuelle"]
    if ecart is not None and ecart > 1:
        streak_affichee = 0

    return {
        "streak_actuelle": streak_affichee,
        "meilleure_streak": data["meilleure_streak"],
        "joue_aujourdhui": ecart == 0,
    }


def marquer_jour_joue():
    data = _charger()
    ecart = _ecart_en_jours(data["dernier_jour_joue"])

    if ecart == 0:
        return

    if ecart == 1:
        nouvelle_streak = data["streak_actuelle"] + 1
    else:
        nouvelle_streak = 1

    data["streak_actuelle"] = nouvelle_streak
    data["meilleure_streak"] = max(data["meilleure_streak"], nouvelle_streak)
    data["dernier_jour_joue"] = date.today().isoformat()
    _sauvegarder(data)