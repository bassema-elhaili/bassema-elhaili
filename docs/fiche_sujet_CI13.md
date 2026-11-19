# Fiche du sujet attribué — CI13

**Titre :** Marchés exportateurs à fort potentiel
**Type :** classification binaire supervisée (source S5 — Banque mondiale, indicateurs du commerce).

**Problématique :** à partir des indicateurs commerciaux et macroéconomiques de l'année `t`, prédire si la croissance des importations d'un pays en `t+1` dépassera 10 %.

**Jeu de données :** Banque mondiale (WDI), 193 pays, 2000–2024, fréquence annuelle, licence CC BY 4.0, extrait le 19/11/2026. Observations pays-année ; montants en USD courants, croissances et ouverture en %.

**Algorithme principal :** Random Forest Classifier (200 arbres), comparé à `DummyClassifier(strategy="most_frequent")`.

**Métrique principale :** F1-score sur la classe positive ; objectif ≥ 0,40 et supérieur à la référence, fixé avant expérimentation. Métriques secondaires : accuracy, précision, rappel, ROC-AUC, matrice de confusion.

**Protocole :** découpage chronologique (entraînement ≤ 2019, test 2020–2023), validation croisée stratifiée à 5 plis sur l'entraînement, réglage de `max_depth` et `min_samples_leaf`, prétraitements ajustés sur le train uniquement via `Pipeline` / `ColumnTransformer`.

**Résultats :** voir `docs/resultats.json` et `rapport/rapport.pdf`.
