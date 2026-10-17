/**
 * Pont radio sur ESP32 externe — brouillon historique, exclu des environnements actifs.
 * Cible explicitement un ESP32 DevKit, pas le Cardputer. SPI 18/19/23, CE 4, CSN 5, UART 16/17, canal
 * 76 et NRF_ROLE 0/1. Deux rôles complémentaires sont nécessaires.
 * Référence à privilégier : experiments/20-nrf24 (autre architecture).
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
// Cible : ESP32 DevKit externe, PAS le Cardputer. Voir le guide NRF24.
#include <Arduino.h>
#include <SPI.h>
#include <RF24.h>
#include <lab_logic.h>
#ifndef NRF_ROLE
#define NRF_ROLE 0
#endif
RF24 radio(4, 5);
const uint8_t addresses[][6] = {"CPL01", "CPL02"};
HardwareSerial terminal(2);
lab::LineBuffer<31> fromUSB, fromCard;
bool ready = false;
void report(const String &line) { Serial.println(line); terminal.println(line); }
void sendLine(const char *text) {
    if (!ready) { report("NRF24 absent"); return; }
    char packet[32] = {}; strlcpy(packet, text, sizeof(packet));
    radio.stopListening(); bool ok = radio.write(packet, sizeof(packet)); radio.startListening();
    report(ok ? "TX acquitte" : "TX sans acquittement");
}
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Serial.begin(115200); terminal.begin(115200, SERIAL_8N1, 16, 17);
    SPI.begin(18, 19, 23, 5);
    ready = radio.begin();
    if (!ready) { report("NRF24 absent : verifier cablage"); return; }
    radio.setPALevel(RF24_PA_MIN); radio.setDataRate(RF24_1MBPS); radio.setChannel(76);
    radio.setPayloadSize(32); radio.setRetries(5, 5);
    radio.openWritingPipe(addresses[NRF_ROLE]); radio.openReadingPipe(1, addresses[1-NRF_ROLE]);
    radio.startListening(); report("Pont NRF24 pret");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    while(Serial.available()) if(fromUSB.push(Serial.read())) { sendLine(fromUSB.value()); fromUSB.clear(); }
    while(terminal.available()) if(fromCard.push(terminal.read())) { sendLine(fromCard.value()); fromCard.clear(); }
    if(ready && radio.available()) { char packet[33] = {}; radio.read(packet, 32); report("RX: " + String(packet)); }
    delay(1);
}
