/**
 * Messages entre deux Cardputer — documentation française du laboratoire.
 * Échanger un message entre deux Cardputer sur le même canal.
 * Matériel : Deux Cardputer ; adaptation possible sur un second ESP32.
 * Compiler depuis la racine : pio run -e espnow.
 * Utilisation : Téléverser le même programme sur les deux ; presser Entrée alternativement.
 * Résultat à vérifier : Le pair reçoit Bonjour ; le retour d’envoi seul ne garantit pas la réception
 * applicative.
 * Lecture détaillée et raccordement : README.md et docs/experiences/wifi-bluetooth.md.
 */
#include <CardputerLab.h>
#include <LabFormats.h>
#include <lab_config.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>
// La tâche radio et loop ne dessinent pas simultanément : elles échangent des copies de paquets via
// une file FreeRTOS.
QueueHandle_t received;
uint8_t broadcast[6] = {255,255,255,255,255,255};
uint32_t sequence = 0;
bool ready = false;
// Callback exécuté dans le contexte Wi-Fi : valider taille, signature et terminaison du texte, puis
// déposer sans attendre.
void onReceive(const uint8_t*, const uint8_t* data, int length) {
    Lab::Packet packet;
    // xQueueSend avec attente nulle peut abandonner un paquet si les quatre places sont occupées ; aucun
    // écran dans ce callback.
    if (length > 0 && Lab::decodePacket(data, static_cast<size_t>(length), packet)) xQueueSend(received, &packet, 0);
}
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("17 | Messages ESP-NOW"); WiFi.mode(WIFI_STA); WiFi.disconnect();
    esp_wifi_set_channel(LAB_ESPNOW_CHANNEL, WIFI_SECOND_CHAN_NONE);
    // La file contient quatre paquets complets ; tester son allocation avant d’enregistrer le callback.
    received = xQueueCreate(4, sizeof(Lab::Packet));
    if (!received || esp_now_init() != ESP_OK) { Lab::line("Erreur initialisation"); return; }
    esp_now_register_recv_cb(onReceive);
    // Adresse broadcast, canal commun et absence de chiffrement : les deux cartes doivent employer la même
    // configuration.
    esp_now_peer_info_t peer = {}; memcpy(peer.peer_addr, broadcast, 6); peer.channel = LAB_ESPNOW_CHANNEL; peer.encrypt = false;
    ready = esp_now_add_peer(&peer) == ESP_OK;
    Lab::line(ready ? "ENTREE : envoyer Bonjour" : "Erreur ajout pair");
    Lab::line("Deux cartes sur le canal " + String(LAB_ESPNOW_CHANNEL)); Lab::line("Demonstration non chiffree");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update(); if (!ready) { delay(10); return; }
    if (Lab::enter()) {
        Lab::Packet packet = {}; packet.magic = Lab::PACKET_MAGIC; packet.sequence = ++sequence; strcpy(packet.text, "Bonjour du Cardputer");
        // ESP_OK signifie que le pilote accepte l’envoi, pas que le pair a reçu ni traité le message.
        esp_err_t status = esp_now_send(broadcast, reinterpret_cast<uint8_t*>(&packet), sizeof(packet));
        Lab::body(); Lab::line(status == ESP_OK ? "Trame confiee au pilote" : "Erreur envoi"); Lab::line("Pas d'accuse applicatif en broadcast");
    }
    Lab::Packet packet;
    // Lire une copie validée dans le contexte principal avant d’accéder à l’affichage.
    if (xQueueReceive(received, &packet, 0) == pdTRUE) { Lab::body(); Lab::line("Recu #" + String(packet.sequence)); Lab::line(packet.text); }
    delay(5);
}
