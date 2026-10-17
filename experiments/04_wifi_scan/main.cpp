/**
 * Ancien scan Wi-Fi — brouillon historique, exclu des environnements actifs.
 * Appel WiFi.scanNetworks(false, true), synchrone et sans option passive explicite ; s relance.
 * Référence à privilégier : experiments/04-wifi-scan.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <WiFi.h>
// Le scan est lancé à la demande et conserve seulement ce que cette variante affiche ou écrit sur le
// port série.
void scan() {
    Lab::screen("Recherche des reseaux...");
    const int n = WiFi.scanNetworks(false, true);
    String text = "Reseaux: " + String(n) + "\n";
    if (n < 0) text = "Erreur scan Wi-Fi\n";
    for (int i = 0; i < n; ++i) {
        String line = WiFi.SSID(i).substring(0, 16) + " " + WiFi.RSSI(i) + "dBm ch" + WiFi.channel(i);
        Serial.println(line);
        if (i < 8) text += line + "\n";
    }
    WiFi.scanDelete();
    Lab::screen(text + "s: relancer / ! capture");
}
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() { Lab::begin("04 Observation Wi-Fi 2.4GHz"); WiFi.mode(WIFI_STA); WiFi.disconnect(); scan(); }
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
// Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
// série, non validé sur la dalle.
void loop() { if (Lab::input() == 's') scan(); delay(10); }
