/**
 * Serveur Web local — documentation française du laboratoire.
 * Servir une page et une API depuis le Cardputer.
 * Matériel : Cardputer et navigateur sur téléphone ou PC.
 * Compiler depuis la racine : pio run -e wifi-web.
 * Utilisation : Rejoindre Cardputer-Lab avec le mot de passe affiché, puis ouvrir son adresse HTTP.
 * Résultat à vérifier : La page et /api/status retournent durée de fonctionnement et tension batterie.
 * Lecture détaillée et raccordement : README.md et docs/experiences/wifi-bluetooth.md.
 */
#include <CardputerLab.h>
#include <WiFi.h>
#include <WebServer.h>
#include <lab_config.h>
// HTTP local sur le port 80. Le programme crée son propre point d’accès ; il ne configure pas de route
// vers Internet.
WebServer server(80);
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("05 | Tableau de bord local");
    if (!WiFi.softAP(LAB_AP_SSID, LAB_AP_PASSWORD)) { Lab::line("Erreur point d'acces"); return; }
    // La page est construite à chaque requête : batterie en millivolts et durée en secondes reflètent
    // l’instant de consultation.
    server.on("/", []() {
        String html = "<!doctype html><html lang='fr'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Cardputer Lab</title><style>body{font:20px system-ui;max-width:720px;margin:50px auto;padding:20px;background:#101c30;color:#e9f4ff}a{color:#6de0d0}</style><h1>Cardputer Lab</h1><p>Serveur local sur le Cardputer.</p><p>Batterie : ";
        html += String(M5Cardputer.Power.getBatteryVoltage()) + " mV</p><p>Depuis le demarrage : " + String(millis()/1000) + " s</p><a href='/'>Actualiser</a></html>";
        server.send(200, "text/html; charset=utf-8", html);
    });
    // Point d’entrée JSON pour un client local ; champs uptime_s et battery_mv, sans état persistant.
    server.on("/api/status", []() { server.send(200, "application/json", "{\"uptime_s\":" + String(millis()/1000) + ",\"battery_mv\":" + String(M5Cardputer.Power.getBatteryVoltage()) + "}"); });
    // Démarrer l’écoute après l’enregistrement des routes, puis afficher l’adresse attribuée au point
    // d’accès.
    server.begin(); Lab::line(LAB_AP_SSID); Lab::line("Mot de passe :"); Lab::line(LAB_AP_PASSWORD);
    Lab::line("http://" + WiFi.softAPIP().toString());
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() { M5Cardputer.update(); server.handleClient(); delay(2); }
