/**
 * Paquets NRF24 à deux stations — documentation française du laboratoire.
 * Échanger des paquets entre deux radios NRF24 additionnelles.
 * Matériel : Deux NRF24, deux contrôleurs, adaptateur microSD/SPI et alimentation 3,3 V.
 * Compiler depuis la racine : pio run -e nrf24.
 * Utilisation : Retirer SD, vérifier le câblage du guide, presser Entrée sur une seule station à la
 * fois.
 * Résultat à vérifier : Le pair affiche Salut N ; l’émetteur indique si l’accusé matériel a été reçu.
 * Lecture détaillée et raccordement : README.md et docs/experiences/nrf24.md.
 */
#include <CardputerLab.h>
#include <LabFormats.h>
#include <RF24.h>
// Matériel additionnel : adaptateur microSD vers SPI, régulateur 3,3 V,
// NRF24L01+ et seconde station. AUCUNE carte SD dans cette expérience.
// Les signaux SPI viennent du connecteur microSD ; CE/CSN du Grove.
RF24 radio(Lab::YELLOW, Lab::WHITE);
const uint8_t address[6] = "LAB01";
bool ready = false;
uint32_t sequence = 0;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("20 | NRF24 : liaison de test");
    // Maintenir CS de la SD inactif ; les broches SPI sont récupérées par un adaptateur et aucune microSD
    // ne doit être insérée.
    pinMode(Lab::SD_CS, OUTPUT); digitalWrite(Lab::SD_CS, HIGH);
    SPI.begin(Lab::SD_SCK, Lab::SD_MISO, Lab::SD_MOSI, Lab::SD_CS);
    ready = radio.begin(&SPI);
    if (!ready) { Lab::line("NRF24 absent / verifier SPI"); return; }
    // Canal 40 = 2440 MHz. Débit, canal, adresse et taille de charge doivent être identiques sur les deux
    // stations.
    radio.setChannel(40); radio.setDataRate(RF24_1MBPS); radio.setPALevel(RF24_PA_MIN);
    // Charge fixe de 16 octets ; le réglage des retransmissions concerne les accusés matériels NRF24.
    radio.setPayloadSize(16); radio.setRetries(5, 3);
    radio.openWritingPipe(address); radio.openReadingPipe(1, address); radio.startListening();
    Lab::line("2440 MHz | ENTREE : message"); Lab::line("2 stations, meme configuration");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update(); if (!ready) { delay(10); return; }
    if (Lab::enter()) {
        char payload[16] = {}; snprintf(payload, sizeof(payload), "Salut %lu", static_cast<unsigned long>(++sequence));
        // Passer brièvement de réception à émission, puis rétablir immédiatement l’écoute du pair.
        radio.stopListening(); bool delivered = radio.write(payload, sizeof(payload)); radio.startListening();
        Lab::body(); Lab::line(delivered ? "Accuse NRF24 recu" : "Pas de reponse du pair");
    }
    if (radio.available()) {
        // Réserver un octet nul supplémentaire pour afficher sans dépasser les 16 octets reçus.
        char payload[17] = {}; radio.read(payload, 16);
        Lab::body(); Lab::line("Message :"); Lab::line(payload);
    }
    delay(5);
}
