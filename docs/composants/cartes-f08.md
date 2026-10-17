# Cartes RFID F08 13,56 MHz

Les [cartes F08 du cahier des charges](https://shop.m5stack.com/products/13-56mhz-rfid-card-f08-chip-5pcs) sont des cartes passives de la famille compatible MIFARE Classic 1K / ISO14443-A. Elles s'alimentent dans le champ du lecteur. La capacité utile dépend de la séparation entre blocs de données, données constructeur et contrôle d'accès ; « 1 Ko » ne signifie pas 1 Ko libre pour un fichier.

## Préparer le lecteur

Installer et connecter le [RFID2](rfid2.md). Lancer `i2c-scan` puis `rfid-uid`, sans écrire. Étiqueter physiquement une carte **TEST LAB** parmi le lot. Ne pas utiliser un badge d'accès existant pour le premier essai.

![Lecteur, carte et liaison I²C](../assets/schemas/rfid.svg)

## Comprendre l'organisation

Une Classic 1K comporte 16 secteurs de 4 blocs de 16 octets. Le dernier bloc de chaque secteur est un **trailer** qui contient des clés et des conditions d'accès. Le bloc 0 contient les données constructeur et l'UID : une carte F08 ordinaire n'est pas une carte à UID réinscriptible.

| Secteur | Blocs | Usage dans ce laboratoire |
|---|---|---|
| 0 | 0, 1, 2, 3 | Aucun écrit ; 0 constructeur, 3 trailer |
| 1 | 4, 5, 6, 7 | **Bloc 4 seulement** ; 7 trailer |
| 2 à 15 | 8 à 63 | Aucun écrit local ; chaque quatrième bloc est un trailer |

Cette organisation vient du [pilote et de ses commentaires MIFARE](../../upstream/sources/m5rfid-legacy/MFRC522_I2C.h). Ne pas appliquer automatiquement cette carte mémoire à un NTAG ou à un badge DESFire.

## Essai de lecture et d'écriture

1. Charger `rfid-bloc` et ouvrir le moniteur série à 115200 bauds.
2. Présenter TEST LAB sans appuyer sur `w`. Lire le bloc 4 et noter les 16 octets imprimés. Une erreur signifie que l'authentification ou la lecture n'a pas abouti.
3. Retirer la carte. Appuyer sur `w`, puis la représenter dans les dix secondes.
4. Vérifier le message **« Ecriture relue et verifiee »**. En cas d'erreur, ne pas supposer que le contenu est resté intact : relire.
5. Retirer et représenter la carte en mode lecture ; retrouver le texte en hexadécimal. Pour le modifier, changer les 16 octets de `payload` et recompiler.

Le programme utilise la clé A `FF FF FF FF FF FF`, courante à l'état usine. Il n'effectue ni recherche de clés, ni changement des droits, ni écriture d'UID. Les cartes déjà configurées peuvent refuser l'opération.

## Ce que l'expérience permet

Tester la persistance d'un texte après redémarrage, associer une carte à une fiche d'inventaire ou comparer les UID de ses cartes. Une reconnaissance par UID peut servir à une démonstration, mais ne constitue pas une authentification robuste pour une vraie serrure. « Copier 16 octets de données » et « reproduire un badge d'accès » sont deux résultats différents ; ce projet ne prétend pas obtenir le second.

Les [exemples officiels récents](../../upstream/sources/m5rfid/examples) permettent d'étudier d'autres opérations avec leurs propres prérequis. Les captures du [guide RFID2](rfid2.md) sont des démonstrations visuelles, pas des lectures effectuées sur vos cartes.
