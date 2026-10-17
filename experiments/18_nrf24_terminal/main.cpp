/**
 * Terminal UART pour pont NRF24 — brouillon historique, exclu des environnements actifs.
 * Envoie une ligne de 30 caractères maximum via UART 115200. Le Cardputer n’y pilote pas directement
 * le NRF24 : un ESP32 externe sert de pont.
 * Référence à privilégier : experiments/20-nrf24 (autre architecture).
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <lab_logic.h>
HardwareSerial bridge(1);
lab::LineBuffer<128> incoming;
String text;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("18 NRF24 via pont ESP32 (option)");
    bridge.begin(115200, SERIAL_8N1, GROVE_WHITE, GROVE_YELLOW);
    Lab::screen("Saisir max. 30 caracteres\nEntree: envoyer au pont UART\nNRF24 externe et pont requis");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (c == '\n') { bridge.println(text); text = ""; }
    else if (c == '\b') { if(text.length()) text.remove(text.length()-1); Lab::screen(text); }
    else if (c && text.length()<30) { text += c; Lab::screen(text); }
    while (bridge.available()) if (incoming.push(bridge.read())) {
        Lab::screen(String(incoming.value())); Serial.println(incoming.value()); incoming.clear();
    }
    delay(1);
}
