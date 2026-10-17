/**
 * Afficher position et heure UTC — documentation française du laboratoire.
 * Distinguer réception NMEA, acquisition et position récente.
 * Matériel : Cardputer, Grove et GPS/BDS v1.1.
 * Compiler depuis la racine : pio run -e gps.
 * Utilisation : Sortir, orienter l’antenne vers le ciel, vérifier les octets NMEA et attendre une
 * position récente.
 * Résultat à vérifier : Latitude, longitude, satellites, altitude/vitesse disponibles et heure UTC.
 * Lecture détaillée et raccordement : README.md et docs/composants/gps-at6668.md.
 */
#include <CardputerLab.h>
#include <TinyGPS++.h>
TinyGPSPlus gps;
// UART matériel 1 : RX côté Cardputer sur G1, TX sur G2, indépendamment de la console USB.
HardwareSerial gnss(1);
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("15 | GPS / BDS AT6668"); gnss.setRxBufferSize(2048);
    gnss.begin(Lab::GPS_BAUD, SERIAL_8N1, Lab::GPS_RX, Lab::GPS_TX);
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    // Vider fréquemment l’UART et fournir chaque octet au parseur NMEA, même lorsque l’écran n’est pas
    // rafraîchi.
    while (gnss.available()) gps.encode(gnss.read());
    M5Cardputer.update();
    static uint32_t refresh = 0;
    if (millis() - refresh < 1000) return;
    refresh = millis(); Lab::body();
    Lab::line("NMEA recus : " + String(gps.charsProcessed()));
    Lab::line("Satellites : " + String(gps.satellites.isValid() ? gps.satellites.value() : 0));
    // Une valeur valide mais trop ancienne est refusée : ici, la fraîcheur maximale est de trois secondes.
    if (gps.location.isValid() && gps.location.age() < 3000) {
        Lab::line("Lat : " + String(gps.location.lat(), 6));
        Lab::line("Lon : " + String(gps.location.lng(), 6));
        if (gps.altitude.isValid() && gps.altitude.age() < 3000) Lab::line("Altitude : " + String(gps.altitude.meters(), 1) + " m");
        if (gps.speed.isValid() && gps.speed.age() < 3000) Lab::line("Vitesse : " + String(gps.speed.kmph(), 1) + " km/h");
    } else Lab::line("Pas de position recente : sortir");
    // L’heure affichée est UTC ; aucune conversion en heure locale ni en heure d’été n’est appliquée.
    if (gps.time.isValid() && gps.time.age() < 3000) {
        char time[32]; snprintf(time, sizeof(time), "UTC %02d:%02d:%02d", gps.time.hour(), gps.time.minute(), gps.time.second()); Lab::line(time);
    }
    if (gps.charsProcessed() == 0 && millis() > 5000) Lab::line("Verifier RX=G1 / debit=115200");
}
