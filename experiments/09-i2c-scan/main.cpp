/**
 * Détecter le RFID2 sur I²C — documentation française du laboratoire.
 * Confirmer la présence du lecteur RFID2 avant toute lecture de carte.
 * Matériel : Cardputer, Grove et RFID2.
 * Compiler depuis la racine : pio run -e i2c-scan.
 * Utilisation : Brancher hors tension, lancer le programme ; s refait le scan.
 * Résultat à vérifier : Le RFID2 doit répondre à 0x28 sur SDA G2 / SCL G1.
 * Lecture détaillée et raccordement : README.md et docs/composants/rfid2.md.
 */
#include <CardputerLab.h>
void scan() {
    Lab::body(); Lab::line("SDA=G2 / SCL=G1 | s : relancer");
    unsigned found = 0;
    // Parcourir les adresses 7 bits usuelles 0x08 à 0x77, en évitant les plages réservées.
    for (uint8_t address = 8; address < 120; ++address) {
        // Un acquittement indique une présence sur le bus, sans identifier le modèle ni lire ses registres.
        if (Lab::i2cPresent(address)) { ++found; Lab::line("Adresse : 0x" + String(address, HEX)); }
    }
    Lab::line(String(found) + " reponse(s), RFID2 = 0x28");
}
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() { Lab::begin("09 | Scanner I2C Grove"); Lab::i2cBegin(); scan(); }
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() { M5Cardputer.update(); if (Lab::pressed('s')) scan(); delay(10); }
