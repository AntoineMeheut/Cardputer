# 05 — Serveur Web local

Matériel : **Cardputer et navigateur sur téléphone ou PC**. Lire [le guide détaillé](../../docs/experiences/wifi-bluetooth.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e wifi-web
pio run -e wifi-web -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Rejoindre Cardputer-Lab avec le mot de passe affiché, puis ouvrir son adresse HTTP.

Résultat attendu : La page et /api/status retournent durée de fonctionnement et tension batterie.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/cardputer-demo) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#wifi-web) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

WebServer écoute sur le port 80. La page HTML est construite dans le firmware ; l’API renvoie deux valeurs numériques. Exemple fictif : {"uptime_s":42,"battery_mv":4020}.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Rejoindre Cardputer-Lab depuis un téléphone ou ordinateur avec la clé de démonstration cardputer-lab.
2. Ouvrir l’adresse affichée, normalement http://192.168.4.1, puis utiliser Actualiser.
3. Ouvrir /api/status et comparer uptime_s et battery_mv avec les informations de la page.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Ce point d’accès local ne fournit pas Internet. Si le téléphone quitte le réseau sans Internet, le maintenir connecté pour l’essai. L’aperçu pédagogique du guide n’est pas ce serveur exécuté.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
