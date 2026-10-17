# Outils sur ordinateur

Exécuter les commandes **depuis la racine Cardputer**, avec l’environnement Python activé. Python 3.12 minimum est nécessaire à l’extraction des archives ; PlatformIO est déclaré dans [requirements.txt](../requirements.txt). Les outils graphiques demandent les dépendances supplémentaires indiquées ci-dessous.

| Outil | Commande / entrées | Sorties et effets |
|---|---|---|
| [fetch_upstream.py](fetch_upstream.py) | `python tools/fetch_upstream.py` ; manifeste des commits | Téléchargements, extraction et contrôle ; aucune exécution des projets tiers. `--verify` contrôle localement. |
| [build_all.py](build_all.py) | `python tools/build_all.py` | Compile chaque cible et remplace `build/NOM.log` et `build/compilation.json` ; aucun flash. |
| [test_host.py](test_host.py) | `python tools/test_host.py` ; compilateur `c++` disponible | Tests Python, tests C++ puis relecture du WAV ; fichiers temporaires nettoyés. |
| [check_docs.py](check_docs.py) | `python tools/check_docs.py` | Liens locaux, SVG et accord catalogue/PlatformIO ; statut non nul si erreur. |
| [check_documentation.py](check_documentation.py) | `python tools/check_documentation.py` | Couverture des README de code et liens des sections françaises tierces. |
| [upstream_documentation.py](upstream_documentation.py) | `python tools/upstream_documentation.py verify` ou `apply` | Vérifier ou réappliquer les insertions connues ; refus des modifications personnelles inconnues. |
| [gps_csv_to_gpx.py](gps_csv_to_gpx.py) | `python tools/gps_csv_to_gpx.py fixtures/trace-exemple.csv trace.gpx` | Trois points fictifs vers un fichier GPX neuf ; aucun réseau ni écrasement. |
| [lab_catalog.py](lab_catalog.py) | `python tools/lab_catalog.py` | Régénère le catalogue et la partie automatique des README actifs, en préservant le complément français balisé. |
| [build_assets.py](build_assets.py) | `python tools/build_assets.py` | Remplace neuf schémas SVG et `apercu.html` depuis les modèles du script. |
| [capture_previews.py](capture_previews.py) | `python tools/capture_previews.py` | Remplace seize PNG d’aperçu ; Playwright et Chromium requis. |
| [build_branding.py](build_branding.py) | `python tools/build_branding.py` | Régénère la bannière SVG ; PyMuPDF et deux polices locales requis, voir [l’identité visuelle](../docs/assets/identite/README.md). |
| [prepare_publication.py](prepare_publication.py) | `python tools/prepare_publication.py --check` puis sans option | Contrôle les fichiers publics, crée un ZIP et un manifeste SHA-256 ; Python et Git, aucun réseau ni modification du dépôt Git local. |
| [guide_pdf](guide_pdf/README.md) | Préparation puis composition | PDF A4, annexes, signets et inventaires ; dépendances et polices propres au générateur. |

## Pages autonomes

Ouvrir [apercu.html](apercu.html) directement dans un navigateur pour choisir une expérience ; son hash d’URL sélectionne la fiche. Les données sont fictives. Le modèle à modifier est dans `build_assets.py`.

Ouvrir [modulation.html](modulation.html), choisir OOK, FSK ou FM puis déplacer Déviation. `draw()` intègre une phase et construit les chemins SVG de la porteuse et de sa commande ; les valeurs n’ont pas d’unités radio réelles. Aucun matériel n’est piloté.

## Installation des captures

Installer [requirements-dev.txt](../requirements-dev.txt), puis le navigateur avec `python -m playwright install chromium`. Le cache attendu par le script est `.cache/playwright` ; configurer `PLAYWRIGHT_BROWSERS_PATH` vers ce dossier pendant l’installation si nécessaire. Un poste interdisant les processus graphiques peut empêcher la capture même si le code est correct.

## Retours et erreurs

Les scripts de contrôle retournent un statut non nul en cas d’échec. Le convertisseur CSV valide toutes les lignes avant création du GPX et refuse une destination existante. La compilation conserve son journal, y compris en cas d’échec. Ne pas déduire un résultat matériel d’une capture d’aperçu ou d’un code de retour du compilateur.
