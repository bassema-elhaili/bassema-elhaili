#!/usr/bin/env python3
"""Finalise le notebook exécuté et génère rapport PDF, diapositives et docs."""

import json
import subprocess
from pathlib import Path

import nbformat
from nbconvert.exporters import HTMLExporter
from weasyprint import HTML

RACINE = Path(__file__).resolve().parents[1]
NOTEBOOK = RACINE / "notebooks" / "projet_CI13.ipynb"


def lire_metriques(nb) -> dict:
    for cellule in nb.cells:
        for sortie in cellule.get("outputs", []):
            texte = str(sortie.get("text", ""))
            if "METRIQUES_JSON=" in texte:
                return json.loads(texte.split("METRIQUES_JSON=", 1)[1].strip())
    raise ValueError("Métriques introuvables : exécuter d'abord le notebook.")


def remplacer_nb(nb, valeurs: dict) -> None:
    for cellule in nb.cells:
        if cellule.cell_type != "markdown":
            continue
        for cle, valeur in valeurs.items():
            cellule.source = cellule.source.replace(f"@@{cle}@@", str(valeur))
        assert "@@" not in cellule.source, "Marqueur non remplacé dans une cellule."


def main() -> None:
    nb = nbformat.read(NOTEBOOK, as_version=4)
    m = lire_metriques(nb)

    importances = m["importances"]
    variable_top = max(importances, key=importances.get)
    matrice = m["matrice_confusion"]
    objectif = ("ATTEINT" if m["test_f1"] >= 0.40 and m["test_f1"] > m["test_f1_reference"]
                else "NON ATTEINT")
    valeurs = {
        "PERIODE": m["periode"],
        "N_LIGNES": m["n_lignes"],
        "N_COLONNES": m["n_colonnes"],
        "N_PAYS": m["n_pays"],
        "MANQ_IMP": m["manq_imp"],
        "MANQ_CROISS": m["manq_croiss"],
        "MANQ_OPEN": m["manq_open"],
        "MANQ_GDP": m["manq_gdp"],
        "MANQ_PCAP": m["manq_pcap"],
        "INTERP1": (
            "La croissance médiane est positive la plupart des années (environ "
            f"+{m['croissance_mediane']:.1f} % en moyenne), mais elle s'effondre lors des chocs "
            "mondiaux : −17,8 % en 2009, −11,3 % en 2015 et −12,0 % en 2020, "
            "suivis d'un rebond à +24,8 % en 2021. Le marché des importations est donc "
            "cyclique et volatile."
        ),
        "INTERP2": (
            "Les deux nuages se superposent largement : l'ouverture commerciale seule "
            "ne sépare pas les marchés à fort potentiel des autres (corrélation faible, "
            f"r ≈ 0,06). La croissance des importations est très dispersée à ouverture égale : "
            "d'autres signaux (croissance passée, PIB) sont nécessaires."
        ),
        "INTERP3": (
            f"Les pays les plus dynamiques sur la période sont {m['top_pays']}, "
            "avec une croissance moyenne des importations nettement supérieure à la médiane "
            "mondiale. Leur couleur (part de années « fort potentiel ») montre que la "
            "dynamique moyenne ne garantit pas un classement stable année après année."
        ),
        "CV_REF": m["cv_reference"],
        "CV_FORET": m["cv_foret"],
        "F1_REF": m["test_f1_reference"],
        "ACC_REF": m["test_acc_reference"],
        "F1_FORET": m["test_f1"],
        "ACC_FORET": m["test_acc"],
        "PRECISION": m["test_precision"],
        "RAPPEL": m["test_rappel"],
        "AUC": m["test_auc"],
        "MATRICE": str(matrice),
        "VAR_IMP": f"« {variable_top} » (importance {importances[variable_top]:.3f})",
        "CORREL": m["correlation"],
        "OBJECTIF": objectif,
    }
    remplacer_nb(nb, valeurs)
    nbformat.write(nb, NOTEBOOK)
    print(f"Notebook finalisé : {NOTEBOOK}")

    # --- Export HTML puis PDF du notebook / compte rendu ---
    rapport = RACINE / "rapport"
    rapport.mkdir(exist_ok=True)
    html, _ = HTMLExporter().from_notebook_node(nb)
    css_supplementaire = (
        "<style>pre, code, div.highlight, .highlight pre {white-space: pre-wrap !important; "
        "word-break: break-word !important; overflow-wrap: anywhere !important; "
        "font-size: 8.5pt !important;} table {font-size: 8pt !important;}</style>"
    )
    html_pdf = html.replace("</head>", css_supplementaire + "</head>")
    (rapport / "rapport.html").write_text(html, encoding="utf-8")
    HTML(string=html_pdf, base_url=str(RACINE)).write_pdf(rapport / "rapport.pdf")
    print(f"Rapport : {rapport / 'rapport.pdf'}")

    # --- Métriques sauvegardées pour les autres livrables ---
    docs = RACINE / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "resultats.json").write_text(
        json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # --- Six diapositives (source LaTeX + PDF) ---
    presentation = RACINE / "presentation"
    presentation.mkdir(exist_ok=True)
    tex = r'''\documentclass[aspectratio=169,10pt]{beamer}
\usepackage[french]{babel}
\usepackage{graphicx,booktabs}
\graphicspath{{../figures/}}
\usetheme{Madrid}
\setbeamertemplate{footline}[frame number]
\definecolor{vert}{HTML}{0F766E}
\setbeamercolor{alerted text}{fg=vert}
\title{CI13 --- Marchés exportateurs à fort potentiel}
\subtitle{Contrôle continu Partie B --- S7 Commerce international}
\author{Bassema El Haili --- Code Apogée 26006128}
\institute{ENCG Settat --- BD \& DS --- A. Larhlimi}
\date{19/11/2026}
\begin{document}
\begin{frame}{1. Identité, problématique et objectif}
\textbf{Bassema El Haili} --- Code Apogée 26006128 --- Groupe S7 CI
\par\textbf{Sujet CI13 --- Marchés exportateurs à fort potentiel}
\par\bigskip
\textbf{Question :} les indicateurs commerciaux et macroéconomiques de l'année $t$
permettent-ils de prédire une croissance des importations supérieure à \textbf{10~\%} en $t+1$ ?
\par\bigskip
\textbf{Intérêt :} cibler les destinations à fort potentiel pour la prospection export.
\par\bigskip
\textbf{Tâche :} classification binaire supervisée.
\par\textbf{Objectif fixé avant test :} F1 $\geq 0{,}40$ et supérieur à la référence naïve.
\end{frame}

\begin{frame}{2. Jeu de données}
Source : \textbf{Banque mondiale (WDI)}, API publique, licence CC BY 4.0.
\par Période \PEN{} --- \NBL{} lignes, \NPAYS{} pays, fréquence annuelle.
\par Variables : importations (USD), croissance des importations (\%), ouverture (\% PIB),
croissance du PIB (\%), PIB/hab. (USD), cible binaire.
\par\bigskip
Qualité : agrégats exclus, doublons pays-année supprimés, aucune valeur manquante sur
les importations ou l'ouverture ; 0,74~\% de manquants sur la croissance du PIB.
\end{frame}

\begin{frame}{3. Exploration}
\begin{columns}
\column{0.55\textwidth}
\includegraphics[width=\textwidth]{fig1_croissance_annuelle.png}
\par Croissance médiane : creux en 2009, 2015, 2020 ; rebond en 2021.
\column{0.45\textwidth}
\includegraphics[width=\textwidth]{fig3_top_pays.png}
\par Pays les plus dynamiques : Serbie, Lao PDR, Kirghizistan.
\end{columns}
\end{frame}

\begin{frame}{4. Algorithme et protocole}
\includegraphics[width=0.92\textwidth]{schema_algorithme.png}
\par\textbf{Random Forest} (200 arbres) : bootstrap, sélection aléatoire de variables, vote majoritaire.
\par\textbf{Sans fuite :} variables passées uniquement ; entraînement $\leq$ 2019, test 2020--2023 ;
imputation/standardisation ajustées sur le train ; réglage par validation croisée stratifiée (5 plis).
\par Hyperparamètres : profondeur et minimum par feuille.
\end{frame}

\begin{frame}{5. Résultats}
\begin{tabular}{lccc}
\toprule
Méthode & F1 validation & F1 test & Accuracy test \\
\midrule
Référence naïve & \CVREF{} & \F1REF{} & \ACCREF{} \\
Forêt aléatoire & \CVFORET{} & \F1FORET{} & \ACCFORET{} \\
\bottomrule
\end{tabular}
\par\bigskip
Précision \PREC{}, rappel \RAP{}, ROC-AUC \AUC{}. Matrice de confusion : \MATRICE{}.
\par\bigskip
\includegraphics[width=0.8\textwidth]{fig4_resultats.png}
\end{frame}

\begin{frame}{6. Conclusion, limites, amélioration}
\textbf{Objectif \OBJECTIF{} :} F1 de \F1FORET{} contre \F1REF{} pour la référence.
Le modèle aide à \textbf{présélectionner} des marchés, sans pronostic certain.
\par\bigskip
\textbf{Limites :} croissance annuelle volatile et faible corrélation passé/futur (r $\approx 0{,}11$) ;
données agrégées (pas de code SH) ; chocs 2020--2023.
\par\bigskip
\textbf{Amélioration :} flux bilatéraux par produit, horizon 3 ans, gradient boosting et
seuil de décision calibré selon le coût des erreurs.
\end{frame}
\end{document}
'''
    remplacements_tex = {
        "\\PEN{}": f"{m['periode']}".replace("–", "--"),
        "\\NBL{}": str(m["n_lignes"]),
        "\\NPAYS{}": str(m["n_pays"]),
        "\\CVREF{}": str(m["cv_reference"]),
        "\\F1REF{}": str(m["test_f1_reference"]),
        "\\ACCREF{}": str(m["test_acc_reference"]),
        "\\CVFORET{}": str(m["cv_foret"]),
        "\\F1FORET{}": str(m["test_f1"]),
        "\\ACCFORET{}": str(m["test_acc"]),
        "\\PREC{}": str(m["test_precision"]),
        "\\RAP{}": str(m["test_rappel"]),
        "\\AUC{}": str(m["test_auc"]),
        "\\MATRICE{}": str(matrice).replace("[", "{").replace("]", "}"),
        "\\OBJECTIF{}": objectif,
    }
    for cle, valeur in remplacements_tex.items():
        tex = tex.replace(cle, valeur)
    (presentation / "presentation.tex").write_text(tex, encoding="utf-8")
    for _ in range(2):  # deux passes pour les références / numéros de page
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "presentation.tex"],
            cwd=presentation, check=True, stdout=subprocess.DEVNULL,
        )
    print(f"Présentation : {presentation / 'presentation.pdf'}")


if __name__ == "__main__":
    main()
