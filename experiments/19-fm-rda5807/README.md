# 19 — Radio FM avec module additionnel

Matériel : **RDA5807, adaptation 3,3 V, antenne et audio externe ; absents de la liste initiale**. Lire [le guide détaillé](../../docs/experiences/fm.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e fm-rda5807
pio run -e fm-rda5807 -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Vérifier le montage documenté ; + / - règlent la fréquence par pas de 0,1 MHz.

Résultat attendu : La station est entendue sur la sortie audio du module FM, pas sur le haut-parleur interne.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/rda5807) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#fm-rda5807) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le code cherche une réponse à 0x10 ou 0x11, fixe le volume à 3 et limite l’accord entre 87,5 et 108 MHz.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Vérifier le module, l’alimentation 3,3 V et les niveaux I²C ; ajouter antenne et sortie audio externe.
2. Démarrer à 99,5 MHz. Utiliser + et - pour avancer par pas de 0,1 MHz.
3. Chercher une station connue et comparer l’affichage à l’accord audible.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `draw()`, `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

L’audio provient du RDA5807, pas du haut-parleur intégré. Le module n’appartient pas à l’inventaire initial et la réception physique n’a pas été testée ici.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
