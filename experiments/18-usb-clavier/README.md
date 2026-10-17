# 18 — Phrase au clavier USB

Matériel : **Cardputer, câble USB de données et éditeur de texte**. Lire [le guide détaillé](../../docs/composants/cardputer.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e usb-clavier
pio run -e usb-clavier -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Ouvrir un éditeur vide sur son poste ; presser Entrée sur le Cardputer.

Résultat attendu : Une phrase fixe est saisie une fois par pression ; disposition US de la bibliothèque HID.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5cardputer) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#usb-clavier) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

USBHIDKeyboard est démarré au setup. Le texte n’est envoyé que sur l’événement Entrée, puis les touches sont relâchées.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Installer l’environnement usb-clavier, qui utilise ARDUINO_USB_MODE=0.
2. Ouvrir un document texte vide sur le poste et placer le curseur dedans. Utiliser une disposition US pour correspondre à la bibliothèque.
3. Presser Entrée sur le Cardputer : Bonjour depuis Cardputer est saisi une fois.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Si le port série change ou disparaît, revenir au mode G0 pour reprogrammer. Les paramètres USB de cette cible ne doivent pas être copiés vers toutes les autres.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
