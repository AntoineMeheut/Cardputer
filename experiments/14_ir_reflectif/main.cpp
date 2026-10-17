/**
 * Réflectif avec calibration — brouillon historique, exclu des environnements actifs.
 * c calibre l’état de repos et remet le compteur à zéro. Le brouillon utilise lab::Debouncer ; le
 * programme actif considère directement DO actif bas.
 * Référence à privilégier : experiments/10-ir-reflectif.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <lab_logic.h>
lab::Debouncer debounce;
unsigned count = 0;
int emptyLevel = HIGH;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("14 Capteur IR reflectif U175");
    pinMode(GROVE_YELLOW, INPUT); analogReadResolution(12);
    emptyLevel = digitalRead(GROVE_YELLOW);
    Lab::screen("Demarrer sans objet\nc: calibrer et remettre a zero");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    if (Lab::input() == 'c') { emptyLevel = digitalRead(GROVE_YELLOW); count = 0; debounce = lab::Debouncer(); }
    bool object = digitalRead(GROVE_YELLOW) != emptyLevel;
    if (debounce.update(object, millis())) ++count;
    static uint32_t last = 0;
    if (millis()-last > 100) {
        last = millis();
        Lab::screen("ADC GPIO1: " + String(analogRead(GROVE_WHITE)) + "\nObjet: " + (debounce.state() ? "oui" : "non") +
                    "\nPassages: " + count + "\nc: calibrer sans objet\nADC = intensite, pas distance");
    }
    delay(2);
}
