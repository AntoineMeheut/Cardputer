# Validation du laboratoire

Validation effectuée le **10 octobre 2026**, sur macOS ARM64. Cible de compilation : ESP32-S3 / Cardputer K132, PlatformIO 6.1.18, plateforme Espressif32 6.9.0 et Arduino-ESP32 2.0.17. Les bibliothèques locales correspondent aux commits du [manifeste](../upstream/manifest.json).

Une nouvelle compilation des **20 cibles a réussi le 17 octobre 2026**, après ajout des commentaires. Les [preuves du 17 octobre](code/rapports/README.md) et le [bilan documentaire](code/README.md) complètent ce rapport initial. Les essais physiques restent à effectuer.

## Résultats établis

| Vérification | Résultat |
|---|---|
| Compilation des environnements de `platformio.ini` | **20/20 réussis** |
| Sources tierces | **18/18** archives/arborescences conformes aux empreintes |
| Fichiers WAV | En-tête généré en C++ et relu par le module Python `wave` : mono, 16 bits, 16 kHz, une seconde |
| Écriture RFID locale | Garde vérifiée : seul le bloc 4 est accepté |
| Messages ESP-NOW | Rejet des tailles incorrectes, signature incorrecte et chaînes non terminées |
| Conversion GPS | GPX valide, altitude facultative, rejet des coordonnées invalides/non finies, UTC exigé, pas d'écrasement |
| Documents | Liens locaux et association catalogue/environnements vérifiés par `tools/check_docs.py` |
| Visuels | 9 SVG générés ; 16 captures du navigateur ; contrôle visuel d'exemples et vérification du rendu |

La [preuve de compilation JSON](validation-compilation.json) conserve l'environnement, l'état, la consommation statique estimée et l'empreinte de chaque binaire. Les journaux détaillés sont dans `build/` sur le poste, et seront joints comme artefacts de la CI lorsqu'elle sera exécutée sur GitHub. La CI a été préparée mais **n'a pas été exécutée sur GitHub** dans cette session.

La compilation ne démontre pas la qualité radio, l'autonomie, la portée ou la justesse d'une mesure physique. La RAM indiquée est l'allocation statique du compilateur ; Wi-Fi/BLE et d'autres fonctions allouent aussi de la mémoire à l'exécution.

## Essais matériels à réaliser

Aucun appareil connecté n'a été programmé ni testé pendant cette préparation. Tous les points suivants restent donc **à vérifier sur matériel** :

| Montage | Observation à consigner |
|---|---|
| Cardputer seul | Écran, touches, bouton G0, bip, tension |
| microSD / micro | Notes persistantes, prise WAV et lecture audible |
| Wi-Fi / BLE | Réseau de test observé, page accessible, balise visible |
| Téléviseur | Réaction à votre code IR documenté |
| RF433 T/R | Décodage de la trame synthétique sur une seconde station |
| RFID2 / F08 | Adresse I²C, lecture UID puis relecture du bloc 4 après écriture |
| U175 | AO/DO cohérents et compteur d'approches |
| GPS / GPS-SD | NMEA, fix récent, heure UTC, CSV fermé et GPX |
| ESP-NOW / USB | Réception entre deux cartes, saisie volontaire de la phrase |
| FM / NRF24 | D'abord validation du montage additionnel, puis audio ou échanges |

Les firmwares tiers complets (Bruce, Launcher, etc.) ont été téléchargés et inventoriés, **pas compilés ni testés en totalité**. Les dossiers d'expériences dont le nom utilise des soulignés sont des brouillons conservés, hors du parcours et de la matrice de compilation actuelle.

## Reproduire

```sh
python tools/test_host.py
python tools/check_docs.py
python tools/fetch_upstream.py --verify
python tools/build_all.py
```

Pour un changement limité, recompiler seulement son environnement. Une mise à jour des bibliothèques ou de la plateforme demande une nouvelle compilation complète et des essais matériels correspondants ; ne pas conserver ce rapport comme preuve d'une version différente.
