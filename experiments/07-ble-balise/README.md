# 07 — Émettre une balise BLE

Matériel : **Cardputer et second appareil de scan BLE**. Lire [le guide détaillé](../../docs/experiences/wifi-bluetooth.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e ble-balise
pio run -e ble-balise -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Chercher Cardputer-Lab avec le scanner ; Espace coupe ou rétablit les annonces.

Résultat attendu : Une balise non connectable, sans service GATT, apparaît dans un scanner BLE.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/bruce) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#ble-balise) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le type ADV_TYPE_NONCONN_IND rend cette balise non connectable. Les bornes d’intervalle sont 800 et 1600 unités BLE de 0,625 ms.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Lancer le programme et rechercher Cardputer-Lab sur un second scanner BLE.
2. Presser Espace ; vérifier le message Annonce arretee et attendre la disparition des nouvelles observations.
3. Presser de nouveau Espace pour reprendre.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `draw()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Ne pas essayer de lire un service GATT : ce programme n’en crée aucun. Le brouillon 07_ble_message propose un autre fonctionnement, non validé.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
