/**
 * Écouter les annonces BLE — documentation française du laboratoire.
 * Afficher les annonces Bluetooth Low Energy.
 * Matériel : Cardputer ; balise BLE ou téléphone pour l’essai.
 * Compiler depuis la racine : pio run -e ble-scan.
 * Utilisation : Attendre quatre secondes ; s recommence. Consulter le moniteur pour tous les
 * résultats.
 * Résultat à vérifier : Noms annoncés et RSSI ; un appareil sans nom n’est pas forcément absent.
 * Lecture détaillée et raccordement : README.md et docs/experiences/wifi-bluetooth.md.
 */
#include <CardputerLab.h>
#include <BLEDevice.h>
BLEScan* scanner;
void scan() {
    Lab::body(); Lab::line("Ecoute BLE pendant 4 secondes...");
    // Scan bloquant de quatre secondes. Le clavier ne peut pas relancer le scan pendant cet appel.
    BLEScanResults results = scanner->start(4, false);
    Lab::body(); Lab::line(String(results.getCount()) + " annonces | s : relancer");
    for (int i = 0; i < results.getCount(); ++i) {
        BLEAdvertisedDevice item = results.getDevice(i);
        // Le nom est facultatif dans une annonce BLE ; son absence n’est pas une erreur de réception.
        String label = item.haveName() ? String(item.getName().c_str()) : "(sans nom)";
        String text = label.substring(0, 23) + " " + String(item.getRSSI()) + " dBm";
        // L’écran ne présente que six entrées ; le moniteur série reçoit les suivantes.
        if (i < 6) Lab::line(text); else Serial.println(text);
    }
    // Les résultats appartiennent au scanner ; les copier/afficher avant de libérer sa liste interne.
    scanner->clearResults();
}
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() { Lab::begin("06 | Observateur Bluetooth LE"); BLEDevice::init(""); scanner = BLEDevice::getScan(); scanner->setActiveScan(false); scan(); }
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() { M5Cardputer.update(); if (Lab::pressed('s')) scan(); delay(10); }
