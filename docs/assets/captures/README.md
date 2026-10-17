# Captures : origine et limites

Les 16 PNG de ce dossier sont de **véritables captures du rendu navigateur** de [l'aperçu pédagogique local](../../../tools/apercu.html), effectuées le 10 octobre 2026. L'interface et ses données sont des **maquettes**. Ce ne sont ni des photos d'un Cardputer, ni des captures du firmware exécuté sur un appareil, ni la preuve d'un essai matériel.

Chaque vue porte la mention « DÉMONSTRATION » et utilise des valeurs fictives. Les commandes et manipulations renvoient aux programmes réels du dépôt. Aucun SSID privé, UID réel ou lieu personnel n'a été utilisé pour ces aperçus.

| Images | Contenu |
|---|---|
| [Installation](installation.png), [diagnostic](diagnostic.png) | Premier parcours |
| [Notes](notes-sd.png), [audio](micro-wav.png) | Stockage et enregistrement |
| [Wi-Fi](wifi.png), [Web](wifi-web.png), [BLE](ble.png) | Radios intégrées |
| [TV](ir-tv.png), [réflectif](ir-reflectif.png) | Deux usages IR distincts |
| [RF réception](rf433-rx.png), [RF émission](rf433-tx.png) | Trames de laboratoire |
| [RFID](rfid.png) | Identification fictive |
| [GPS](gps.png), [trace](gps-sd.png) | Position et journal fictifs |
| [FM](fm.png), [NRF24](nrf24.png) | Extensions nécessitant du matériel |

## Régénérer

```sh
python -m pip install playwright==1.63.0
python tools/build_assets.py
PLAYWRIGHT_BROWSERS_PATH=.cache/playwright playwright install chromium
python tools/capture_previews.py
```

Sous PowerShell, définir `$env:PLAYWRIGHT_BROWSERS_PATH = '.cache/playwright'` avant l'installation du navigateur. L'aperçu HTML est également utilisable sans Playwright, en l'ouvrant directement.

## Ajouter les résultats sur matériel

Pour chaque expérience, photographier l'écran avec son titre et le montage hors tension séparément. Ajouter modèle, version du code, alimentation et observation. Masquer les données personnelles avant de placer l'image dans le dépôt. Conserver les originaux dans `captures-privees/`, ignoré par Git. Une photo du résultat réel pourra être ajoutée sous un nom explicite, par exemple `gps-k132-essai-2026-10-11.jpg`, accompagnée de sa légende.

Les fonctions de capture présentes dans d'anciens brouillons ne sont pas validées sur la dalle ST7789 ; ne pas les utiliser comme preuve sans vérifier qu'elles lisent bien un tampon d'image exploitable.
