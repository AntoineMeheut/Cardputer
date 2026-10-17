/**
 * Journal GPS et export GPX — documentation française du laboratoire.
 * Enregistrer une trace CSV proprement fermée et la convertir en GPX.
 * Matériel : Cardputer, GPS v1.1, Grove et microSD FAT32.
 * Compiler depuis la racine : pio run -e gps-sd.
 * Utilisation : Attendre une position, marcher, presser q pour fermer, éteindre puis copier le CSV.
 * Résultat à vérifier : Un fichier /trace-N.csv sans écrasement ; conversion locale avec
 * tools/gps_csv_to_gpx.py.
 * Lecture détaillée et raccordement : README.md et docs/composants/gps-at6668.md.
 */
#include <CardputerLab.h>
#include <TinyGPS++.h>
TinyGPSPlus gps;
HardwareSerial gnss(1);
// Garder le fichier ouvert pendant la session et fermer sur q avant retrait de la carte.
File track;
String path;
unsigned points = 0;
bool logging = false;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("16 | Trace GPS sur microSD");
    gnss.setRxBufferSize(4096); gnss.begin(Lab::GPS_BAUD, SERIAL_8N1, Lab::GPS_RX, Lab::GPS_TX);
    if (!Lab::sdBegin()) { Lab::line("Erreur SD"); return; }
    // Un nouveau nom /trace-N.csv préserve les sessions précédentes ; une chaîne vide signale l’épuisement
    // des noms.
    path = Lab::nextFile("/trace-", ".csv");
    if (!path.length()) { Lab::line("Aucun nom libre"); return; }
    track = SD.open(path, FILE_WRITE);
    // Écrire une seule ligne d’en-tête conforme au convertisseur tools/gps_csv_to_gpx.py.
    if (!track || !track.println("utc,latitude,longitude,altitude_m,satellites")) { if (track) track.close(); Lab::line("Creation fichier impossible"); return; }
    logging = true; track.flush(); Lab::line(path); Lab::line("q : fermer avant retrait de la SD");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    while (gnss.available()) gps.encode(gnss.read());
    M5Cardputer.update();
    if (Lab::pressed('q') && logging) { track.close(); logging = false; Lab::body(); Lab::line("Fichier ferme. Eteindre avant retrait"); }
    static uint32_t last = 0, refresh = 0;
    // Enregistrer au plus une fois par seconde, seulement une position actualisée avec date et heure
    // récentes.
    if (logging && millis() - last >= 1000 && gps.location.isUpdated() && gps.location.isValid() && gps.location.age() < 2000
        && gps.date.isValid() && gps.date.age() < 2000 && gps.time.isValid() && gps.time.age() < 2000) {
        last = millis();
        char utc[30]; snprintf(utc, sizeof(utc), "%04d-%02d-%02dT%02d:%02d:%02dZ", gps.date.year(), gps.date.month(), gps.date.day(), gps.time.hour(), gps.time.minute(), gps.time.second());
        // Coordonnées décimales à six chiffres ; laisser l’altitude vide si elle est indisponible, sans
        // inventer zéro.
        String row = String(utc) + "," + String(gps.location.lat(), 6) + "," + String(gps.location.lng(), 6) + ",";
        if (gps.altitude.isValid() && gps.altitude.age() < 2000) row += String(gps.altitude.meters(), 1);
        row += ","; if (gps.satellites.isValid() && gps.satellites.age() < 2000) row += String(gps.satellites.value());
        // flush réduit les données restant en tampon ; à la première écriture incomplète, fermer et arrêter le
        // journal.
        bool ok = track.println(row) >= row.length(); track.flush();
        if (!ok) { track.close(); logging = false; Lab::body(); Lab::line("Erreur ecriture : journal ferme"); }
        else ++points;
    }
    if (logging && millis() - refresh >= 1000) {
        refresh = millis(); Lab::body(); Lab::line(path); Lab::line(String(points) + " points enregistres");
        Lab::line(gps.location.isValid() && gps.location.age() < 2000 ? "Position recente" : "Attente de position GNSS");
        Lab::line("q : fermer le journal");
    }
    delay(2);
}
