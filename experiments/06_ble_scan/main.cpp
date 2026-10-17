/**
 * Scan avec NimBLE — brouillon historique, exclu des environnements actifs.
 * Dépend de NimBLEDevice et de son API de résultats. La cible active utilise BLEDevice de la pile
 * fournie par Arduino-ESP32.
 * Référence à privilégier : experiments/06-ble-scan.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <NimBLEDevice.h>
// Le scan est lancé à la demande et conserve seulement ce que cette variante affiche ou écrit sur le
// port série.
void scan() {
    Lab::screen("Ecoute BLE pendant 4 secondes...");
    auto scanner = NimBLEDevice::getScan();
    scanner->setActiveScan(false);
    auto results = scanner->start(4, false);
    String text = "Annonceurs: " + String(results.getCount()) + "\n";
    for (int i = 0; i < results.getCount(); ++i) {
        auto d = results.getDevice(i);
        String line = String(d.getName().c_str()).substring(0, 16) + " " + d.getRSSI() + "dBm";
        Serial.println(line);
        if (i < 8) text += line + "\n";
    }
    scanner->clearResults();
    Lab::screen(text + "s: relancer");
}
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() { Lab::begin("06 Annonces Bluetooth LE"); NimBLEDevice::init(""); scan(); }
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
// Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
// série, non validé sur la dalle.
void loop() { if (Lab::input() == 's') scan(); delay(10); }
