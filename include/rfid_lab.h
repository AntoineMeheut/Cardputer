/**
 * Adaptation du pilote MFRC522-I2C au RFID Unit 2 WS1850S.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <CardputerLab.h>
#include <MFRC522_I2C.h>
// Le connecteur du RFID2 n'expose pas RESET. Ne pas appeler PCD_Init() du
// pilote historique : il manipule une broche de reset inexistante.
// Retourne false si le lecteur n’acquitte pas, ne sort pas du reset en 300 ms ou expose une version
// invalide ; aucun accès aux blocs d’une carte ici.
inline bool beginRfid(MFRC522& reader) {
    Lab::i2cBegin();
    if (!Lab::i2cPresent(0x28)) return false;
    // Déclencher le reset par registre, car le module Grove n’expose aucune broche RESET pilotable.
    reader.PCD_WriteRegister(MFRC522::CommandReg, MFRC522::PCD_SoftReset);
    delay(50);
    uint32_t start = millis();
    // Le bit PowerDown (0x10) reste actif pendant la sortie du reset ; attendre sans bloquer
    // définitivement la boucle.
    while (reader.PCD_ReadRegister(MFRC522::CommandReg) & 0x10) {
        if (millis() - start > 300) return false;
        delay(1);
    }
    byte version = reader.PCD_ReadRegister(MFRC522::VersionReg);
    if (version == 0 || version == 0xFF) return false;
    // Configuration du timer et de la modulation reprise pour les échanges ISO14443A : préscaler,
    // rechargement, ASK et graine CRC sont liés au protocole, pas à l’adresse I²C.
    reader.PCD_WriteRegister(MFRC522::TModeReg, 0x80);
    reader.PCD_WriteRegister(MFRC522::TPrescalerReg, 0xA9);
    reader.PCD_WriteRegister(MFRC522::TReloadRegH, 0x03);
    reader.PCD_WriteRegister(MFRC522::TReloadRegL, 0xE8);
    reader.PCD_WriteRegister(MFRC522::TxASKReg, 0x40);
    reader.PCD_WriteRegister(MFRC522::ModeReg, 0x3D);
    reader.PCD_AntennaOn();
    Serial.printf("Version lecteur : 0x%02X\n", version);
    return true;
}
// Formate size octets en hexadécimal à deux chiffres séparés par des espaces ; le tampon doit contenir
// au moins size octets.
inline String hexBytes(const byte* bytes, size_t size) {
    String result;
    for (size_t i = 0; i < size; ++i) { if (bytes[i] < 16) result += '0'; result += String(bytes[i], HEX); if (i + 1 < size) result += ' '; }
    return result;
}
