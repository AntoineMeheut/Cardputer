# 10 — Mesurer et compter les approches

Matériel : **Cardputer, Grove et U175**. Lire [le guide détaillé](../../docs/composants/ir-reflectif.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e ir-reflectif
pio run -e ir-reflectif -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Approcher une feuille blanche puis noire ; observer AO/DO et presser r pour remettre le compteur à zéro.

Résultat attendu : La mesure change avec la réflexion ; le compteur détecte les approches lentes.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5unified) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#ir-reflectif) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

DO sur G2 est actif bas ; AO sur G1 est lu sur 12 bits. Le filtre de transition vaut 100 ms et l’écran est actualisé toutes les 200 ms.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Démarrer sans obstacle proche, noter DO et AO.
2. Approcher lentement une feuille blanche puis noire à angle comparable. Observer les différences et le compteur.
3. Effectuer dix approches espacées, compter manuellement, puis presser r.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

AO représente une intensité brute de 0 à 4095, pas des centimètres. Saturation, couleur, angle et lumière ambiante affectent la mesure.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
