# Paramètres et adaptation des modules

Ces en-têtes sont accessibles aux programmes sélectionnés par [platformio.ini](../platformio.ini). Ils ne constituent pas une application autonome.

| Fichier | Rôle | Utilisation |
|---|---|---|
| [lab_config.h](lab_config.h) | Nom et clé du point d’accès, code NEC, trame RF433 et canal ESP-NOW | Modifier la constante voulue puis recompiler la cible concernée. Les cartes d’un même essai ESP-NOW doivent partager le canal. |
| [rfid_lab.h](rfid_lab.h) | Initialisation WS1850S sans RESET physique et rendu des octets en hexadécimal | Appeler `beginRfid(reader)` une fois et vérifier son retour avant les échanges avec une carte. |

## Exemple RFID

Voir le programme complet [rfid-uid](../experiments/13-rfid-uid/README.md). Le lecteur est à l’adresse I²C `0x28`, SDA G2 et SCL G1. `beginRfid` attend le reset logiciel, contrôle la version, configure le timer et active l’antenne ; il ne lit ni n’écrit un bloc de carte. `hexBytes(bytes, size)` suppose un tampon de `size` octets lisibles.

## Modifier les réglages

Depuis la racine : `pio run -e ir-tv`, `pio run -e wifi-web`, `pio run -e rf433-tx` ou `pio run -e espnow`, selon la constante changée. Les broches communes sont définies dans [CardputerLab.h](../lib/CardputerLab/src/CardputerLab.h), et non dans `lab_config.h`.

Les anciens brouillons attendent parfois `AP_SSID`, `IR_ENABLED`, `GROVE_*` ou `SD_*`. Ces noms ne sont pas fournis par cet en-tête actuel : consulter leur README avant adaptation. Le code NEC est un exemple, pas une commande universelle pour tous les téléviseurs.
