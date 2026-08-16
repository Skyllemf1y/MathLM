// =============================================================
//  cours.js
// -------------------------------------------------------------
//  Corrige le QCM directement dans le navigateur : pas besoin
//  d'un aller-retour au serveur pour un simple quiz d'auto-
//  évaluation. Chaque question (.carte-qcm) porte un attribut
//  data-bonne-reponse avec l'index (0 à 3) de la bonne réponse.
// =============================================================

const boutonCorriger = document.getElementById("bouton-corriger-qcm");
const scoreQcm = document.getElementById("score-qcm");
const cartesQcm = document.querySelectorAll(".carte-qcm");

function corrigerQcm() {
    let nbBonnes = 0;
    let nbRepondues = 0;

    cartesQcm.forEach((carte) => {
        const bonneReponse = carte.dataset.bonneReponse;
        const radioCoche = carte.querySelector("input[type='radio']:checked");
        const feedback = carte.querySelector(".feedback-qcm");
        const labels = carte.querySelectorAll(".option-qcm");

        labels.forEach((label) => label.classList.remove("option-correcte", "option-incorrecte"));

        if (!radioCoche) {
            feedback.textContent = "⚠️ Pas de réponse sélectionnée";
            feedback.style.color = "var(--couleur-texte-doux)";
            return;
        }

        nbRepondues++;
        const labelChoisi = radioCoche.closest(".option-qcm");

        if (radioCoche.value === bonneReponse) {
            nbBonnes++;
            feedback.textContent = "✅ Correct !";
            feedback.style.color = "var(--couleur-succes)";
            labelChoisi.classList.add("option-correcte");
        } else {
            feedback.textContent = "❌ Incorrect";
            feedback.style.color = "var(--couleur-erreur)";
            labelChoisi.classList.add("option-incorrecte");
            const labelCorrect = carte.querySelectorAll(".option-qcm")[parseInt(bonneReponse)];
            labelCorrect.classList.add("option-correcte");
        }
    });

    scoreQcm.textContent = `Score : ${nbBonnes} / ${cartesQcm.length}`;
    if (nbRepondues < cartesQcm.length) {
        scoreQcm.textContent += " (réponds à toutes les questions pour un score complet)";
    }
}

boutonCorriger.addEventListener("click", corrigerQcm);