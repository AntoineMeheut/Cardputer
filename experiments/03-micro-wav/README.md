# 03 — Enregistrer et écouter un WAV

Matériel : **Cardputer ; microSD facultative pour conserver le fichier**. Lire [le guide détaillé](../../docs/composants/cardputer.md) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e micro-wav
pio run -e micro-wav -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

Presser r, parler une seconde, puis p pour écouter la prise. Répéter r crée un nouveau fichier.

Résultat attendu : Un signal mono 16 kHz / 16 bits est conservé en RAM et, si disponible, sur SD.

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/m5cardputer) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#micro-wav) est une démonstration avec données fictives, pas un émulateur de l'ESP32.

<!-- documentation-code-fr -->
## Comprendre le programme

Le tampon contient 16 000 échantillons int16_t, soit 32 000 octets. Un en-tête RIFF/WAVE de 44 octets précède les données. Micro et haut-parleur sont arrêtés alternativement.

Les commentaires de [main.cpp](main.cpp) détaillent les états, les unités, les délais et les contrôles avant chaque opération importante.

### Démonstration détaillée

1. Appuyer sur r et parler pendant la seconde d’enregistrement.
2. Appuyer sur p pour réécouter la prise en RAM. Répéter r pour une autre prise.
3. Avec une SD, retrouver micro-0.wav puis micro-1.wav. Vérifier : mono, 16 bits, 16 000 Hz, une seconde.

### Points d’entrée et dépendances

- `setup()` initialise le programme une fois ; `loop()` traite ensuite les événements en continu.
- Repères présents dans ce fichier : `setup()`, `loop()`.
- [Interface commune](../../lib/CardputerLab/README.md) : écran, clavier, SD et formats partagés.
- [Paramètres et pilote RFID](../../include/README.md) : constantes communes et raccordement.

### Diagnostiquer un résultat inattendu

Sans SD, l’écoute reste possible en RAM. Une capture échouée ne produit pas une prise valide. Le code impose une attente maximale de trois secondes au micro.

Une compilation réussie vérifie la construction du firmware ; elle ne confirme ni le câblage ni une réception radio. Les états attendus ci-dessus restent à confronter à un essai réel.
