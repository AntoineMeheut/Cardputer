/**
 * FM avec bouclage de bande — brouillon historique, exclu des environnements actifs.
 * +/- parcourent la bande avec retour à l’autre extrémité ; volume 4 et détection seulement à 0x10. La
 * version active s’arrête aux bornes.
 * Référence à privilégier : experiments/19-fm-rda5807.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <Wire.h>
#include <RDA5807.h>
RDA5807 radio;
bool ready = false;
void draw() { Lab::screen("Frequence: " + String(radio.getFrequency()/100.0, 2) + " MHz\n+/- pas de 100kHz\nAudio sur sortie du module\nEcouteurs + antenne requis"); }
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("17 Recepteur FM RDA5807 (option)");
    Wire.begin(GROVE_YELLOW, GROVE_WHITE, 100000);
    Wire.beginTransmission(0x10);
    ready = Wire.endTransmission() == 0;
    if (!ready) { Lab::screen("RDA5807 absent a 0x10\nVerifier alimentation 3.3V"); return; }
    radio.setup(); radio.setVolume(4); radio.setFrequency(9950); draw();
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (ready && (c == '+' || c == '-')) {
        uint16_t f = radio.getFrequency();
        f = c == '+' ? (f >= 10800 ? 8750 : f+10) : (f <= 8750 ? 10800 : f-10);
        radio.setFrequency(f); draw();
    }
    delay(10);
}
