/**
 * Observer les réseaux Wi-Fi — documentation française du laboratoire.
 * Observer les annonces des points d’accès Wi-Fi 2,4 GHz.
 * Matériel : Cardputer ; point d’accès 2,4 GHz pour vérifier.
 * Compiler depuis la racine : pio run -e wifi-scan.
 * Utilisation : Attendre le scan passif ; n change de page, s relance.
 * Résultat à vérifier : SSID, canal et RSSI sont visibles ; les réseaux 5 GHz seuls sont absents.
 * Lecture détaillée et raccordement : README.md et docs/experiences/wifi-bluetooth.md.
 */
#include <CardputerLab.h>
#include <WiFi.h>
bool scanning = false;
// page est un index à partir de zéro ; quatre réseaux sont affichés par page.
int count = 0, page = 0;
void draw() {
    Lab::body(); Lab::line(String(count) + " reseaux | n : suite | s : scan");
    for (int i = page * 4; i < count && i < page * 4 + 4; ++i) {
        Lab::line(WiFi.SSID(i).substring(0, 23));
        Lab::line(" ch " + String(WiFi.channel(i)) + "  " + String(WiFi.RSSI(i)) + " dBm");
    }
}
void scan() {
    // Libérer les résultats du scan précédent avant de lancer une nouvelle collecte.
    WiFi.scanDelete(); count = 0; page = 0;
    Lab::body(); Lab::line("Ecoute passive des balises...");
    // async, SSID cachés, balayage passif : aucun probe request.
    int result = WiFi.scanNetworks(true, true, true, 300);
    // Un échec ou une liste vide produit zéro résultat ; le code ne transforme pas une erreur négative en
    // nombre de réseaux.
    scanning = result == WIFI_SCAN_RUNNING;
    if (!scanning) { count = result > 0 ? result : 0; draw(); }
}
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() { Lab::begin("04 | Reseaux Wi-Fi 2,4 GHz"); WiFi.mode(WIFI_STA); WiFi.disconnect(); scan(); }
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    if (scanning) {
        // Interroger la fin du scan sans bloquer la lecture du clavier pendant tout le balayage.
        int result = WiFi.scanComplete();
        if (result != WIFI_SCAN_RUNNING) { scanning = false; count = result > 0 ? result : 0; draw(); }
    } else if (Lab::pressed('s')) scan();
    else if (Lab::pressed('n') && count > 0) { page = (page + 1) % ((count + 3) / 4); draw(); }
    delay(10);
}
