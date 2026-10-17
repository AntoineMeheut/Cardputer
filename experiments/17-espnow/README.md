# 17 — Messages entre deux Cardputer

Matériel : **Deux Cardputer ; adaptation possible sur un second ESP32**. Lire [le guide détaillé](../../docs/experiences/wifi-bluetooth.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e espnow
pio run -e espnow -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Téléverser le même programme sur les deux ; presser Entrée alternativement.

Résultat attendu : Le pair reçoit Bonjour ; le retour d’envoi seul ne garantit pas la réception applicative.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/cardputer-demo) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#espnow) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le paquet possède une signature, un compteur et 32 octets de texte. La réception vérifie taille, signature et terminaison ; une file de quatre paquets sépare le rappel radio de l’interface.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Installer espnow sur les deux cartes, avec LAB_ESPNOW_CHANNEL identique, par défaut 1.
2. Presser Entrée sur A ; chercher Recu #1 et Bonjour du Cardputer sur B.
3. Répéter depuis B. Noter séparément la remise au pilote et la réception visible chez le pair.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `onReceive()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

La diffusion est non chiffrée et sans accusé applicatif. Trame confiee au pilote ne prouve pas que B a affiché le message.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
