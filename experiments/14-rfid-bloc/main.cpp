/**
 * Lire et écrire le bloc 4 de test — documentation française du laboratoire.
 * Lire puis remplacer les 16 octets du seul bloc 4 d’une F08 de test.
 * Matériel : Cardputer, RFID2 et F08 vierge réservée au laboratoire.
 * Compiler depuis la racine : pio run -e rfid-bloc.
 * Utilisation : Lire d’abord sans w. Retirer la carte ; w arme dix secondes, puis représenter la carte
 * TEST.
 * Résultat à vérifier : Le bloc 4 seul est remplacé puis relu ; les trailers et le bloc constructeur
 * ne sont pas écrits.
 * Lecture détaillée et raccordement : README.md et docs/composants/cartes-f08.md.
 */
#include <rfid_lab.h>
#include <LabFormats.h>
MFRC522 reader(0x28, 255);
bool ready, writeArmed = false;
uint32_t armedAt = 0;
// Seul le bloc de données 4 est autorisé ; ne pas remplacer par un trailer contenant clés et droits
// d’accès.
constexpr byte BLOCK = 4;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("14 | Carte de test : bloc 4"); ready = beginRfid(reader);
    Lab::line(ready ? "Lecture par defaut. Carte F08 vierge." : "Erreur RFID / I2C");
    Lab::line("w : armer ecriture pendant 10 s"); Lab::line("Puis presenter la carte de TEST");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    if (!ready) { delay(20); return; }
    // Une commande explicite arme une seule écriture, valable dix secondes ; le mode normal reste la
    // lecture.
    if (Lab::pressed('w')) { writeArmed = true; armedAt = millis(); Lab::body(); Lab::line("ECRITURE armee : bloc 4 seulement"); Lab::line("Presenter une F08 vierge sous 10 s"); }
    if (writeArmed && millis() - armedAt > 10000) { writeArmed = false; Lab::body(); Lab::line("Lecture seule : delai expire"); }
    if (!reader.PICC_IsNewCardPresent() || !reader.PICC_ReadCardSerial()) { delay(30); return; }
    // Consommer l’armement dès la présentation d’une carte, même si l’authentification ou le type ne
    // convient pas.
    bool doWrite = writeArmed; writeArmed = false;
    Lab::body();
    // Le parcours vise une Classic 1K de test. Les autres types n’emploient pas nécessairement cette
    // organisation mémoire.
    if (reader.PICC_GetType(reader.uid.sak) != MFRC522::PICC_TYPE_MIFARE_1K) {
        Lab::line("Carte non Classic 1K : operation refusee");
    } else {
        MFRC522::MIFARE_Key key;
        memset(key.keyByte, 0xFF, sizeof(key.keyByte)); // Clé usine d'une carte de test neuve.
        byte status = reader.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, BLOCK, &key, &reader.uid);
        // Une lecture MIFARE exige un tampon de 18 octets : 16 données plus les deux octets CRC.
        byte bytes[18] = {}; byte size = sizeof(bytes);
        if (status == MFRC522::STATUS_OK) status = reader.MIFARE_Read(BLOCK, bytes, &size);
        if (status != MFRC522::STATUS_OK) Lab::line("Lecture refusee : " + String(reader.GetStatusCodeName(status)));
        else {
            Serial.println("AVANT bloc 4 : " + hexBytes(bytes, 16));
            Lab::line("Bloc 4 : " + hexBytes(bytes, 8)); Lab::line(hexBytes(bytes + 8, 8));
            // La garde centralisée writableLabBlock est testée sur ordinateur et limite l’écriture au bloc 4.
            if (doWrite && Lab::writableLabBlock(BLOCK)) {
                byte payload[16] = {'C','A','R','D','P','U','T','E','R',' ','L','A','B',' ','F','R'};
                status = reader.MIFARE_Write(BLOCK, payload, sizeof(payload));
                // Réinitialiser la capacité avant la relecture, puis comparer les 16 octets écrits.
                size = sizeof(bytes);
                if (status == MFRC522::STATUS_OK) status = reader.MIFARE_Read(BLOCK, bytes, &size);
                Lab::line(status == MFRC522::STATUS_OK && memcmp(bytes, payload, 16) == 0 ? "Ecriture relue et verifiee" : "Ecriture / verification echouee");
            }
        }
    }
    reader.PICC_HaltA(); reader.PCD_StopCrypto1(); Lab::line("Retirer carte. w : armer a nouveau");
}
