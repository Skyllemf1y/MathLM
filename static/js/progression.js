// =============================================================
//  progression.js
// -------------------------------------------------------------
//  Applique la largeur de chaque barre de progression, lue depuis
//  son attribut data-largeur. On évite ainsi de mettre du code
//  Jinja directement dans un style="", ce que VSCode signale (à
//  tort) comme une erreur de syntaxe CSS.
// =============================================================

document.querySelectorAll(".barre-progression-remplissage[data-largeur]").forEach((barre) => {
    barre.style.width = barre.dataset.largeur + "%";
});