# Matrice de compatibilité

Le matériel cible est le **Cardputer K132**, pas le Cardputer-ADV. Le premier n'a ni IMU ni connecteur d'extension ADV. Les broches de ses périphériques internes sont déjà utilisées.

| Fonction | Présente ou matériel requis | Limites pratiques |
|---|---|---|
| Wi-Fi | ESP32-S3 intégré | 2,4 GHz ; le scan ne montre pas les réseaux 5 GHz seuls |
| Bluetooth | BLE intégré | Pas de Bluetooth Classic, donc pas de casque A2DP avec ce laboratoire |
| IR émission | LED intégrée, G44 | Ligne de visée et protocole correct requis |
| IR réception TV | Récepteur démodulé additionnel | Le U175 réflectif ne convient pas |
| 433,92 MHz | RF433T/R listés | ASK/OOK ; pas de réception FSK ni de spectre large bande |
| RFID HF | RFID2 WS1850S + carte F08 | Les exemples locaux utilisent le chemin ISO14443-A / Classic 1K |
| RFID 125 kHz / UHF | Lecteur dédié absent | Incompatible avec le WS1850S à 13,56 MHz |
| GPS/GNSS | AT6668 listé | Récepteur de navigation ; pas d'émission GPS |
| Radio FM broadcast | RDA5807 supplémentaire | Réception analogique sur la sortie audio du module |
| NRF24 | Deux NRF24 + adaptation SPI/3,3 V | Protocole distinct du Wi-Fi et du BLE malgré la bande 2,4 GHz |
| CC1101 | Module et adaptation SPI supplémentaires | Aucun CC1101 dans l'inventaire initial |
| SDR / spectre RF | Récepteur SDR externe | Le RSSI Wi-Fi n'est pas un analyseur de spectre universel |
| ESP-NOW | Une seconde carte ESP32 pour recevoir | Wi-Fi 2,4 GHz, même canal, protocole distinct d'une connexion IP |
| microSD | Carte microSD supplémentaire si non possédée | FAT32 pour le parcours ; aucune SD pendant l'expérience NRF24 |

Les brochages des modules sont dans [le guide Grove](composants/cable-grove.md). Les ports sont **alternatifs** : on ne peut pas utiliser le GPS UART, le RFID I²C et le capteur analogique simultanément avec un simple câble en Y. Un hub I²C ne transforme pas un périphérique UART ou analogique en périphérique I²C. Le couple RF433T/R peut partager 5 V/GND sur un câblage adapté, car TX utilise G2 et RX G1 ; ce montage n'est pas fourni par l'unique câble droit.

Sources : [Cardputer et brochage](https://docs.m5stack.com/en/core/Cardputer), [BLE sur ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/ble/overview.html), [RFID2](https://docs.m5stack.com/en/unit/Unit_RFID2), [documentation RF24](https://nrf24.github.io/RF24/).
