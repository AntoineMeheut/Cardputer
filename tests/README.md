# Tests exécutables sur ordinateur

Depuis la racine :

```sh
python tools/test_host.py
```

Prérequis : Python, Git et un compilateur C++ accessible par `c++`, avec C++11. Aucun Cardputer, module radio ou carte SD n’est nécessaire.

| Source | Ce qui est vérifié |
|---|---|
| [test_formats.cpp](test_formats.cpp) | WAV PCM mono, garde du bloc RFID 4, taille/signature/terminaison des paquets ESP-NOW. |
| [test_gpx.py](test_gpx.py) | Conversion de trois points, altitude absente, refus d’écrasement, valeurs non finies, coordonnées hors limites et heure non UTC. |
| [test_upstream_documentation.py](test_upstream_documentation.py) | Réversibilité exacte des commentaires, détection des éditions inconnues, idempotence, validation avant écriture et empreinte des arbres d’origine. |
| [test_publication.py](test_publication.py) | Exclusion des fichiers privés et caches, refus des liens extérieurs ou vers des rapports non distribués, intégrité et déterminisme du ZIP. |

`tools/test_host.py` exécute la découverte Python, construit le test C++ dans un répertoire temporaire, puis relit le WAV avec le module standard `wave`. Cette seconde lecture évite de vérifier un format uniquement avec son propre producteur.

Pour exécuter seulement les tests Python : `python -m unittest discover -s tests -v`. Le jeu de données est documenté dans [fixtures](../fixtures/README.md). Ces contrôles n’attestent ni une qualité audio réelle, ni une réception radio, ni un fonctionnement du lecteur RFID.
