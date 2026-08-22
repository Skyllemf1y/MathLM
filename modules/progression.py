import json
import os
from modules.stockage_joueur import chemin_fichier_joueur


def _normaliser(valeur_chapitre) -> dict:
    if isinstance(valeur_chapitre, dict):
        return {
            "dernier_niveau_valide": valeur_chapitre.get("dernier_niveau_valide", 0),
            "cours_vu": valeur_chapitre.get("cours_vu", False),
            "meilleure_note_test": valeur_chapitre.get("meilleure_note_test"),
        }
    return {"dernier_niveau_valide": valeur_chapitre, "cours_vu": False, "meilleure_note_test": None}


def _charger(pseudo: str) -> dict:
    chemin = chemin_fichier_joueur(pseudo, "progression.json")
    if not os.path.exists(chemin):
        return {}
    with open(chemin, "r", encoding="utf-8") as f:
        data_brute = json.load(f)
    return {cid: _normaliser(v) for cid, v in data_brute.items()}


def _sauvegarder(pseudo: str, data: dict):
    chemin = chemin_fichier_joueur(pseudo, "progression.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _obtenir_chapitre(data: dict, chapitre_id: str) -> dict:
    return data.get(chapitre_id, {"dernier_niveau_valide": 0, "cours_vu": False, "meilleure_note_test": None})


def dernier_niveau_valide(pseudo: str, chapitre_id: str) -> int:
    return _obtenir_chapitre(_charger(pseudo), chapitre_id)["dernier_niveau_valide"]


def niveau_est_debloque(pseudo: str, chapitre_id: str, niveau: int) -> bool:
    return niveau <= dernier_niveau_valide(pseudo, chapitre_id) + 1


def niveau_est_valide(pseudo: str, chapitre_id: str, niveau: int) -> bool:
    return niveau <= dernier_niveau_valide(pseudo, chapitre_id)


def valider_niveau(pseudo: str, chapitre_id: str, niveau: int):
    data = _charger(pseudo)
    infos = _obtenir_chapitre(data, chapitre_id)
    if niveau > infos["dernier_niveau_valide"]:
        infos["dernier_niveau_valide"] = niveau
        data[chapitre_id] = infos
        _sauvegarder(pseudo, data)


def cours_est_vu(pseudo: str, chapitre_id: str) -> bool:
    return _obtenir_chapitre(_charger(pseudo), chapitre_id)["cours_vu"]


def marquer_cours_vu(pseudo: str, chapitre_id: str):
    data = _charger(pseudo)
    infos = _obtenir_chapitre(data, chapitre_id)
    if not infos["cours_vu"]:
        infos["cours_vu"] = True
        data[chapitre_id] = infos
        _sauvegarder(pseudo, data)


def meilleure_note_test(pseudo: str, chapitre_id: str):
    return _obtenir_chapitre(_charger(pseudo), chapitre_id)["meilleure_note_test"]


def enregistrer_note_test(pseudo: str, chapitre_id: str, note: int):
    data = _charger(pseudo)
    infos = _obtenir_chapitre(data, chapitre_id)
    if infos["meilleure_note_test"] is None or note > infos["meilleure_note_test"]:
        infos["meilleure_note_test"] = note
        data[chapitre_id] = infos
        _sauvegarder(pseudo, data)