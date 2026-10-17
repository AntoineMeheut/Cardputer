# 15 — Afficher position et heure UTC

Matériel : **Cardputer, Grove et GPS/BDS v1.1**. Lire [le guide détaillé](../../docs/composants/gps-at6668.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e gps
pio run -e gps -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Sortir, orienter l’antenne vers le ciel, vérifier les octets NMEA et attendre une position récente.

Résultat attendu : Latitude, longitude, satellites, altitude/vitesse disponibles et heure UTC.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/tinygpsplus) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#gps) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le tampon UART vaut 2048 octets. TinyGPSPlus reçoit les octets en continu. Les données de position de plus de trois secondes ne sont plus affichées comme actuelles.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Brancher le GPS v1.1 AT6668 : RX Cardputer G1, TX Cardputer G2 ; 115200 bauds.
2. Placer l’antenne face au ciel et vérifier que NMEA recus progresse.
3. Attendre une position récente et relever latitude, longitude et heure UTC ; altitude et vitesse sont conditionnelles.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Aucun octet : vérifier câble, débit et version de module. Des octets sans fix : améliorer la vue du ciel. L’UTC ne correspond pas directement à l’heure locale.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
