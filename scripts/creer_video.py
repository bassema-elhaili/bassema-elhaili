#!/usr/bin/env python3
"""Génère video/demonstration.mp4 (720p, voix off française).

La voix est synthétique (edge-tts, voix fr-FR-DeniseNeural) : la vidéo sert de
démonstration prête à l'emploi, à remplacer par un enregistrement de votre voix
si l'enseignant exige une voix personnelle.

Prérequis : pip install edge-tts ; ffmpeg, ffprobe et pdftoppm sur le PATH.
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path

import edge_tts

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "video" / "demonstration.mp4"
VOIX = "fr-FR-DeniseNeural"
FPS = 24
LARGEUR, HAUTEUR = 1280, 720

# (texte parlé, numéro de diapositive utilisée comme visuel)
SEGMENTS = [
    (
        "Bonjour, je suis Bassema El Haili, code Apogée 26006128, étudiante en S7 "
        "Commerce international à l'ENCG Settat. Mon sujet, CI13, porte sur les marchés "
        "exportateurs à fort potentiel. La question est la suivante : les indicateurs "
        "commerciaux de l'année t permettent-ils de prédire une croissance des importations "
        "supérieure à dix pour cent l'année suivante ?",
        1,
    ),
    (
        "Les données proviennent de la Banque mondiale. Elles couvrent cent "
        "quatre-vingt-treize pays et quatre mille deux cent quarante et une observations "
        "annuelles. Les variables sont les importations, l'ouverture commerciale, la "
        "croissance du PIB et le PIB par habitant. Le découpage est chronologique : "
        "entraînement jusqu'en deux mille dix-neuf, test à partir de deux mille vingt.",
        2,
    ),
    (
        "J'ai retenu une forêt aléatoire de deux cents arbres, comparée à un classificateur "
        "naïf. Les prétraitements, l'imputation et la mise à l'échelle sont ajustés sur "
        "l'entraînement seulement, dans un pipeline. Les hyperparamètres ont été réglés "
        "par validation croisée stratifiée à cinq plis, sans jamais toucher au jeu de test.",
        4,
    ),
    (
        "Voici les résultats. La référence naïve obtient un F1-score nul : elle ne détecte "
        "aucun marché à fort potentiel. La forêt aléatoire atteint un F1 de zéro virgule "
        "quatre cent quarante-neuf sur le test, avec une précision de zéro virgule cinq "
        "cent trente et un et un ROC-AUC de zéro virgule cinq cent soixante et un. "
        "L'objectif fixé avant l'expérience est atteint.",
        5,
    ),
    (
        "En conclusion, la croissance passée des importations est peu corrélée à la croissance "
        "future. Le modèle sert donc à présélectionner des destinations pour la prospection, "
        "pas à garantir un pronostic. Sa limite principale : des données agrégées, sans détail "
        "par produit ni par partenaire commercial.",
        6,
    ),
]


async def generer_audio(texte: str, chemin: Path) -> None:
    await edge_tts.Communicate(texte, VOIX, rate="+28%").save(str(chemin))


def duree(chemin: Path) -> float:
    resultat = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(chemin)],
        check=True, capture_output=True, text=True,
    )
    return float(resultat.stdout.strip())


def diapositif(numero: int, chemin: Path) -> None:
    subprocess.run(
        ["pdftoppm", "-f", str(numero), "-l", str(numero), "-png",
         "-scale-to-x", str(LARGEUR), "-scale-to-y", str(HAUTEUR),
         "-singlefile", "presentation/presentation.pdf", str(chemin.with_suffix(""))],
        cwd=RACINE, check=True, capture_output=True,
    )
    # pdftoppm ajoute l'extension .png
    if not chemin.exists():
        candidat = Path(str(chemin) + ".png")
        if candidat.exists():
            candidat.replace(chemin)


def segment_video(image: Path, audio: Path, duree_sec: float, sortie: Path) -> None:
    images = int((duree_sec + 0.6) * FPS)
    filtre = (
        f"scale={LARGEUR}:{HAUTEUR}:force_original_aspect_ratio=increase,"
        f"crop={LARGEUR}:{HAUTEUR},"
        f"zoompan=z='min(zoom+0.00015,1.05)':d=1:x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)':s={LARGEUR}x{HAUTEUR}:fps={FPS},format=yuv420p"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loop", "1", "-i", str(image), "-i", str(audio),
         "-filter_complex", f"[0:v]{filtre}[v];[1:a]apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", str(duree_sec + 0.6),
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "160k", str(sortie)],
        check=True, capture_output=True,
    )


def main() -> None:
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="video_ci13_") as dossier:
        tmp = Path(dossier)
        fichiers = []
        for i, (texte, numero_diapo) in enumerate(SEGMENTS, start=1):
            audio = tmp / f"audio{i}.mp3"
            image = tmp / f"image{i}.png"
            video = tmp / f"segment{i}.mp4"
            print(f"Segment {i}/{len(SEGMENTS)} : voix + diapositive {numero_diapo} ...")
            asyncio.run(generer_audio(texte, audio))
            diapositif(numero_diapo, image)
            d = duree(audio)
            segment_video(image, audio, d, video)
            fichiers.append(video)

        liste = tmp / "liste.txt"
        liste.write_text("".join(f"file '{f}'\n" for f in fichiers), encoding="utf-8")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(liste),
             "-c", "copy", "-movflags", "+faststart", str(SORTIE)],
            check=True, capture_output=True,
        )

    print(f"Vidéo : {SORTIE}")
    print("Durée :", subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(SORTIE)],
        check=True, capture_output=True, text=True,
    ).stdout.strip(), "s")
    print("Taille :", round(SORTIE.stat().st_size / 1_000_000, 1), "Mo")


if __name__ == "__main__":
    main()
