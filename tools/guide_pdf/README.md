# Générateur du guide PDF français

Lire [REGENERER.txt](REGENERER.txt) pour les commandes. Le générateur utilise ReportLab, Pillow et PyMuPDF, déclarés dans [requirements.txt](requirements.txt), ainsi que les polices macOS Arial et Menlo.

```sh
# Depuis la racine du projet
.venv/bin/python -m pip install -r tools/guide_pdf/requirements.txt
.venv/bin/python tools/guide_pdf/prepare.py
.venv/bin/python tools/guide_pdf/build.py
```

| Fichier | Responsabilité |
|---|---|
| [content.py](content.py) | Notices éditoriales : expériences, brouillons, projets tiers et applications. |
| [prepare.py](prepare.py) | Inventaires et extraits, fiches HTML dans `tmp/pdfs`. |
| [build.py](build.py) | Mise en page, citations locales, figures, sommaire, signets et pièces jointes. |
| [assets](assets/README.md) | Captures et constats datés réutilisés pour l’édition publiée. |

Sortie : [Cardputer-Guide-complet-FR.pdf](../../output/pdf/Cardputer-Guide-complet-FR.pdf). Les fichiers de travail se trouvent sous `tmp/pdfs/`. Les [captures de portails](../../docs/assets/portails/README.md) et les images du dépôt sont conservées avec les sources du générateur.

## Maintenir le contenu

Le PDF livré est une **édition datée**, antérieure à l’enrichissement des commentaires et README. Les extraits numérotés, les nombres de fichiers et les constats inscrits dans `build.py` ne se mettent pas tous à jour automatiquement. Revoir ces passages et les notices de `content.py` avant de publier une nouvelle édition ; préparer un inventaire ne relance ni une compilation, ni des essais physiques.

## Vérifier le rendu

Ouvrir le PDF ou rendre les pages avec PyMuPDF. Contrôler titres, tableaux, contraste des schémas, retours de code, légendes, signets et pièces jointes. Une figure doit rester accompagnée de sa provenance. Les maquettes ne doivent jamais être décrites comme des captures d’exécution du Cardputer.
