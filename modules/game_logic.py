import random

from modules.question_generator import generer_question
from modules.progression import valider_niveau, enregistrer_note_test, dernier_niveau_valide, meilleure_note_test
from modules.personalization import ajouter_score
from modules.streak import marquer_jour_joue
from modules.challenge import enregistrer_score_challenge
from modules.erreurs import enregistrer_reponse, obtenir_taux_erreur
from config import VIES_INITIALES, POINTS_PAR_BONNE_REPONSE, NB_QUESTIONS_PAR_NIVEAU, NB_QUESTIONS_TEST, CHAPITRES


class PartieEnCours:
    def __init__(self, pseudo: str, chapitre_id, niveau, est_test: bool = False, est_challenge: bool = False):
        self.pseudo = pseudo
        self.chapitre_id = chapitre_id
        self.niveau = niveau
        self.est_test = est_test
        self.est_challenge = est_challenge
        self.vies = VIES_INITIALES
        self.score = 0
        self.nb_questions_posees = 0
        self.nb_bonnes_reponses = 0
        self.question_actuelle = None
        self.nouvelle_question()

    def _prochaine_selection(self):
        if self.est_challenge:
            chapitres_ids = list(CHAPITRES.keys())
            poids = []
            for cid in chapitres_ids:
                nb_niveaux = CHAPITRES[cid]["nb_niveaux"]
                valides = dernier_niveau_valide(self.pseudo, cid)
                poids_progression = max(1, nb_niveaux - valides)

                taux_erreur = obtenir_taux_erreur(self.pseudo, cid)
                poids.append(poids_progression * (1 + taux_erreur))

            chapitre_choisi = random.choices(chapitres_ids, weights=poids, k=1)[0]
            nb_niveaux = CHAPITRES[chapitre_choisi]["nb_niveaux"]
            return chapitre_choisi, random.randint(1, nb_niveaux)

        if self.est_test:
            nb_niveaux = CHAPITRES[self.chapitre_id]["nb_niveaux"]
            return self.chapitre_id, random.randint(1, nb_niveaux)
        return self.chapitre_id, self.niveau

    def nouvelle_question(self):
        chapitre_choisi, niveau_choisi = self._prochaine_selection()
        self.question_actuelle = generer_question(chapitre_choisi, niveau_choisi)

    def valider_reponse(self, reponse_joueur):
        bonne_reponse = self.question_actuelle["reponse"]
        explication = self.question_actuelle.get("explication", "")
        tolerance = self.question_actuelle.get("tolerance", 0)
        chapitre_de_la_question = self.question_actuelle["chapitre"]

        try:
            reponse_joueur = float(reponse_joueur)
        except (TypeError, ValueError):
            reponse_joueur = None

        est_correct = reponse_joueur is not None and abs(reponse_joueur - bonne_reponse) <= max(tolerance, 1e-9)

        enregistrer_reponse(self.pseudo, chapitre_de_la_question, est_correct)

        self.nb_questions_posees += 1
        if est_correct:
            self.score += POINTS_PAR_BONNE_REPONSE
            self.nb_bonnes_reponses += 1
            marquer_jour_joue(self.pseudo)
        else:
            self.vies = max(0, self.vies - 1)

        niveau_reussi = False
        note = None
        nouveau_record_challenge = False

        if self.est_challenge:
            partie_terminee = self.vies <= 0
            if partie_terminee:
                nouveau_record_challenge = enregistrer_score_challenge(self.pseudo, self.score)
        elif self.est_test:
            partie_terminee = self.nb_questions_posees >= NB_QUESTIONS_TEST
            if partie_terminee:
                note = round(100 * self.nb_bonnes_reponses / self.nb_questions_posees)
                ancienne_meilleure_note = meilleure_note_test(self.pseudo, self.chapitre_id)
                enregistrer_note_test(self.pseudo, self.chapitre_id, note)
                if ancienne_meilleure_note is None or note > ancienne_meilleure_note:
                    ajouter_score(self.pseudo, self.score)
        else:
            if self.nb_bonnes_reponses >= NB_QUESTIONS_PAR_NIVEAU:
                partie_terminee = True
                niveau_reussi = True
                est_nouveau_niveau = self.niveau > dernier_niveau_valide(self.pseudo, self.chapitre_id)
                valider_niveau(self.pseudo, self.chapitre_id, self.niveau)
                if est_nouveau_niveau:
                    ajouter_score(self.pseudo, self.score)
            elif self.vies <= 0:
                partie_terminee = True
            else:
                partie_terminee = False

        if not partie_terminee:
            self.nouvelle_question()

        return {
            "correct": est_correct, "bonne_reponse": bonne_reponse, "explication": explication,
            "vies": self.vies, "score": self.score, "nb_bonnes_reponses": self.nb_bonnes_reponses,
            "nb_questions_posees": self.nb_questions_posees, "partie_terminee": partie_terminee,
            "niveau_reussi": niveau_reussi, "note": note, "est_challenge": self.est_challenge,
            "nouveau_record_challenge": nouveau_record_challenge,
            "prochaine_question": self.question_actuelle["texte"] if not partie_terminee else None,
        }

    def vers_dict(self):
        return {
            "pseudo": self.pseudo, "chapitre_id": self.chapitre_id, "niveau": self.niveau,
            "est_test": self.est_test, "est_challenge": self.est_challenge, "vies": self.vies,
            "score": self.score, "nb_questions_posees": self.nb_questions_posees,
            "nb_bonnes_reponses": self.nb_bonnes_reponses, "question_actuelle": self.question_actuelle,
        }

    @staticmethod
    def depuis_dict(data: dict):
        partie = PartieEnCours.__new__(PartieEnCours)
        partie.pseudo = data["pseudo"]
        partie.chapitre_id = data["chapitre_id"]
        partie.niveau = data["niveau"]
        partie.est_test = data["est_test"]
        partie.est_challenge = data.get("est_challenge", False)
        partie.vies = data["vies"]
        partie.score = data["score"]
        partie.nb_questions_posees = data["nb_questions_posees"]
        partie.nb_bonnes_reponses = data["nb_bonnes_reponses"]
        partie.question_actuelle = data["question_actuelle"]
        return partie