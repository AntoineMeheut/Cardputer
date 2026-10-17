# 09 — Détecter le RFID2 sur I²C

Matériel : **Cardputer, Grove et RFID2**. Lire [le guide détaillé](../../docs/composants/rfid2.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e i2c-scan
pio run -e i2c-scan -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Brancher hors tension, lancer le programme ; s refait le scan.

Résultat attendu : Le RFID2 doit répondre à 0x28 sur SDA G2 / SCL G1.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5rfid) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#i2c-scan) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le bus est à 100 kHz et le délai Wire à 50 ms. Le scan interroge les adresses 0x08 à 0x77.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Brancher RFID2 hors tension : SDA sur G2, SCL sur G1, alimentation et masse.
2. Démarrer et chercher Adresse : 0x28.
3. Presser s après une reconnexion réalisée hors tension ; passer ensuite à rfid-uid.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `scan()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Une réponse confirme le bus et l’adresse, pas la lecture radio. Le GPS UART et le capteur analogique ne répondent pas à ce scan.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
