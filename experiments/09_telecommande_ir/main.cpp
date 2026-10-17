/**
 * Émission IR conditionnelle — brouillon historique, exclu des environnements actifs.
 * t émet uniquement si IR_ENABLED est vrai ; attend TV_NEC_CODE et IR_LED. Ces symboles ne sont pas
 * fournis par la configuration active.
 * Référence à privilégier : experiments/08-ir-tv.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
IRsend sender(IR_LED);
uint32_t last = 0;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("09 Television : emission NEC");
    sender.begin();
    Lab::screen(IR_ENABLED ? "t: envoyer le code configure\nViser le recepteur du televiseur" : "Configurer TV_NEC_CODE puis\nIR_ENABLED dans lab_config.h\nRecompiler avant emission");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    if (Lab::input() == 't' && IR_ENABLED && millis()-last >= 1000) {
        last = millis(); sender.sendNEC(TV_NEC_CODE, 32);
        Lab::screen("Code NEC envoye: 0x" + String(TV_NEC_CODE, HEX) + "\nt: renvoyer");
    }
    delay(5);
}
