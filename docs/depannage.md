# Dépannage

| Symptôme | Contrôle prioritaire | Suite |
|---|---|---|
| `pio` introuvable | Activer `.venv`, vérifier `pip install -r requirements.txt` | Utiliser `python -m platformio` |
| Source ou bibliothèque absente | `python tools/fetch_upstream.py` | Vérifier réseau et espace disque ; ne pas prendre une version arbitraire |
| Empreinte de source différente | Un fichier dans `upstream/sources` a été modifié | Sauvegarder son adaptation ailleurs avant de restaurer l'instantané |
| Port USB absent | Câble de données et port direct | Mode G0 ; refaire `pio device list` |
| Port occupé | Moniteur série ou autre application ouverte | Fermer le logiciel puis recommencer |
| Téléversement impossible | G0 à la mise sous tension et port correct | Réduire `upload_speed` à 115200 si nécessaire |
| Mauvais programme à l'écran | Nom de l'environnement téléversé | Revenir à `diagnostic`, puis vérifier le titre |
| Écran noir après USB HID | Options USB spécifiques à `usb-clavier` | Récupérer en mode G0 ; le port peut changer |
| Aucun périphérique I²C | Noir/rouge et SDA G2 / SCL G1 | Un GPS UART ne répondra jamais au scan I²C |
| Aucun badge RFID | Type 13,56 MHz, une carte proche | Vérifier 0x28 puis tester une F08 connue |
| Échec de lecture/écriture F08 | Carte Classic 1K de test et clé usine | Ne pas modifier les trailers pour « réparer » l'essai |
| RF433 vide | GPIO 1 et source ASK/OOK à 433,92 MHz | Protocole peut être non pris en charge par rc-switch |
| Émission RF sans effet | Récepteur séparé et mêmes paramètres | Le texte « envoyée » n'est pas un accusé radio |
| TV sans réaction | Code, ordre des bits, protocole et visée | U175 n'est pas un récepteur d'apprentissage |
| GPS sans octets | v1.1 AT6668 : 115200, RX=G1, TX=G2 | Vérifier alimentation et câble |
| GPS sans position | Antenne au ciel, délai d'acquisition | Les octets NMEA et le fix sont deux états différents |
| SD absente | FAT32, contacts, carte saine | Ne pas formater une carte contenant des données sans sauvegarde |
| Micro muet / haut-parleur muet | Ressources audio utilisées successivement | `micro-wav` arrête l'un avant d'activer l'autre |
| Aucun réseau Wi-Fi | Point d'accès 2,4 GHz | Un réseau 5 GHz seul n'est pas pris en charge |
| Balise BLE invisible dans les réglages | Utiliser un scanner BLE | Une annonce non connectable n'est pas un casque Bluetooth |
| FM absente | Module RDA5807 ajouté, antenne et sortie audio | Le matériel initial ne contient pas de tuner FM |
| NRF24 sans réponse | SPI, 3,3 V, canal et station distante | Aucun branchement direct 5 V au NRF24 |

Si une compilation échoue, conserver le **premier message d'erreur**, le nom de l'environnement et les versions affichées. Les dernières lignes seules peuvent masquer l'origine. `python tools/build_all.py` enregistre les journaux dans `build/` ; ce dossier n'est pas publié.

Ne pas lancer un effacement complet de la flash pour une simple erreur de câble, de port ou de compilation. Repartir du [diagnostic](../experiments/01-diagnostic/README.md) puis réintroduire un périphérique à la fois.
