/**
 * Ancien clavier USB — brouillon historique, exclu des environnements actifs.
 * t saisit Cardputer labo. La cible active envoie Bonjour depuis Cardputer avec Entrée et possède son
 * environnement USB dédié.
 * Référence à privilégier : experiments/18-usb-clavier.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <USB.h>
#include <USBHIDKeyboard.h>
USBHIDKeyboard keyboard;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("16 Clavier USB de demonstration");
    keyboard.begin(); USB.begin();
    Lab::screen("Ouvrir un editeur sur le PC\nt: taper Cardputer labo\nAucun envoi au demarrage\nDisposition PC: US pour ce test");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    if (Lab::input() == 't') { keyboard.print("Cardputer labo"); keyboard.releaseAll(); }
    delay(10);
}
