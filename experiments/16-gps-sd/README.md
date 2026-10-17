# 16 — Journal GPS et export GPX

Matériel : **Cardputer, GPS v1.1, Grove et microSD FAT32**. Lire [le guide détaillé](../../docs/composants/gps-at6668.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e gps-sd
pio run -e gps-sd -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Attendre une position, marcher, presser q pour fermer, éteindre puis copier le CSV.

Résultat attendu : Un fichier /trace-N.csv sans écrasement ; conversion locale avec tools/gps_csv_to_gpx.py.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/tinygpsplus) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#gps-sd) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Au maximum une ligne par seconde ; les données requises doivent avoir moins de deux secondes. Le CSV contient utc, latitude, longitude, altitude_m, satellites. Le programme n’invente pas de fix.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Insérer la SD et brancher le GPS hors tension ; démarrer et lire le nom trace-N.csv.
2. Attendre position, date et heure récentes ; effectuer un court parcours et observer le nombre de points.
3. Presser q, attendre Fichier ferme, éteindre, copier le CSV puis exécuter le convertisseur sur le poste.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Une SD absente empêche le journal. Un champ altitude peut rester vide. Ne pas retirer la SD pendant l’écriture ; q ferme définitivement le fichier pour cette session.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
