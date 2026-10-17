/**
 * Envoyer une trame RF de laboratoire — documentation française du laboratoire.
 * Envoyer une trame synthétique contrôlée vers son récepteur.
 * Matériel : Cardputer, RF433T et une station réceptrice séparée.
 * Compiler depuis la racine : pio run -e rf433-tx.
 * Utilisation : Attendre cinq secondes, presser Entrée et vérifier la réception sur la seconde
 * station.
 * Résultat à vérifier : Trois répétitions de la trame synthétique 0x5A1234 ; aucune émission
 * automatique.
 * Lecture détaillée et raccordement : README.md et docs/composants/rf433-emetteur.md.
 */
#include <CardputerLab.h>
#include <RCSwitch.h>
#include <lab_config.h>
RCSwitch radio;
uint32_t lastSend = 0;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("12 | Emission RF433 de test");
    // Protocole 1, impulsion de base 350 microsecondes, trois répétitions par demande.
    radio.enableTransmit(Lab::YELLOW); radio.setProtocol(1); radio.setPulseLength(350); radio.setRepeatTransmit(3);
    Lab::line("TX sur G2 / jaune"); Lab::line("Trame synthetique : 0x" + String(LAB_RF_CODE, HEX));
    Lab::line("ENTREE : 3 repetitions"); Lab::line("Intervalle minimal : 5 secondes");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // Attendre cinq secondes entre demandes, y compris après le démarrage ; aucune émission périodique
    // autonome.
    if (Lab::enter() && millis() - lastSend >= 5000) {
        // Le code tient sur 24 bits. Le récepteur séparé est nécessaire pour confirmer la réception.
        radio.send(LAB_RF_CODE, 24); lastSend = millis();
        Lab::body(); Lab::line("Trame de laboratoire envoyee"); Lab::line("Attendre 5 s puis ENTREE");
    }
}
