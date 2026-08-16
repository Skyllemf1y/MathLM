# =============================================================
#  modules/progression.py
# -------------------------------------------------------------
#  Gère la SAUVEGARDE de la progression (fichier JSON local,
#  un seul joueur pour l'instant -- pas encore de comptes).
#
#  Chaque chapitre est un dictionnaire avec 3 informations :
#  {
#      "arithmetique": {
#          "dernier_niveau_valide": 4,
#          "cours_vu": true,
#          "meilleure_note_test": 85
#      },
#      ...
#  }
#
#  COMPATIBILITÉ : si tu avais déjà joué avant cette mise à jour,
#  ton fichier contient l'ANCIEN format (juste un nombre). La
#  fonction _normaliser() le convertit automatiquement.
# =============================================================

import json
import os

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_PROGRESSION = os.path.join(DOSSIER_DATA, "progression.json")


def _normaliser(valeur_chapitre) -> dict:
    if isinstance(valeur_chapitre, dict):
        return {
            "dernier_niveau_valide": valeur_chapitre.get("dernier_niveau_valide", 0),
            "cours_vu": valeur_chapitre.get("cours_vu", False),
            "meilleure_note_test": valeur_chapitre.get("meilleure_note_test"),
        }
    else:
        return {
            "dernier_niveau_valide": valeur_chapitre,
            "cours_vu": False,
            "meilleure_note_test": None,
        }


def _charger() -> dict:
    if not os.path.exists(FICHIER_PROGRESSION):
        return {}
    with open(FICHIER_PROGRESSION, "r", encoding="utf-8") as f:
        data_brute = json.load(f)
    return {chapitre_id: _normaliser(valeur) for chapitre_id, valeur in data_brute.items()}


def _sauvegarder(data: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_PROGRESSION, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _obtenir_chapitre(data: dict, chapitre_id: str) -> dict:
    return data.get(chapitre_id, {"dernier_niveau_valide": 0, "cours_vu": False, "meilleure_note_test": None})


def dernier_niveau_valide(chapitre_id: str) -> int:
    data = _charger()
    return _obtenir_chapitre(data, chapitre_id)["dernier_niveau_valide"]


def niveau_est_debloque(chapitre_id: str, niveau: int) -> bool:
    return niveau <= dernier_niveau_valide(chapitre_id) + 1


def niveau_est_valide(chapitre_id: str, niveau: int) -> bool:
    return niveau <= dernier_niveau_valide(chapitre_id)


def valider_niveau(chapitre_id: str, niveau: int):
    data = _charger()
    infos = _obtenir_chapitre(data, chapitre_id)
    if niveau > infos["dernier_niveau_valide"]:
        infos["dernier_niveau_valide"] = niveau
        data[chapitre_id] = infos
        _sauvegarder(data)


def cours_est_vu(chapitre_id: str) -> bool:
    data = _charger()
    return _obtenir_chapitre(data, chapitre_id)["cours_vu"]


def marquer_cours_vu(chapitre_id: str):
    data = _charger()
    infos = _obtenir_chapitre(data, chapitre_id)
    if not infos["cours_vu"]:
        infos["cours_vu"] = True
        data[chapitre_id] = infos
        _sauvegarder(data)


def meilleure_note_test(chapitre_id: str):
    data = _charger()
    return _obtenir_chapitre(data, chapitre_id)["meilleure_note_test"]


def enregistrer_note_test(chapitre_id: str, note: int):
    data = _charger()
    infos = _obtenir_chapitre(data, chapitre_id)
    if infos["meilleure_note_test"] is None or note > infos["meilleure_note_test"]:
        infos["meilleure_note_test"] = note
        data[chapitre_id] = infos
        _sauvegarder(data)