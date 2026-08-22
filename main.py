import os
from functools import wraps
from flask import Flask, render_template, session, jsonify, request, redirect, url_for, flash

from config import CHAPITRES, NOM_APPLICATION, NB_QUESTIONS_PAR_NIVEAU, NB_QUESTIONS_TEST, VIES_INITIALES
from modules.game_logic import PartieEnCours
from modules.progression import (
    niveau_est_debloque,
    niveau_est_valide,
    dernier_niveau_valide,
    marquer_cours_vu,
    cours_est_vu,
    meilleure_note_test,
)
from modules.cours import COURS
from modules.personalization import obtenir_profil, sauvegarder_avatar, AVATARS_DISPONIBLES
from modules.classement import obtenir_classement
from modules.rangs import obtenir_rang, progression_vers_rang_suivant
from modules.streak import obtenir_streak
from modules.challenge import obtenir_meilleur_score_challenge
from modules.comptes import creer_compte, verifier_identifiants
from modules.badges import calculer_badges

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cle-de-developpement-local-jamais-utilisee-en-ligne")


def connexion_requise(fonction):
    @wraps(fonction)
    def fonction_protegee(*args, **kwargs):
        if "pseudo_compte" not in session:
            flash("Connecte-toi pour accéder à cette page.", "erreur")
            return redirect(url_for("connexion"))
        return fonction(*args, **kwargs)
    return fonction_protegee


@app.context_processor
def injecter_nom_application():
    return {"nom_application": NOM_APPLICATION}


@app.context_processor
def injecter_utilisateur_connecte():
    return {"utilisateur_connecte": session.get("pseudo_compte")}


@app.context_processor
def injecter_profil():
    pseudo = session.get("pseudo_compte")
    if pseudo is None:
        return {"profil_utilisateur": None}
    profil = obtenir_profil(pseudo)
    profil["rang"] = obtenir_rang(profil["score_total"])
    return {"profil_utilisateur": profil}


@app.context_processor
def injecter_streak():
    pseudo = session.get("pseudo_compte")
    if pseudo is None:
        return {"streak_utilisateur": None}
    return {"streak_utilisateur": obtenir_streak(pseudo)}


@app.route("/")
def accueil():
    return render_template("index.html", chapitres=CHAPITRES)


@app.route("/cours")
def liste_cours():
    return render_template("liste_cours.html", titre_page="Cours", chapitres=CHAPITRES)


@app.route("/classement")
def classement():
    entrees = obtenir_classement(top=20)
    for entree in entrees:
        entree["rang"] = obtenir_rang(entree["score_total"])

    return render_template(
        "classement.html",
        titre_page="Classement",
        entrees=entrees,
        pseudo_actuel=session.get("pseudo_compte"),
    )


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        pseudo = request.form.get("pseudo", "").strip()
        mot_de_passe = request.form.get("mot_de_passe", "")
        confirmation = request.form.get("confirmation", "")

        if mot_de_passe != confirmation:
            flash("Les deux mots de passe ne correspondent pas.", "erreur")
        else:
            succes, message_erreur = creer_compte(pseudo, mot_de_passe)
            if succes:
                session["pseudo_compte"] = pseudo
                flash(f"Bienvenue {pseudo} ! Ton compte a été créé.", "succes")
                return redirect(url_for("accueil"))
            else:
                flash(message_erreur, "erreur")

    return render_template("inscription.html", titre_page="Inscription")


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        pseudo = request.form.get("pseudo", "").strip()
        mot_de_passe = request.form.get("mot_de_passe", "")

        if verifier_identifiants(pseudo, mot_de_passe):
            session["pseudo_compte"] = pseudo
            flash(f"Content de te revoir, {pseudo} !", "succes")
            return redirect(url_for("accueil"))
        else:
            flash("Pseudo ou mot de passe incorrect.", "erreur")

    return render_template("connexion.html", titre_page="Connexion")


@app.route("/deconnexion")
def deconnexion():
    session.pop("pseudo_compte", None)
    session.pop("partie", None)
    flash("Tu es déconnecté.", "succes")
    return redirect(url_for("accueil"))


@app.route("/chapitre/<chapitre_id>")
@connexion_requise
def chapitre(chapitre_id):
    pseudo = session["pseudo_compte"]
    infos = CHAPITRES[chapitre_id]
    niveaux = list(range(1, infos["nb_niveaux"] + 1))

    etats_niveaux = [
        {
            "numero": n,
            "valide": niveau_est_valide(pseudo, chapitre_id, n),
            "debloque": niveau_est_debloque(pseudo, chapitre_id, n),
        }
        for n in niveaux
    ]

    return render_template(
        "chapitre.html",
        chapitre_id=chapitre_id,
        nom_chapitre=infos["nom"],
        titre_page=infos["nom"],
        etats_niveaux=etats_niveaux,
    )


@app.route("/cours/<chapitre_id>")
@connexion_requise
def cours(chapitre_id):
    pseudo = session["pseudo_compte"]
    infos = CHAPITRES[chapitre_id]
    contenu_cours = COURS[chapitre_id]
    marquer_cours_vu(pseudo, chapitre_id)

    return render_template(
        "cours.html",
        chapitre_id=chapitre_id,
        nom_chapitre=infos["nom"],
        titre_page=infos["nom"] + " · Cours",
        cours=contenu_cours,
    )


@app.route("/progression")
@connexion_requise
def voir_progression():
    pseudo = session["pseudo_compte"]
    resume_chapitres = []
    for chapitre_id, infos in CHAPITRES.items():
        nb_valides = dernier_niveau_valide(pseudo, chapitre_id)
        nb_total = infos["nb_niveaux"]
        resume_chapitres.append({
            "chapitre_id": chapitre_id,
            "nom": infos["nom"],
            "nb_valides": nb_valides,
            "nb_total": nb_total,
            "pourcentage": round(100 * nb_valides / nb_total),
            "cours_vu": cours_est_vu(pseudo, chapitre_id),
            "note_test": meilleure_note_test(pseudo, chapitre_id),
        })

    return render_template("progression.html", titre_page="Ma progression", resume_chapitres=resume_chapitres)


@app.route("/profil", methods=["GET", "POST"])
@connexion_requise
def profil():
    pseudo = session["pseudo_compte"]
    badges = calculer_badges(pseudo)

    if request.method == "POST":
        avatar_choisi = request.form.get("avatar", "")
        sauvegarder_avatar(pseudo, avatar_choisi)
        return redirect(url_for("profil"))

    profil_actuel = obtenir_profil(pseudo)
    return render_template(
        "profil.html",
        titre_page="Profil",
        avatars_disponibles=AVATARS_DISPONIBLES,
        progression_rang=progression_vers_rang_suivant(profil_actuel["score_total"]),
    )


@app.route("/jouer/<chapitre_id>/<int:niveau>")
@connexion_requise
def jouer(chapitre_id, niveau):
    pseudo = session["pseudo_compte"]

    if not niveau_est_debloque(pseudo, chapitre_id, niveau):
        return redirect(url_for("chapitre", chapitre_id=chapitre_id))

    partie = PartieEnCours(pseudo, chapitre_id, niveau, est_test=False)
    session["partie"] = partie.vers_dict()

    return render_template(
        "game.html",
        chapitre_id=chapitre_id,
        nom_chapitre=CHAPITRES[chapitre_id]["nom"],
        titre_page=CHAPITRES[chapitre_id]["nom"],
        niveau=niveau,
        est_test=False,
        est_challenge=False,
        url_retour=url_for("chapitre", chapitre_id=chapitre_id),
        question=partie.question_actuelle["texte"],
        vies=partie.vies,
        vies_max=VIES_INITIALES,
        score=partie.score,
        objectif=NB_QUESTIONS_PAR_NIVEAU,
        nb_bonnes_reponses=0,
    )


@app.route("/test/<chapitre_id>")
@connexion_requise
def test_chapitre(chapitre_id):
    pseudo = session["pseudo_compte"]

    partie = PartieEnCours(pseudo, chapitre_id, niveau=1, est_test=True)
    session["partie"] = partie.vers_dict()

    return render_template(
        "game.html",
        chapitre_id=chapitre_id,
        nom_chapitre=CHAPITRES[chapitre_id]["nom"],
        titre_page=CHAPITRES[chapitre_id]["nom"] + " · Test",
        niveau=None,
        est_test=True,
        est_challenge=False,
        url_retour=url_for("chapitre", chapitre_id=chapitre_id),
        question=partie.question_actuelle["texte"],
        vies=partie.vies,
        vies_max=VIES_INITIALES,
        score=partie.score,
        objectif=NB_QUESTIONS_TEST,
        nb_bonnes_reponses=0,
    )


@app.route("/challenge")
@connexion_requise
def challenge():
    pseudo = session["pseudo_compte"]

    partie = PartieEnCours(pseudo, chapitre_id=None, niveau=None, est_test=False, est_challenge=True)
    session["partie"] = partie.vers_dict()

    return render_template(
        "game.html",
        chapitre_id=None,
        nom_chapitre="Mode Challenge",
        titre_page="Challenge infini",
        niveau=None,
        est_test=False,
        est_challenge=True,
        url_retour=url_for("accueil"),
        question=partie.question_actuelle["texte"],
        vies=partie.vies,
        vies_max=VIES_INITIALES,
        score=partie.score,
        objectif=None,
        nb_bonnes_reponses=0,
        meilleur_score_challenge=obtenir_meilleur_score_challenge(pseudo),
    )


@app.route("/valider", methods=["POST"])
def valider():
    if "pseudo_compte" not in session or "partie" not in session:
        return jsonify({"erreur": "Aucune partie en cours"}), 400

    partie = PartieEnCours.depuis_dict(session["partie"])
    reponse_joueur = request.json.get("reponse")

    resultat = partie.valider_reponse(reponse_joueur)
    session["partie"] = partie.vers_dict()

    return jsonify(resultat)


if __name__ == "__main__":
    app.run(debug=True)