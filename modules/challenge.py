import json
import os
from modules.stockage_joueur import chemin_fichier_joueur


def _charger(pseudo: str) -> dict:
    chemin = chemin_fichier_joueur(pseudo, "challenge.json")
    if not os.path.exists(chemin):
        return {"meilleur_score": 0}
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(pseudo: str, data: dict):
    chemin = chemin_fichier_joueur(pseudo, "challenge.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def obtenir_meilleur_score_challenge(pseudo: str) -> int:
    return _charger(pseudo)["meilleur_score"]


def enregistrer_score_challenge(pseudo: str, score: int) -> bool:
    data = _charger(pseudo)
    if score > data["meilleur_score"]:
        data["meilleur_score"] = score
        _sauvegarder(pseudo, data)
        return True
    return False