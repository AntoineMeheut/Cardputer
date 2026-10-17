/**
 * Diagnostic du Cardputer — documentation française du laboratoire.
 * Vérifier les périphériques intégrés avant de raccorder un accessoire.
 * Matériel : Cardputer seul.
 * Compiler depuis la racine : pio run -e diagnostic.
 * Utilisation : Taper des lettres, presser s pour un bip, puis G0.
 * Résultat à vérifier : Écran, clavier, tension batterie et bouton sont affichés.
 * Lecture détaillée et raccordement : README.md et docs/composants/cardputer.md.
 */
#include <CardputerLab.h>
// Conserve le dernier événement clavier entre deux rafraîchissements de l’écran.
String lastKey = "Appuyer sur une touche";
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() { Lab::begin("01 | Diagnostic Cardputer"); }
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    if (M5Cardputer.Keyboard.isChange() && M5Cardputer.Keyboard.isPressed()) {
        // keys.word contient les caractères imprimables ; Entrée et Effacer sont des drapeaux séparés.
        auto keys = M5Cardputer.Keyboard.keysState();
        lastKey = "Touches : ";
        for (char key : keys.word) lastKey += key;
        if (keys.enter) lastKey += "[ENTREE]";
        if (keys.del) lastKey += "[EFFACER]";
    }
    // Un appui sur s lance un bip de 880 Hz pendant 120 ms ; le son ne joue pas au démarrage.
    if (Lab::pressed('s')) { M5Cardputer.Speaker.setVolume(80); M5Cardputer.Speaker.tone(880, 120); }
    // Le clavier est interrogé à chaque tour, mais le dessin est limité à deux fois par seconde. La
    // soustraction non signée tolère le débordement de millis().
    static uint32_t refresh = 0;
    if (millis() - refresh < 500) return;
    refresh = millis(); Lab::body();
    Lab::line("Ecran / clavier / batterie / son");
    Lab::line("Batterie : " + String(M5Cardputer.Power.getBatteryVoltage()) + " mV");
    Lab::line("RAM libre : " + String(ESP.getFreeHeap()));
    Lab::line("Flash : " + String(ESP.getFlashChipSize() / 1048576) + " Mio");
    Lab::line(lastKey.substring(0, 38));
    Lab::line("s : bip   G0 : bouton utilisateur");
    Lab::line(M5Cardputer.BtnA.isPressed() ? "G0 appuye" : "G0 relache");
}
