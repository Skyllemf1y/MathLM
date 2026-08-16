# =============================================================
#  main.py
# -------------------------------------------------------------
#  Point d'entrée : le "chef d'orchestre".
#  Pour lancer l'app :  python main.py
# =============================================================

from flask import Flask, render_template, session, jsonify, request, redirect, url_for

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
from modules.personalization import obtenir_profil, sauvegarder_profil, AVATARS_DISPONIBLES
from modules.classement import obtenir_classement
from modules.rangs import obtenir_rang, progression_vers_rang_suivant
from modules.streak import obtenir_streak
from modules.challenge import obtenir_meilleur_score_challenge

app = Flask(__name__)
app.secret_key = "7ee8e6af6c5f0fd3d2166839c9d30fb3ec62dc759e6d867acd1546873f211882"


@app.context_processor
def injecter_nom_application():
    return {"nom_application": NOM_APPLICATION}


@app.context_processor
def injecter_profil():
    profil = obtenir_profil()
    profil["rang"] = obtenir_rang(profil["score_total"])
    return {"profil_utilisateur": profil}


@app.context_processor
def injecter_streak():
    return {"streak_utilisateur": obtenir_streak()}


@app.route("/")
def accueil():
    return render_template("index.html", chapitres=CHAPITRES)


@app.route("/chapitre/<chapitre_id>")
def chapitre(chapitre_id):
    infos = CHAPITRES[chapitre_id]
    niveaux = list(range(1, infos["nb_niveaux"] + 1))

    etats_niveaux = [
        {
            "numero": n,
            "valide": niveau_est_valide(chapitre_id, n),
            "debloque": niveau_est_debloque(chapitre_id, n),
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


@app.route("/cours")
def liste_cours():
    return render_template(
        "liste_cours.html",
        titre_page="Cours",
        chapitres=CHAPITRES,
    )


@app.route("/cours/<chapitre_id>")
def cours(chapitre_id):
    infos = CHAPITRES[chapitre_id]
    contenu_cours = COURS[chapitre_id]

    marquer_cours_vu(chapitre_id)

    return render_template(
        "cours.html",
        chapitre_id=chapitre_id,
        nom_chapitre=infos["nom"],
        titre_page=infos["nom"] + " · Cours",
        cours=contenu_cours,
    )


@app.route("/progression")
def voir_progression():
    resume_chapitres = []
    for chapitre_id, infos in CHAPITRES.items():
        nb_valides = dernier_niveau_valide(chapitre_id)
        nb_total = infos["nb_niveaux"]

        resume_chapitres.append({
            "chapitre_id": chapitre_id,
            "nom": infos["nom"],
            "nb_valides": nb_valides,
            "nb_total": nb_total,
            "pourcentage": round(100 * nb_valides / nb_total),
            "cours_vu": cours_est_vu(chapitre_id),
            "note_test": meilleure_note_test(chapitre_id),
        })

    return render_template(
        "progression.html",
        titre_page="Ma progression",
        resume_chapitres=resume_chapitres,
    )


@app.route("/classement")
def classement():
    entrees = obtenir_classement(top=20)
    for entree in entrees:
        entree["rang"] = obtenir_rang(entree["score_total"])

    profil_actuel = obtenir_profil()

    return render_template(
        "classement.html",
        titre_page="Classement",
        entrees=entrees,
        pseudo_actuel=profil_actuel["pseudo"],
    )


@app.route("/profil", methods=["GET", "POST"])
def profil():
    if request.method == "POST":
        pseudo_saisi = request.form.get("pseudo", "")
        avatar_choisi = request.form.get("avatar", "")
        sauvegarder_profil(pseudo_saisi, avatar_choisi)
        return redirect(url_for("profil"))

    profil_actuel = obtenir_profil()
    return render_template(
        "profil.html",
        titre_page="Profil",
        avatars_disponibles=AVATARS_DISPONIBLES,
        progression_rang=progression_vers_rang_suivant(profil_actuel["score_total"]),
    )


@app.route("/jouer/<chapitre_id>/<int:niveau>")
def jouer(chapitre_id, niveau):
    if not niveau_est_debloque(chapitre_id, niveau):
        return redirect(url_for("chapitre", chapitre_id=chapitre_id))

    partie = PartieEnCours(chapitre_id, niveau, est_test=False)
    session["partie"] = partie.vers_dict()

    return render_template(
        "game.html",
        chapitre_id=chapitre_id,
        nom_chapitre=CHAPITRES[chapitre_id]["nom"],
        titre_page=CHAPITRES[chapitre_id]["nom"],
        niveau=niveau,
        est_test=False,
        question=partie.question_actuelle["texte"],
        vies=partie.vies,
        vies_max=VIES_INITIALES,
        score=partie.score,
        objectif=NB_QUESTIONS_PAR_NIVEAU,
        nb_bonnes_reponses=0,
        est_challenge=False,
        url_retour=url_for("chapitre", chapitre_id=chapitre_id),
    )


@app.route("/test/<chapitre_id>")
def test_chapitre(chapitre_id):
    partie = PartieEnCours(chapitre_id, niveau=1, est_test=True)
    session["partie"] = partie.vers_dict()

    return render_template(
        "game.html",
        chapitre_id=chapitre_id,
        nom_chapitre=CHAPITRES[chapitre_id]["nom"],
        titre_page=CHAPITRES[chapitre_id]["nom"] + " · Test",
        niveau=None,
        est_test=True,
        question=partie.question_actuelle["texte"],
        vies=partie.vies,
        vies_max=VIES_INITIALES,
        score=partie.score,
        objectif=NB_QUESTIONS_TEST,
        nb_bonnes_reponses=0,
        est_challenge=False,
        url_retour=url_for("chapitre", chapitre_id=chapitre_id),
    )


@app.route("/challenge")
def challenge():
    partie = PartieEnCours(chapitre_id=None, niveau=None, est_test=False, est_challenge=True)
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
        meilleur_score_challenge=obtenir_meilleur_score_challenge(),
    )


@app.route("/valider", methods=["POST"])
def valider():
    if "partie" not in session:
        return jsonify({"erreur": "Aucune partie en cours"}), 400

    partie = PartieEnCours.depuis_dict(session["partie"])
    reponse_joueur = request.json.get("reponse")

    resultat = partie.valider_reponse(reponse_joueur)
    session["partie"] = partie.vers_dict()

    return jsonify(resultat)


if __name__ == "__main__":
    app.run(debug=True)