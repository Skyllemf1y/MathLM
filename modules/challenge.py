# =============================================================
#  modules/challenge.py
# -------------------------------------------------------------
#  Gère le RECORD du mode "challenge infini". Ce score n'alimente
#  PAS le classement principal (mode infini = grindable à l'infini,
#  ça casserait l'anti-triche des niveaux/tests). Record perso séparé.
# =============================================================

import json
import os

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_CHALLENGE = os.path.join(DOSSIER_DATA, "challenge.json")


def _charger() -> dict:
    if not os.path.exists(FICHIER_CHALLENGE):
        return {"meilleur_score": 0}
    with open(FICHIER_CHALLENGE, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(data: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_CHALLENGE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def obtenir_meilleur_score_challenge() -> int:
    return _charger()["meilleur_score"]


def enregistrer_score_challenge(score: int) -> bool:
    data = _charger()
    if score > data["meilleur_score"]:
        data["meilleur_score"] = score
        _sauvegarder(data)
        return True
    return False