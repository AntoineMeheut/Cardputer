# Adaptateur RfidLegacy

Cette bibliothèque relie les expériences locales au pilote [MFRC522-I2C archivé](../../upstream/sources/m5rfid-legacy). Ses deux fichiers dans [src](src/README.md) incluent les sources tierces par chemin relatif. Les auteurs et la licence du pilote restent attachés au projet d’origine.

Utiliser `#include <rfid_lab.h>` depuis les expériences RFID du laboratoire : [lecture UID](../../experiments/13-rfid-uid/README.md) et [bloc 4](../../experiments/14-rfid-bloc/README.md). L’initialisation WS1850S est dans [include/rfid_lab.h](../../include/rfid_lab.h), car le module n’expose pas la broche RESET attendue par l’ancien pilote.

Préparer les instantanés avec `python tools/fetch_upstream.py`, puis compiler `pio run -e rfid-uid`. Ne pas ajouter en parallèle un second fichier objet du même pilote : les implémentations seraient définies deux fois.
