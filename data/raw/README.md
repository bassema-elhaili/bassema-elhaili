# Données brutes — sujet CI13

**Fichier :** `donnees_CI13.csv` — 4 434 lignes × 7 colonnes (avant création de la cible), 193 pays, 2000–2024.

**Source :** Banque mondiale — World Development Indicators (WDI), API publique v2 :

- `NE.IMP.GNFS.CD` — importations de biens et services (USD courants)
- `NE.TRD.GNFS.ZS` — commerce en % du PIB
- `NY.GDP.MKTP.KD.ZG` — croissance annuelle du PIB (%)
- `NY.GDP.PCAP.CD` — PIB par habitant (USD courants)

URL : `https://api.worldbank.org/v2/en/indicator/<CODE>?downloadformat=csv`

**Licence :** CC BY 4.0 (Banque mondiale) — réutilisation autorisée avec attribution.

**Date d'extraction :** 19/11/2026.

**Traitement :** agrégats régionaux exclus à l'aide du fichier `Metadata_Country` fourni par l'API, lignes sans importations supprimées, doublons pays-année supprimés.

**Reproduire :** `python scripts/telecharger_donnees.py` (aucune clé d'API requise).
