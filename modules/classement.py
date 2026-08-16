# =============================================================
#  modules/classement.py
# -------------------------------------------------------------
#  Stocke le CLASSEMENT : une liste de joueurs avec leur score
#  total, triée du plus grand au plus petit score.
# =============================================================

import json
import os

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_CLASSEMENT = os.path.join(DOSSIER_DATA, "classement.json")


def _charger() -> dict:
    if not os.path.exists(FICHIER_CLASSEMENT):
        return {}
    with open(FICHIER_CLASSEMENT, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(data: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_CLASSEMENT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def mettre_a_jour_classement(pseudo: str, avatar: str, score_total: int):
    data = _charger()
    data[pseudo] = {"avatar": avatar, "score_total": score_total}
    _sauvegarder(data)


def retirer_du_classement(pseudo: str):
    data = _charger()
    if pseudo in data:
        del data[pseudo]
        _sauvegarder(data)


def obtenir_classement(top: int = 20) -> list:
    data = _charger()
    entrees = [
        {"pseudo": pseudo, "avatar": infos["avatar"], "score_total": infos["score_total"]}
        for pseudo, infos in data.items()
    ]
    entrees.sort(key=lambda e: e["score_total"], reverse=True)
    return entrees[:top]