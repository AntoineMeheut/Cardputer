/**
 * Audio à 8 kHz et niveau RMS — brouillon historique, exclu des environnements actifs.
 * r enregistre 8000 échantillons, p écoute et t produit une tonalité. Aucun WAV sur SD dans ce
 * brouillon.
 * Référence à privilégier : experiments/03-micro-wav.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <math.h>
int16_t samples[8000];
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("02 Audio : micro + HP");
    M5Cardputer.Speaker.setVolume(80);
    Lab::screen("r: enregistrer 1 seconde\np: ecouter\nt: tonalite\n! capture");
}
bool recorded = false;
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (c == 'r') {
        M5Cardputer.Speaker.end();
        M5Cardputer.Mic.begin();
        Lab::screen("Enregistrement 1 seconde...");
        const bool started = M5Cardputer.Mic.record(samples, 8000, 8000);
        while (M5Cardputer.Mic.isRecording()) delay(1);
        M5Cardputer.Mic.end();
        recorded = started;
        double sum = 0;
        if (started) for (auto s : samples) sum += double(s) * s;
        Lab::screen(started ? "RMS: " + String(sqrt(sum / 8000), 1) + "\np: ecouter / r: recommencer"
                            : "Erreur micro. Redemarrer.");
    }
    if (c == 't' || (c == 'p' && recorded)) {
        M5Cardputer.Mic.end();
        M5Cardputer.Speaker.begin();
        if (c == 't') M5Cardputer.Speaker.tone(880, 200);
        else M5Cardputer.Speaker.playRaw(samples, 8000, 8000);
        while (M5Cardputer.Speaker.isPlaying()) delay(1);
        M5Cardputer.Speaker.end();
    }
    delay(5);
}
