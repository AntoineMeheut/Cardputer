/**
 * Ancienne réception RF433 — brouillon historique, exclu des environnements actifs.
 * Attend des trames rc-switch sur GROVE_WHITE ; affiche valeur, longueur, protocole et impulsion.
 * Référence à privilégier : experiments/11-rf433-rx.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <RCSwitch.h>
RCSwitch receiver;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("11 RF433 reception ASK");
    receiver.enableReceive(digitalPinToInterrupt(GROVE_WHITE));
    Lab::screen("Attente d'une trame compatible\nRX : fil blanc / GPIO1");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    Lab::input();
    if (receiver.available()) {
        String text = "Valeur: " + String(receiver.getReceivedValue()) + "\nBits: " + receiver.getReceivedBitlength() +
            "\nProtocole: " + receiver.getReceivedProtocol() + "\nImpulsion us: " + receiver.getReceivedDelay();
        Serial.println(text); Lab::screen(text); receiver.resetAvailable();
    }
    delay(1);
}
