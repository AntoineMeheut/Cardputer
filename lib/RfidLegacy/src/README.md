# Fichiers d’adaptation du pilote

[MFRC522_I2C.h](MFRC522_I2C.h) rend les déclarations amont visibles ; [MFRC522_I2C.cpp](MFRC522_I2C.cpp) compile l’implémentation amont dans la bibliothèque locale. Le chemin relatif remonte jusqu’à `upstream/sources/m5rfid-legacy` : conserver cette organisation ou adapter ensemble les deux inclusions.

Lire le [README parent](../README.md) pour la construction et les limites du lecteur WS1850S. Ces fichiers ne possèdent ni `setup` ni `loop` et ne doivent pas être téléversés séparément. Les commentaires français ajoutés aux sources tierces sont traçables dans [la documentation des instantanés](../../../upstream/README.md).
