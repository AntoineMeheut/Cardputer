/**
 * Diagnostic et luminosité — brouillon historique, exclu des environnements actifs.
 * Les touches + et - règlent la luminosité ; la batterie est présentée en pourcentage. Le raccourci !
 * appelle une ancienne capture série non validée.
 * Référence à privilégier : experiments/01-diagnostic.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
unsigned brightness = 100;
String last = "Appuyer sur une touche";
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() { Lab::begin("01 Diagnostic Cardputer"); }
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    const char c = Lab::input();
    if (c) {
        last = c == '\n' ? "Entree" : String(c);
        if (c == '+') brightness = min(255U, brightness + 15);
        if (c == '-') brightness = brightness > 15 ? brightness - 15 : 15;
        M5Cardputer.Display.setBrightness(brightness);
    }
    static uint32_t previous = 0;
    if (millis() - previous > 250) {
        previous = millis();
        Lab::screen("Touche: " + last + "\nBatterie: " + String(M5Cardputer.Power.getBatteryLevel()) +
                    "%\nRAM libre: " + String(ESP.getFreeHeap()) + "\nLuminosite: " + brightness +
                    "\n+/- luminosite\n! capture via USB");
    }
    delay(5);
}
