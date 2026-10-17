# Catalogue des 20 expériences

Tous les programmes sont indépendants et destinés au **Cardputer K132**. Commencer par 01, puis suivre le guide du composant. Les expériences 19 et 20 exigent du matériel supplémentaire ; 17 demande deux stations. Les opérations SD nécessitent une carte ajoutée à l’inventaire initial.

| N° | Expérience | Environnement PlatformIO | Matériel |
|---|---|---|---|
| 01 | [Diagnostic du Cardputer](01-diagnostic/README.md) | `diagnostic` | Cardputer seul |
| 02 | [Carnet sur microSD](02-notes-sd/README.md) | `notes-sd` | Cardputer et microSD FAT32 |
| 03 | [Enregistrer et écouter un WAV](03-micro-wav/README.md) | `micro-wav` | Cardputer ; microSD facultative pour conserver le fichier |
| 04 | [Observer les réseaux Wi-Fi](04-wifi-scan/README.md) | `wifi-scan` | Cardputer ; point d’accès 2,4 GHz pour vérifier |
| 05 | [Serveur Web local](05-wifi-web/README.md) | `wifi-web` | Cardputer et navigateur sur téléphone ou PC |
| 06 | [Écouter les annonces BLE](06-ble-scan/README.md) | `ble-scan` | Cardputer ; balise BLE ou téléphone pour l’essai |
| 07 | [Émettre une balise BLE](07-ble-balise/README.md) | `ble-balise` | Cardputer et second appareil de scan BLE |
| 08 | [Télécommande TV infrarouge](08-ir-tv/README.md) | `ir-tv` | Cardputer, votre TV et un code NEC compatible connu |
| 09 | [Détecter le RFID2 sur I²C](09-i2c-scan/README.md) | `i2c-scan` | Cardputer, Grove et RFID2 |
| 10 | [Mesurer et compter les approches](10-ir-reflectif/README.md) | `ir-reflectif` | Cardputer, Grove et U175 |
| 11 | [Recevoir une trame ASK/OOK](11-rf433-rx/README.md) | `rf433-rx` | Cardputer, RF433R et émetteur de test compatible |
| 12 | [Envoyer une trame RF de laboratoire](12-rf433-tx/README.md) | `rf433-tx` | Cardputer, RF433T et une station réceptrice séparée |
| 13 | [Lire l’identifiant des cartes F08](13-rfid-uid/README.md) | `rfid-uid` | Cardputer, RFID2, Grove et carte F08 |
| 14 | [Lire et écrire le bloc 4 de test](14-rfid-bloc/README.md) | `rfid-bloc` | Cardputer, RFID2 et F08 vierge réservée au laboratoire |
| 15 | [Afficher position et heure UTC](15-gps/README.md) | `gps` | Cardputer, Grove et GPS/BDS v1.1 |
| 16 | [Journal GPS et export GPX](16-gps-sd/README.md) | `gps-sd` | Cardputer, GPS v1.1, Grove et microSD FAT32 |
| 17 | [Messages entre deux Cardputer](17-espnow/README.md) | `espnow` | Deux Cardputer ; adaptation possible sur un second ESP32 |
| 18 | [Phrase au clavier USB](18-usb-clavier/README.md) | `usb-clavier` | Cardputer, câble USB de données et éditeur de texte |
| 19 | [Radio FM avec module additionnel](19-fm-rda5807/README.md) | `fm-rda5807` | RDA5807, adaptation 3,3 V, antenne et audio externe ; absents de la liste initiale |
| 20 | [Paquets NRF24 à deux stations](20-nrf24/README.md) | `nrf24` | Deux NRF24, deux contrôleurs, adaptateur microSD/SPI et alimentation 3,3 V |

## Continuer les explorations

Après ces bases : graphe du signal micro, synthétiseur au clavier, lecteur WAV, dessin sur écran, jeu de mémoire RFID, inventaire de cartes, histogramme du capteur réflectif, protocole RF avec compteur, pertes radio selon la distance, favoris TV, RSSI selon la position, API HTTP locale, échange ESP-NOW avec accusé, horloge UTC, distance GPS filtrée, export cartographique, RDS FM et réseau de capteurs NRF24.

Ces prolongements sont des pistes à adapter, pas des programmes supplémentaires présentés comme terminés. Les [projets téléchargés](../upstream/README.md) donnent les bases correspondantes.

Les dossiers avec soulignés, comme `01_diagnostic`, sont des brouillons conservés hors de cette matrice. Voir [l'état du projet](../docs/etat-projet.md) avant de les reprendre.

<!-- documentation-code-fr -->
## Lire le code et les variantes historiques

Chaque programme actif possède des commentaires français et une section « Comprendre le programme » dans son README. Les variantes ci-dessous sont exclues de la matrice de compilation ; leur README décrit les dépendances à adapter.

| Brouillon | Fonction | Référence active |
|---|---|---|
| [01_diagnostic](01_diagnostic/README.md) | Diagnostic et luminosité | `01-diagnostic` |
| [02_audio](02_audio/README.md) | Audio à 8 kHz et niveau RMS | `03-micro-wav` |
| [03_carnet_sd](03_carnet_sd/README.md) | Carnet de 160 caractères | `02-notes-sd` |
| [04_wifi_scan](04_wifi_scan/README.md) | Ancien scan Wi-Fi | `04-wifi-scan` |
| [05_web_local](05_web_local/README.md) | Ancien serveur Web | `05-wifi-web` |
| [06_ble_scan](06_ble_scan/README.md) | Scan avec NimBLE | `06-ble-scan` |
| [07_ble_message](07_ble_message/README.md) | Bloc-notes BLE GATT | `07-ble-balise` |
| [08_espnow](08_espnow/README.md) | Compteur ESP-NOW | `17-espnow` |
| [09_telecommande_ir](09_telecommande_ir/README.md) | Émission IR conditionnelle | `08-ir-tv` |
| [10_i2c](10_i2c/README.md) | Ancien scanner I²C | `09-i2c-scan` |
| [11_rf433_reception](11_rf433_reception/README.md) | Ancienne réception RF433 | `11-rf433-rx` |
| [12_rf433_emission](12_rf433_emission/README.md) | Ancienne émission RF433 | `12-rf433-tx` |
| [13_rfid](13_rfid/README.md) | RFID combiné | `13-rfid-uid / 14-rfid-bloc` |
| [14_ir_reflectif](14_ir_reflectif/README.md) | Réflectif avec calibration | `10-ir-reflectif` |
| [15_gps](15_gps/README.md) | GPS avec journal optionnel | `15-gps / 16-gps-sd` |
| [16_usb_clavier](16_usb_clavier/README.md) | Ancien clavier USB | `18-usb-clavier` |
| [17_fm](17_fm/README.md) | FM avec bouclage de bande | `19-fm-rda5807` |
| [18_nrf24_terminal](18_nrf24_terminal/README.md) | Terminal UART pour pont NRF24 | `20-nrf24 (autre architecture)` |
| [19_nrf24_pont](19_nrf24_pont/README.md) | Pont radio sur ESP32 externe | `20-nrf24 (autre architecture)` |
