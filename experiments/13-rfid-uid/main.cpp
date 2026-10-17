/**
 * Lire l’identifiant des cartes F08 — documentation française du laboratoire.
 * Identifier une carte sans modifier sa mémoire.
 * Matériel : Cardputer, RFID2, Grove et carte F08.
 * Compiler depuis la racine : pio run -e rfid-uid.
 * Utilisation : Présenter une seule carte, relever son UID, puis la retirer avant une nouvelle
 * lecture.
 * Résultat à vérifier : UID, SAK et type sont affichés, sans écriture sur la carte.
 * Lecture détaillée et raccordement : README.md et docs/composants/rfid2.md.
 */
#include <rfid_lab.h>
// Adresse I²C 0x28 ; la valeur 255 n’est pas une broche RESET utilisable. beginRfid réalise un reset
// logiciel.
MFRC522 reader(0x28, 255);
bool ready;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("13 | Identification carte RFID"); ready = beginRfid(reader);
    Lab::line(ready ? "Presenter une carte F08" : "RFID absent ou erreur I2C");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // Arrêter la tentative si le lecteur manque, si aucune nouvelle carte n’est détectée ou si la
    // sélection UID échoue.
    if (!ready || !reader.PICC_IsNewCardPresent() || !reader.PICC_ReadCardSerial()) { delay(30); return; }
    Lab::body(); Lab::line("UID : " + hexBytes(reader.uid.uidByte, reader.uid.size));
    Lab::line("SAK : 0x" + String(reader.uid.sak, HEX));
    Lab::line(String(reader.PICC_GetTypeName(reader.PICC_GetType(reader.uid.sak))));
    Lab::line("Retirer la carte pour recommencer");
    // Placer la carte en HALT et arrêter Crypto1 ; retirer puis représenter la carte pour recommencer.
    reader.PICC_HaltA(); reader.PCD_StopCrypto1();
}
