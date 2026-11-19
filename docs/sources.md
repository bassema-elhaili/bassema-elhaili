# Sources et références

## Données

- **World Bank Open Data — World Development Indicators (WDI).** https://data.worldbank.org
  - Importations de biens et services (USD courants) : `NE.IMP.GNFS.CD`
  - Commerce en % du PIB : `NE.TRD.GNFS.ZS`
  - Croissance du PIB (annuel, %) : `NY.GDP.MKTP.KD.ZG`
  - PIB par habitant (USD courants) : `NY.GDP.PCAP.CD`
  - Téléchargement : `https://api.worldbank.org/v2/en/indicator/<CODE>?downloadformat=csv`
  - Licence : CC BY 4.0 · Extraction : 19/11/2026 · Téléchargement reproductible : `scripts/telecharger_donnees.py`.

## Encadrement pédagogique

- A. Larhlimi, *Contrôle continu — Partie B : Machine Learning appliqué au commerce international*, ENCG Settat, 2026–2027.
- A. Larhlimi, *Guide pratique à cocher — Contrôle continu Partie B*, ENCG Settat, 2026–2027.

## Logiciels

- scikit-learn 1.9.1 (`RandomForestClassifier`, `DummyClassifier`, `Pipeline`, `ColumnTransformer`, `GridSearchCV`).
- pandas 3.1.1, NumPy 2.5.5, matplotlib 3.11.2, requests 2.34.2.
- nbconvert 7.17.2 + WeasyPrint 70.0 pour l'export PDF du notebook ; pdflatex pour les diapositives.
