/**
 * Radio FM avec module additionnel — documentation française du laboratoire.
 * Accorder un tuner FM additionnel et écouter sa sortie audio.
 * Matériel : RDA5807, adaptation 3,3 V, antenne et audio externe ; absents de la liste initiale.
 * Compiler depuis la racine : pio run -e fm-rda5807.
 * Utilisation : Vérifier le montage documenté ; + / - règlent la fréquence par pas de 0,1 MHz.
 * Résultat à vérifier : La station est entendue sur la sortie audio du module FM, pas sur le haut-
 * parleur interne.
 * Lecture détaillée et raccordement : README.md et docs/experiences/fm.md.
 */
#include <CardputerLab.h>
#include <RDA5807.h>
RDA5807 radio;
// Fréquence en centièmes de MHz : 9950 signifie 99,50 MHz ; un pas de 10 correspond à 100 kHz.
uint16_t frequency = 9950;
bool ready = false;
void draw() { Lab::body(); Lab::line("FM : " + String(frequency / 100.0, 1) + " MHz"); Lab::line("+ / - : pas de 0,1 MHz"); Lab::line("Audio sur sortie du module FM"); }
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("19 | FM : module additionnel"); Lab::i2cBegin();
    // Chercher les adresses de commande du RDA5807 ; cette détection ne valide pas l’antenne ni la sortie
    // audio.
    ready = Lab::i2cPresent(0x10) || Lab::i2cPresent(0x11);
    if (!ready) { Lab::line("RDA5807 absent (non fourni)"); return; }
    radio.setup(); radio.setVolume(3); radio.setFrequency(frequency); draw();
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update(); if (!ready) { delay(20); return; }
    // La plage est bornée à 87,5–108 MHz, sans rebouclage automatique aux extrémités.
    bool changed = false;
    if (Lab::pressed('+') && frequency < 10800) { frequency += 10; changed = true; }
    if (Lab::pressed('-') && frequency > 8750) { frequency -= 10; changed = true; }
    // Éviter une écriture I²C et un redessin tant que la fréquence n’a pas changé.
    if (changed) { radio.setFrequency(frequency); draw(); }
    delay(10);
}
