import random
from modules.comptes import PREFIXE_INVITE
from modules.stockage_joueur import DOSSIER_JOUEURS
import os


def generer_pseudo_invite() -> str:
    while True:
        numero = random.randint(1000, 9999)
        pseudo = f"{PREFIXE_INVITE}{numero}"
        dossier = os.path.join(DOSSIER_JOUEURS, pseudo)
        if not os.path.exists(dossier):
            return pseudo


def est_invite(pseudo: str) -> bool:
    return pseudo is not None and pseudo.startswith(PREFIXE_INVITE)