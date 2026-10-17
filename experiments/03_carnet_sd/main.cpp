/**
 * Carnet de 160 caractères — brouillon historique, exclu des environnements actifs.
 * Saisie jusqu’à 160 caractères avec Lab::append ; la version active limite la saisie à 80 et contrôle
 * explicitement l’écriture.
 * Référence à privilégier : experiments/02-notes-sd.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
String note;
bool ready;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("03 Carnet microSD");
    ready = Lab::sdBegin();
    Lab::screen(ready ? "Saisir une note (160 car.)\nEntree: enregistrer" : "Erreur SD : FAT32, carte inseree ?");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (!ready || !c) { delay(5); return; }
    if (c == '\n') {
        bool ok = Lab::append("/notes.txt", note + "\n");
        if (ok) note = "";
        Lab::screen(ok ? "Note sauvegardee.\nSaisir la suivante." : "Echec ecriture. Note conservee:\n" + note);
        return;
    }
    if (c == '\b') { if (note.length()) note.remove(note.length() - 1); }
    else if (note.length() < 160) note += c;
    Lab::screen(note);
}
