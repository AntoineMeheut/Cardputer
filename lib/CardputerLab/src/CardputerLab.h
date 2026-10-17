/**
 * Interface matérielle des vingt expériences actives.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <M5Cardputer.h>
#include <SD.h>
#include <SPI.h>
#include <Wire.h>

// Cardputer K132 d'origine. Les couleurs sont celles du câble Grove M5Stack.
namespace Lab {
// Broches du K132 original : ne pas transférer ces constantes à une autre carte sans contrôler son
// schéma.
constexpr int YELLOW = 2, WHITE = 1, IR_TX = 44;
constexpr int SD_CS = 12, SD_MOSI = 14, SD_SCK = 40, SD_MISO = 39;
constexpr int GPS_RX = WHITE, GPS_TX = YELLOW;
constexpr uint32_t GPS_BAUD = 115200;
// Initialise M5Cardputer et la console 115200 bauds, dessine le bandeau 240×20 et place le curseur
// dans la zone de contenu.
inline void begin(const char* title) {
    auto cfg = M5.config();
    M5Cardputer.begin(cfg, true);
    Serial.begin(115200);
    M5Cardputer.Display.setRotation(1);
    M5Cardputer.Display.setTextSize(1);
    M5Cardputer.Display.setTextColor(TFT_WHITE, TFT_BLACK);
    M5Cardputer.Display.fillScreen(TFT_BLACK);
    M5Cardputer.Display.fillRect(0, 0, 240, 20, 0x0255);
    M5Cardputer.Display.setCursor(4, 6);
    M5Cardputer.Display.print(title);
    M5Cardputer.Display.setCursor(4, 26);
    Serial.println(title);
}
// Efface seulement la zone sous le bandeau. Ne réinitialise ni les périphériques ni les données de
// l’expérience.
inline void body() {
    M5Cardputer.Display.fillRect(0, 22, 240, 113, TFT_BLACK);
    M5Cardputer.Display.setCursor(4, 26);
}
// Duplique la ligne vers l’écran et la console série, ce qui permet de récupérer les résultats qui
// dépassent la hauteur visible.
inline void line(const String& text) {
    M5Cardputer.Display.println(text);
    Serial.println(text);
}
// Contrat : appeler M5Cardputer.update avant ce test. Retourne vrai sur un nouvel événement contenant
// le caractère demandé.
inline bool pressed(char key) {
    if (!M5Cardputer.Keyboard.isChange() || !M5Cardputer.Keyboard.isPressed()) return false;
    for (char value : M5Cardputer.Keyboard.keysState().word) if (value == key) return true;
    return false;
}
// Entrée est un drapeau distinct des caractères imprimables ; ce test évite de la chercher dans
// keysState().word.
inline bool enter() {
    return M5Cardputer.Keyboard.isChange() && M5Cardputer.Keyboard.isPressed()
        && M5Cardputer.Keyboard.keysState().enter;
}
// Initialise le bus SPI et monte une SD à 10 MHz ; retourne faux si le montage échoue ou si aucune
// carte n’est détectée.
inline bool sdBegin() {
    SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
    return SD.begin(SD_CS, SPI, 10000000) && SD.cardType() != CARD_NONE;
}
// Précondition : SD montée. Cherche le premier nom libre de 0 à 9999 ; retourne une chaîne vide si
// aucun nom ne convient. Ne crée pas encore le fichier.
inline String nextFile(const char* prefix, const char* extension) {
    for (unsigned i = 0; i < 10000; ++i) {
        String path = String(prefix) + String(i) + extension;
        if (!SD.exists(path)) return path;
    }
    return "";
}
// Bus Grove : SDA G2, SCL G1, 100 kHz ; un délai de 50 ms évite d’attendre indéfiniment un
// périphérique muet.
inline void i2cBegin() { Wire.begin(YELLOW, WHITE, 100000); Wire.setTimeOut(50); }
// Émet une transaction sans données. Un ACK confirme une adresse, pas la nature ni le bon
// fonctionnement complet du module.
inline bool i2cPresent(uint8_t address) {
    Wire.beginTransmission(address);
    return Wire.endTransmission() == 0;
}
}
