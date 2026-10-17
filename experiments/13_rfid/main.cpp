/**
 * RFID combiné — brouillon historique, exclu des environnements actifs.
 * Réunit UID, lecture et écriture du bloc 4. Utilise la classe MFRC522_I2C et PCD_Init, différents du
 * pilote MFRC522 et du reset logiciel retenus dans le parcours actif.
 * Référence à privilégier : experiments/13-rfid-uid / 14-rfid-bloc.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <Wire.h>
#include <MFRC522_I2C.h>
#include <lab_logic.h>
MFRC522_I2C reader(0x28, -1, &Wire);
MFRC522_I2C::MIFARE_Key keyA;
bool armed = false;
uint32_t armedAt = 0;
constexpr uint8_t block = 4;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("13 RFID2 / carte F08");
    Wire.begin(GROVE_YELLOW, GROVE_WHITE, 100000); Wire.setTimeOut(50);
    reader.PCD_Init();
    memset(keyA.keyByte, 0xFF, 6);
    Lab::screen("Presenter une carte F08\nLecture UID + bloc 4\nw: armer ecriture 10 secondes\nSeulement vos cartes de test");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (c == 'w') { armed = true; armedAt = millis(); Lab::screen("Ecriture armee pour 10 secondes\nPresenter votre carte de test\nBloc 4 remplace par CARDPUTER-LAB"); }
    if (armed && millis() - armedAt >= 10000) { armed = false; Lab::screen("Armement expire. Lecture seule."); }
    if (!reader.PICC_IsNewCardPresent() || !reader.PICC_ReadCardSerial()) { delay(20); return; }
    String text = "UID:";
    for (uint8_t i = 0; i < reader.uid.size; ++i) { if (reader.uid.uidByte[i] < 16) text += '0'; text += String(reader.uid.uidByte[i], HEX); }
    auto type = reader.PICC_GetType(reader.uid.sak);
    if (type == MFRC522_I2C::PICC_TYPE_MIFARE_1K) {
        auto status = reader.PCD_Authenticate(MFRC522_I2C::PICC_CMD_MF_AUTH_KEY_A, block, &keyA, &reader.uid);
        if (status == MFRC522_I2C::STATUS_OK) {
            if (armed && lab::writableF08Block(block)) {
                uint8_t payload[16] = {'C','A','R','D','P','U','T','E','R','-','L','A','B',0,0,0};
                status = reader.MIFARE_Write(block, payload, sizeof(payload));
                text += status == MFRC522_I2C::STATUS_OK ? "\nEcriture OK" : "\nEcriture en echec";
            }
            uint8_t data[18] = {}, size = sizeof(data);
            status = reader.MIFARE_Read(block, data, &size);
            if (status == MFRC522_I2C::STATUS_OK) {
                text += "\nBloc 4:\n";
                for (int i=0; i<16; ++i) { if (data[i]<16) text += '0'; text += String(data[i], HEX); text += ' '; if(i==7) text+='\n'; }
            } else text += "\nLecture en echec";
        } else text += "\nCle FF refusee / auth echec";
    } else text += "\nType hors F08/Classic 1K";
    armed = false;
    reader.PICC_HaltA(); reader.PCD_StopCrypto1();
    text += "\nRetirer puis representer la carte";
    Serial.println(text); Lab::screen(text);
}
