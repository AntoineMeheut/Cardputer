/**
 * Ancienne émission RF433 — brouillon historique, exclu des environnements actifs.
 * t envoie selon RF_PROTOCOL, RF_PULSE_US, RF_REPEATS et RF_BITS, avec intervalle de deux secondes. La
 * cible active fixe trois répétitions et cinq secondes.
 * Référence à privilégier : experiments/12-rf433-tx.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <RCSwitch.h>
RCSwitch sender;
uint32_t last = 0;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("12 RF433 emission ASK");
    sender.enableTransmit(GROVE_YELLOW);
    sender.setProtocol(RF_PROTOCOL); sender.setPulseLength(RF_PULSE_US); sender.setRepeatTransmit(RF_REPEATS);
    Lab::screen("t: trame de laboratoire\nValeur: " + String(RF_TEST_CODE) + "\nTX : jaune / GPIO2\nIntervalle minimal 2 secondes");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    if (Lab::input() == 't' && millis() - last >= 2000) {
        last = millis(); sender.send(RF_TEST_CODE, RF_BITS);
        Lab::screen("Trame envoyee: " + String(RF_TEST_CODE) + "\nt: nouvel envoi");
    }
    delay(5);
}
