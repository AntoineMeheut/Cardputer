# Contribuer au laboratoire

Le projet cible d'abord le Cardputer K132 et les huit équipements du cahier des charges. Documenter en français les prérequis, le modèle exact, les broches, les commandes, le résultat attendu et les limites d'une nouvelle expérience.

## Vérifier une modification

```sh
python tools/test_host.py
python tools/check_docs.py
python tools/fetch_upstream.py --verify
pio run -e ENVIRONNEMENT_MODIFIE
```

La vérification complète est `python tools/build_all.py`. Ajouter un environnement dans `platformio.ini` et une entrée dans `tools/lab_catalog.py` pour une nouvelle expérience. Régénérer les README de programmes avec `python tools/lab_catalog.py` et les visuels avec `python tools/build_assets.py` après mise à jour du catalogue. Le générateur de README conserve les compléments situés après `<!-- documentation-code-fr -->`.

Les commentaires français ajoutés dans `upstream/sources/` à la demande de l’utilisateur sont une exception documentaire tracée par [le registre des ajouts](upstream/documentation-fr/README.md). Les archives et les instructions originales restent conservées. Pour modifier le fonctionnement d’une source tierce, créer une adaptation locale et en indiquer l’origine ; ne pas modifier les empreintes amont pour faire accepter une différence.

Après une modification de documentation, exécuter aussi `python tools/check_documentation.py` et `python tools/upstream_documentation.py verify`. Ce dernier vérifie la version enregistrée ; une édition personnelle supplémentaire nécessite une nouvelle revue du registre et ne sera pas écrasée par sa réapplication.

## Documenter un essai matériel

Indiquer modèle et révision, version de la bibliothèque, alimentation, câblage, commande utilisée et observation. Une compilation réussie n'est pas un test matériel. Distinguer « attendu », « observé » et « non testé ». Ajouter une photo réelle après retrait des coordonnées GPS, SSID privés et identifiants personnels visibles. Les captures d'aperçu doivent conserver leur mention de démonstration.

## Préparer GitHub

Suivre le [guide de publication manuelle](docs/publication/README.md). `python tools/prepare_publication.py --check` contrôle la copie publique ; la même commande sans option crée un ZIP propre et son manifeste SHA-256, sans créer de dépôt distant ni exécuter de `push`.

Après restauration, le dossier de travail comprend les téléchargements complets, mais `.gitignore` exclut leurs caches, l'environnement Python, les outils installés, les binaires compilés et les captures privées. Le manifeste, les guides et les programmes originaux sont destinés au dépôt. Après un clone ou un nettoyage, `python tools/fetch_upstream.py` restaure les projets référencés.

Initialiser Git dans ce dossier si nécessaire, consulter `git status` puis ajouter seulement les fichiers voulus. Ne pas inclure les archives de plusieurs centaines de mégaoctets, des clés Wi-Fi, des traces personnelles ou des firmwares construits sans vérifier les conditions de leurs dépendances. Choisir ensuite son nom de dépôt et son compte GitHub. Aucun dépôt distant n'est créé automatiquement par ce laboratoire.

Les anciens dossiers d'expériences comportant un souligné (`01_diagnostic`, etc.) sont conservés comme brouillons, hors des environnements vérifiés. Une contribution peut en récupérer une idée après révision et adaptation, mais ne doit pas les présenter comme les programmes du parcours actuel.
