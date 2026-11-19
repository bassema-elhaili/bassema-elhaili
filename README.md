# CI13 — Marchés exportateurs à fort potentiel

Compte rendu individuel — Contrôle continu Partie B · S7 Commerce international · ENCG Settat
**Bassema El Haili** — Code Apogée 26006128 — Module BD & DS — A. Larhlimi.

Classification binaire : à partir des indicateurs de l'année `t`, prédire si la croissance des importations d'un pays en `t+1` dépasse **10 %**. Modèle principal : **Random Forest** comparé à une référence naïve.

## Résultat en bref

| Méthode | F1 validation | F1 test | Accuracy test |
|---|---|---|---|
| Référence naïve (classe majoritaire) | 0.000 | 0.000 | 0.500 |
| Forêt aléatoire (200 arbres) | 0.545 | **0.449** | 0.523 |

Objectif annoncé avant expérimentation : F1 ≥ 0,40 et supérieur à la référence → **atteint**. Précision 0,531 · rappel 0,389 · ROC-AUC 0,561. Voir `docs/resultats.json`.

## Arborescence

```text
.
├── README.md                    # ce fichier
├── requirements.txt             # versions Python
├── .gitignore
├── DECLARATION_IA.md            # déclaration d'usage des outils d'IA
├── data/raw/
│   ├── donnees_CI13.csv         # 4 241 observations, 193 pays, 2000-2023
│   └── README.md                # source, licence, date d'extraction
├── scripts/
│   ├── telecharger_donnees.py   # téléchargement reproductible (API Banque mondiale)
│   ├── construire_notebook.py   # génération de la structure du notebook
│   └── generer_livrables.py     # rapport PDF, 6 diapositives, docs
├── docs/
│   ├── fiche_sujet_CI13.md      # fiche du sujet attribué
│   ├── sources.md               # références et licence
│   └── resultats.json           # métriques calculées
├── notebooks/
│   └── projet_CI13.ipynb        # notebook exécuté (code + compte rendu intégré)
├── figures/                     # 3 figures d'exploration, schéma, résultats
├── rapport/
│   ├── rapport.pdf              # export du compte rendu (15 pages)
│   └── rapport.html
├── presentation/
│   ├── presentation.pdf         # exactement 6 diapositives
│   └── presentation.tex         # source LaTeX
└── video/
    ├── demonstration.mp4        # 87 s, 720p, voix off française
    └── README.md                # plan de la vidéo et note sur la voix
```

## Reproduction

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Données : déjà fournies dans data/raw/. Pour les régénérer :
python scripts/telecharger_donnees.py

# Notebook (exécuter les cellules dans l'ordre) :
jupyter nbconvert --to notebook --execute --inplace notebooks/projet_CI13.ipynb

# Rapport PDF et diapositives (à partir du notebook exécuté) :
python scripts/generer_livrables.py
```

Graine fixée à 42, chemins relatifs, aucune clé d'API.

## Livrables

- [x] Notebook exécuté : `notebooks/projet_CI13.ipynb`
- [x] Compte rendu PDF : `rapport/rapport.pdf`
- [x] Six diapositives : `presentation/presentation.pdf` + source `.tex`
- [x] Figures : `figures/`
- [x] README, dépendances, déclaration IA, fiche sujet, sources
- [x] Vidéo MP4 (87 s, 720p) : `video/demonstration.mp4` (voix off synthétique, voir `video/README.md`)
- [ ] Formulaire officiel : https://forms.gle/SmfW9kbcNbsz4Q8a7

Le dépôt porte le nom `bassema-elhaili` (créé avant l'attribution) ; la convention de l'énoncé est `CodeApogee-Nom-Groupe`.
