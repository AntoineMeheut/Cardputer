/**
 * Phrase au clavier USB — documentation française du laboratoire.
 * Saisir volontairement une phrase fixe dans un éditeur.
 * Matériel : Cardputer, câble USB de données et éditeur de texte.
 * Compiler depuis la racine : pio run -e usb-clavier.
 * Utilisation : Ouvrir un éditeur vide sur son poste ; presser Entrée sur le Cardputer.
 * Résultat à vérifier : Une phrase fixe est saisie une fois par pression ; disposition US de la
 * bibliothèque HID.
 * Lecture détaillée et raccordement : README.md et docs/composants/cardputer.md.
 */
#include <CardputerLab.h>
#include <USB.h>
#include <USBHIDKeyboard.h>
// Utiliser l’environnement usb-clavier : son mode USB diffère des autres expériences dans
// platformio.ini.
USBHIDKeyboard keyboard;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("18 | Clavier USB volontaire"); keyboard.begin(); USB.begin();
    Lab::line("Ouvrir un editeur texte sur le PC"); Lab::line("ENTREE : saisir Bonjour une fois");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // La phrase est envoyée une fois par changement d’état Entrée ; releaseAll évite de laisser une touche
    // HID maintenue.
    if (Lab::enter()) { keyboard.print("Bonjour depuis Cardputer"); keyboard.releaseAll(); }
    delay(5);
}
