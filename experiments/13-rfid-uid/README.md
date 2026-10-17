# 13 — Lire l’identifiant des cartes F08

Matériel : **Cardputer, RFID2, Grove et carte F08**. Lire [le guide détaillé](../../docs/composants/rfid2.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e rfid-uid
pio run -e rfid-uid -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Présenter une seule carte, relever son UID, puis la retirer avant une nouvelle lecture.

Résultat attendu : UID, SAK et type sont affichés, sans écriture sur la carte.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5rfid-legacy) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#rfid-uid) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le lecteur est initialisé par reset logiciel. Le code termine l’échange avec PICC_HaltA et PCD_StopCrypto1.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Vérifier auparavant l’adresse I²C 0x28 avec l’expérience 09.
2. Présenter une seule F08 et lire l’UID, le SAK et le type.
3. Retirer la carte avant de la représenter ; comparer avec une seconde carte de test.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Le WS1850S utilise ici le chemin Classic 1K. Un UID de démonstration comme 04 11 22 33 ne provient pas d’une lecture physique dans ce guide.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
