# 11 — Recevoir une trame ASK/OOK

Matériel : **Cardputer, RF433R et émetteur de test compatible**. Lire [le guide détaillé](../../docs/composants/rf433-recepteur.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e rf433-rx
pio run -e rf433-rx -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Déclencher la source de test ; comparer code, bits, protocole et durée.

Résultat attendu : Une trame compatible s’affiche ; l’absence de décodage ne prouve pas l’absence de signal.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/rc-switch) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#rf433-rx) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le programme attend radio.available(), affiche les paramètres puis réinitialise l’indicateur de réception. 0x5A1234 vaut 5 902 900 en décimal.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Brancher le récepteur RF433R : sortie sur G1.
2. Sur une seconde station, émettre la trame synthétique de l’expérience 12.
3. Comparer 0x5A1234, 24 bits, protocole 1 et impulsion de 350 µs.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Une absence de décodage ne prouve pas une absence de signal RF. Fréquence, modulation, protocole et temporisation doivent correspondre.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
