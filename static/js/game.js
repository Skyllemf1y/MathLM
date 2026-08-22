const champReponse = document.getElementById("champ-reponse");
const boutonValider = document.getElementById("bouton-valider");
const texteQuestion = document.getElementById("texte-question");
const messageResultat = document.getElementById("message-resultat");
const explicationErreur = document.getElementById("explication-erreur");
const affichageVies = document.getElementById("vies");
const affichageScore = document.getElementById("score");
const barreRemplissage = document.getElementById("barre-progression-remplissage");
const texteProgression = document.getElementById("texte-progression");
const boutonContinuer = document.getElementById("bouton-continuer");
const chronoValeur = document.getElementById("chrono-valeur");

const VIES_MAX = parseInt(affichageVies.dataset.viesMax);
if (barreRemplissage) {
    barreRemplissage.style.width = barreRemplissage.dataset.largeur + "%";
}

const OBJECTIF = texteProgression ? parseInt(texteProgression.textContent.split("/")[1].trim()) : null;

const debutChrono = Date.now();
let intervalleChrono = null;

function formaterTemps(secondesTotal) {
    const minutes = Math.floor(secondesTotal / 60);
    const secondes = secondesTotal % 60;
    return minutes + ":" + String(secondes).padStart(2, "0");
}

function tempsEcouleEnSecondes() {
    return Math.floor((Date.now() - debutChrono) / 1000);
}

function demarrerChrono() {
    intervalleChrono = setInterval(() => {
        chronoValeur.textContent = formaterTemps(tempsEcouleEnSecondes());
    }, 1000);
}

function mettreAJourCoeurs(viesRestantes) {
    let html = "";
    for (let i = 0; i < VIES_MAX; i++) {
        const classe = i < viesRestantes ? "coeur" : "coeur coeur-perdu";
        html += `<span class="${classe}">❤</span>`;
    }
    affichageVies.innerHTML = html;
}

function mettreAJourProgression(nbBonnesReponses) {
    if (!barreRemplissage || !texteProgression) return;
    const pourcentage = Math.min(100, Math.round((nbBonnesReponses / OBJECTIF) * 100));
    barreRemplissage.style.width = pourcentage + "%";
    texteProgression.textContent = nbBonnesReponses + " / " + OBJECTIF;
}

async function validerReponse() {
    const reponse = champReponse.value;

    const res = await fetch("/valider", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reponse: reponse }),
    });

    const data = await res.json();

    mettreAJourCoeurs(data.vies);
    affichageScore.textContent = "⭐ " + data.score;
    mettreAJourProgression(data.nb_bonnes_reponses);

    if (data.correct) {
        messageResultat.textContent = "✅ Bonne réponse !";
        messageResultat.style.color = "var(--couleur-succes)";
        explicationErreur.style.display = "none";
    } else {
        messageResultat.textContent = "❌ Faux, la réponse était " + data.bonne_reponse;
        messageResultat.style.color = "var(--couleur-erreur)";

        if (data.explication) {
            explicationErreur.textContent = "💡 " + data.explication;
            explicationErreur.style.display = "block";
        }
    }

    if (data.partie_terminee) {
        clearInterval(intervalleChrono);
        const tempsFinal = formaterTemps(tempsEcouleEnSecondes());
        chronoValeur.textContent = tempsFinal;

        champReponse.disabled = true;
        boutonValider.disabled = true;
        boutonContinuer.style.display = "inline-block";

        const pourcentageReussite = data.nb_questions_posees > 0
            ? Math.round(100 * data.nb_bonnes_reponses / data.nb_questions_posees)
            : 0;

        if (data.niveau_reussi) {
            texteQuestion.textContent =
                `🎉 Niveau validé ! Score : ${pourcentageReussite}% (${data.nb_bonnes_reponses}/${data.nb_questions_posees}) · Temps : ${tempsFinal}`;
        } else if (data.note !== null && data.note !== undefined) {
            texteQuestion.textContent =
                `🏁 Test terminé ! Note : ${data.note}% · Temps : ${tempsFinal}`;
        } else if (data.est_challenge) {
            const titre = data.nouveau_record_challenge ? "🏆 Nouveau record !" : "🎲 Partie terminée !";
            texteQuestion.textContent =
                `${titre} Score : ${data.score} pts (${pourcentageReussite}% de réussite) · Temps : ${tempsFinal}`;
        } else {
            texteQuestion.textContent =
                `💔 Plus de vies ! Score : ${pourcentageReussite}% (${data.nb_bonnes_reponses}/${data.nb_questions_posees}) · Temps : ${tempsFinal}`;
        }
    } else {
        texteQuestion.textContent = data.prochaine_question;
        champReponse.value = "";
        champReponse.focus();
    }
}

boutonValider.addEventListener("click", validerReponse);

champReponse.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        validerReponse();
    }
});

demarrerChrono();