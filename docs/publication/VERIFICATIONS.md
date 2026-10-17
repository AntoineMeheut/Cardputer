# Préparation et nettoyage du 17 octobre 2026

## Contrôles effectués

| Contrôle | Résultat et portée |
|---|---|
| Bannière | SVG original rendu et inspecté ; lettres vectorisées, sans ressource distante. |
| Documents | Liens locaux et correspondance des 20 environnements contrôlés avant retrait des caches. |
| Code documenté | 47 répertoires de code local, 4 697 sources/configurations tierces, 1 125 README tiers et 10 346 liens français contrôlés. |
| Tests sur ordinateur | 10 tests Python, tests C++ des formats et relecture WAV réussis, également dans une extraction neuve du ZIP. |
| Publication | Sélection conforme au `.gitignore`, fichiers requis présents, liens distribués vérifiés, liens amont différés identifiés. |
| Archive | Chaque entrée ZIP relue et comparée à son SHA-256 ; manifeste séparé fourni. |
| Git | Initialisation et indexation réalisées uniquement dans un dossier temporaire ; `git diff --cached --check` réussi. |
| Configuration GitHub | YAML du workflow et métadonnées des modèles d’issue analysés sans erreur. |
| Restauration complète | Les 18 projets ont été extraits de nouveau dans une copie temporaire issue du ZIP ; 5 738 fichiers documentés reconstruits, puis empreintes amont et documentaires vérifiées. |

L’essai de restauration a réutilisé les archives originales locales, avec tout accès réseau désactivé dans le script de cet essai. Il valide le contenu livré et sa réapplication ; il ne constitue pas un nouveau test de disponibilité des serveurs GitHub. Les compilations des vingt programmes sont celles du [rapport du 17 octobre](../code/rapports/compilation-2026-10-17.json), antérieures à la mise en forme du README. Aucun programme actif embarqué n’a été modifié pour cette publication.

## Nettoyage demandé

Les répertoires reproductibles sont retirés du poste : `.venv`, `.pio`, `.platformio`, `.cache`, `build`, `tmp`, `upstream/archives` et les dix-huit arbres téléchargés sous `upstream/sources`. Les fichiers Finder et caches `__pycache__` sont également retirés. Les programmes, y compris les 19 brouillons historiques, restent présents.

Les éléments conservés comprennent :

- les sources locales, les notices et les captures pédagogiques ;
- le guide PDF et son générateur ;
- le manifeste des révisions tierces et le registre de tous les ajouts français ;
- les preuves publiques de validation ;
- le ZIP GitHub et son manifeste dans `output/publication/` ;
- une petite sauvegarde privée des originaux locaux et des journaux dans `output/sauvegardes/preparation-2026-10-17.zip`.

La mesure de volume avant/après est enregistrée localement dans `output/sauvegardes/nettoyage-2026-10-17.json`. Ces sauvegardes et les ZIP d’export ne sont pas inclus dans le futur dépôt ; le PDF l’est.

## Reprendre le développement

Recréer l’environnement et les sources depuis la racine :

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/fetch_upstream.py
pio run -e diagnostic
```

Sur Windows, suivre les variantes du [guide d’installation](../installation.md). Les outils graphiques et le générateur PDF ont leurs propres dépendances facultatives, documentées dans [tools](../../tools/README.md).

Après nettoyage, `python3 -B tools/prepare_publication.py --check` reste disponible sans restaurer les sources. Les contrôles complets `check_docs.py`, `check_documentation.py` et `fetch_upstream.py --verify` nécessitent d’abord leur restauration. L’option `-B` évite de recréer les caches Python pendant un simple contrôle de l’export.

Aucune publication, création de dépôt distant, release, installation sur Cardputer ou exécution de GitHub Actions n’a été effectuée pendant cette préparation.
