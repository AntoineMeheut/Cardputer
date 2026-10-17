/**
 * Ancien scanner I²C — brouillon historique, exclu des environnements actifs.
 * Utilise GROVE_YELLOW et GROVE_WHITE via Lab.h. s réinterroge les adresses.
 * Référence à privilégier : experiments/09-i2c-scan.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <Wire.h>
// Le scan est lancé à la demande et conserve seulement ce que cette variante affiche ou écrit sur le
// port série.
void scan() {
    String found = "Adresses I2C (hex):\n";
    unsigned count = 0;
    for (uint8_t address = 8; address < 120; ++address) {
        Wire.beginTransmission(address);
        if (Wire.endTransmission() == 0) { found += "0x" + String(address, HEX) + " "; ++count; }
    }
    Lab::screen(found + "\nTotal: " + count + "\ns: relancer");
    Serial.println(found);
}
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() { Lab::begin("10 Scanner Grove I2C"); Wire.begin(GROVE_YELLOW, GROVE_WHITE, 100000); Wire.setTimeOut(50); scan(); }
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
// Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
// série, non validé sur la dalle.
void loop() { if (Lab::input() == 's') scan(); delay(10); }
