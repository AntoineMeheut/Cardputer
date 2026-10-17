# Auteurs et licences des composants tiers

Les programmes pédagogiques locaux utilisent les API des bibliothèques citées. Les 18 archives téléchargées sont conservées **sans modification de leurs octets**, avec leurs mentions d’origine. Les sources extraites reçoivent des commentaires et des README français, enregistrés dans un [registre réversible](upstream/documentation-fr/README.md). Le contrôle d’intégrité reconstitue les octets d’origine avant comparaison au manifeste. Le répertoire `lib/RfidLegacy` est uniquement un adaptateur de construction qui inclut le pilote historique ; son initialisation spécifique au WS1850S est dans `include/rfid_lab.h`.

| Projet | Licence ou déclaration principale trouvée | Preuve dans l'instantané |
|---|---|---|
| m5cardputer | MIT | [Mention conservée](upstream/sources/m5cardputer/src/M5Cardputer.h) |
| m5unified | MIT | [Mention conservée](upstream/sources/m5unified/LICENSE) |
| m5gfx | MIT | [Mention conservée](upstream/sources/m5gfx/LICENSE) |
| cardputer-demo | MIT | [Mention conservée](upstream/sources/cardputer-demo/LICENSE) |
| m5rfid | MIT | [Mention conservée](upstream/sources/m5rfid/LICENSE) |
| m5rfid-legacy | LicenseRef-Public-Domain | [Mention conservée](upstream/sources/m5rfid-legacy/MFRC522_I2C.h) |
| tinygpsplus | LGPL-2.1-or-later | [Mention conservée](upstream/sources/tinygpsplus/src/TinyGPS++.h) |
| rc-switch | LGPL-2.1-or-later | [Mention conservée](upstream/sources/rc-switch/RCSwitch.h) |
| irremote | MIT | [Mention conservée](upstream/sources/irremote/LICENSE.txt) |
| rf24 | GPL-2.0 | [Mention conservée](upstream/sources/rf24/LICENSE) |
| rf24network | GPL-2.0 | [Mention conservée](upstream/sources/rf24network/LICENSE) |
| rda5807 | MIT | [Mention conservée](upstream/sources/rda5807/license.txt) |
| launcher | MIT | [Mention conservée](upstream/sources/launcher/LICENSE) |
| bruce | AGPL-3.0 | [Mention conservée](upstream/sources/bruce/LICENSE) |
| evil-cardputer | MIT | [Mention conservée](upstream/sources/evil-cardputer/README.md) |
| bus-pirate | MIT | [Mention conservée](upstream/sources/bus-pirate/LICENSE) |
| microhydra | GPL-3.0 | [Mention conservée](upstream/sources/microhydra/LICENSE) |
| microhydra-apps | MIT | [Mention conservée](upstream/sources/microhydra-apps/LICENSE) |

La déclaration de domaine public du pilote historique est reproduite telle qu'elle existe dans son en-tête ; elle n'a pas été transformée en licence MIT. M5Cardputer porte des identifiants SPDX MIT dans ses sources. Certains dépôts incluent également des polices, images, pilotes, bases de données ou dépendances dont les conditions diffèrent de la licence principale : conserver leurs notices individuelles.

Les outils de compilation téléchargés par PlatformIO (Arduino-ESP32, Espressif, bibliothèques système et IRremote 4.7.1) ont leurs propres licences dans `.platformio/` et `.pio/libdeps/`. Les binaires de compilation et ces caches ne sont pas destinés au dépôt GitHub de ce laboratoire. Si des binaires sont distribués ensuite, examiner les obligations des bibliothèques effectivement liées à chacun d'eux et fournir les sources/notices nécessaires.

Les captures pédagogiques et schémas du laboratoire sont originaux. Les pages produit M5Stack sont citées, sans copie de leurs photographies dans les guides.
