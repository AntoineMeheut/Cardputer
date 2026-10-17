# Workflow de vérification

[verify.yml](verify.yml) utilise Ubuntu et Python 3.12. Il contrôle d’abord la sélection des fichiers publics, puis installe les dépendances, restaure les instantanés, vérifie leurs empreintes, contrôle les liens, exécute les tests hôte et compile les vingt environnements. Le jeton GitHub n’a qu’un accès de lecture au contenu. Le travail est limité à 60 minutes ; une nouvelle exécution sur la même référence remplace celle encore en cours.

Les journaux sous `build/` sont publiés comme artefact même après un échec. Aucune étape n’envoie un firmware vers un matériel physique. Le workflow ne prouve pas qu’un essai sur Cardputer a réussi et sa présence ne prouve pas qu’il a déjà tourné sur un dépôt distant.

Après ajout d’une expérience, maintenir ensemble le [catalogue](../../tools/lab_catalog.py) et [platformio.ini](../../platformio.ini). Les scripts locaux détaillent les mêmes vérifications dans [tools](../../tools/README.md).
