# Bibliothèques locales

| Répertoire | Usage |
|---|---|
| [CardputerLab](CardputerLab/README.md) | Interface active pour écran/clavier/SD/I²C, formats binaires et variantes historiques. |
| [RfidLegacy](RfidLegacy/README.md) | Adaptateur de construction vers le pilote MFRC522-I2C archivé. |

PlatformIO découvre les bibliothèques locales depuis ce dossier. Les dépendances externes supplémentaires sont sélectionnées dans [platformio.ini](../platformio.ini), généralement par lien vers `upstream/sources`. Compiler une expérience depuis la racine, par exemple `pio run -e diagnostic` ; ne pas compiler tous les `main.cpp` ensemble.

Après une modification des formats purs : `python tools/test_host.py`. Après une modification matérielle commune : compiler les cibles concernées, puis effectuer un essai sur leur matériel. Une compilation seule ne valide pas les branchements.
