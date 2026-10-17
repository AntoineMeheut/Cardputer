/**
 * Carnet sur microSD — documentation française du laboratoire.
 * Créer un carnet persistant, une note par ligne.
 * Matériel : Cardputer et microSD FAT32.
 * Compiler depuis la racine : pio run -e notes-sd.
 * Utilisation : Saisir une note de 80 caractères maximum, corriger avec effacement, valider par
 * Entrée.
 * Résultat à vérifier : Chaque note est ajoutée à /notes.txt ; lire le fichier sur ordinateur après
 * extinction.
 * Lecture détaillée et raccordement : README.md et docs/composants/cardputer.md.
 */
#include <CardputerLab.h>
String note, message;
// Le montage de la SD est essayé une fois au démarrage ; redémarrer après correction du support.
bool ready = false;
void draw() { Lab::body(); Lab::line("Saisir puis ENTREE pour ajouter"); Lab::line("/notes.txt (80 caracteres max)"); Lab::line(note); Lab::line(message); }
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("02 | Carnet sur microSD"); ready = Lab::sdBegin();
    message = ready ? "SD prete" : "Erreur SD : verifier FAT32"; draw();
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // Sans SD, aucune saisie n’est acceptée. Le filtre sur les changements évite de répéter une touche
    // maintenue.
    if (!ready || !M5Cardputer.Keyboard.isChange() || !M5Cardputer.Keyboard.isPressed()) return;
    auto keys = M5Cardputer.Keyboard.keysState();
    // La limite porte sur les octets de String ; elle évite de faire grossir indéfiniment le tampon en
    // RAM.
    for (char c : keys.word) if (note.length() < 80) note += c;
    if (keys.del && note.length()) note.remove(note.length() - 1);
    if (keys.enter && note.length()) {
        // FILE_APPEND conserve les notes précédentes ; la fermeture valide l’écriture avant de libérer le
        // fichier.
        File file = SD.open("/notes.txt", FILE_APPEND);
        if (!file) message = "Ouverture impossible";
        else {
            // Garder la note en RAM en cas d’écriture insuffisante permet à l’utilisateur de réessayer.
            size_t count = file.println(note); file.close();
            message = count >= note.length() ? "Note ajoutee" : "Erreur : ecriture incomplete";
            if (count >= note.length()) note = "";
        }
    }
    draw();
}
