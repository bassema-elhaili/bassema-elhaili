#!/usr/bin/env python3
"""Télécharge les indicateurs Banque mondiale utilisés pour le sujet CI13.

Sujet CI13 — Marchés exportateurs à fort potentiel.
Source : World Bank Open Data (WDI), API v2, licence CC BY 4.0.
Aucune clé d'API n'est nécessaire.

Usage :
    python scripts/telecharger_donnees.py
Sortie :
    data/raw/donnees_CI13.csv
"""

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "data" / "raw" / "donnees_CI13.csv"
SORTIE.parent.mkdir(parents=True, exist_ok=True)

ANNEE_MIN, ANNEE_MAX = 2000, 2024
BASE = "https://api.worldbank.org/v2/en/indicator"

INDICATEURS = {
    "NE.IMP.GNFS.CD": "imports_val",      # Importations de biens et services (USD courants)
    "NE.TRD.GNFS.ZS": "trade_openness",   # Commerce en % du PIB
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",    # Croissance annuelle du PIB (%)
    "NY.GDP.PCAP.CD": "gdp_per_capita",   # PIB par habitant (USD courants)
}


def telecharger(indicateur: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Télécharge le CSV complet (zip) d'un indicateur et le renvoie en format long."""
    url = f"{BASE}/{indicateur}?downloadformat=csv"
    reponse = requests.get(url, timeout=120)
    reponse.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(reponse.content)) as archive:
        nom_pays = next(n for n in archive.namelist() if n.startswith("Metadata_Country"))
        nom_data = next(n for n in archive.namelist() if n.startswith("API_"))
        pays = pd.read_csv(archive.open(nom_pays))
        data = pd.read_csv(archive.open(nom_data), skiprows=4)

    annees = [str(a) for a in range(ANNEE_MIN, ANNEE_MAX + 1)]
    data = data[["Country Name", "Country Code"] + annees].melt(
        id_vars=["Country Name", "Country Code"],
        var_name="year",
        value_name="valeur",
    )
    data["year"] = data["year"].astype(int)
    data = data.rename(columns={"Country Name": "country", "Country Code": "countryiso3"})

    # Un agrégat régional n'a pas de région dans le fichier de métadonnées.
    pays = pays[["Country Code", "Region"]].dropna(subset=["Region"])
    return data, pays[["Country Code"]]


def main() -> None:
    df = None
    pays_retenus = None

    for code, colonne in INDICATEURS.items():
        data, pays = telecharger(code)
        print(f"  {code:20s} -> {colonne:16s} {len(data)} valeurs")
        data = data.rename(columns={"valeur": colonne})
        df = data if df is None else df.merge(
            data, on=["country", "countryiso3", "year"], how="outer"
        )
        pays_retenus = pays if pays_retenus is None else pays_retenus

    df = df[df["countryiso3"].isin(set(pays_retenus["Country Code"]))].copy()
    df = df.dropna(subset=["imports_val"])
    df = df[df["imports_val"] > 0]
    df = df.drop_duplicates(subset=["country", "year"])
    df = df.sort_values(["country", "year"]).reset_index(drop=True)

    for c in INDICATEURS.values():
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df.to_csv(SORTIE, index=False, encoding="utf-8")
    print(f"\nÉcrit : {SORTIE}  ({df.shape[0]} lignes x {df.shape[1]} colonnes)")
    print(f"Période : {df.year.min()}-{df.year.max()} | pays : {df.country.nunique()}")


if __name__ == "__main__":
    main()
