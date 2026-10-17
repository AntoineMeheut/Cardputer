# 08 — Télécommande TV infrarouge

Matériel : **Cardputer, votre TV et un code NEC compatible connu**. Lire [le guide détaillé](../../docs/experiences/television-ir.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e ir-tv
pio run -e ir-tv -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Renseigner LAB_NEC_CODE, viser votre TV puis presser Entrée.

Résultat attendu : Une trame NEC est émise ; la réaction de la TV valide le code, pas le seul texte à l’écran.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/irremote) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#ir-tv) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

IRsend utilise G44 et une trame NEC de 32 bits. 0x20DF10EF est une valeur d’exemple, pas une commande universelle.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Identifier le code NEC de son appareil et remplacer LAB_NEC_CODE dans include/lab_config.h.
2. Compiler et installer ir-tv ; viser le récepteur IR du téléviseur.
3. Après au moins une seconde, presser Entrée une fois et vérifier la réaction réelle du téléviseur.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Le message Une trame NEC envoyee indique l’appel logiciel. Vérifier le protocole, l’ordre des bits et la visée si le téléviseur ne réagit pas. U175 ne permet pas d’apprendre le code.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
