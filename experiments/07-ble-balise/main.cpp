/**
 * Émettre une balise BLE — documentation française du laboratoire.
 * Annoncer le nom Cardputer-Lab sans connexion GATT.
 * Matériel : Cardputer et second appareil de scan BLE.
 * Compiler depuis la racine : pio run -e ble-balise.
 * Utilisation : Chercher Cardputer-Lab avec le scanner ; Espace coupe ou rétablit les annonces.
 * Résultat à vérifier : Une balise non connectable, sans service GATT, apparaît dans un scanner BLE.
 * Lecture détaillée et raccordement : README.md et docs/experiences/wifi-bluetooth.md.
 */
#include <CardputerLab.h>
#include <BLEDevice.h>
BLEAdvertising* advertising;
// Cet état reflète la commande locale de démarrage/arrêt, pas une confirmation par un scanner distant.
bool active = true;
void draw() { Lab::body(); Lab::line("Nom : Cardputer-Lab"); Lab::line(active ? "Annonce BLE active" : "Annonce arretee"); Lab::line("Espace : marche / arret"); }
// Point d’entrée Arduino, exécuté une fois : préparer l’affichage, les interfaces et l’état initial de
// cette expérience.
void setup() {
    Lab::begin("07 | Balise Bluetooth LE"); BLEDevice::init("Cardputer-Lab");
    advertising = BLEDevice::getAdvertising();
    // 0x06 annonce le mode découvrable général et l’absence de Bluetooth classique.
    BLEAdvertisementData data; data.setName("Cardputer-Lab"); data.setFlags(0x06);
    // Annonce non connectable : aucun service GATT ni échange de données par connexion n’est créé.
    advertising->setAdvertisementData(data); advertising->setAdvertisementType(ADV_TYPE_NONCONN_IND);
    // Unités BLE de 0,625 ms : 800 à 1600 représentent des intervalles de 500 à 1000 ms.
    advertising->setMinInterval(800); advertising->setMaxInterval(1600); advertising->start(); draw();
}
// Boucle Arduino répétée : prendre en compte les événements et les données disponibles ; les
// temporisations locales limitent les opérations coûteuses.
void loop() {
    M5Cardputer.update();
    if (Lab::pressed(' ')) { active = !active; if (active) advertising->start(); else advertising->stop(); draw(); }
    delay(10);
}
