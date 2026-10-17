# 02 — Carnet sur microSD

Matériel : **Cardputer et microSD FAT32**. Lire [le guide détaillé](../../docs/composants/cardputer.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e notes-sd
pio run -e notes-sd -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Saisir une note de 80 caractères maximum, corriger avec effacement, valider par Entrée.

Résultat attendu : Chaque note est ajoutée à /notes.txt ; lire le fichier sur ordinateur après extinction.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5cardputer) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#notes-sd) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le fichier est ouvert en ajout, puis fermé après chaque note. Le code contrôle le nombre d’octets écrits avant de vider la saisie.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Insérer une microSD FAT32 hors tension et démarrer ; attendre SD prete.
2. Taper une phrase de 80 caractères maximum, effacer un caractère puis valider par Entrée.
3. Vérifier Note ajoutee, saisir une seconde note, éteindre et ouvrir notes.txt sur l’ordinateur.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `draw()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Erreur SD : contrôler format et contacts. Ouverture impossible : vérifier l’espace et l’état de la carte. Conserver la note si l’écriture échoue.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
