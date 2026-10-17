# Explorer les firmwares téléchargés

Les archives sont des instantanés de sources : **aucun firmware tiers n'a été exécuté ni téléversé** pendant la préparation du laboratoire. Chaque dépôt conserve ses instructions en langue d'origine. Les guides français locaux servent de points d'entrée.

| Projet | Parcours intéressant | Point d'entrée local |
|---|---|---|
| Démo M5Stack | Vérification du matériel et interface de référence | [README](../../upstream/sources/cardputer-demo/README.md) |
| M5Launcher | Installer et choisir des firmwares | [README](../../upstream/sources/launcher/README.md) |
| Bruce | Télécommande IR, observation radio, RFID et GPS avec matériel compatible | [README](../../upstream/sources/bruce/README.md) |
| Evil-Cardputer | Étude des interfaces Wi-Fi et de l'organisation du programme | [README](../../upstream/sources/evil-cardputer/README.md) |
| ESP32-Bus-Pirate | Console de laboratoire I²C/UART et inspection de bus | [README](../../upstream/sources/bus-pirate/README.md) |
| MicroHydra | Développer de petites applications MicroPython | [README](../../upstream/sources/microhydra/README.md) |
| MicroHydra Apps | Jeux, utilitaires et exemples d'interface | [README](../../upstream/sources/microhydra-apps/README.md) |

## Méthode d'installation

1. Vérifier la prise en charge du **Cardputer d'origine** à la révision inscrite dans [le manifeste](../../upstream/manifest.json).
2. Lire la procédure du dépôt. Certaines sources exigent ESP-IDF, des sous-modules ou une version Arduino différente de celle du laboratoire.
3. Si l'on utilise un binaire de release, identifier s'il s'agit d'une **image fusionnée**, d'une **application seule** ou d'un paquet destiné à Launcher. Les offsets ne sont pas interchangeables.
4. Préserver les données utiles du firmware précédent. Reprendre la commande exacte de flash de cette version, avec son port et ses fichiers ; ne pas appliquer aveuglément un offset `0x0` à un `firmware.bin` d'application.
5. Pour M5Launcher, employer le format et le mode d'installation décrits dans son README. Les binaires PlatformIO de ce laboratoire utilisent une table de partitions autonome ; leur compatibilité Launcher n'est pas validée ici.
6. Revenir à `diagnostic` par le [parcours PlatformIO](../installation.md) si l'on veut retrouver une référence simple. Le mode ROM G0 permet normalement de reprogrammer la flash même si l'application ne démarre plus.

## Expérimentations à privilégier

Pour illustrer le thème des portails de connexion, trois [maquettes de sensibilisation](../ateliers/portails-fictifs/README.md) proposent des univers bureautique, bancaire et Wi-Fi ferroviaire entièrement fictifs. Elles fonctionnent dans le navigateur, avec des données fixes et sans collecte d'identifiants.

Dans Bruce, commencer par l'affichage, le navigateur de fichiers, la télécommande de son téléviseur et l'observation de ses propres signaux de test. Dans Bus Pirate, commencer par un scan I²C du RFID2 ou l'affichage NMEA du GPS en adaptant G1/G2. Dans MicroHydra, créer une petite application clavier/écran, puis consulter les pilotes supportés pour le matériel externe.

La compatibilité déclarée pour **PN532**, **CC1101**, **NRF24** ou **RDA5807** ne signifie pas que le **WS1850S**, le **SYN115** ou le **U175** sont automatiquement des remplacements. Vérifier la puce attendue par la fonction et les définitions de broches.

Les archives peuvent contenir des fonctions de tests réseau offensifs, des binaires, des ressources ou des pilotes visant d'autres cartes. Leur téléchargement est un archivage documentaire ; les expériences locales ne déclenchent pas ces fonctions. Elles restent soumises aux licences propres à chaque projet, répertoriées dans [THIRD_PARTY.md](../../THIRD_PARTY.md).
