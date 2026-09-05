import json
import os
from modules.stockage_joueur import chemin_fichier_joueur

SEUIL_MINIMUM_REPONSES = 5


def _charger(pseudo: str) -> dict:
    chemin = chemin_fichier_joueur(pseudo, "erreurs.json")
    if not os.path.exists(chemin):
        return {}
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(pseudo: str, data: dict):
    chemin = chemin_fichier_joueur(pseudo, "erreurs.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def enregistrer_reponse(pseudo: str, chapitre_id: str, est_correct: bool):
    data = _charger(pseudo)
    infos = data.get(chapitre_id, {"nb_reponses": 0, "nb_erreurs": 0})

    infos["nb_reponses"] += 1
    if not est_correct:
        infos["nb_erreurs"] += 1

    data[chapitre_id] = infos
    _sauvegarder(pseudo, data)


def obtenir_taux_erreur(pseudo: str, chapitre_id: str) -> float:
    data = _charger(pseudo)
    infos = data.get(chapitre_id, {"nb_reponses": 0, "nb_erreurs": 0})

    if infos["nb_reponses"] < SEUIL_MINIMUM_REPONSES:
        return 0.0

    return infos["nb_erreurs"] / infos["nb_reponses"]


def obtenir_points_faibles(pseudo: str, chapitres_ids: list, top: int = 3) -> list:
    data = _charger(pseudo)
    resultats = []

    for cid in chapitres_ids:
        infos = data.get(cid, {"nb_reponses": 0, "nb_erreurs": 0})
        if infos["nb_reponses"] < SEUIL_MINIMUM_REPONSES:
            continue
        taux = infos["nb_erreurs"] / infos["nb_reponses"]
        if taux > 0:
            resultats.append({"chapitre_id": cid, "taux_erreur": taux, "nb_reponses": infos["nb_reponses"]})

    resultats.sort(key=lambda r: r["taux_erreur"], reverse=True)
    return resultats[:top]