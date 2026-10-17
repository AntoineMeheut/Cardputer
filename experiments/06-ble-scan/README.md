# 06 — Écouter les annonces BLE

Matériel : **Cardputer ; balise BLE ou téléphone pour l’essai**. Lire [le guide détaillé](../../docs/experiences/wifi-bluetooth.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e ble-scan
pio run -e ble-scan -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Attendre quatre secondes ; s recommence. Consulter le moniteur pour tous les résultats.

Résultat attendu : Noms annoncés et RSSI ; un appareil sans nom n’est pas forcément absent.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/bruce) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#ble-scan) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le scanner est passif. Il affiche le nom annoncé et le RSSI, puis libère les résultats. Un appareil sans nom reste comptabilisé.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Mettre une balise de test à proximité et lancer le scan de quatre secondes.
2. Lire les six premiers résultats à l’écran ; ouvrir le moniteur série pour la liste complète.
3. Presser s pour recommencer après déplacement ou arrêt de la balise.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `scan()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Utiliser un scanner BLE pour comparer les observations. Les réglages Bluetooth du téléphone ne présentent pas forcément les balises non connectables.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
