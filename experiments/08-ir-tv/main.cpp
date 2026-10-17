/**
 * Télécommande TV infrarouge — documentation française du laboratoire.
 * Émettre volontairement une commande NEC vers son téléviseur.
 * Matériel : Cardputer, votre TV et un code NEC compatible connu.
 * Compiler depuis la racine : pio run -e ir-tv.
 * Utilisation : Renseigner LAB_NEC_CODE, viser votre TV puis presser Entrée.
 * Résultat à vérifier : Une trame NEC est émise ; la réaction de la TV valide le code, pas le seul
 * texte à l’écran.
 * Lecture détaillée et raccordement : README.md et docs/experiences/television-ir.md.
 */
#include <CardputerLab.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <lab_config.h>
// La LED IR du K132 est raccordée à GPIO 44 via la constante commune IR_TX.
IRsend infrared(Lab::IR_TX);
uint32_t lastSend = 0;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("08 | Telecommande IR NEC"); infrared.begin();
    Lab::line("Configurer LAB_NEC_CODE d'abord");
    Lab::line("Viser votre TV puis ENTREE");
    Lab::line("Code : 0x" + String(LAB_NEC_CODE, HEX));
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // L’émission dépend d’un événement Entrée et d’un délai minimal ; le premier envoi est possible après
    // une seconde.
    if (Lab::enter() && millis() - lastSend >= 1000) {
        // Émettre exactement 32 bits du code configuré. Le texte de succès n’atteste pas une réaction du
        // téléviseur.
        infrared.sendNEC(LAB_NEC_CODE, 32); lastSend = millis();
        Lab::body(); Lab::line("Une trame NEC envoyee"); Lab::line("ENTREE : envoyer a nouveau");
    }
}
