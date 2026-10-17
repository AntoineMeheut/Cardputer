# Données fictives pour les essais

[trace-exemple.csv](trace-exemple.csv) contient trois points GPS de démonstration ; ce n’est pas une trace personnelle relevée sur le terrain.

| Colonne | Format attendu |
|---|---|
| `utc` | Date et heure ISO 8601 en UTC, avec `Z` ou un décalage nul. |
| `latitude` | Degrés décimaux finis dans [-90, 90]. |
| `longitude` | Degrés décimaux finis dans [-180, 180]. |
| `altitude_m` | Nombre fini ou cellule vide ; le troisième point n’a pas d’altitude. |
| `satellites` | Information éventuelle du journal embarqué, non exportée dans le GPX. |

Depuis la racine : `python tools/gps_csv_to_gpx.py fixtures/trace-exemple.csv trace.gpx`. Choisir un nom de sortie inexistant. Le résultat attendu est trois points ; le fichier ne doit pas être créé si une ligne est invalide. Voir les [tests](../tests/README.md) pour les cas d’erreur.
