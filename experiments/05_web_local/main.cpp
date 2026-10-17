/**
 * Ancien serveur Web — brouillon historique, exclu des environnements actifs.
 * Utilise AP_SSID et AP_PASSWORD et une route /etat retournant uptime_ms et heap. Ces constantes
 * diffèrent de LAB_AP_* dans la configuration actuelle.
 * Référence à privilégier : experiments/05-wifi-web.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <WiFi.h>
#include <WebServer.h>
WebServer server(80);
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("05 Serveur web local");
    WiFi.mode(WIFI_AP);
    if (!WiFi.softAP(AP_SSID, AP_PASSWORD)) { Lab::screen("Erreur point d'acces"); return; }
    server.on("/", []() {
        server.send(200, "text/html; charset=utf-8", "<!doctype html><html lang='fr'><meta name='viewport' content='width=device-width'><title>Cardputer</title><h1>Laboratoire Cardputer</h1><p>Connexion locale reussie.</p><p><a href='/etat'>Afficher l'etat JSON</a></p></html>");
    });
    server.on("/etat", []() {
        server.send(200, "application/json", "{\"uptime_ms\":" + String(millis()) + ",\"heap\":" + String(ESP.getFreeHeap()) + "}");
    });
    server.onNotFound([]() { server.send(404, "text/plain", "Route inconnue"); });
    server.begin();
    Lab::screen(String("SSID: ") + AP_SSID + "\nCle: " + AP_PASSWORD + "\nhttp://" + WiFi.softAPIP().toString() + "\nPas de connexion Internet");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
// Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
// série, non validé sur la dalle.
void loop() { Lab::input(); server.handleClient(); delay(2); }
