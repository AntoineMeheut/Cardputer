/**
 * Mesurer et compter les approches — documentation française du laboratoire.
 * Comparer la lumière réfléchie et compter des approches lentes.
 * Matériel : Cardputer, Grove et U175.
 * Compiler depuis la racine : pio run -e ir-reflectif.
 * Utilisation : Approcher une feuille blanche puis noire ; observer AO/DO et presser r pour remettre
 * le compteur à zéro.
 * Résultat à vérifier : La mesure change avec la réflexion ; le compteur détecte les approches lentes.
 * Lecture détaillée et raccordement : README.md et docs/composants/ir-reflectif.md.
 */
#include <CardputerLab.h>
uint32_t events = 0, lastTransition = 0;
bool previous = false;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("10 | Capteur IR reflectif"); pinMode(Lab::YELLOW, INPUT);
    // AO est lu sur 12 bits (0 à 4095) ; ce nombre est une intensité réfléchie, pas une distance calibrée.
    analogReadResolution(12); analogSetPinAttenuation(Lab::WHITE, ADC_11db);
    // Mémoriser l’état initial évite de compter un objet déjà présent au démarrage.
    previous = digitalRead(Lab::YELLOW) == LOW;
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    bool detected = digitalRead(Lab::YELLOW) == LOW;
    // Comptage des fronts d'approche, filtrés à 100 ms (pas un tachymètre rapide).
    // L’entrée DO est active à LOW ; seul le front d’approche incrémente le compteur, après filtrage
    // temporel.
    if (detected != previous && millis() - lastTransition >= 100) {
        previous = detected; lastTransition = millis(); if (detected) ++events;
    }
    if (Lab::pressed('r')) events = 0;
    // La cadence d’affichage de 200 ms est indépendante du comptage effectué dans la boucle.
    static uint32_t refresh = 0;
    if (millis() - refresh >= 200) {
        refresh = millis(); Lab::body();
        Lab::line("DO G2 : " + String(digitalRead(Lab::YELLOW)));
        Lab::line("AO G1 : " + String(analogRead(Lab::WHITE)) + " / 4095");
        Lab::line("Approches : " + String(events));
        Lab::line("r : remettre le compteur a zero");
        Lab::line("Intensite reflechie, pas des cm");
    }
    delay(5);
}
