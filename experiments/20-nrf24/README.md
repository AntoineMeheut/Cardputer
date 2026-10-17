# 20 — Paquets NRF24 à deux stations

Matériel : **Deux NRF24, deux contrôleurs, adaptateur microSD/SPI et alimentation 3,3 V**. Lire [le guide détaillé](../../docs/experiences/nrf24.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e nrf24
pio run -e nrf24 -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Retirer SD, vérifier le câblage du guide, presser Entrée sur une seule station à la fois.

Résultat attendu : Le pair affiche Salut N ; l’émetteur indique si l’accusé matériel a été reçu.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/rf24) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#nrf24) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Canal 40 correspond ici à 2440 MHz. Le programme passe brièvement de l’écoute à l’émission ; G12 est maintenu haut pour désélectionner la SD.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Retirer toute microSD. Raccorder SPI via un adaptateur, CE sur G2, CSN sur G1 et alimentation 3,3 V stable.
2. Installer la même configuration sur deux stations : canal 40, 1 Mbit/s, adresse LAB01, charge utile 16 octets.
3. Presser Entrée sur une seule station à la fois ; vérifier Salut N sur le pair et l’accusé matériel côté émetteur.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Ce montage utilise les contacts SPI du logement microSD. Le brouillon de pont UART emploie canal 76, adresses CPL01/CPL02 et 32 octets : les deux montages ne sont pas interopérables tels quels.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
