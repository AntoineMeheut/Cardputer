/**
 * Compteur ESP-NOW — brouillon historique, exclu des environnements actifs.
 * t envoie huit octets : signature CPLB puis compteur. Le format actif est différent et ajoute une
 * chaîne de caractères.
 * Référence à privilégier : experiments/17-espnow.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
uint8_t broadcast[] = {255,255,255,255,255,255};
portMUX_TYPE mutex = portMUX_INITIALIZER_UNLOCKED;
uint32_t received = 0, sent = 0;
bool changed = false, ready = false;
// Callback radio : les données partagées sont protégées par section critique et l’écran est actualisé
// dans loop.
void onReceive(const uint8_t *, const uint8_t *data, int len) {
    if (len != 8 || memcmp(data, "CPLB", 4)) return;
    uint32_t n;
    memcpy(&n, data + 4, 4);
    portENTER_CRITICAL(&mutex); received = n; changed = true; portEXIT_CRITICAL(&mutex);
}
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("08 ESP-NOW, canal 1");
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
    if (esp_now_init() != ESP_OK) { Lab::screen("Erreur ESP-NOW"); return; }
    esp_now_register_recv_cb(onReceive);
    esp_now_peer_info_t peer = {};
    memcpy(peer.peer_addr, broadcast, 6); peer.channel = 1; peer.encrypt = false;
    ready = esp_now_add_peer(&peer) == ESP_OK;
    Lab::screen(ready ? "t: envoyer compteur\nSecond Cardputer requis\nDiffusion locale non chiffree" : "Erreur ajout pair");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    if (Lab::input() == 't' && ready) {
        uint8_t data[8] = {'C','P','L','B'}; ++sent; memcpy(data+4, &sent, 4);
        Lab::screen(esp_now_send(broadcast, data, sizeof(data)) == ESP_OK ? "Envoi demande: " + String(sent) : "Erreur envoi");
    }
    portENTER_CRITICAL(&mutex); bool show = changed; uint32_t n = received; changed = false; portEXIT_CRITICAL(&mutex);
    if (show) Lab::screen("Compteur recu: " + String(n) + "\nt: envoyer");
    delay(5);
}
