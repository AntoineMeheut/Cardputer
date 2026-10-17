/**
 * Bloc-notes BLE GATT — brouillon historique, exclu des environnements actifs.
 * Crée un service et une caractéristique publics en lecture/notification. Entrée publie la saisie de
 * 20 caractères maximum. Ce comportement diffère de la balise non connectable active.
 * Référence à privilégier : experiments/07-ble-balise.
 * Avant utilisation : lire README.md ; ne pas compiler ce fichier comme une cible déjà validée.
 */
#include <Lab.h>
#include <NimBLEDevice.h>
NimBLECharacteristic *message;
String value;
// Initialisation de la variante historique. Les constantes et la version des bibliothèques doivent
// être adaptées avant compilation.
void setup() {
    Lab::begin("07 Bloc-notes BLE GATT");
    NimBLEDevice::init("Cardputer-Labo");
    auto server = NimBLEDevice::createServer();
    auto service = server->createService("a1b20001-77c0-4000-8000-000000000001");
    message = service->createCharacteristic("a1b20002-77c0-4000-8000-000000000001", NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::NOTIFY);
    message->setValue("Bonjour du Cardputer");
    service->start();
    auto advertising = NimBLEDevice::getAdvertising();
    advertising->addServiceUUID(service->getUUID());
    advertising->start();
    Lab::screen("Connecter un client BLE GATT\nSaisir un texte, puis Entree\nLecture/notification publique");
}
// Traitement des entrées de cette variante ; consulter les touches ci-dessous, qui peuvent différer du
// programme actif.
void loop() {
    // Lab::input met aussi à jour le clavier ; le caractère ! est réservé à l’ancien essai de capture
    // série, non validé sur la dalle.
    char c = Lab::input();
    if (c == '\n') { message->setValue(value.c_str()); message->notify(); value = ""; Lab::screen("Message publie"); }
    else if (c == '\b') { if (value.length()) value.remove(value.length()-1); Lab::screen(value); }
    else if (c && value.length() < 20) { value += c; Lab::screen(value); }
    // NimBLE relance les annonces apres une deconnexion par defaut.
    delay(5);
}
