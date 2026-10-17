# Sources documentaires et décisions

Consultation : **10 octobre 2026**. Les guides français sont rédigés pour ce laboratoire ; les pages citées restent les références des fabricants. Les logiciels téléchargés sont figés séparément dans [le manifeste](../upstream/manifest.json).

| Sujet | Source primaire | Décision retenue |
|---|---|---|
| Cardputer K132 | [M5Stack](https://docs.m5stack.com/en/core/Cardputer) | G2/G1 Grove, IR G44, microSD G12/14/40/39 ; cible sans ADV |
| Câble | [Produit fourni](https://shop.m5stack.com/products/4pin-buckled-grove-cable) | Quatre fils ; intitulé actuel différent de l'URL historique |
| RF433T | [Fiche](https://docs.m5stack.com/en/unit/Unit_RF433T), [produit](https://shop.m5stack.com/products/rf-unit-433mhz-transmitter-syn115) | SYN115, jaune TX, 433,92 MHz ASK |
| RF433R | [Fiche](https://docs.m5stack.com/en/unit/Unit_RF433R), [produit](https://shop.m5stack.com/products/rf-unit-433mhz-receiver-syn513r) | Blanc RX ; divergence SYN513R dans l'URL / SYN531R dans la fiche explicitée |
| Cartes F08 | [Produit fourni](https://shop.m5stack.com/products/13-56mhz-rfid-card-f08-chip-5pcs) | Essais sur cartes de test HF ; chemin Classic 1K |
| Réflectif U175 | [Fiche](https://docs.m5stack.com/en/unit/Unit_Reflective_IR), [produit](https://shop.m5stack.com/products/infrared-reflective-sensor-unit), [schéma](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/628/SCH_UNIT_Reflective_IR_V1.0_sch_01.png) | DO jaune, AO blanc ; régulateur interne 3,3 V ; pas un décodeur TV |
| RFID2 | [Fiche](https://docs.m5stack.com/en/unit/Unit_RFID2), [produit](https://shop.m5stack.com/products/rfid-unit-2-ws1850s) | I²C 0x28, SDA jaune/SCL blanc, WS1850S |
| GPS v1.1 | [Fiche](https://docs.m5stack.com/en/unit/Unit-GPS%20v1.1), [produit](https://shop.m5stack.com/products/gps-bds-unit-v1-1-at6668) | 115200 8N1, RX contrôleur sur G1 |
| Bluetooth | [Espressif ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/ble/overview.html) | BLE pris en charge, Bluetooth Classic absent |
| NRF24 | [RF24](https://nrf24.github.io/RF24/) | Pilote SPI distinct, extension physique obligatoire |
| FM | [PU2CLR RDA5807](https://pu2clr.github.io/RDA5807/) | Tuner et sortie audio additionnels |

La documentation en ligne peut évoluer après cette date. Pour les brochages, contrôler le modèle inscrit sur l'objet ; pour le logiciel, le commit du manifeste prime sur le nom courant d'une branche. Les liens « stable » Espressif peuvent décrire une API plus récente que le core Arduino figé localement.
