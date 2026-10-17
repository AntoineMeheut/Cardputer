/**
 * Enregistrer et écouter un WAV — documentation française du laboratoire.
 * Enregistrer une seconde de son, l’écouter et éventuellement la conserver.
 * Matériel : Cardputer ; microSD facultative pour conserver le fichier.
 * Compiler depuis la racine : pio run -e micro-wav.
 * Utilisation : Presser r, parler une seconde, puis p pour écouter la prise. Répéter r crée un nouveau
 * fichier.
 * Résultat à vérifier : Un signal mono 16 kHz / 16 bits est conservé en RAM et, si disponible, sur SD.
 * Lecture détaillée et raccordement : README.md et docs/composants/cardputer.md.
 */
#include <CardputerLab.h>
#include <LabFormats.h>
constexpr size_t SAMPLES = 16000; // Une seconde, 32 ko, sans dépendre de PSRAM.
// PCM signé mono : 16 000 échantillons de deux octets donnent 32 000 octets pour une seconde.
int16_t samples[SAMPLES];
// record démarre une opération asynchrone ; son retour seul ne signifie pas que le tampon est rempli.
bool ready = false, hasRecording = false;
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("03 | Micro et fichier WAV"); ready = Lab::sdBegin();
    M5Cardputer.Speaker.end();
    Lab::line(ready ? "SD prete" : "SD absente : lecture RAM possible");
    Lab::line("r : enregistrer 1 s   p : ecouter");
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    // Microphone et haut-parleur sont utilisés successivement : arrêter la sortie avant de démarrer la
    // capture.
    if (Lab::pressed('r')) {
        Lab::body(); Lab::line("Enregistrement...");
        M5Cardputer.Speaker.end();
        if (!M5Cardputer.Mic.begin()) { Lab::line("Erreur micro"); return; }
        hasRecording = M5Cardputer.Mic.record(samples, SAMPLES, 16000);
        uint32_t start = millis();
        // Attendre au plus trois secondes et rendre la main au système avec delay(1). Un dépassement invalide
        // la prise.
        while (M5Cardputer.Mic.isRecording() && millis() - start < 3000) delay(1);
        if (M5Cardputer.Mic.isRecording()) hasRecording = false;
        M5Cardputer.Mic.end();
        if (!hasRecording) { Lab::line("Capture echouee"); return; }
        if (ready) {
            // Choisir un nom libre empêche d’écraser les prises antérieures ; la lecture audio utilisera toujours
            // le tampon RAM.
            String path = Lab::nextFile("/micro-", ".wav");
            File file = path.length() ? SD.open(path, FILE_WRITE) : File();
            if (!file) Lab::line("Impossible de creer le WAV");
            else {
                // Le fichier commence par 44 octets RIFF/WAV, puis le PCM brut ; contrôler séparément les deux
                // écritures.
                uint8_t header[44]; Lab::wavHeader(header, sizeof(samples), 16000);
                bool ok = file.write(header, sizeof(header)) == sizeof(header);
                ok = (file.write(reinterpret_cast<uint8_t*>(samples), sizeof(samples)) == sizeof(samples)) && ok;
                file.close(); Lab::line(ok ? path : "Erreur d'ecriture WAV");
            }
        }
        Lab::line("r : recommencer   p : ecouter");
    }
    // Ne lire que si une capture valide existe. Le fichier SD n’est pas relu dans cette démonstration.
    if (Lab::pressed('p') && hasRecording) {
        M5Cardputer.Mic.end(); M5Cardputer.Speaker.begin(); M5Cardputer.Speaker.setVolume(80);
        M5Cardputer.Speaker.playRaw(samples, SAMPLES, 16000, false);
        while (M5Cardputer.Speaker.isPlaying()) delay(1);
        M5Cardputer.Speaker.end();
    }
}
