import os
import json
from modules.stockage_joueur import DOSSIER_JOUEURS
from config import CHAPITRES


def obtenir_statistiques_globales() -> list:
    totaux = {cid: {"nb_reponses": 0, "nb_erreurs": 0} for cid in CHAPITRES}

    if os.path.exists(DOSSIER_JOUEURS):
        for nom_dossier in os.listdir(DOSSIER_JOUEURS):
            chemin_erreurs = os.path.join(DOSSIER_JOUEURS, nom_dossier, "erreurs.json")
            if not os.path.exists(chemin_erreurs):
                continue
            with open(chemin_erreurs, "r", encoding="utf-8") as f:
                data_joueur = json.load(f)
            for cid, infos in data_joueur.items():
                if cid not in totaux:
                    continue
                totaux[cid]["nb_reponses"] += infos.get("nb_reponses", 0)
                totaux[cid]["nb_erreurs"] += infos.get("nb_erreurs", 0)

    resultats = []
    for cid, infos in totaux.items():
        nb_reponses = infos["nb_reponses"]
        taux_erreur = round(100 * infos["nb_erreurs"] / nb_reponses) if nb_reponses > 0 else 0
        resultats.append({
            "chapitre_id": cid, "nom": CHAPITRES[cid]["nom"],
            "nb_reponses": nb_reponses, "nb_erreurs": infos["nb_erreurs"], "taux_erreur": taux_erreur,
        })

    resultats.sort(key=lambda r: r["taux_erreur"], reverse=True)
    return resultats


def compter_joueurs() -> int:
    if not os.path.exists(DOSSIER_JOUEURS):
        return 0
    return len(os.listdir(DOSSIER_JOUEURS))