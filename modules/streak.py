import json
import os
from datetime import date
from modules.stockage_joueur import chemin_fichier_joueur


def _charger(pseudo: str) -> dict:
    chemin = chemin_fichier_joueur(pseudo, "streak.json")
    if not os.path.exists(chemin):
        return {"dernier_jour_joue": None, "streak_actuelle": 0, "meilleure_streak": 0}
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(pseudo: str, data: dict):
    chemin = chemin_fichier_joueur(pseudo, "streak.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ecart_en_jours(dernier_jour_str):
    if dernier_jour_str is None:
        return None
    return (date.today() - date.fromisoformat(dernier_jour_str)).days


def obtenir_streak(pseudo: str) -> dict:
    data = _charger(pseudo)
    ecart = _ecart_en_jours(data["dernier_jour_joue"])
    streak_affichee = data["streak_actuelle"]
    if ecart is not None and ecart > 1:
        streak_affichee = 0
    return {
        "streak_actuelle": streak_affichee,
        "meilleure_streak": data["meilleure_streak"],
        "joue_aujourdhui": ecart == 0,
    }


def marquer_jour_joue(pseudo: str):
    data = _charger(pseudo)
    ecart = _ecart_en_jours(data["dernier_jour_joue"])
    if ecart == 0:
        return
    nouvelle_streak = data["streak_actuelle"] + 1 if ecart == 1 else 1
    data["streak_actuelle"] = nouvelle_streak
    data["meilleure_streak"] = max(data["meilleure_streak"], nouvelle_streak)
    data["dernier_jour_joue"] = date.today().isoformat()
    _sauvegarder(pseudo, data)