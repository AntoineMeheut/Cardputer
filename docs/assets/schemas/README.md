# Schémas du laboratoire

Ces neuf SVG sont des illustrations originales générées par [build_assets.py](../../../tools/build_assets.py), à partir des [brochages sourcés](../../sources.md). Ils décrivent des connexions électriques ; ils ne constituent pas des vues mécaniques des connecteurs ni des circuits imprimés validés.

| Schéma | Usage |
|---|---|
| [Vue du laboratoire](laboratoire.svg) | Périphériques et thèmes |
| [Grove](grove.svg) | Les quatre couleurs |
| [RF433T](rf433-tx.svg) | Émission G2 |
| [RF433R](rf433-rx.svg) | Réception G1 |
| [RFID](rfid.svg) | SDA G2 / SCL G1 |
| [Réflectif](ir-reflectif.svg) | DO G2 / AO G1 |
| [GPS](gps.svg) | RX contrôleur G1 / TX G2 |
| [FM](fm.svg) | Extension avec alimentation régulée et audio externe |
| [NRF24](nrf24.svg) | Extension SPI via adaptateur microSD |

Couper l'alimentation avant de raccorder. Le 5 V d'alimentation Grove n'est pas le niveau logique des GPIO.
