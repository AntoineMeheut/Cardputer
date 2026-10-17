# 14 — Lire et écrire le bloc 4 de test

Matériel : **Cardputer, RFID2 et F08 vierge réservée au laboratoire**. Lire [le guide détaillé](../../docs/composants/cartes-f08.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e rfid-bloc
pio run -e rfid-bloc -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Lire d’abord sans w. Retirer la carte ; w arme dix secondes, puis représenter la carte TEST.

Résultat attendu : Le bloc 4 seul est remplacé puis relu ; les trailers et le bloc constructeur ne sont pas écrits.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5rfid-legacy) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#rfid-bloc) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le programme exige une Classic 1K, utilise la clé A usine FF FF FF FF FF FF et écrit CARDPUTER LAB FR, exactement 16 octets. Une relecture et memcmp contrôlent le résultat.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Sans presser w, présenter TEST LAB et conserver les 16 octets AVANT affichés sur le port série.
2. Retirer la carte. Presser w puis la représenter dans les dix secondes.
3. Vérifier Ecriture relue et verifiee ; retirer puis représenter en lecture pour confirmer la persistance.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Le bloc constructeur et les trailers sont exclus. En cas d’erreur, relire pour connaître l’état effectif. Une carte à clés différentes peut refuser l’authentification.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
