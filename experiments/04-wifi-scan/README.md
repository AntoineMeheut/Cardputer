# 04 — Observer les réseaux Wi-Fi

Matériel : **Cardputer ; point d’accès 2,4 GHz pour vérifier**. Lire [le guide détaillé](../../docs/experiences/wifi-bluetooth.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e wifi-scan
pio run -e wifi-scan -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Attendre le scan passif ; n change de page, s relance.

Résultat attendu : SSID, canal et RSSI sont visibles ; les réseaux 5 GHz seuls sont absents.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/cardputer-demo) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#wifi-scan) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le scan est asynchrone et passif avec prise en compte des SSID cachés. Les valeurs RSSI sont des observations radio, pas des distances.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Allumer son point d’accès de test en 2,4 GHz, puis lancer le programme.
2. Lire le SSID, le canal et le RSSI ; n passe à la page suivante, par groupes de quatre réseaux.
3. Déplacer le Cardputer puis presser s pour comparer un nouveau relevé.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `draw()`, `scan()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Un réseau seulement 5 GHz ne peut pas apparaître. Un nom vide peut correspondre à un SSID caché. Le scan n’établit pas de connexion au réseau.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
