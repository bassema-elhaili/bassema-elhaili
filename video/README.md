# Vidéo explicative

`demonstration.mp4` est présent : **87 secondes**, **1280×720 (720p, 16:9)**, voix off en français, avec les mêmes données, métriques et visuels que le notebook et les six diapositives.

Déroulé :

| Temps | Contenu |
|---|---|
| 0–20 s | Identité (Bassema El Haili, 26006128, S7 CI), sujet CI13 et problématique |
| 20–45 s | Jeu de données Banque mondiale (193 pays, 4 241 observations) et découpage chronologique |
| 45–65 s | Forêt aléatoire, pipeline sans fuite et validation croisée |
| 65–80 s | Tableau comparatif référence vs modèle, F1 = 0,449 |
| 80–87 s | Conclusion, limite principale et piste d'amélioration |

⚠️ **Important :** la voix est **synthétique** (français `fr-FR-DeniseNeural`, générée avec `edge-tts`) car aucun micro n'était disponible ici. Si l'enseignant exige une voix personnelle, réenregistrez la narration avec votre voix en gardant exactement le même plan et les mêmes chiffres (`docs/resultats.json`).

Pour régénérer la vidéo : `pip install edge-tts` puis `python scripts/creer_video.py` (nécessite aussi `ffmpeg` et `pdftoppm`).
