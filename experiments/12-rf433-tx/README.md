# 12 — Envoyer une trame RF de laboratoire

Matériel : **Cardputer, RF433T et une station réceptrice séparée**. Lire [le guide détaillé](../../docs/composants/rf433-emetteur.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e rf433-tx
pio run -e rf433-tx -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Attendre cinq secondes, presser Entrée et vérifier la réception sur la seconde station.

Résultat attendu : Trois répétitions de la trame synthétique 0x5A1234 ; aucune émission automatique.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/rc-switch) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#rf433-tx) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Les réglages sont protocole 1, impulsion 350 µs, trois répétitions et charge utile 24 bits. Aucun envoi n’est automatique au démarrage.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Brancher RF433T : entrée TX sur G2. Préparer une seconde station en réception.
2. Attendre cinq secondes après le démarrage, puis presser Entrée.
3. Lire la trame sur le récepteur ; attendre cinq secondes avant un autre envoi.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

L’indication envoyee ne vaut pas accusé de réception. Utiliser uniquement la source de test prévue pour cette démonstration.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
