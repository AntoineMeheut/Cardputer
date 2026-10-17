/**
 * Interface historique des brouillons ; préférer CardputerLab.h pour les expériences actives.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <M5Cardputer.h>
#include <SPI.h>
#include <SD.h>
#include <lab_config.h>

namespace Lab {
// Ancienne initialisation de l’écran : elle règle aussi la luminosité à 100 et utilise une disposition
// différente du bandeau actif.
inline void begin(const char *title) {
    auto config = M5.config();
    M5Cardputer.begin(config, true);
    Serial.begin(115200);
    M5Cardputer.Display.setRotation(1);
    M5Cardputer.Display.setTextSize(1);
    M5Cardputer.Display.setTextColor(TFT_WHITE, TFT_BLACK);
    M5Cardputer.Display.setBrightness(100);
    M5Cardputer.Display.fillScreen(TFT_BLACK);
    M5Cardputer.Display.setCursor(0, 0);
    M5Cardputer.Display.println(title);
    Serial.println(title);
}
// Redessine une zone de texte brute ; contrairement à Lab::line, ce texte n’est pas automatiquement
// dupliqué sur Serial.
inline void screen(const String &text) {
    M5Cardputer.Display.fillRect(0, 16, 240, 119, TFT_BLACK);
    M5Cardputer.Display.setCursor(0, 18);
    M5Cardputer.Display.print(text);
}
// Actualise le clavier et ne conserve qu’un caractère par événement : Entrée devient LF, Effacer
// devient retour arrière, absence d’événement devient zéro.
inline char key() {
    M5Cardputer.update();
    if (!M5Cardputer.Keyboard.isChange() || !M5Cardputer.Keyboard.isPressed()) return 0;
    auto state = M5Cardputer.Keyboard.keysState();
    if (state.enter) return '\n';
    if (state.del) return '\b';
    return state.word.empty() ? 0 : state.word.front();
}
// Cette variante monte à 20 MHz et suppose des constantes SD_* externes, absentes du lab_config.h
// actuel. Adapter avant compilation.
inline bool sdBegin() {
    SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
    return SD.begin(SD_CS, SPI, 20000000);
}
// Ouvre en ajout, écrit puis vide les tampons et ferme à chaque appel ; retourne vrai si tous les
// octets du texte ont été acceptés.
inline bool append(const char *path, const String &text) {
    File file = SD.open(path, FILE_APPEND);
    if (!file) return false;
    const size_t written = file.print(text);
    file.flush();
    file.close();
    return written == text.length();
}
// Ancien essai de capture, commande !. Aucun convertisseur capture_ecran.py
// n’est présent dans le projet ; ce chemin n’a pas été validé sur le matériel.
// Tentative historique de lecture RGB565 ligne par ligne. La présence de readRect ne prouve pas que le
// bus/dalle permet de relire les pixels.
inline void capture() {
    uint16_t pixels[240];
    Serial.println("CPFRAME 240 135");
    for (int y = 0; y < 135; ++y) {
        M5Cardputer.Display.readRect(0, y, 240, 1, pixels);
        for (auto pixel : pixels) Serial.printf("%04X", pixel);
        Serial.println();
    }
    Serial.println("CPFRAME END");
}
// Intercepte ! pour la tentative de capture, puis masque cette commande à l’application appelante.
inline char input() {
    char c = key();
    if (c == '!') { capture(); return 0; }
    return c;
}
}
