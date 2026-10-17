/**
 * GPS avec journal optionnel — brouillon historique, exclu des environnements actifs.
 * l active le journal trace.csv, n copie les octets NMEA sur USB ; le CSV ajoute hdop. L’en-tête
 * TinyGPSPlus.h diffère de TinyGPS++.h utilisé par l’archive locale.
 * Référence à privilégier : experiments/15-gps / 16-gps-sd.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <TinyGPSPlus.h>
TinyGPSPlus gps;
HardwareSerial gnss(1);
bool sdReady = false, logging = false;
uint32_t lastScreen = 0, lastLog = 0;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("15 GPS AT6668 + trace CSV");
    gnss.setRxBufferSize(4096);
    gnss.begin(GPS_BAUD, SERIAL_8N1, GROVE_WHITE, GROVE_YELLOW);
    sdReady = Lab::sdBegin();
    if (sdReady && !SD.exists("/trace.csv")) sdReady = Lab::append("/trace.csv", "utc,latitude,longitude,altitude_m,satellites,hdop\n");
    Lab::screen("Attente NMEA a 115200 bauds\nl: activer journal SD\nn: NMEA brut via USB");
}
bool raw = false;
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (c == 'l' && sdReady) logging = !logging;
    if (c == 'n') raw = !raw;
    while (gnss.available()) { char b = gnss.read(); if (raw) Serial.write(b); gps.encode(b); }
    const bool fresh = gps.location.isValid() && gps.location.age() < 2000;
    if (millis() - lastScreen >= 500) {
        lastScreen = millis();
        String text = "Octets: " + String(gps.charsProcessed()) + " Sat: " + gps.satellites.value() + "\n";
        text += fresh ? "Lat: " + String(gps.location.lat(), 6) + "\nLon: " + String(gps.location.lng(), 6) : "Position indisponible / ancienne";
        text += "\nSD: " + String(sdReady ? "OK" : "absente/erreur") + " Journal: " + (logging ? "ON" : "OFF") + "\nl: journal / n: NMEA USB";
        Lab::screen(text);
    }
    if (logging && fresh && gps.date.isValid() && gps.time.isValid() && gps.date.age()<2000 && gps.time.age()<2000 && millis()-lastLog>=1000) {
        lastLog = millis();
        char stamp[32];
        snprintf(stamp, sizeof(stamp), "%04d-%02d-%02dT%02d:%02d:%02dZ", gps.date.year(), gps.date.month(), gps.date.day(), gps.time.hour(), gps.time.minute(), gps.time.second());
        String row = String(stamp) + "," + String(gps.location.lat(), 7) + "," + String(gps.location.lng(), 7) + ",";
        if (gps.altitude.isValid() && gps.altitude.age()<2000) row += String(gps.altitude.meters(), 2);
        row += "," + String(gps.satellites.value()) + "," + String(gps.hdop.hdop(), 2) + "\n";
        if (!Lab::append("/trace.csv", row)) { logging = false; sdReady = false; }
    }
    delay(1);
}
