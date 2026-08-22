# =============================================================
#  modules/comptes.py
# -------------------------------------------------------------
#  SESSION 1 : gère les COMPTES (inscription/connexion) -- c'est
#  à dire uniquement "qui a le droit de se connecter, avec quel
#  mot de passe".
#
#  IMPORTANT À COMPRENDRE : ce fichier ne touche PAS à la
#  progression, au score, au profil de jeu affiché (pseudo/avatar
#  en jeu restent gérés par modules/personalization.py, encore
#  partagés par tout le monde pour l'instant, comme avant). La
#  vraie séparation "chaque joueur a SES données" arrive à la
#  PROCHAINE session (migration des données). Ici, on pose juste
#  la fondation : des comptes qui existent vraiment, protégés par
#  un mot de passe.
#
#  SÉCURITÉ : le mot de passe n'est JAMAIS stocké tel quel dans le
#  fichier. On stocke un "hash" (une empreinte à sens unique,
#  impossible à retransformer en mot de passe d'origine), grâce à
#  werkzeug -- une bibliothèque déjà installée avec Flask, donc
#  aucune nouvelle dépendance à ajouter.
# =============================================================

import json
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash

DOSSIER_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
FICHIER_COMPTES = os.path.join(DOSSIER_DATA, "comptes.json")

# Un pseudo valide : 3 à 20 caractères, lettres/chiffres/tirets/underscores
# UNIQUEMENT. Ça élimine dès maintenant les caractères "dangereux" (comme
# / ou ..), qui poseraient un problème de sécurité à la session suivante,
# quand chaque pseudo servira à nommer un dossier de données sur le serveur.
_REGEX_PSEUDO_VALIDE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def _charger() -> dict:
    """Charge tous les comptes. Format : {"pseudo": {"mot_de_passe_hash": "..."}}"""
    if not os.path.exists(FICHIER_COMPTES):
        return {}
    with open(FICHIER_COMPTES, "r", encoding="utf-8") as f:
        return json.load(f)


def _sauvegarder(data: dict):
    os.makedirs(DOSSIER_DATA, exist_ok=True)
    with open(FICHIER_COMPTES, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def pseudo_est_valide(pseudo: str) -> bool:
    return bool(_REGEX_PSEUDO_VALIDE.match(pseudo))


def compte_existe(pseudo: str) -> bool:
    return pseudo in _charger()


def creer_compte(pseudo: str, mot_de_passe: str):
    """
    Essaie de créer un compte.
    Renvoie un tuple (succes: bool, message_erreur: str).
    Si succes est True, message_erreur est une chaîne vide.
    """
    if not pseudo_est_valide(pseudo):
        return False, "Le pseudo doit faire entre 3 et 20 caractères (lettres, chiffres, - et _ uniquement)."

    if len(mot_de_passe) < 4:
        return False, "Le mot de passe doit faire au moins 4 caractères."

    data = _charger()
    if pseudo in data:
        return False, "Ce pseudo est déjà pris."

    data[pseudo] = {"mot_de_passe_hash": generate_password_hash(mot_de_passe)}
    _sauvegarder(data)
    return True, ""


def verifier_identifiants(pseudo: str, mot_de_passe: str) -> bool:
    """Renvoie True si le pseudo existe ET que le mot de passe correspond."""
    data = _charger()
    compte = data.get(pseudo)
    if compte is None:
        return False
    return check_password_hash(compte["mot_de_passe_hash"], mot_de_passe)