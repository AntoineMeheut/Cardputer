/**
 * Recevoir une trame ASK/OOK — documentation française du laboratoire.
 * Décoder une trame ASK/OOK compatible avec rc-switch.
 * Matériel : Cardputer, RF433R et émetteur de test compatible.
 * Compiler depuis la racine : pio run -e rf433-rx.
 * Utilisation : Déclencher la source de test ; comparer code, bits, protocole et durée.
 * Résultat à vérifier : Une trame compatible s’affiche ; l’absence de décodage ne prouve pas l’absence
 * de signal.
 * Lecture détaillée et raccordement : README.md et docs/composants/rf433-recepteur.md.
 */
#include <CardputerLab.h>
#include <RCSwitch.h>
RCSwitch radio;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("11 | Reception RF433 ASK/OOK");
    // La bibliothèque mesure les impulsions sur interruption GPIO 1 ; le module fournit le signal RF
    // démodulé.
    radio.enableReceive(digitalPinToInterrupt(Lab::WHITE));
    Lab::line("RX sur G1 / blanc"); Lab::line("Attente d'une trame compatible");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // Traiter uniquement une trame que rc-switch a reconnue ; les protocoles inconnus peuvent rester
    // invisibles.
    if (radio.available()) {
        Lab::body(); Lab::line("Code : " + String(radio.getReceivedValue()));
        Lab::line("Hex : 0x" + String(radio.getReceivedValue(), HEX));
        Lab::line("Bits : " + String(radio.getReceivedBitlength()));
        Lab::line("Protocole : " + String(radio.getReceivedProtocol()));
        Lab::line("Impulsion : " + String(radio.getReceivedDelay()) + " us");
        // Consommer le résultat pour ne pas réafficher continuellement la même trame.
        radio.resetAvailable();
    }
    delay(5);
}
