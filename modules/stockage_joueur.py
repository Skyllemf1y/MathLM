import os

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
DOSSIER_JOUEURS = os.path.join(DOSSIER_DATA, "joueurs")


def chemin_fichier_joueur(pseudo: str, nom_fichier: str) -> str:
    dossier_joueur = os.path.join(DOSSIER_JOUEURS, pseudo)
    os.makedirs(dossier_joueur, exist_ok=True)
    return os.path.join(dossier_joueur, nom_fichier)