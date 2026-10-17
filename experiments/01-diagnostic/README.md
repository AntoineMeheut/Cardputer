# 01 — Diagnostic du Cardputer

Matériel : **Cardputer seul**. Lire [le guide détaillé](../../docs/composants/cardputer.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e diagnostic
pio run -e diagnostic -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Taper des lettres, presser s pour un bip, puis G0.

Résultat attendu : Écran, clavier, tension batterie et bouton sont affichés.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5cardputer) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#diagnostic) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

L’écran est rafraîchi toutes les 500 ms. La tension affichée ne permet pas à elle seule de déduire l’autonomie.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Démarrer sans module Grove et lire le titre du programme.
2. Taper Bonjour ; vérifier la ligne Touches. Presser s pour demander un bip de 880 Hz pendant 120 ms.
3. Maintenir G0 puis le relâcher ; observer son état. Relever la tension, la RAM libre et la taille de flash.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Un écran allumé ne valide pas le clavier. Si les touches sont absentes, vérifier le modèle K132 et l’initialisation M5Cardputer.begin(cfg, true).

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
