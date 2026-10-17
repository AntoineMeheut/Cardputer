# Commentaires français des projets tiers

Ce répertoire conserve les ajouts réalisés à la demande de l’utilisateur dans les dix-huit instantanés de [sources](../sources). Les archives originales et les empreintes du [manifeste](../manifest.json) restent les références amont. Les notices et licences originales n’ont pas été remplacées.

## Contenu

- `ajouts.json.gz` : registre reproductible de chaque insertion, avec chemin, position en octets, texte ajouté, empreinte avant et empreinte après. Les ajouts concernent des commentaires et des README.
- [inventaire-code.json](inventaire-code.json) : chaque source/configuration parcourue, son rôle, les symboles et dépendances repérés.
- [formats-sans-commentaires.json](formats-sans-commentaires.json) : fichiers expliqués dans les README plutôt que modifiés, notamment le JSON strict qui n’accepte pas les commentaires.
- [bilan.json](bilan.json) : comptes de couverture de cette opération.

Les commentaires de fichiers indiquent le projet, le rôle du module, les dépendances repérées et le README à consulter. Les README décrivent la construction du projet parent, les exemples du dossier, les sous-répertoires et les limites. Ils complètent les détails d’API déjà présents dans les commentaires amont. Les tableaux de pixels, polices et ressources ne sont pas présentés comme des programmes autonomes.

## Vérifier et réappliquer

Depuis la racine Cardputer :

```sh
# Contrôler les ajouts documentaires exacts
python tools/upstream_documentation.py verify

# Contrôler les sources d’origine, après retrait virtuel des seuls ajouts connus
python tools/fetch_upstream.py --verify

# Réappliquer les ajouts sur des sources originales déjà restaurées
python tools/upstream_documentation.py apply

# Vérifier la couverture des README et les liens des sections françaises
python tools/check_documentation.py
```

Le téléchargement normal par `fetch_upstream.py` restaure aussi les ajouts enregistrés après validation de l’instantané. La réapplication est idempotente : un fichier déjà conforme n’est pas réécrit. Une modification personnelle inconnue est refusée, jamais remplacée silencieusement.

La vérification d’arbre retire virtuellement les ajouts reconnus, retrouve les octets originaux et compare l’empreinte au manifeste. Elle ne supprime pas aveuglément tous les commentaires. Un changement d’instruction, de commentaire non enregistré ou de ressource reste détecté. Les fichiers Finder `.DS_Store` sont ignorés dans cette comparaison ; aucun n’était présent dans les dix-huit archives originales.

## Récupérer les originaux

Les archives `upstream/archives/ID.tar.gz` contiennent toujours les sources d’origine. Pour comparer, extraire une archive dans un **autre répertoire** et conserver sa racine. Ne pas extraire par-dessus des adaptations personnelles. L’outil expose aussi `original_bytes` pour reconstruire et vérifier un fichier en mémoire ; aucune commande de suppression de la copie documentée n’est nécessaire pour contrôler son intégrité.

## Limites de la documentation

Les repères de symboles et d’imports proviennent d’une lecture statique. Ils ne constituent pas une preuve que chaque branche, chaque carte ou chaque exemple compile et fonctionne. Les sous-modules absents, les SDK Android/ESP-IDF et les matériels additionnels restent à préparer suivant les notices originales. Les commandes de construction ne déclenchent pas automatiquement un téléversement.

Les commentaires ajoutés déplacent les numéros de ligne. Les extraits du PDF précédemment livré restent ceux de son édition datée. Pour modifier les programmes eux-mêmes, créer une adaptation et la valider séparément ; ne pas réécrire les empreintes d’origine pour masquer une différence.
